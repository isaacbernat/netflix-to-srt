import os
import re
import unittest

from to_srt import to_srt


class TestToSrt(unittest.TestCase):
    SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "samples")

    def test_sample_files(self):
        input_extensions = {".xml", ".vtt"}
        for input_file in sorted(os.listdir(self.SAMPLES_DIR)):
            base, ext = os.path.splitext(input_file)
            if ext.lower() not in input_extensions:
                continue
            with self.subTest(file=input_file):
                expected_srt = os.path.join(self.SAMPLES_DIR, base + ".srt")
                input_path = os.path.join(self.SAMPLES_DIR, input_file)
                with open(input_path, "r", encoding="utf-8") as f:
                    input_content = f.read()
                with open(expected_srt, "r", encoding="utf-8") as f:
                    expected_content = f.read()
                generated_content = to_srt(input_content, ext, delay_ms=0)
                self.assertEqual(generated_content, expected_content)

    def test_delay_subdirectory(self):
        delay_dir = os.path.join(self.SAMPLES_DIR, "delay")
        delay_pattern = re.compile(r"^(.+?)_(plus|minus)_(\d+)$")

        for f in sorted(os.listdir(delay_dir)):
            base, ext = os.path.splitext(f)
            if ext.lower() != ".srt":
                continue
            match = delay_pattern.match(base)
            if not match:
                continue
            prefix, sign, delay_val = match.groups()
            delay_ms = int(delay_val) if sign == "plus" else -int(delay_val)
            input_ext = None
            for ext in [".vtt", ".xml", ".srt"]:
                if os.path.exists(os.path.join(delay_dir, prefix + ext)):
                    input_file = prefix + ext
                    input_ext = ext
                    break
            if input_ext is None:
                raise FileNotFoundError(
                    f"No input file found for prefix '{prefix}' "
                    f"(looked for .vtt, .xml, .srt)"
                )
            with self.subTest(input_file=input_file, delay=delay_val):
                expected_srt = os.path.join(delay_dir, f)
                input_path = os.path.join(delay_dir, input_file)
                with open(input_path, "r", encoding="utf-8") as f:
                    input_content = f.read()
                with open(expected_srt, "r", encoding="utf-8") as f:
                    expected_content = f.read()
                generated_content = to_srt(input_content, input_ext, delay_ms=delay_ms)
                self.assertEqual(generated_content, expected_content)


if __name__ == "__main__":
    unittest.main()
