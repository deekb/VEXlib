from VEXLib.Geometry.Translation2d import Translation2d
from VEXLib.Geometry.Rotation2d import Rotation2d


class Pose2d:
    """Represents a 2D pose composed of a Translation2d and a Rotation2d."""

    def __init__(self, translation: Translation2d = Translation2d(), rotation: Rotation2d = Rotation2d()):
        """Initialize the Pose2d object with translation and rotation."""
        self.translation = translation
        self.rotation = rotation

    @staticmethod
    def _check_compatibility(other):
        """
        Checks whether the other argument is a Pose2d object; and raises an error if not
        Args:
            other: The object to compare against

        Raises:
            ValueError
        """
        if isinstance(other, Pose2d):
            return

        raise ValueError("Pose2d and " + str(type(other)) +
                         " are not compatible types, please use Pose2d objects only with other Pose2d object, "
                         "to circumvent this error you can access the internal properties of the Pose2d object and mutate it directly")

    def __add__(self, other):
        """Add two Pose2d objects."""
        self._check_compatibility(other)
        return Pose2d(self.translation + other.translation, self.rotation + other.rotation)

    def __sub__(self, other):
        """Subtract two Pose2d objects."""
        self._check_compatibility(other)
        return Pose2d(self.translation - other.translation, self.rotation - other.rotation)

    def __eq__(self, other):
        """Check if two Pose2d objects are equal."""
        self._check_compatibility(other)
        return self.translation == other.translation and self.rotation == other.rotation

    def __mul__(self, scalar):
        """Multiply Pose2d by a scalar."""
        return Pose2d(self.translation * scalar, self.rotation * scalar)

    def __str__(self):
        """Return the string representation of Pose2d."""
        return "Translation: " + str(self.translation) + ", Rotation: " + str(self.rotation)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def of(cls, translation2d: Translation2d, rotation2d: Rotation2d):
        """Create a Pose2d object from given Translation2d and Rotation2d objects."""
        return cls(translation2d, rotation2d)

    @classmethod
    def from_zero(cls):
        """Create a Pose2d object with zero translation and rotation."""
        return cls(Translation2d(), Rotation2d(0))

    @classmethod
    def from_translation2d(cls, translation2d: Translation2d):
        """Create a Pose2d object from a Translation2d object assuming the rotation is zero radians by default."""
        return cls(translation2d, Rotation2d(0))

    @classmethod
    def from_rotation2d(cls, rotation2d: Rotation2d):
        """Create a Pose2d object from a Rotation2d object assuming the translation is (0, 0) meters by default."""
        return cls(Translation2d(), rotation2d)
