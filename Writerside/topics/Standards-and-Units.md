# Standards and Units 

## Introduction

The following practices and units are used throughout this codebase to prevent confusion about how things work. A clear and consistent set of units and practices allow for better, more readable code.

## Speeds

- Speeds are represented on a scale from -1 to 1.
- The value of -1 denotes the maximum speed in the reverse direction, while 1 denotes the maximum speed in the forward direction.
- A speed of 0 indicates no movement.
- This scale applies to concepts that apply both forward and backwards.

## Rotations

- Rotations are measured in [radians](https://en.wikipedia.org/wiki/Radian).
- A negative angle signifies a clockwise rotation, while a positive angle represents an anticlockwise rotation.

## Rotational Speeds

- Rotational speeds are measured in radians per second squared.
- A value of -pi indicates the maximum rotational acceleration in the clockwise direction, while pi denotes the maximum acceleration in the anticlockwise direction.
- A value of 0 implies no rotational speed/acceleration.

## Conclusion

By adhering to these standardized practices,
users of this library can expect clarity and consistency in handling translational and rotational speeds,
thus minimizing confusion and enhancing usability.
