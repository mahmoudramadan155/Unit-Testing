
class Country:
    """Class for handling country information and validation."""
    
    COUNTRY_DICT = {
        'DK': {'name': 'Denmark'},
        'DE': {'name': 'Germany'},
        'UK': {'name': 'United Kingdom'},
        'SE': {'name': 'Sweden'},
        'NO': {'name': 'Norway'}
    }
    
    @classmethod
    def get_country(cls, iso_code=None):
        """
        Get country information by ISO code.
        
        Args:
            iso_code: Two-letter ISO country code
            
        Returns:
            tuple: (bool, dict) - Success flag and country data if found
            
        Raises:
            TypeError: If iso_code is not a string
            ValueError: If iso_code is not exactly 2 characters
        """
        if iso_code is None:
            raise TypeError('iso_code must be provided as a string')
        
        if not isinstance(iso_code, str):
            raise TypeError('iso_code must be a string')
        elif len(iso_code) != 2:
            raise ValueError('iso_code must be 2 characters long')

        if iso_code in cls.COUNTRY_DICT:
            return True, cls.COUNTRY_DICT[iso_code]
        else:
            return False, None
        