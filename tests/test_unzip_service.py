import os
import unittest
import tempfile
import zipfile
from pathlib import Path
from src.services.recursive_unzip_service import recursive_unzip

class TestRecursiveUnzipService(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.temp_dir.name)
        
        # Create destination directory for extraction
        self.destination = self.base_dir / "extracted"
        self.destination.mkdir(parents=True, exist_ok=True)
        
        # Create a sample text file
        self.sample_file = self.base_dir / "sample.txt"
        self.sample_file.write_text("Hello, World!")
        
        # Create a child (nested) zip file containing a file
        self.child_zip = self.base_dir / "child.zip"
        with zipfile.ZipFile(self.child_zip, "w") as cz:
            cz.writestr("child_file.txt", "This is a nested file.")
        
        # Create an outer zip file that includes the sample text file and the child zip
        self.outer_zip = self.base_dir / "outer.zip"
        with zipfile.ZipFile(self.outer_zip, "w") as oz:
            oz.write(self.sample_file, arcname="sample.txt")
            oz.write(self.child_zip, arcname="child.zip")
    
    def tearDown(self):
        # Cleanup temporary directory
        self.temp_dir.cleanup()
    
    def test_recursive_unzip(self):
        # Run the recursive unzip function on the outer zip file
        result = recursive_unzip([str(self.outer_zip)], self.destination)
        
        # Verify that sample.txt was extracted
        extracted_sample = self.destination / "sample.txt"
        self.assertTrue(extracted_sample.exists(), "sample.txt should be extracted.")
        
        # Verify that child_file.txt from the nested zip was extracted
        extracted_child_file = self.destination / "child_file.txt"
        self.assertTrue(extracted_child_file.exists(), "child_file.txt should be extracted from the nested zip.")
        
        # Verify that the result list contains the paths to the extracted files
        extracted_paths = [Path(p) for p in result]
        self.assertIn(extracted_sample, extracted_paths)
        self.assertIn(extracted_child_file, extracted_paths)

if __name__ == "__main__":
    unittest.main()
