import os
import sys
import logging
from mutagen import File as MutagenFile

def extract_metadata(file_path):
    """Extract metadata from audio/video files using mutagen, fallback to basic file info"""
    try:
        # Try to extract metadata using mutagen first
        mutagen_file = MutagenFile(file_path)
        if mutagen_file is not None:
            metadata = {
                'file_path': file_path,
                'file_size': os.path.getsize(file_path),
                'modified_time': os.path.getmtime(file_path)
            }
            # Add mutagen metadata if available
            if hasattr(mutagen_file, 'info') and mutagen_file.info:
                metadata['duration'] = getattr(mutagen_file.info, 'length', None)
                metadata['bitrate'] = getattr(mutagen_file.info, 'bitrate', None)
            # Add tags if available
            if mutagen_file.tags:
                metadata['tags'] = dict(mutagen_file.tags)
            return metadata
        else:
            # Fallback to basic file info
            stat = os.stat(file_path)
            return {
                'file_path': file_path,
                'file_size': stat.st_size,
                'modified_time': stat.st_mtime
            }
    except Exception:
        return None

def save_to_file(metadata_list, output_file):
    """Save metadata list to JSON file"""
    import json
    with open(output_file, 'w') as f:
        json.dump(metadata_list, f, indent=2)

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(input_directory, output_file):
    # Check if the input directory exists
    if not os.path.isdir(input_directory):
        logging.error(f"Input directory '{input_directory}' does not exist.")
        sys.exit(1)

    # Prepare a list to hold all metadata
    all_metadata = []

    # Walk through the directory to process files
    for root, dirs, files in os.walk(input_directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                logging.info(f"Processing file: {file_path}")
                metadata = extract_metadata(file_path)
                if metadata:
                    all_metadata.append(metadata)
                else:
                    logging.warning(f"No metadata found for file: {file_path}")
            except Exception as e:
                logging.error(f"Failed to process file {file_path}: {e}")

    # Save extracted metadata to the specified output file
    try:
        save_to_file(all_metadata, output_file)
        logging.info(f"Metadata saved to '{output_file}'")
    except Exception as e:
        logging.error(f"Failed to save metadata to file '{output_file}': {e}")

if __name__ == "__main__":
    # Expecting two command-line arguments: input directory and output file
    if len(sys.argv) != 3:
        logging.error("Usage: python main.py <input_directory> <output_file>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_file = sys.argv[2]

    main(input_dir, output_file)

# TODO: Consider adding command-line argument parsing for better usability
# TODO: Implement support for different file types and metadata extraction methods
# TODO: Add unit tests for the individual components (metadata_extractor, output_saver)
