import pandas as pd


class DataPreprocessing:

    def __init__(self, file_name):
        self.file_name = file_name
        self.data1 = self.read_data()
        if self.data1.isnull().values.any():
            self.data1.dropna()

    def read_data(self):
        df = pd.read_csv(self.file_name, index_col='Date', parse_dates=True)
        self.data1 = df[['Items', 'Maximum', 'Minimum', 'Average', 'Unit', 'Type']]
        if self.data1.isnull().values.any():
            self.data1.dropna()
        return self.data1
