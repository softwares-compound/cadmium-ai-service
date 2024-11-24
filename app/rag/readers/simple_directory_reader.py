import os
from typing import List
from llama_index.core  import Document


class SimpleDirectoryReader:
    def __init__(self, code_base_directory: str, file_extensions: List[str]):
        """
        Initialize the SimpleDirectoryReader with a directory and file extensions.

        :param code_base_directory: Path to the directory to read files from.
        :param file_extensions: List of file extensions to include (e.g., ['.py', '.txt']).
        """
        self.code_base_directory = code_base_directory
        self.file_extensions = file_extensions

    def load_data(self) -> List[Document]:
        """
        Load files with specified extensions from the directory and return as documents.

        :return: List of Document objects created from the files.
        """
        documents = []
        for root, _, files in os.walk(self.code_base_directory):
            for file in files:
                if any(file.endswith(ext) for ext in self.file_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        documents.append(
                            Document(
                                text=content,
                                extra_info={"file_path": file_path}
                            )
                        )
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")
        return documents
