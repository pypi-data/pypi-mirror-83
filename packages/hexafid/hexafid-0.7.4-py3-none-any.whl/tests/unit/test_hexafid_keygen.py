# MIT License
# Copyright (c) 2020 h3ky1

# Standard library imports
import unittest

# Third party imports
# Local application imports
import hexafid.hexafid_keygen as keygen


class TestGlobalConstants(unittest.TestCase):

    def test_symbols(self):
        self.assertEqual(len(keygen.SYMBOLS), 64)
        self.assertEqual(keygen.SYMBOLS, 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/')

    def test_keymap(self):
        self.assertEqual(len(keygen.KEYMAP), len(set(keygen.KEYMAP.values())))


class TestRandomKey(unittest.TestCase):

    def test_random_key(self):
        self.assertNotEqual(keygen.SYMBOLS, keygen.get_random_key())


class TestUniqueSequence(unittest.TestCase):

    def test_unique_sequence(self):
        self.assertEqual(keygen.unique(['e', 'f', 'e', 'f']), ['e', 'f'])


class TestGetKeyFromPass(unittest.TestCase):

    def test_get_key_from_pass_forward(self):
        self.assertEqual(keygen.get_key_from_pass('MyPassword123', 'forward', False),
                         'MyPasword123ABCDEFGHIJKLNOQRSTUVWXYZbcefghijklmnpqtuvxz0456789+/')

    def test_get_key_from_pass_reverse(self):
        self.assertEqual(keygen.get_key_from_pass('MyPassword123', 'reverse', False),
                         'MyPasword123/+9876540zxvutqpnmlkjihgfecbZYXWVUTSRQONLKJIHGFEDCBA')

    def test_get_key_from_pass_alternate(self):
        self.assertEqual(keygen.get_key_from_pass('MyPassword123', 'alternate', False),
                         'MyPasword123BDFHJLORTVXZcfhjlnqux0579/+864zvtpmkigebYWUSQNKIGECA')

    def test_bad_b64_pwd(self):
        with self.assertRaises(SystemExit) as cm:
            keygen.get_key_from_pass('ThisIsMyP@ssword', 'forward', False)

        self.assertEqual(cm.exception.code, "Password must use Base64 characters.")


class TestNaturalKeys(unittest.TestCase):

    def test_natural_default(self):
        self.assertEqual(keygen.use_sequence_layout(keygen.SYMBOLS),
                         'ABJICDLKSTbaQRZYEFNMGHPOWXfeUVdckltsmnvu23/+0198ghpoijrqyz76wx54')

    def test_natural_key(self):
        self.assertEqual(keygen.use_sequence_layout(keygen.get_key_from_pass('MyPassword123', 'forward', False)),
                         'My1dPa32GHRQEFONswBAorDCKLVUIJTSbclkefnmz0/+vx98WXhgYZjitu76pq54')


if __name__ == '__main__':
    unittest.main()
