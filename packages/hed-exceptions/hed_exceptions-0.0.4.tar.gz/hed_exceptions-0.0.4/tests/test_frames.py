from unittest import TestCase

from hed_exceptions import frames


class FramesTest(TestCase):
    def __init__(self, *args, **kwargs):
        self.maxDiff = 2000
        super().__init__(*args, **kwargs)

    def setUp(self) -> None:
        self.maxDiff = 2000

    def test_get_caller_direct(self):
        def called_method():
            return frames.get_caller()

        def caller_method():
            local_str = "s"
            local_int = 2
            return called_method()

        fi = caller_method()
        self.assertEqual("caller_method", fi.function)
        self.assertEqual(__file__, fi.filename)
        self.assertDictEqual(
            dict(called_method=called_method, local_str="s", local_int=2),
            fi.frame.f_locals
        )

    def test_get_caller_distant(self):
        self.maxDiff = 2000

        def called_method():
            return frames.get_caller(3)

        def direct_caller():
            return called_method()

        def indirect_caller():
            return direct_caller()

        def distant_caller():
            local_var = 4
            return indirect_caller()

        fi = distant_caller()
        self.assertEqual("distant_caller", fi.function)
        self.assertIn("local_var", fi.frame.f_locals)
        self.assertEqual(4, fi.frame.f_locals["local_var"])

    def test_get_creation_direct(self):
        class Stash:
            def __init__(self):
                self.fi_created = frames.get_creation(self)

        local_c_var = 2
        s = Stash()
        fi = s.fi_created
        self.assertEqual("test_get_creation_direct", fi.function)
        self.assertIn("local_c_var", fi.frame.f_locals)
        self.assertIs(local_c_var, fi.frame.f_locals["local_c_var"])
        self.assertIn("Stash", fi.frame.f_locals)
        self.assertIs(Stash, fi.frame.f_locals["Stash"])

    def test_get_creation_distant(self):
        # randomly defined 'local_bool' to ensure the proper is picked-up
        class A:
            def __init__(self):
                self.fi_created = frames.get_creation(self)

            local_bool = "a"

        class B(A):

            def __init__(self):
                local_bool = 2
                super().__init__()

        class C(B):
            local_bool = None

            def __init__(self):
                super().__init__()

        local_bool = [2, 3, "C"]

        def create_c():
            local_bool = True
            return C()

        local_bool = False
        fi = create_c().fi_created
        self.assertEqual("create_c", fi.function)
        self.assertIn("local_bool", fi.frame.f_locals)
        self.assertIs(True, fi.frame.f_locals["local_bool"])
