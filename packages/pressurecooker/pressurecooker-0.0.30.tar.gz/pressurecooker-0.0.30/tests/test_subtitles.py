import os
import hashlib
import tempfile
from unittest import TestCase
from pressurecooker.subtitles import build_subtitle_converter_from_file
from pressurecooker.subtitles import LANGUAGE_CODE_UNKNOWN
from pressurecooker.subtitles import InvalidSubtitleFormatError
from pressurecooker.subtitles import InvalidSubtitleLanguageError
from le_utils.constants import languages, file_formats

test_files_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files', 'subtitles')


class SubtitleConverterTest(TestCase):
    def get_file_hash(self, path):
        hash = hashlib.md5()
        with open(path, 'rb') as fobj:
            for chunk in iter(lambda: fobj.read(2097152), b""):
                hash.update(chunk)

        return hash.hexdigest()

    def assertFileHashesEqual(self, expected_file, actual_file):
        expected_hash = self.get_file_hash(expected_file)
        actual_hash = self.get_file_hash(actual_file)
        self.assertEqual(expected_hash, actual_hash)

    def test_replace_unknown_language(self):
        expected_language = languages.getlang_by_name('Arabic')

        converter = build_subtitle_converter_from_file(os.path.join(test_files_dir, 'basic.srt'))

        self.assertTrue(converter.has_language(LANGUAGE_CODE_UNKNOWN))
        converter.replace_unknown_language(expected_language.code)

        self.assertTrue(converter.has_language(expected_language.code))
        self.assertFalse(converter.has_language(LANGUAGE_CODE_UNKNOWN))

    def test_srt_conversion(self):
        expected_file = os.path.join(test_files_dir, 'basic.vtt')
        expected_language = languages.getlang_by_name('Arabic')

        converter = build_subtitle_converter_from_file(os.path.join(test_files_dir, 'basic.srt'))
        converter.replace_unknown_language(expected_language.code)

        with tempfile.NamedTemporaryFile() as actual_file:
            converter.write(actual_file.name, expected_language.code)
            self.assertFileHashesEqual(expected_file, actual_file.name)

    def test_expected_srt_conversion(self):
        expected_format = file_formats.SRT
        expected_file = os.path.join(test_files_dir, 'basic.vtt')
        expected_language = languages.getlang_by_name('Arabic')

        converter = build_subtitle_converter_from_file(
            os.path.join(test_files_dir, 'basic.srt'), in_format=expected_format)
        converter.replace_unknown_language(expected_language.code)

        with tempfile.NamedTemporaryFile() as actual_file:
            converter.write(actual_file.name, expected_language.code)
            self.assertFileHashesEqual(expected_file, actual_file.name)

    def test_not_expected_type(self):
        expected_format = file_formats.SCC
        expected_language = languages.getlang_by_name('Arabic')

        converter = build_subtitle_converter_from_file(
            os.path.join(test_files_dir, 'basic.srt'), in_format=expected_format)

        with self.assertRaises(InvalidSubtitleFormatError):
            converter.convert(expected_language.code)

    def test_invalid_format(self):
        expected_language = languages.getlang_by_name('English')

        converter = build_subtitle_converter_from_file(os.path.join(test_files_dir, 'not.txt'))

        with self.assertRaises(InvalidSubtitleFormatError):
            converter.convert(expected_language.code)

    def test_invalid_format__empty(self):
        expected_language = languages.getlang_by_name('English')

        converter = build_subtitle_converter_from_file(os.path.join(test_files_dir, 'empty.ttml'))

        with self.assertRaises(InvalidSubtitleFormatError, msg='Caption file is empty'):
            converter.convert(expected_language.code)

    def test_valid_language(self):
        expected_file = os.path.join(test_files_dir, 'encapsulated.vtt')
        expected_language = languages.getlang_by_name('English')

        converter = build_subtitle_converter_from_file(
            os.path.join(test_files_dir, 'encapsulated.sami'))
        self.assertTrue(converter.has_language(expected_language.code))

        with tempfile.NamedTemporaryFile() as actual_file:
            converter.write(actual_file.name, expected_language.code)
            self.assertFileHashesEqual(expected_file, actual_file.name)

    def test_invalid_language(self):
        expected_language = languages.getlang_by_name('Spanish')

        converter = build_subtitle_converter_from_file(
            os.path.join(test_files_dir, 'encapsulated.sami'))

        with self.assertRaises(InvalidSubtitleLanguageError):
            converter.convert(expected_language.code)
