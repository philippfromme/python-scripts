import os
import re
import argparse

# This script finds files that might be duplicates based on their names. It looks for files that have names ending with (number) before the file extension. For example, it will match files like "Title (1).mp3".
#
# Example usage:
# `python find-duplicate-files.py --folder="./music"`

def find_potential_duplicates(root_folder):
    # Pattern matches filenames ending with (number) before the extension
    pattern = re.compile(r'^(.*) \((\d+)\)(\.[^.]*)$')
    duplicates = []

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if pattern.match(filename):
                duplicates.append(os.path.join(dirpath, filename))
    return duplicates

def main():
    parser = argparse.ArgumentParser(description="Find files that might be duplicates based on name endings like (1), (2), etc.")
    parser.add_argument('--folder', required=True, help="Path to the folder to scan")
    args = parser.parse_args()

    duplicates = find_potential_duplicates(args.folder)
    if duplicates:
        print("Potential duplicate files found:")
        for path in duplicates:
            print(path)
    else:
        print("No potential duplicate files found.")

if __name__ == '__main__':
    main()
