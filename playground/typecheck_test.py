import unittest


def greeting(name: str) -> str:
    return 'Hello ' + name

class TestTypeCheck(unittest.TestCase):

    def test_type_checking(self):
        self.assertRaises(TypeError, greeting, name=42.7)


if __name__ == "__main__":
    unittest.main()
