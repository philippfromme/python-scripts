import os
from tinytag import TinyTag
import argparse

# This script finds MP3 files with all uppercase artist or title metadata. It checks if the artist or title metadata is entirely uppercase. For example, it will match files where the artist is "ARTIST" or the title is "TITLE".
#
# Example usage:
# `python find-uppercase-metadata-mp3s.py --folder="./music"`

def get_all_mp3_files(root_folder):
    mp3_files = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.mp3'):
                mp3_files.append(os.path.join(dirpath, filename))
    return mp3_files

def is_all_upper(text):
    # Only consider alphabetic characters; ignore empty strings
    letters = [ch for ch in text if ch.isalpha()]
    if not letters:
        return False
    return all(ch.isupper() for ch in letters)

def main():
    parser = argparse.ArgumentParser(description="Find MP3 files with all uppercase artist or title metadata.")
    parser.add_argument('--folder', required=True, help="Path to the folder containing mp3 files")
    args = parser.parse_args()

    mp3_files = get_all_mp3_files(args.folder)
    uppercase_artist_files = []
    uppercase_title_files = []

    for file_path in mp3_files:
        try:
            tag = TinyTag.get(file_path)
            artist = tag.artist or ''
            title = tag.title or ''
            if is_all_upper(artist):
                uppercase_artist_files.append((file_path, artist))
            if is_all_upper(title):
                uppercase_title_files.append((file_path, title))
        except Exception as e:
            print(f"Error reading metadata from {file_path}: {e}")

    if uppercase_artist_files:
        print("Files with ALL UPPERCASE ARTIST names:")
        for path, artist in uppercase_artist_files:
            print(f"{path}  [Artist: {artist}]")
    else:
        print("No files found with all uppercase ARTIST names.")

    if uppercase_title_files:
        print("\nFiles with ALL UPPERCASE TITLE names:")
        for path, title in uppercase_title_files:
            print(f"{path}  [Title: {title}]")
    else:
        print("No files found with all uppercase TITLE names.")

if __name__ == '__main__':
    main()
