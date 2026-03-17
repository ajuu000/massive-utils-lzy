import csv
import os

class OutputSaver:
    def __init__(self, output_file):
        self.output_file = output_file
        self.header = ['File Name', 'File Size (bytes)', 'File Type', 'Date Created', 'Date Modified', 'Metadata']

    def save_metadata(self, metadata_list):
        """Save metadata to a CSV file."""
        try:
            # Create directory if it doesn't exist
            output_dir = os.path.dirname(self.output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Write metadata to CSV
            with open(self.output_file, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.header)  # Write header
                
                # Write each metadata entry
                for metadata in metadata_list:
                    writer.writerow([
                        metadata.get('file_name', 'N/A'),
                        metadata.get('file_size', 'N/A'),
                        metadata.get('file_type', 'N/A'),
                        metadata.get('date_created', 'N/A'),
                        metadata.get('date_modified', 'N/A'),
                        metadata.get('metadata', 'N/A')
                    ])
            print(f"Metadata successfully saved to {self.output_file}")
        except Exception as e:
            print(f"Error saving metadata: {e}")

# TODO: Add functionality to append data instead of overwriting
# TODO: Handle specific exceptions for better debugging
# TODO: Consider adding logging instead of print statements for better tracking
# TODO: Implement a method to read existing metadata from the CSV if needed
# TODO: Add tests for various edge cases (e.g., empty metadata list, invalid output path)
