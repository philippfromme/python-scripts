import os
import argparse

# This script finds files or folders with underscores in their names. For example, it will match files like "track_title.mp3" or folders like "album_title".
#
# Example usage:
# `python find-files-with-underscores.py --folder="./music"`

def find_underscored_names(root_folder):
    underscored_paths = []
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Check directories
        for dirname in dirnames:
            if '_' in dirname:
                underscored_paths.append(os.path.join(dirpath, dirname))
        # Check files
        for filename in filenames:
            if '_' in filename:
                underscored_paths.append(os.path.join(dirpath, filename))
    return underscored_paths

def main():
    parser = argparse.ArgumentParser(description="Find files or folders with underscores in their names.")
    parser.add_argument('--folder', required=True, help="Path to the root folder to scan")
    args = parser.parse_args()

    results = find_underscored_names(args.folder)
    if results:
        print("Files or folders with underscores in their names:")
        for path in results:
            print(path)
    else:
        print("No files or folders with underscores found.")

if __name__ == '__main__':
    main()
