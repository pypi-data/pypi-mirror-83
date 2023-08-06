import unittest

from lance.generators.java.typs import *


class TestTypes(unittest.TestCase):

    def test_custom_type(self):
        x, y = process_type(TYPE_CLASS, fqcn="com.susamn.Custom")
        print(x, y)

    def test_void_type(self):
        x, y = process_type(TYPE_VOID)
        print(x, y)

    def test_normal_type(self):
        x, y = process_type(TYPE_STRING)
        print(x, y)


    def test_list_type(self):
        x, y= process_type(TYPE_LIST_STRING)
        print(x, y)

    def test_list_int(self):
        x, y= process_type(TYPE_LIST_INTEGER)
        print(x, y)

    def test_list_float(self):
        x, y= process_type(TYPE_LIST_FLOAT)
        print(x, y)

    def test_list_bool(self):
        x, y= process_type(TYPE_LIST_BOOLEAN)
        print(x, y)


    def test_list_custom(self):
        x, y= process_type(TYPE_LIST_CLASS, fqcn="com.susamn.Foo")
        print(x, y)



if __name__ == '__main__':
    unittest.main()
