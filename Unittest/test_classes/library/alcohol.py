
class Alcohol:
    """Class for handling alcohol-related calculations."""
    
    @staticmethod
    def calc_unit(cl, percentage):
        """
        Calculate alcohol units based on volume and percentage.
        
        Formula: (cl * percentage) / (100 * 1.5)
        
        Args:
            cl: Volume in centiliters
            percentage: Alcohol percentage
            
        Returns:
            float: Alcohol units rounded to 2 decimal places
            
        Raises:
            ValueError: If inputs are not numeric or percentage is out of range
        """
        if not isinstance(percentage, (int, float)) or not isinstance(cl, (int, float)):
            raise ValueError('Both cl and percentage must be numeric values')
        elif percentage > 100 or percentage < 0:
            raise ValueError('Percentage must be between 0 and 100')
        elif cl < 0:
            raise ValueError('Volume (cl) cannot be negative')

        return round((cl * percentage) / (100 * 1.5), 2)

    @staticmethod
    def unit_to_gram(units):
        """
        Convert alcohol units to grams.
        
        Formula: units * 12
        
        Args:
            units: Number of alcohol units
            
        Returns:
            int: Alcohol amount in grams (rounded)
            
        Raises:
            ValueError: If units is not numeric or negative
        """
        if not isinstance(units, (int, float)):
            raise ValueError('Units must be a numeric value')
        elif units < 0:
            raise ValueError('Units cannot be negative')
            
        return round(units * 12)
    