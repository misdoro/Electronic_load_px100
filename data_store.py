from pandas import DataFrame
from datetime import datetime


class DataStore:
    def __init__(self):
        self.reset()

    def __bool__(self):
        return len(self.lastrow) > 0

    def reset(self):
        self.lastrow = {}
        self.data = DataFrame()

    def append(self, row):
        print(row)
        self.lastrow = row
        self.data = self.data.append(row, ignore_index=True)

    def write(self, path):
        print(self.data)
        filename = path + "/" + datetime.now().isoformat() + ".csv"
        self.data.drop_duplicates().to_csv(filename)

    def plot(self, **args):
        return self.data.plot(**args)

    def lastval(self, key):
        return self.lastrow[key]
