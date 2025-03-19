import os
import tempfile
import zipfile
import unittest
from pathlib import Path
from src.services.extraction_service import process_extraction

class TestExtractionService(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for the test
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        
        # Create the folder structure expected by the extraction service
        # The service extracts to "data/extracted"
        self.extraction_dir = Path("data/extracted")
        self.extraction_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a sample text file
        sample_file = Path(self.temp_dir.name) / "test.txt"
        sample_file.write_text("Hello World")
        
        # Create a nested zip file that will be inside the outer zip
        self.nested_zip = Path(self.temp_dir.name) / "nested.zip"
        with zipfile.ZipFile(self.nested_zip, 'w') as nz:
            nz.writestr("nested.txt", "Nested Content")
        
        # Create the outer zip file containing the text file and the nested zip
        self.outer_zip = Path(self.temp_dir.name) / "sample.zip"
        with zipfile.ZipFile(self.outer_zip, 'w') as zf:
            zf.write(sample_file, arcname="test.txt")
            zf.write(self.nested_zip, arcname="nested.zip")
    
    def tearDown(self):
        # Restore the original working directory and cleanup the temp directory
        os.chdir(self.original_cwd)
        self.temp_dir.cleanup()
    
    def test_process_extraction(self):
        # Create a dummy extraction request that includes our outer zip file
        extract_request = {
            "filter_out": [],
            "file": [str(self.outer_zip)],
            "division": {"file": True, "method": True, "class": True, "line": True},
            "filters": {
                "file_extension": {"include": [".py"], "exclude": []},
                "filename": {"include": ["csv"], "exclude": []},
                "method_name": {"include": ["csv"], "exclude": []},
                "class_name": {"include": [], "exclude": []}
            }
        }
        
        # Call process_extraction; it will unzip into "data/extracted" in our temp directory
        result = process_extraction(extract_request)
        
        # Verify that the returned result contains an "extracted_files" key
        self.assertIn("extracted_files", result)
        
        # Check that the main file "test.txt" has been extracted
        extracted_test_txt = self.extraction_dir / "test.txt"
        self.assertTrue(extracted_test_txt.exists(), "test.txt should be extracted")
        
        # Check that the nested zip was extracted (nested.txt should exist)
        extracted_nested_txt = self.extraction_dir / "nested.txt"
        self.assertTrue(extracted_nested_txt.exists(), "nested.txt should be extracted from nested zip")
        
        # Optionally, check that the output list in result contains the expected file paths
        extracted_files = result["extracted_files"]
        self.assertIn(str(extracted_test_txt), extracted_files)
        self.assertIn(str(extracted_nested_txt), extracted_files)

if __name__ == "__main__":
    unittest.main()
