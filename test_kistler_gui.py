import unittest
import os
import pandas as pd
from datetime import datetime
from kistler_gui_project import get_csv, get_Data, Draw

class TestKistlerGUI(unittest.TestCase):

    def setUp(self):
        # Setup mock data and environment for testing
        self.batchFolder = "mock_batch_folder"
        self.final_result = 1
        self.random_selection = 2
        self.file_selection = 5
        self.start_time = '2022-05-29_10'
        self.end_time = '2022-05-29_12'
        
        # Create mock CSV files in batchFolder
        os.makedirs(self.batchFolder, exist_ok=True)
        for i in range(3):
            with open(os.path.join(self.batchFolder, f'mock_file_{i}_OK.csv'), 'w') as f:
                f.write('Mock data')

    def tearDown(self):
        # Clean up any files created during testing
        for file in os.listdir(self.batchFolder):
            os.remove(os.path.join(self.batchFolder, file))
        os.rmdir(self.batchFolder)

    def test_get_csv(self):
        # Test if CSV files are selected correctly based on filters
        csv_files = get_csv(self.batchFolder, self.final_result, self.random_selection, self.file_selection, self.start_time, self.end_time)
        self.assertEqual(len(csv_files), 3)
        self.assertTrue(all(file.endswith("_OK.csv") for file in csv_files))

    def test_get_Data(self):
        # Simulate a CSV data extraction and check if the data format is correct
        file = os.path.join(self.batchFolder, 'mock_file_0_OK.csv')
        batch_no = "111200071336"
        result = get_Data(file, batch_no)

        # Check the expected structure of the result
        self.assertEqual(len(result), 12)
        self.assertEqual(result[0], batch_no)
        self.assertEqual(result[1], 'Mock data')

    def test_Draw(self):
        # Test the Draw function to check if it processes data correctly (no graphical validation)
        df = pd.DataFrame({
            'Final_Result': ['OK', 'NOK'],
            'Timestamp': [datetime.now(), datetime.now()],
            'Year': [2022, 2022],
            'Month': [5, 5],
            'Date': [29, 29],
            'Sensor': ['EO-01', 'EO-02'],
            'SensorValue': [1.0, 2.0]
        })
        targetFolder = "mock_target_folder"
        os.makedirs(targetFolder, exist_ok=True)
        Draw(df, "10min", targetFolder)
        
        # Check if images were generated
        images = [f for f in os.listdir(targetFolder) if f.endswith('.jpg')]
        self.assertGreater(len(images), 0)

        # Clean up generated files
        for img in images:
            os.remove(os.path.join(targetFolder, img))
        os.rmdir(targetFolder)

if __name__ == '__main__':
    unittest.main()
