import unittest
import tempfile
import os
from datetime import datetime
from log_parser.parser import parse_log_file, evaluate_durations


class TestLogParser(unittest.TestCase):
    def setUp(self):
        # Create a temporary log file
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='')
        self.temp_file.write(
            "12:00:00,TaskA,START,123\n"
            "12:05:10,TaskA,END,123\n"
            "13:00:00,TaskB,START,456\n"
            "13:12:00,TaskB,END,456\n"
            "14:00:00,TaskC,START,789\n"
        )
        self.temp_file.close()
        self.filepath = self.temp_file.name

    def tearDown(self):
        os.unlink(self.filepath)

    def test_parse_log_file(self):
        tasks = parse_log_file(self.filepath)
        self.assertIn('123', tasks)
        self.assertEqual(tasks['123']['description'], 'TaskA')
        self.assertIsInstance(tasks['123']['start'], datetime)
        self.assertIsInstance(tasks['123']['end'], datetime)
        self.assertIn('789', tasks)
        self.assertIsNone(tasks['789']['end'])

    def test_evaluate_durations(self):
        tasks = parse_log_file(self.filepath)
        output, incomplete = evaluate_durations(tasks)
        self.assertTrue(any("WARNING" in msg or "ERROR" in msg for msg in output + incomplete))


if __name__ == '__main__':
    unittest.main()
