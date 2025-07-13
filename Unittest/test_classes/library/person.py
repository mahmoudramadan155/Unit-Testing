
from datetime import date

class Person:
    """Class for handling person-related age verification."""
    
    def _calculate_age(self, birthday):
        """
        Calculate a person's age based on their birthday.
        
        Args:
            birthday: date object representing birthday
            
        Returns:
            int: Age in years
            
        Raises:
            TypeError: If birthday is not a date object
        """
        if not isinstance(birthday, date):
            raise TypeError('Birthday must be a date object')
            
        today = date.today()
        return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

    def allowed_to_buy_alcohol(self, birthday, alcohol_percentage):
        """
        Check if a person is allowed to buy alcohol based on age and alcohol percentage.
        
        Rules:
        - Under 16: No alcohol allowed
        - 16-17: Only alcohol ≤16.5% allowed
        - 18+: All alcohol allowed
        
        Args:
            birthday: date object representing birthday
            alcohol_percentage: Alcohol percentage
            
        Returns:
            bool: Whether the person is allowed to buy the alcohol
            
        Raises:
            TypeError: If birthday is not a date object
            ValueError: If alcohol_percentage is invalid
        """
        if not isinstance(birthday, date):
            raise TypeError('Birthday must be a date object')
            
        if not isinstance(alcohol_percentage, (int, float)):
            raise ValueError('Alcohol percentage must be a numeric value')
        elif alcohol_percentage < 0 or alcohol_percentage > 100:
            raise ValueError('Alcohol percentage must be between 0 and 100')
        
        age = self._calculate_age(birthday)
        
        if age < 16:
            return False
        elif 16 <= age < 18:
            return alcohol_percentage <= 16.5
        else:  # age >= 18
            return True

    def allowed_to_buy_tobacco(self, birthday):
        """
        Check if a person is allowed to buy tobacco based on age.
        
        Rules:
        - 18+: Tobacco allowed
        
        Args:
            birthday: date object representing birthday
            
        Returns:
            bool: Whether the person is allowed to buy tobacco
            
        Raises:
            TypeError: If birthday is not a date object
        """
        if not isinstance(birthday, date):
            raise TypeError('Birthday must be a date object')
            
        age = self._calculate_age(birthday)
        return age >= 18
    