import unittest
from VEXLib.Geometry.Translation2d import Translation2d

class TestTranslation2d(unittest.TestCase):
    def test_addition(self):
        t1 = Translation2d.from_meters(3, 4)
        t2 = Translation2d.from_meters(1, 2)
        result = t1 + t2
        self.assertEqual(result.to_meters(), (4, 6))

    def test_subtraction(self):
        t1 = Translation2d.from_meters(3, 4)
        t2 = Translation2d.from_meters(1, 2)
        result = t1 - t2
        self.assertEqual(result.to_meters(), (2, 2))

    def test_equality(self):
        t1 = Translation2d.from_meters(3, 4)
        t2 = Translation2d.from_meters(3, 4)
        self.assertEqual(t1, t2)

    def test_multiplication(self):
        t1 = Translation2d.from_meters(3, 4)
        scalar = 2
        result = t1 * scalar
        self.assertEqual(result.to_meters(), (6, 8))

    def test_from_meters(self):
        t = Translation2d.from_meters(3, 4)
        self.assertEqual(t.to_meters(), (3, 4))

    def test_from_centimeters(self):
        t = Translation2d.from_centimeters(300, 400)
        self.assertAlmostEqual(t.x_component.to_meters(), 3, places=4)
        self.assertAlmostEqual(t.y_component.to_meters(), 4, places=4)

    def test_from_inches(self):
        t = Translation2d.from_inches(118.11, 157.48)
        self.assertAlmostEqual(t.x_component.to_meters(), 3, places=4)
        self.assertAlmostEqual(t.y_component.to_meters(), 4, places=4)

    def test_from_feet(self):
        t = Translation2d.from_feet(9.84252, 13.1234)
        self.assertAlmostEqual(t.x_component.to_meters(), 3, places=4)
        self.assertAlmostEqual(t.y_component.to_meters(), 4, places=4)

    def test_to_meters(self):
        t = Translation2d.from_meters(3, 4)
        x, y = t.to_meters()
        self.assertEqual(x, 3)
        self.assertEqual(y, 4)

    def test_to_centimeters(self):
        t = Translation2d.from_meters(3, 4)
        self.assertEqual(t.to_centimeters(), (300, 400))

    def test_to_inches(self):
        t = Translation2d.from_meters(3, 4)
        x, y = t.to_inches()
        self.assertAlmostEqual(x, 118.11, places=2)
        self.assertAlmostEqual(y, 157.48, places=2)

if __name__ == '__main__':
    unittest.main()
