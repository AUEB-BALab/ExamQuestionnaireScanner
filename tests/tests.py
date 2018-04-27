import unittest
import sys, os

sys.path.append(".")

from CSVparser import checkParityBit

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def test_parity_validID(self):
        self.assertEqual(checkParityBit("100010", 12), True)
        self.assertEqual(checkParityBit("001010", 12), True)
        self.assertNotEqual(checkParityBit("101010", 12), True)
        self.assertNotEqual(checkParityBit("001110", 12), True)


    def test_parity_invalidID(self):
        self.assertEqual(checkParityBit("100110", 12), False)
        self.assertEqual(checkParityBit("000010", 12), False)
        self.assertNotEqual(checkParityBit("000010", 12), True)
        self.assertNotEqual(checkParityBit("110010", 12), True)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test)
    unittest.TextTestRunner().run(suite)