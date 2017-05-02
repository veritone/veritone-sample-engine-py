import unittest

from src.translator import encode_morse, decode_morse

TEXT = 'HELLO VERITONE DEVELOPER'
ENCODED = '.... . .-.. .-.. --- / ...- . .-. .. - --- -. . / -.. . ...- . .-.. --- .--. . .-. '


class TestMorseTranslator(unittest.TestCase):
    def test_encode(self):
        self.assertEqual(encode_morse(TEXT), ENCODED)

    def test_decode(self):
        self.assertEqual(decode_morse(ENCODED), TEXT)


if __name__ == '__main__':
    unittest.main()
