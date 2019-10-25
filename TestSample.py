import unittest

from pyaimms.funcs import aimms


class MyTestCase(unittest.TestCase):
    def test_something(self):
        AIMMS = aimms(path='example/Calling AIMMSCOM', project_name='RunAIMMS.aimms')
        print('word')  # todo; finish implementation
        self.assertEqual(True, False)

    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
