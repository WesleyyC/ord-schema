"""Tests for ord_schema.data_storage."""

import os
import tempfile

from absl import flags
from absl.testing import absltest

from ord_schema import data_storage
from ord_schema import message_helpers
from ord_schema.proto import reaction_pb2


class WriteDataTest(absltest.TestCase):

    def setUp(self):
        super().setUp()
        self.test_subdirectory = tempfile.mkdtemp(dir=flags.FLAGS.test_tmpdir)

    def test_string_value(self):
        message = reaction_pb2.Data(value='test value')
        filename = data_storage.write_data(message, self.test_subdirectory)
        expected = os.path.join(
            self.test_subdirectory,
            'ord_data-'
            '47d1d8273710fd6f6a5995fac1a0983fe0e8828c288e35e80450ddc5c4412def'
            '.txt')
        self.assertEqual(filename, expected)
        # NOTE(kearnes): Open with 'r' to get the decoded string.
        with open(filename, 'r') as f:
            self.assertEqual(message.value, f.read())

    def test_bytes_value(self):
        message = reaction_pb2.Data(bytes_value=b'test value')
        filename = data_storage.write_data(message, self.test_subdirectory)
        expected = os.path.join(
            self.test_subdirectory,
            'ord_data-'
            '47d1d8273710fd6f6a5995fac1a0983fe0e8828c288e35e80450ddc5c4412def'
            '.txt')
        self.assertEqual(filename, expected)
        with open(filename, 'rb') as f:
            self.assertEqual(message.bytes_value, f.read())

    def test_url_value(self):
        message = reaction_pb2.Data(url='test value')
        self.assertIsNone(
            data_storage.write_data(message, self.test_subdirectory))

    def test_missing_value(self):
        message = reaction_pb2.Data()
        with self.assertRaisesRegex(ValueError, 'no value to write'):
            data_storage.write_data(message, self.test_subdirectory)

    def test_min_max_size(self):
        message = reaction_pb2.Data(value='test_value')
        with self.assertRaisesRegex(ValueError, 'must be less than or equal'):
            data_storage.write_data(
                message, self.test_subdirectory, min_size=2.0, max_size=1.0)

    def test_min_size(self):
        message = reaction_pb2.Data(value='test_value')
        self.assertIsNone(
            data_storage.write_data(
                message, self.test_subdirectory, min_size=1.0))

    def test_max_size(self):
        message = reaction_pb2.Data(value='test value')
        with self.assertRaisesRegex(ValueError, 'larger than max_size'):
            data_storage.write_data(
                message, self.test_subdirectory, max_size=1e-6)


class ExtractDataTest(absltest.TestCase):

    def setUp(self):
        super().setUp()
        self.test_subdirectory = tempfile.mkdtemp(dir=flags.FLAGS.test_tmpdir)

    def test_find_data_messages(self):
        message = reaction_pb2.Reaction()
        self.assertEmpty(
            message_helpers.find_submessages(message, reaction_pb2.Data))
        message = reaction_pb2.ReactionObservation()
        message.image.value = 'not an image'
        self.assertLen(
            message_helpers.find_submessages(message, reaction_pb2.Data), 1)
        message = reaction_pb2.ReactionSetup()
        message.automation_code['test1'].value = 'test data 1'
        message.automation_code['test2'].bytes_value = b'test data 2'
        self.assertLen(
            message_helpers.find_submessages(message, reaction_pb2.Data), 2)
        message = reaction_pb2.Reaction()
        message.observations.add().image.value = 'not an image'
        message.setup.automation_code['test1'].value = 'test data 1'
        message.setup.automation_code['test2'].bytes_value = b'test data 2'
        self.assertLen(
            message_helpers.find_submessages(message, reaction_pb2.Data), 3)

    def test_extract_data(self):
        message = reaction_pb2.ReactionObservation()
        message.image.value = 'not an image'
        data_storage.extract_data(message, root=self.test_subdirectory)
        relative_path = (
            'data/54/ord_data-'
            '5464533c9647b67eb320c40ccc5959537c09102ae75388f6a7675b433e745c9d'
            '.txt')
        expected = ('https://github.com/Open-Reaction-Database/'
                    'ord-submissions-test/tree/' + relative_path)
        self.assertEqual(message.image.url, expected)
        with open(os.path.join(self.test_subdirectory, relative_path)) as f:
            self.assertEqual(f.read(), 'not an image')


if __name__ == '__main__':
    absltest.main()
