import os
import shutil

class FileMover:
    def __init__(self, source_path, tags, target_path):
        self.source_path = source_path
        self.tags = tags
        self.target_path = target_path

    def _ensure_target_directory(self):
        if not os.path.exists(self.target_path):
            os.makedirs(self.target_path)

    def _file_matches_tags(self, file_name):
        return any(tag in file_name for tag in self.tags)

    def move_files_by_tags(self):
        self._ensure_target_directory()

        for root, dirs, files in os.walk(self.source_path):
            for file in files:
                file_path = os.path.join(root, file)

                if self._file_matches_tags(file):
                    self._move_file(file_path)

    def _move_file(self, file_path):
        target_path = os.path.join(self.target_path, os.path.basename(file_path))
        shutil.move(file_path, target_path)
        print(f"Moved: {file_path} to {target_path}")
