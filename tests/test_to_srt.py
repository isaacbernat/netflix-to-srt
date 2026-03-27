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

    def _get_input_files(self, directory):
        input_extensions = {".xml", ".vtt"}
        return [
            f for f in os.listdir(directory)
            if os.path.splitext(f)[1].lower() in input_extensions
        ]

    def _get_expected_srt_path(self, input_file, samples_dir):
        base_name = os.path.splitext(input_file)[0]
        return os.path.join(samples_dir, base_name + ".srt")

    def _run_to_srt(self, input_dir, output_dir, delay=None):
        cmd = [sys.executable, self.TO_SRT_SCRIPT, "-i", input_dir, "-o", output_dir]
        if delay is not None:
            cmd.extend(["-d", str(delay)])
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result

    def _get_generated_srt_path(self, input_file, output_dir):
        base_name = os.path.splitext(input_file)[0]
        return os.path.join(output_dir, base_name + ".srt")

    def test_sample_files(self):
        for input_file in self._get_input_files(self.SAMPLES_DIR):
            with self.subTest(file=input_file):
                expected_srt = self._get_expected_srt_path(input_file, self.SAMPLES_DIR)
                self.assertTrue(
                    os.path.exists(expected_srt),
                    f"Expected fixture not found: {expected_srt}"
                )

                self._run_to_srt(self.SAMPLES_DIR, self.test_dir)
                generated_srt = self._get_generated_srt_path(input_file, self.test_dir)

                self.assertTrue(
                    os.path.exists(generated_srt),
                    f"Generated file not found: {generated_srt}"
                )

                with open(expected_srt, "r", encoding="utf-8") as f:
                    expected_content = f.read()
                with open(generated_srt, "r", encoding="utf-8") as f:
                    generated_content = f.read()

                self.assertEqual(
                    generated_content,
                    expected_content,
                    f"Content mismatch for {input_file}"
                )

    def _get_delay_test_cases(self, delay_dir):
        test_cases = []
        delay_pattern = re.compile(r"^(.+?)_(plus|minus)_(\d+)$")

        for f in os.listdir(delay_dir):
            base, ext = os.path.splitext(f)
            if ext.lower() == ".srt":
                match = delay_pattern.match(base)
                if match:
                    prefix, sign, delay_val = match.groups()
                    delay_ms = int(delay_val) if sign == "plus" else -int(delay_val)
                    input_file = prefix + ".vtt"
                    input_file_xml = prefix + ".xml"
                    input_found = None
                    input_base = None
                    if os.path.exists(os.path.join(delay_dir, input_file)):
                        input_found = input_file
                        input_base = prefix
                    elif os.path.exists(os.path.join(delay_dir, input_file_xml)):
                        input_found = input_file_xml
                        input_base = prefix

                    if input_found:
                        test_cases.append({
                            "input_file": input_found,
                            "delay": delay_ms,
                            "expected_fixture": f,
                            "input_base": input_base,
                        })
        return test_cases

    def test_delay_subdirectory(self):
        delay_dir = os.path.join(self.SAMPLES_DIR, "delay")
        if not os.path.exists(delay_dir):
            self.skipTest("Delay subdirectory not found")

        test_cases = self._get_delay_test_cases(delay_dir)
        self.assertTrue(len(test_cases) > 0, "No delay test cases found")

        for case in test_cases:
            with self.subTest(input_file=case["input_file"], delay=case["delay"]):
                expected_srt = os.path.join(delay_dir, case["expected_fixture"])
                self.assertTrue(
                    os.path.exists(expected_srt),
                    f"Expected fixture not found: {expected_srt}"
                )

                self._run_to_srt(delay_dir, self.test_dir, delay=case["delay"])
                generated_srt = os.path.join(self.test_dir, case["input_base"] + ".srt")

                self.assertTrue(
                    os.path.exists(generated_srt),
                    f"Generated file not found: {generated_srt}"
                )

                with open(expected_srt, "r", encoding="utf-8") as f:
                    expected_content = f.read()
                with open(generated_srt, "r", encoding="utf-8") as f:
                    generated_content = f.read()

                self.assertEqual(
                    generated_content,
                    expected_content,
                    f"Content mismatch for {case['input_file']} with delay {case['delay']}"
                )


if __name__ == "__main__":
    unittest.main()
