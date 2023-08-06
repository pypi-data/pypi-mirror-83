# MIT License
# Copyright (c) 2020 h3ky1

# Standard library imports
import unittest
# Third party imports
from click.testing import CliRunner
# Local application imports
from hexafid.hexafid_cli import main as hexafid


class TestVersion(unittest.TestCase):

    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(hexafid, ['--version'])
        assert result.exit_code == 0
        assert "version" in result.output


class TestHelp(unittest.TestCase):

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(hexafid, ['--help'])
        assert result.exit_code == 0
        assert "Show this message and exit." in result.output


class TestEncryption(unittest.TestCase):

    def test_message_default_encryption_with_prompt(self):
        runner = CliRunner()
        result = runner.invoke(hexafid, input='Hello World\n')
        assert not result.exception
        assert "Ciphertext" in result.output

    def test_message_default_encryption_with_key_and_file(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('hello.txt', 'w') as f:
                f.write('Hello World')

            result = runner.invoke(hexafid, ['--key', 'MyPassword123', '--filein', 'hello.txt', '--field'])
            assert result.exit_code == 0
            assert "MyPasword123" in result.output  # also tests key generation but that is redundant for UI

    def test_message_ctr_encryption_with_keygen_and_file(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('hello.txt', 'w') as f:
                f.write('Hello World')

            result = runner.invoke(hexafid, ['--filein', 'hello.txt', '--mode', 'CTR'])
            assert result.exit_code == 0
            assert "Ciphertext" in result.output

    def test_message_ecb_encryption_with_keygen_and_file(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('hello.txt', 'w') as f:
                f.write('Hello World')

            result = runner.invoke(hexafid, ['--filein', 'hello.txt', '--mode', 'ECB'])
            assert result.exit_code == 0
            assert "Ciphertext" in result.output

    def test_message_encryption_to_file(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('hello.txt', 'w') as f:
                f.write('Hello World')
            encrypted = runner.invoke(hexafid,
                                      ['--encrypt', '--filein', 'hello.txt', '--fileout', 'crypt.txt',
                                       '--key', 'swordfish', '--field'])
            with open('crypt.txt', 'r') as f:
                decrypted = runner.invoke(hexafid,
                                          ['--decrypt', '--filein', 'crypt.txt', '--key', 'swordfish', '--field'])
                assert not encrypted.exception
                assert "Hello/World" in decrypted.output


class TestDecryption(unittest.TestCase):

    def test_message_default_decryption_with_prompt(self):
        runner = CliRunner()
        result = runner.invoke(hexafid, ['--decrypt', '--key', 'swordfish', '--field'],
                               input='uridA4XXr2xbj7OQWVwXzavXcKzKaW==\n')
        assert not result.exception
        assert "Hello/World" in result.output

    def test_message_decryption_to_file(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(hexafid, ['--decrypt', '--fileout', 'hello.txt', '--key', 'swordfish', '--field'],
                                   input='uridA4XXr2xbj7OQWVwXzavXcKzKaW==\n')
            with open('hello.txt', 'r') as f:
                assert not result.exception
                assert "Hello/World" in f.read()
