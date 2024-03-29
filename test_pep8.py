#!/usr/bin/python3
""" Tests every .py file for pycodestyle errors """

import os
import pycodestyle


def check_directory(directory):
    """
    Check every file in a directory for pycodestyle errors.

    Args:
        directory (str): The directory to check.

    Returns:
        list: A list of tuples containing filename and error messages.
    """
    files_with_errors = []
    style_checker = pycodestyle.StyleGuide()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                result = style_checker.check_files([file_path])
                if result.total_errors > 0:
                    files_with_errors.append((file_path, result.messages))

    return files_with_errors


if __name__ == "__main__":
    directory_to_check = "/path/to/your/directory"
    errors = check_directory(directory_to_check)

    if errors:
        print("Files with pycodestyle errors:")
        for file_path, messages in errors:
            print(f"File: {file_path}")
            for message in messages:
                print(f"  {message}")
    else:
        print("No pycodestyle errors found.")
