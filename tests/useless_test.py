import unittest


class DownloaderTest(unittest.TestCase):
    def test_dummy(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])


if __name__ == '__main__':
    unittest.main()
