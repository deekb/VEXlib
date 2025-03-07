import argparse
import re
import shutil
import sys
import time

from rich.console import Console

from .Constants import *
from .Utils import get_removable_disks, get_available_modules, get_checksum, detect_dependencies, unmount_drive, \
    convert_size

os.chdir(PROJECT_ROOT)

parser = argparse.ArgumentParser()
# parser.add_argument("-a", "--remote-address", help="The address of the remote device connected to the brain and running the RemoteDeploy.py script from the util folder", type=str)
# parser.add_argument("-p", "--remote-port", help="The port of the remote device connected to the brain and running the RemoteDeploy.py script from the util folder", type=int, default=5000)
parser.parse_args()


def exclude_from_deploy(filename):
    # This function tells the program which files to ignore while scanning the "deploy" directory
    return re.search(DEPLOY_EXCLUDE_REGEX, filename) is not None


console = Console()
deployed_count = 0
deployed_size_bytes = 0


def copy_libraries(libraries, directory):
    global deployed_count, deployed_size_bytes
    for file in libraries:
        if os.path.isfile(directory):
            os.remove(directory)
        if not os.path.exists(directory):
            os.mkdir(directory)
        file_to_copy_checksum = get_checksum(file)
        file_to_overwrite = os.path.join(directory, (file.split(os.sep)[-1]))
        file_to_overwrite_checksum = None
        if os.path.isfile(file_to_overwrite):
            file_to_overwrite_checksum = get_checksum(file_to_overwrite)
        elif os.path.isdir(file_to_overwrite):
            print(f"{file_to_overwrite} exists as folder, removing it")
            os.rmdir(file_to_overwrite)
            shutil.copy(file, directory)
            deployed_count += 1
            deployed_size_bytes += os.path.getsize(file)
        if file_to_copy_checksum != file_to_overwrite_checksum:
            if file_to_overwrite_checksum:
                print(f"{file_to_overwrite} exists but has invalid checksum: {file_to_overwrite_checksum}, pushing")
                os.remove(file_to_overwrite)
            else:
                print(f"{file_to_overwrite} does not exist, pushing")
            shutil.copy(file, directory)
            deployed_count += 1
            deployed_size_bytes += os.path.getsize(file)


def main():
    failure_count = 0
    vex_disk = None
    with console.status("[cyan]Searching for VEX disk...") as status:
        while failure_count < FIND_VEX_DISK_MAX_ATTEMPTS - 1:
            for disk in get_removable_disks(POSIX_MOUNT_POINT_DIR):
                if DRIVE_IDENTIFIER_STRING in disk.name:
                    vex_disk = disk.path
                    break  # Found the vex disk
            if vex_disk is not None:
                break
            failure_count += 1
            time.sleep(FIND_VEX_DISK_TIME_BETWEEN_ATTEMPTS)

    if failure_count >= FIND_VEX_DISK_MAX_ATTEMPTS - 1:
        console.print(f"[red]Could not find any drive with drive identifier \"{DRIVE_IDENTIFIER_STRING}\"")
        sys.exit(19)  # ENODEV No such device

    available_libraries = get_available_modules(SRC_DIRECTORY)

    required_libraries = ["main"]

    required_libraries.extend(
        detect_dependencies(SRC_DIRECTORY, MAIN_PROGRAM, available_libraries, VEX_BUILTIN_MODULES))

    print(required_libraries)

    libraries_to_copy = {}

    for library in required_libraries:
        if library in available_libraries:
            libraries_to_copy[library] = available_libraries[library]
        else:
            raise ModuleNotFoundError(f"Couldn't find library '{library}'")

    deploy_objects = []
    library_objects = []

    for root, dirs, files in os.walk(DEPLOY_DIRECTORY):
        for file in files:
            dependency = str(os.path.join(root, file))
            if os.path.isfile(dependency) and not exclude_from_deploy(dependency):
                deploy_objects.append(os.path.join(DEPLOY_DIRECTORY, dependency))

    for root, dirs, files in os.walk(VEXLIB_DIRECTORY):
        for file in files:
            if exclude_from_deploy(file):
                continue
            to_copy = str(os.path.join(root, file))
            target_path = os.path.join(POSIX_MOUNT_POINT_DIR, vex_disk, "VEXLib",
                                       os.path.relpath(to_copy, VEXLIB_DIRECTORY))
            target_dir = os.path.dirname(target_path)
            if not os.path.isdir(target_dir):
                if os.path.isfile(target_dir):
                    os.unlink(target_dir)
                os.makedirs(target_dir)
            if os.path.isfile(target_path):
                if get_checksum(target_path) == get_checksum(to_copy):
                    print("Checksum match")
                    continue

            print(f"Copying {to_copy} to {target_path}")
            shutil.copy(to_copy, target_path)

    start_time = time.monotonic()

    with console.status("[cyan]Copying libraries...") as status:
        # Copy all source files (main.py and its dependencies) into the root directory
        copy_libraries(libraries_to_copy.values(), os.path.join(POSIX_MOUNT_POINT_DIR, vex_disk))

        # Copy all deploy objects to the "deploy" directory
        copy_libraries(deploy_objects, os.path.join(os.path.join(POSIX_MOUNT_POINT_DIR, vex_disk), "deploy"))

        copy_libraries(library_objects, os.path.join(os.path.join(POSIX_MOUNT_POINT_DIR, vex_disk), "deploy"))

    if not os.path.isdir(os.path.join(POSIX_MOUNT_POINT_DIR, vex_disk, "logs")):
        os.mkdir(os.path.join(POSIX_MOUNT_POINT_DIR, vex_disk, "logs"))
    with console.status("[cyan]Unmounting drive please wait [yellow]:warning:") as status:
        unmount_drive(os.path.join(POSIX_MOUNT_POINT_DIR, vex_disk))
    console.print("[green]You may now remove the drive :thumbsup:")
    console.print(
        f"[green]Uploaded [bold green]{deployed_count}[reset][green] files ([bold green]{convert_size(deployed_size_bytes)}[reset][green]) in [bold green]{round(time.monotonic() - start_time, 2)}[reset][green] seconds")


if __name__ == "__main__":
    main()
