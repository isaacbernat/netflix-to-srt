import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


class TestToSrt(unittest.TestCase):
    SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "samples")
    TO_SRT_SCRIPT = os.path.join(os.path.dirname(__file__), "..", "to_srt.py")

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def _run_to_srt(self, input_dir, output_dir, delay=None):
        cmd = [sys.executable, self.TO_SRT_SCRIPT, "-i", input_dir, "-o", output_dir]
        if delay is not None:
            cmd.extend(["-d", str(delay)])
        return subprocess.run(cmd, capture_output=True, text=True)

    def test_sample_files(self):
        input_extensions = {".xml", ".vtt"}
        for input_file in os.listdir(self.SAMPLES_DIR):
            base, ext = os.path.splitext(input_file)
            if ext.lower() not in input_extensions:
                continue
            with self.subTest(file=input_file):
                expected_srt = os.path.join(self.SAMPLES_DIR, base + ".srt")
                self._run_to_srt(self.SAMPLES_DIR, self.test_dir)
                generated_srt = os.path.join(self.test_dir, base + ".srt")
                with open(expected_srt, "r", encoding="utf-8") as f:
                    expected_content = f.read()
                with open(generated_srt, "r", encoding="utf-8") as f:
                    generated_content = f.read()
                self.assertEqual(generated_content, expected_content)

    def test_delay_subdirectory(self):
        delay_dir = os.path.join(self.SAMPLES_DIR, "delay")
        delay_pattern = re.compile(r"^(.+?)_(plus|minus)_(\d+)$")

        for f in os.listdir(delay_dir):
            base, ext = os.path.splitext(f)
            if ext.lower() != ".srt":
                continue
            match = delay_pattern.match(base)
            if not match:
                continue
            prefix, sign, delay_val = match.groups()
            delay_ms = int(delay_val) if sign == "plus" else -int(delay_val)
            input_file = prefix + ".vtt"
            if not os.path.exists(os.path.join(delay_dir, input_file)):
                input_file = prefix + ".xml"
            with self.subTest(input_file=input_file, delay=delay_val):
                expected_srt = os.path.join(delay_dir, f)
                self._run_to_srt(delay_dir, self.test_dir, delay=delay_ms)
                generated_srt = os.path.join(self.test_dir, prefix + ".srt")
                with open(expected_srt, "r", encoding="utf-8") as f:
                    expected_content = f.read()
                with open(generated_srt, "r", encoding="utf-8") as f:
                    generated_content = f.read()
                self.assertEqual(generated_content, expected_content)


if __name__ == "__main__":
    unittest.main()
