import unittest
import demo 

class testCalc(unittest.TestCase):
    def test_add(self):
        self.assertEqual(demo.calc.add(5,10),15, "Should be 15")
        self.assertEqual(demo.calc.add(-1,-1),-2)
        self.assertEqual(demo.calc.add(-1,1),0)

    def test_subtract(self):
        self.assertEqual(demo.calc.subtract(5,10),-5, "Should be -5")
        self.assertEqual(demo.calc.subtract(-1,-1),0)
        self.assertEqual(demo.calc.subtract(-1,1),-2)

    def test_multiply(self):
        self.assertEqual(demo.calc.multiple(5,10),50, "Should be 50")
        self.assertEqual(demo.calc.multiple(-1,-1),1)
        self.assertEqual(demo.calc.multiple(-1,1),-1)

    def test_divide(self):
        result = demo.calc.divide(10,5)
        self.assertEqual(result, 2 , "Should be 2")

        with self.assertRaises(ValueError):
            demo.calc.divide(10,0)

if __name__ == "__main__":
    unittest.main()
    