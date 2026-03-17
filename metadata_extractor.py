import os
import mimetypes
import logging
from mutagen import File as MutagenFile
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MetadataExtractor:
    def __init__(self, file_paths):
        self.file_paths = file_paths

    def extract_metadata(self):
        metadata_list = []
        for file_path in self.file_paths:
            try:
                metadata = self._extract_from_file(file_path)
                if metadata:
                    metadata_list.append(metadata)
            except Exception as e:
                logging.warning(f"Failed to extract metadata from {file_path}: {e}")
        return metadata_list

    def _extract_from_file(self, file_path):
        # Get file type using mimetypes
        mime_type, _ = mimetypes.guess_type(file_path)
        logging.info(f"Processing file: {file_path} (Type: {mime_type})")

        # Check for supported file types
        if mime_type and mime_type.startswith('audio'):
            return self._extract_audio_metadata(file_path)
        elif mime_type and mime_type.startswith('video'):
            return self._extract_video_metadata(file_path)
        elif mime_type and mime_type.startswith('image'):
            return self._extract_image_metadata(file_path)
        else:
            logging.warning(f"Unsupported file type for {file_path}")
            return None

    def _extract_audio_metadata(self, file_path):
        try:
            audio = MutagenFile(file_path, easy=True)
            if audio is None:
                return None
            return { 
                'file': file_path,
                'type': 'audio',
                'metadata': dict(audio)
            }
        except Exception as e:
            logging.error(f"Error extracting audio metadata: {e}")
            return None

    def _extract_video_metadata(self, file_path):
        # Placeholder for video metadata extraction logic
        logging.info(f"Video metadata extraction not implemented yet for {file_path}")
        return None

    def _extract_image_metadata(self, file_path):
        # Placeholder for image metadata extraction logic
        logging.info(f"Image metadata extraction not implemented yet for {file_path}")
        return None

def main():
    # Example usage
    input_files = ['example.mp3', 'example.mp4', 'example.jpg']  # Replace with actual files
    extractor = MetadataExtractor(input_files)
    metadata = extractor.extract_metadata()
    logging.info(f"Extracted Metadata: {metadata}")

if __name__ == "__main__":
    main()
