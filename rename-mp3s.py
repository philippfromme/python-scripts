import os
import argparse
from tinytag import TinyTag
from tqdm import tqdm
from colorama import Fore, Style, init

# This script renames MP3 files based on their metadata with different format options:
# - Format 1 (full): "Artist - Album - 01 Title.mp3"
# - Format 2 (simple): "01 Title.mp3"
#
# Example usage:
# `python rename-mp3s.py --folder="./music" --format=full --dry-run`
# `python rename-mp3s.py --folder="./music" --format=simple --dry-run`

def get_all_mp3_files(root_folder):
    mp3_files = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.mp3'):
                mp3_files.append(os.path.join(dirpath, filename))
    return mp3_files

def sanitize_filename_component(component):
    # Remove or replace characters that are invalid in filenames
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for ch in invalid_chars:
        component = component.replace(ch, '')
    return component.strip()

def generate_filename(tag, format_type):
    """Generate filename based on metadata and format type"""
    artist = sanitize_filename_component(tag.artist or 'Unknown Artist')
    album = sanitize_filename_component(tag.album or 'Unknown Album')
    track = tag.track or 0
    title = sanitize_filename_component(tag.title or 'Unknown Title')
    track_str = f"{int(track):02}" if track else "00"
    
    if format_type == 'full':
        # Format: "Artist - Album - 01 Title.mp3"
        return f"{artist} - {album} - {track_str} {title}.mp3"
    elif format_type == 'simple':
        # Format: "01 Title.mp3"
        return f"{track_str} {title}.mp3"
    else:
        raise ValueError(f"Unknown format type: {format_type}")

def main():
    init(autoreset=True)  # Initialize colorama
    parser = argparse.ArgumentParser(description="Rename mp3 files based on metadata.")
    parser.add_argument('--folder', required=True, help="Path to the folder containing mp3 files")
    parser.add_argument('--format', choices=['full', 'simple'], default='full', 
                       help="Naming format: 'full' for 'Artist - Album - 01 Title.mp3', 'simple' for '01 Title.mp3'")
    parser.add_argument('--dry-run', action='store_true', help="Show what would be renamed without making changes")
    args = parser.parse_args()

    mp3_files = get_all_mp3_files(args.folder)

    for file_path in tqdm(mp3_files, desc="Processing MP3 files"):
        try:
            tag = TinyTag.get(file_path)
            new_name = generate_filename(tag, args.format)
            new_path = os.path.join(os.path.dirname(file_path), new_name)

            if file_path != new_path:
                if args.dry_run:
                    print(f"{Fore.CYAN}[DRY RUN]{Style.RESET_ALL} Would rename:\n  From: {file_path}\n  To:   {new_path}")
                else:
                    os.rename(file_path, new_path)
                    print(f"{Fore.GREEN}Renamed:{Style.RESET_ALL}\n  From: {file_path}\n  To:   {new_path}")
            # else:
                # print(f"{Fore.YELLOW}No rename needed for: {file_path}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error processing {file_path}: {e}{Style.RESET_ALL}")

if __name__ == '__main__':
    main()
