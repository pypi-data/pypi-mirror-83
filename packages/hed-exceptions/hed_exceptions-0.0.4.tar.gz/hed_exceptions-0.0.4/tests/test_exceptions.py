from unittest import TestCase

from hed_exceptions.exceptions import ArgumentError


class ArgumentErrorTest(TestCase):

    def test_raise_with_name_and_msg(self):
        def func(b):
            raise ArgumentError("b", "No like it!")

        try:
            func("k0r")
        except ArgumentError as e:
            self.assertEqual("No like it!", e.msg)
            self.assertEqual("b", e.arg.name)
            self.assertEqual(str, e.arg.type)
            self.assertEqual("k0r", e.arg.value)
            self.assertEqual(
                "ArgumentError('No like it!', Arg(name='b', type=<class 'str'>, value='k0r'))",
                repr(e)
            )

    def test_raise_with_no_msg(self):
        def func(a):
            raise ArgumentError("a")

        try:
            func(1)
        except ArgumentError as e:
            self.assertEqual(
                "ArgumentError('Bad arg!', Arg(name='a', type=<class 'int'>, value=1))",
                repr(e)
            )

    def test_constructor_with_no_or_empty_name(self):
        with self.assertRaises(TypeError):
            ArgumentError(None)
        with self.assertRaises(ValueError):
            ArgumentError("  \t ")

    def test_constructor_with_no_such_var_in_closure(self):
        with self.assertRaises(KeyError):
            ArgumentError("nope")
