""" Unit tests for readers"""
import pkg_resources
import unittest
from LoggerReader import readers

pkg = "LoggerReader"


class TestFG2_399(unittest.TestCase):

    def setUp(self):
        dat_fg2_399 = pkg_resources.resource_filename(pkg, "sample_files/FG2_399.csv")
        self.reader = readers.FG2()
        self.reader.read(dat_fg2_399)

    def test_array_shape(self):
        self.assertEqual(self.reader.get_data().shape[0], 9869)
        self.assertEqual(self.reader.get_data().shape[1], 8)

    def test_date_order(self):
        self.assertLess(self.reader.get_data().iloc[1,0], self.reader.get_data().iloc[10,0])
        self.assertGreater(self.reader.get_data().iloc[100,0], self.reader.get_data().iloc[10,0])


class TestGP5W_270(unittest.TestCase):

    def setUp(self):
        dat_gp5w_270 = pkg_resources.resource_filename(pkg, "sample_files/GP5W_270.csv")
        self.reader = readers.GP5W()
        self.reader.read(dat_gp5w_270)

    def test_array_shape(self):
        self.assertEqual(self.reader.get_data().shape[0], 2206)
        self.assertEqual(self.reader.get_data().shape[1], 8)

    def test_date_order(self):
        self.assertLess(self.reader.get_data().iloc[1,0], self.reader.get_data().iloc[10,0])
        self.assertGreater(self.reader.get_data().iloc[100,0], self.reader.get_data().iloc[10,0])


class TestGP5W_260(unittest.TestCase):

    def setUp(self):
        dat_gp5w_260 = pkg_resources.resource_filename(pkg, "sample_files/GP5W_260.csv")
        self.reader = readers.GP5W()
        self.reader.read(dat_gp5w_260)

    def test_array_shape(self):
        self.assertEqual(self.reader.get_data().shape[0], 1882)
        self.assertEqual(self.reader.get_data().shape[1], 4)

    def test_date_order(self):
        self.assertLess(self.reader.get_data().iloc[1,0], self.reader.get_data().iloc[10,0])
        self.assertGreater(self.reader.get_data().iloc[100,0], self.reader.get_data().iloc[10,0])


if __name__ == '__main__':
    unittest.main()
