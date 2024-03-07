# Standards and Units 

## Introduction

The following practices and units are used throughout this codebase to prevent confusion about how things work. A clear and consistent set of units and practices allow for better, more readable code.

## Speeds

- Speeds are represented on a scale from -1 to 1.
- The value of -1 denotes the maximum speed in one direction, while 1 denotes the maximum speed in the opposite direction.
- A speed of 0 indicates no movement.
- This scale applies to concepts that apply both forward and backwards.

## Rotations

- Rotations are measured in [radians](https://en.wikipedia.org/wiki/Radian).
- A negative angle signifies a clockwise rotation, while a positive angle represents an anticlockwise rotation.

## Rotational Speeds

- Rotational speeds are measured in radians per second squared (rad/sec^2).
- Similar to speeds, rotational speeds are represented on a scale from -1 to 1 or 0 to 1, depending on the context.
- A value of -1 indicates the maximum rotational acceleration in one direction, while 1 denotes the maximum acceleration in the opposite direction.
- A value of 0 implies no rotational acceleration.

## Conclusion

By adhering to these standardized practices, users of the Python library can expect clarity and consistency in handling speeds, rotations, and rotational speeds, thus minimizing confusion and enhancing usability.
