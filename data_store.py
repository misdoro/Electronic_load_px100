from pandas import DataFrame
from datetime import datetime


class DataStore:
    def __init__(self):
        self.data = DataFrame(columns=['time', 'current', 'voltage'])

    def reset(self):
        self.data = self.data.drop()
        print(self.data)

    def append(self, row):
        print(row)
        self.data = self.data.append(row, ignore_index=True)

    def write(self, path):
        print(self.data)
        filename = path + "/" + datetime.now().isoformat() + ".csv"
        self.data.drop_duplicates().to_csv(filename)
