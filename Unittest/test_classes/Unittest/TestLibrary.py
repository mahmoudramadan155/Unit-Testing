import unittest
from datetime import date, timedelta

from library.country import Country
from library.alcohol import Alcohol
from library.person import Person


class TestCountry(unittest.TestCase):
    """Test suite for Country class."""
    
    def test_allow_country(self):
        """Test valid country codes return correct information."""
        iso_code_test_list = ['DK', 'DE', 'UK', 'SE', 'NO']
        for iso_code in iso_code_test_list:
            country = Country.get_country(iso_code=iso_code)
            self.assertTrue(country[0])
            self.assertEqual(dict, type(country[1]))
            self.assertIn('name', country[1])

    def test_disallow_country(self):
        """Test invalid country codes return correct response."""
        country = Country.get_country(iso_code='DA')
        self.assertFalse(country[0])
        self.assertIsNone(country[1])
        
        country = Country.get_country(iso_code='XX')
        self.assertFalse(country[0])
        self.assertIsNone(country[1])

    def test_raise_country_TypeError(self):
        """Test TypeError is raised for incorrect types."""
        with self.assertRaises(TypeError):
            Country.get_country()
            
        with self.assertRaises(TypeError):
            Country.get_country(iso_code=12)
            
        with self.assertRaises(TypeError):
            Country.get_country(iso_code=None)
            
        with self.assertRaises(TypeError):
            Country.get_country(iso_code=True)

    def test_raise_country_ValueError(self):
        """Test ValueError is raised for incorrect formats."""
        with self.assertRaises(ValueError):
            Country.get_country(iso_code='Denmark')
            
        with self.assertRaises(ValueError):
            Country.get_country(iso_code='D')
            
        with self.assertRaises(ValueError):
            Country.get_country(iso_code='')
            
        with self.assertRaises(ValueError):
            Country.get_country(iso_code='DEU')


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


class TestPerson(unittest.TestCase):
    """Test suite for Person class."""
    
    def setUp(self):
        self.person = Person()
        
        # Create test birthdays for different ages
        today = date.today()
        self.birthday_15 = today.replace(year=today.year - 15)
        self.birthday_16 = today.replace(year=today.year - 16)
        self.birthday_17 = today.replace(year=today.year - 17)
        self.birthday_18 = today.replace(year=today.year - 18)
        self.birthday_21 = today.replace(year=today.year - 21)
        
        # Handle birthdays that would be in the future this year
        if self.birthday_15 > today:
            self.birthday_15 = self.birthday_15.replace(year=self.birthday_15.year - 1)
        if self.birthday_16 > today:
            self.birthday_16 = self.birthday_16.replace(year=self.birthday_16.year - 1)
        if self.birthday_17 > today:
            self.birthday_17 = self.birthday_17.replace(year=self.birthday_17.year - 1)
        if self.birthday_18 > today:
            self.birthday_18 = self.birthday_18.replace(year=self.birthday_18.year - 1)
        if self.birthday_21 > today:
            self.birthday_21 = self.birthday_21.replace(year=self.birthday_21.year - 1)

    def test_calculate_age(self):
        """Test age calculation works correctly."""
        self.assertEqual(15, self.person._calculate_age(self.birthday_15))
        self.assertEqual(16, self.person._calculate_age(self.birthday_16))
        self.assertEqual(17, self.person._calculate_age(self.birthday_17))
        self.assertEqual(18, self.person._calculate_age(self.birthday_18))
        self.assertEqual(21, self.person._calculate_age(self.birthday_21))

    def test_allowed_to_buy_alcohol_underage(self):
        """Test underage persons cannot buy alcohol."""
        self.assertFalse(self.person.allowed_to_buy_alcohol(self.birthday_15, 4.6))
        self.assertFalse(self.person.allowed_to_buy_alcohol(self.birthday_15, 16.5))
        self.assertFalse(self.person.allowed_to_buy_alcohol(self.birthday_15, 40.0))

    def test_allowed_to_buy_alcohol_16_17(self):
        """Test 16-17 year olds can only buy low-percentage alcohol."""
        # 16-year-old
        self.assertTrue(self.person.allowed_to_buy_alcohol(self.birthday_16, 4.6))
        self.assertTrue(self.person.allowed_to_buy_alcohol(self.birthday_16, 16.5))
        self.assertFalse(self.person.allowed_to_buy_alcohol(self.birthday_16, 16.6))
        self.assertFalse(self.person.allowed_to_buy_alcohol(self.birthday_16, 40.0))
        
        # 17-year-old
        self.assertTrue(self.person.allowed_to_buy_alcohol(self.birthday_17, 4.6))
        self.assertTrue(self.person.allowed_to_buy_alcohol(self.birthday_17, 16.5))
        self.assertFalse(self.person.allowed_to_buy_alcohol(self.birthday_17, 16.6))
        self.assertFalse(self.person.allowed_to_buy_alcohol(self.birthday_17, 40.0))

    def test_allowed_to_buy_alcohol_18_plus(self):
        """Test 18+ year olds can buy any alcohol."""
        self.assertTrue(self.person.allowed_to_buy_alcohol(self.birthday_18, 4.6))
        self.assertTrue(self.person.allowed_to_buy_alcohol(self.birthday_18, 16.5))
        self.assertTrue(self.person.allowed_to_buy_alcohol(self.birthday_18, 40.0))
        self.assertTrue(self.person.allowed_to_buy_alcohol(self.birthday_18, 100.0))
        
        self.assertTrue(self.person.allowed_to_buy_alcohol(self.birthday_21, 4.6))
        self.assertTrue(self.person.allowed_to_buy_alcohol(self.birthday_21, 16.5))
        self.assertTrue(self.person.allowed_to_buy_alcohol(self.birthday_21, 40.0))
        self.assertTrue(self.person.allowed_to_buy_alcohol(self.birthday_21, 100.0))

    def test_allowed_to_buy_alcohol_invalid_inputs(self):
        """Test invalid inputs for allowed_to_buy_alcohol raise appropriate errors."""
        with self.assertRaises(TypeError):
            self.person.allowed_to_buy_alcohol("not-a-date", 40.0)
            
        with self.assertRaises(ValueError):
            self.person.allowed_to_buy_alcohol(self.birthday_18, -1)
            
        with self.assertRaises(ValueError):
            self.person.allowed_to_buy_alcohol(self.birthday_18, 101)
            
        with self.assertRaises(ValueError):
            self.person.allowed_to_buy_alcohol(self.birthday_18, "40")

    def test_allowed_to_buy_tobacco(self):
        """Test tobacco purchase age verification."""
        self.assertFalse(self.person.allowed_to_buy_tobacco(self.birthday_15))
        self.assertFalse(self.person.allowed_to_buy_tobacco(self.birthday_16))
        self.assertFalse(self.person.allowed_to_buy_tobacco(self.birthday_17))
        self.assertTrue(self.person.allowed_to_buy_tobacco(self.birthday_18))
        self.assertTrue(self.person.allowed_to_buy_tobacco(self.birthday_21))

    def test_allowed_to_buy_tobacco_invalid_inputs(self):
        """Test invalid inputs for allowed_to_buy_tobacco raise appropriate errors."""
        with self.assertRaises(TypeError):
            self.person.allowed_to_buy_tobacco("not-a-date")
            
        with self.assertRaises(TypeError):
            self.person.allowed_to_buy_tobacco(None)


if __name__ == '__main__':
    unittest.main()
