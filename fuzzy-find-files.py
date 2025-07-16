import os
import argparse
import shutil
from rapidfuzz import fuzz
from tqdm import tqdm
from colorama import Fore, Style, init

# This script recursively fuzzy-matches files from a source folder to a target folder. It can optionally sort matched files into 'found' and 'not-found' folders.
#
# Example usage:
# `python fuzzy-find-files.py --source="./source" --target="./target" --not-found-only --sort`

def get_all_files(root_folder):
    file_paths = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            file_paths.append(os.path.join(dirpath, filename))
    return file_paths

def move_file_preserve_structure(src_file, src_root, dest_root):
    # Preserve subfolder structure
    rel_path = os.path.relpath(src_file, src_root)
    dest_path = os.path.join(dest_root, rel_path)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.move(src_file, dest_path)

def main():
    init(autoreset=True)
    parser = argparse.ArgumentParser(description="Recursively fuzzy-match files from source to target folder.")
    parser.add_argument('--source', required=True, help="Path to the source folder")
    parser.add_argument('--target', required=True, help="Path to the target folder")
    parser.add_argument('--not-found-only', action='store_true', help="Show only source files with no fuzzy matches")
    parser.add_argument('--sort', action='store_true', help="Move matched files to 'found' and unmatched to 'not-found' folders")
    args = parser.parse_args()

    source_folder = args.source
    target_folder = args.target

    source_files = get_all_files(source_folder)
    target_files = get_all_files(target_folder)
    target_file_names = [(os.path.basename(f), f) for f in target_files]

    found_folder = os.path.join(source_folder, 'found')
    not_found_folder = os.path.join(source_folder, 'not-found')

    for src_file in tqdm(source_files, desc="Processing source files"):
        src_name = os.path.basename(src_file)
        matches = []
        for tgt_name, tgt_path in target_file_names:
            similarity = fuzz.ratio(src_name, tgt_name)
            if similarity >= 99:
                matches.append((tgt_path, similarity))
        if matches:
            if not args.not_found_only:
                print(f"{Fore.GREEN}Matches for '{src_name}':{Style.RESET_ALL}")
                for match_path, sim in matches:
                    print(f"  - {match_path} {Fore.YELLOW}(Similarity: {sim:.0f}%)")
            if args.sort:
                move_file_preserve_structure(src_file, source_folder, found_folder)
        else:
            print(f"{Fore.RED}No match found for '{src_name}'.{Style.RESET_ALL}")
            if args.sort:
                move_file_preserve_structure(src_file, source_folder, not_found_folder)

if __name__ == "__main__":
    main()
