import unittest

from pyaimms.funcs import aimms


class MyTestCase(unittest.TestCase):
    def test_something(self):
        AIMMS = aimms(path=r'c:\Users\wsun\OneDrive - University of Edinburgh\AIMMS G_converted - AP', project_name='OPF ANM.aimms')
        print('word')
        self.assertEqual(True, False)

    def test_something(self):
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
