import os
import shutil


class OutputWriter:
    def __init__(self, output_folder: str):
        self.output_folder = output_folder

    def write_all(self, files: list[tuple[str, str]], clear_output: bool = False):
        self._check_no_duplicates(files)

        if clear_output:
            self._clear_output_folder()

        for path, content in files:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

    def _check_no_duplicates(self, files: list[tuple[str, str]]):
        paths = [path for path, _ in files]
        duplicates = {p for p in paths if paths.count(p) > 1}
        if duplicates:
            raise ValueError(f"Duplicate output file(s): {', '.join(duplicates)}")

    def _clear_output_folder(self):
        if os.path.exists(self.output_folder) and os.path.isdir(self.output_folder):
            shutil.rmtree(self.output_folder)
