import unittest

from library.country import Country

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

if __name__ == '__main__':
    unittest.main()