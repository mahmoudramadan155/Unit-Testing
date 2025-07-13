"""
Unit testing: we are also say component testing.

Test Runner

The Module That Run The Unit Testing (unittest, pytest)

Test case:
Smallest Unit Of Testing
It Use Asserts Methods To Check For Actions And Responses

Test Suite:
Collection Of Multiple Tests Or Test Cases

Test Report
A Full Report Contains The Failure Or Succeed

Unittest
Add Tests Into Classes As Methods

ex: Senario 
your company is hired by a bank to develop online banking application
# requirement analysis
1- Login valid credentials
2- deposit
3- withdraw
4- transfer


1-> login component
login id & password

test cases:
1- enter valid ID & password -> happy senario case
2- enter invalid id & password
3- empty login ID & click login

Objective:

    Understand and use Pytest for testing Python code Effectively

What is testing and why is it Important?

    It is the process of ensuring that our code functions correctly, meets
    requirements, and is free of bugs

    Early bug detection

    Improves Code Quality and Reliability

    Facilitates Maintenance Ensuring changes do not break existing code

    Boosts Productivity & Confidence for stakeholders

    Enhances User Experience

What will we learn?

    How to install pytest
    Explain the structure of a test function
    How to use assertions to test expected outcomes
    How to runs tests and interpret the outputs
    Best practices for naming & organizing test files & functions
    What are fixtures and how to use them
    How to test functions and Classes

Adv unit testing
1- developers looking to learn what functionality is provided by a unit 
    and how to use it can look at the unit tests to gain a basic understanding of the unit API.

unit testing allows the programmer to refactor code at a later date,

"Advantages of Unit Test"
    1) Confidence between Developer and Code 
    2) Fixing Bugs at early stage 
    3) Maintenance is quick.
    4) Self Documenting 
    5) High Quality Code

Unit Testing Disadvantages
1- unit testing can't be expected to catch every error in a program.
 it is not possible to evaluate all execution pathes even in the most trivial program

unittest

the unittest framework produce 3 possible outputs:- OK, FAILED, and ERROR

OK: when all the tests pass

FAILED: When an AssertionError exception is raised (assertion is unseccful), the output FAILED

ERROR: When ALL the test cases did not pass and it raises an excption other than Assertion

"""

import unittest

# assert 3*8 == 24, "should be 24"

# def test_case_one():
#     assert 5 * 10 == 50, "Should Be 50"

# def test_case_two():
#     assert 5 * 50 == 240, "Should Be 250"

# def test_case_multiply_1():
#     assert 5*10 == 50, "should be 50"

# def test_case_multiply_2():
#     assert 5*11 == 55, "should be 55"

# def test_case_multiply_3():
#     assert 5*12 == 60, "should be 60"

# test_case_multiply_1()
# test_case_multiply_2()
# test_case_multiply_3()

# class myTestCases(unittest.TestCase):
#     def test_one(self):
#         self.assertTrue(100 > 99, 'should be true')

#     def test_two(self):
#         self.assertEqual(40+60,100, "should be 100")

#     def test_three(self):
#         self.assertGreater(102, 101, "Should Be True")
    
#     def test_upper(self):
#         self.assertEqual('iti'.upper(), "ITI")

#     def test_isupper(self):
#         self.assertTrue('ITI'.isupper())
#         self.assertFalse('ITI'.islower())


class calc:
    def add(x,y):
        return x+y
    
    def subtract(x,y):
        return x-y
    
    def multiple(x,y):
        return x*y
    
    def divide(x,y):
        if y==0:
            raise ValueError("Can't divide by zero!")
        return x/y

class Rectangle:
    def __init__(self,width, height):
        self.width = width
        self.height = height

    def get_area(self):
        return self.width*self.height
    
    def set_width(self, width):
        self.width = width
    
    def set_height(self, height):
        self.height = height

class TestGetAreaRectangle(unittest.TestCase):
    def runTest(self):
        rectangle = Rectangle(3,3)
        self.assertEqual(rectangle.get_area(),9, 'Inncorrect area')

if __name__ == "__main__":
    unittest.main()
    
    