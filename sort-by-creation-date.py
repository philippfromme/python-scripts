import os
import datetime
import shutil
from tqdm import tqdm
from colorama import Fore, Style, init

# This script sorts audio files (MP3/WAV) into year-named folders based on their creation date.
# It creates a folder for each year and moves files into the corresponding folder.
#
# Example usage:
# `python sort-by-creation-date.py`

def get_creation_date(file_path):
    """Cross-platform file creation date as datetime"""
    if os.name == 'nt':  # Windows
        creation_time = os.path.getctime(file_path)
    else:
        stat = os.stat(file_path)
        try:
            creation_time = stat.st_birthtime  # macOS
        except AttributeError:
            creation_time = stat.st_ctime  # Linux fallback
    return datetime.datetime.fromtimestamp(creation_time)

def get_all_audio_files(root_folder):
    audio_files = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith(('.mp3', '.wav')):
                full_path = os.path.join(dirpath, filename)
                # Skip files already inside a year-named folder
                rel = os.path.relpath(full_path, root_folder)
                if not rel.split(os.sep)[0].isdigit():
                    audio_files.append(full_path)
    return audio_files

def move_file_to_year_folder(file_path, root_folder):
    creation_date = get_creation_date(file_path)
    year_folder = os.path.join(root_folder, str(creation_date.year))
    os.makedirs(year_folder, exist_ok=True)

    filename = os.path.basename(file_path)
    destination = os.path.join(year_folder, filename)

    counter = 1
    base, ext = os.path.splitext(filename)
    while os.path.exists(destination):
        destination = os.path.join(year_folder, f"{base}_{counter}{ext}")
        counter += 1

    shutil.move(file_path, destination)
    return destination, creation_date

def main():
    init(autoreset=True)
    root_folder = input("Enter the path to the folder containing your audio files: ").strip()

    if not os.path.isdir(root_folder):
        print(f"{Fore.RED}Error: '{root_folder}' is not a valid directory.{Style.RESET_ALL}")
        return

    audio_files = get_all_audio_files(root_folder)
    if not audio_files:
        print(f"{Fore.YELLOW}No MP3 or WAV files found in '{root_folder}'.{Style.RESET_ALL}")
        return

    print(f"Moving {len(audio_files)} file(s) (MP3/WAV) into year folders under '{root_folder}':\n")
    for file_path in tqdm(audio_files, desc="Moving files"):
        try:
            new_path, creation_date = move_file_to_year_folder(file_path, root_folder)
            print(f"{Fore.GREEN}Moved:{Style.RESET_ALL}\n  From: {file_path}\n  To:   {new_path}\n  Year: {creation_date.year}")
        except Exception as e:
            print(f"{Fore.RED}Error moving '{file_path}': {e}{Style.RESET_ALL}")

if __name__ == '__main__':
    main()
