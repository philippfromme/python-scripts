import os
import re
import argparse
import shutil
from tqdm import tqdm
from colorama import Fore, Style, init

# This script sorts MP3 files into Artist/Album folders based on their filenames. It expects filenames in the format: "Artist - Album - 01 Title.mp3".
#
# Example usage:
# `python sort-mp3s.py --folder="./music"`

def get_all_mp3_files(root_folder):
    mp3_files = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.mp3'):
                mp3_files.append(os.path.join(dirpath, filename))
    return mp3_files

def parse_filename(filename):
    # Expects: <Artist> - <Album> - <Track Number> <Title>.mp3
    match = re.match(r'^(.*?) - (.*?) - \d{2,} .*\.mp3$', filename)
    if match:
        artist = match.group(1).strip()
        album = match.group(2).strip()
        return artist, album
    return None, None

def main():
    init(autoreset=True)
    parser = argparse.ArgumentParser(description="Sort mp3 files into Artist/Album folders based on filename.")
    parser.add_argument('--folder', required=True, help="Path to the folder containing mp3 files")
    args = parser.parse_args()

    root_folder = args.folder
    mp3_files = get_all_mp3_files(root_folder)

    for file_path in tqdm(mp3_files, desc="Sorting MP3 files"):
        filename = os.path.basename(file_path)
        artist, album = parse_filename(filename)
        if artist and album:
            dest_dir = os.path.join(root_folder, artist, album)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, filename)
            if os.path.abspath(file_path) != os.path.abspath(dest_path):
                shutil.move(file_path, dest_path)
                print(f"{Fore.GREEN}Moved:{Style.RESET_ALL} {filename} -> {dest_dir}")
            else:
                print(f"{Fore.YELLOW}Already in place:{Style.RESET_ALL} {filename}")
        else:
            print(f"{Fore.RED}Skipped (unmatched pattern):{Style.RESET_ALL} {filename}")

if __name__ == '__main__':
    main()
