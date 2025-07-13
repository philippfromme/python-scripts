import os
import re
import argparse

# This script finds MP3 files that do not match the naming pattern: "Artist - Album - 01 Title.mp3"
#
# Example usage:
# `python find-mp3s-not-matching.py --folder="./music"`

def get_all_mp3_files(root_folder):
    mp3_files = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.mp3'):
                mp3_files.append(os.path.join(dirpath, filename))
    return mp3_files

def main():
    parser = argparse.ArgumentParser(description="Find MP3 files not matching the naming pattern.")
    parser.add_argument('--folder', required=True, help="Path to the folder containing mp3 files")
    args = parser.parse_args()

    # Pattern: Artist - Album - 02 Title.mp3
    pattern = re.compile(r'^.+ - .+ - \d{2} .+\.mp3$', re.IGNORECASE)

    mp3_files = get_all_mp3_files(args.folder)
    non_matching = []

    for file_path in mp3_files:
        filename = os.path.basename(file_path)
        if not pattern.match(filename):
            non_matching.append(file_path)

    if non_matching:
        print("Files NOT matching the pattern:")
        for path in non_matching:
            print(path)
    else:
        print("All MP3 files match the pattern.")

if __name__ == '__main__':
    main()
