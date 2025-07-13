import unittest

from library.alcohol import Alcohol

class TestAlcohol(unittest.TestCase):
    """Test suite for Alcohol class."""
    
    def setUp(self):
        self.alcohol = Alcohol()

    def test_calc_unit_valid_inputs(self):
        """Test calculation of alcohol units with valid inputs."""
        self.assertEqual(1.01, self.alcohol.calc_unit(cl=33, percentage=4.6))
        self.assertEqual(14.0, self.alcohol.calc_unit(cl=70, percentage=30))
        self.assertEqual(20.0, self.alcohol.calc_unit(cl=30, percentage=100))
        self.assertEqual(0.0, self.alcohol.calc_unit(cl=30, percentage=0))
        self.assertEqual(0.0, self.alcohol.calc_unit(cl=0, percentage=40))

    def test_calc_unit_invalid_inputs(self):
        """Test ValueError is raised for invalid inputs to calc_unit."""
        with self.assertRaises(ValueError):
            self.alcohol.calc_unit(cl=30, percentage=101)
            
        with self.assertRaises(ValueError):
            self.alcohol.calc_unit(cl=30, percentage=-1)
            
        with self.assertRaises(ValueError):
            self.alcohol.calc_unit(cl=30, percentage='40')
            
        with self.assertRaises(ValueError):
            self.alcohol.calc_unit(cl=None, percentage=50)
            
        with self.assertRaises(ValueError):
            self.alcohol.calc_unit(cl='30', percentage=50)
            
        with self.assertRaises(ValueError):
            self.alcohol.calc_unit(cl=-10, percentage=50)

    def test_unit_to_gram_valid_inputs(self):
        """Test conversion of units to grams with valid inputs."""
        self.assertEqual(12, self.alcohol.unit_to_gram(units=1))
        self.assertEqual(18, self.alcohol.unit_to_gram(units=1.5))
        self.assertEqual(45, self.alcohol.unit_to_gram(units=3.75))
        self.assertEqual(0, self.alcohol.unit_to_gram(units=0))

    def test_unit_to_gram_invalid_inputs(self):
        """Test ValueError is raised for invalid inputs to unit_to_gram."""
        with self.assertRaises(ValueError):
            self.alcohol.unit_to_gram(units=-1)
            
        with self.assertRaises(ValueError):
            self.alcohol.unit_to_gram(units='3')
            
        with self.assertRaises(ValueError):
            self.alcohol.unit_to_gram(units=None)

if __name__ == '__main__':
    unittest.main()
