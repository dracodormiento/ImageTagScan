import os
import subprocess

# Directory to scan (will be passed as an environment variable)
#SCAN_DIR = os.getenv("SCAN_DIR", "/data")
SCAN_DIR = r"\\Furst_NAS\photo\Shared Family Photos\Pics\Do Not Display"

# File to save the results
OUTPUT_FILE = "exif_matches.txt"

# Keyword to match in file descriptions
DESCRIPTION_KEYWORD = "example_keyword"  # Replace with the keyword you're looking for

def extract_metadata_with_exiftool(file_path):
    try:
        # Normalize the path to handle both Windows and UNIX-based systems
        file_path = os.path.normpath(file_path)

        # Run ExifTool command and capture output
        result = subprocess.run(
            ["exiftool", "-j", file_path], 
            capture_output=True, text=True
        )
        if result.returncode == 0:
            # Parse the JSON output
            metadata = result.stdout
            return metadata
    except Exception as e:
        print(f"Error reading metadata from {file_path}: {e}")
    return None

def scan_directory(directory):
    matches = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                
                metadata = extract_metadata_with_exiftool(file_path)
                if metadata:
                    print(f"Metadata for {file_path}:\n{metadata}")
                    
                    # Search for file description
                    if DESCRIPTION_KEYWORD.lower() in metadata.lower():
                        print(f"Match found in file: {file_path}")
                        matches.append(file_path)
                else:
                    print(f"No metadata found in {file_path}")
    return matches

def main():
    matches = scan_directory(SCAN_DIR)
    with open(OUTPUT_FILE, "w") as f:
        for match in matches:
            f.write(match + "\n")
    print(f"Matching files saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
