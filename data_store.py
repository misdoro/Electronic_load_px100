from datetime import datetime
from os import path

from pandas import DataFrame
import pandas as pd


class DataStore:
    def __init__(self):
        self.reset()

    def __bool__(self):
        return len(self.lastrow) > 0

    def reset(self):
        self.lastrow = {}
        self.data = DataFrame()

    def append(self, row):
        # Only log on state changes or significant events to reduce terminal spam
        current_time = datetime.now()
        should_log = False
        
        # Log on state changes (on/off)
        if self.lastrow and self.lastrow.get('is_on') != row['is_on']:
            should_log = True
            state = "ON" if row['is_on'] else "OFF"
            print(f"{current_time.isoformat(sep=' ', timespec='seconds')} Device turned {state}")
        
        # Log every 60 seconds during operation (instead of 10)
        elif row.get('is_on') and (not hasattr(self, 'last_log_time') or 
                                   (current_time - self.last_log_time).total_seconds() > 60):
            should_log = True
            print(f"{current_time.isoformat(sep=' ', timespec='seconds')} Running: {row['time']} - V={row['voltage']:.3f} I={row['current']:.3f} Ah={row['cap_ah']:.2f}")
        
        if should_log:
            self.last_log_time = current_time

        self.lastrow = row

        # Create DataFrame with explicit columns to avoid FutureWarning
        if self.data.empty:
            # If data is empty, create DataFrame directly from row
            self.data = DataFrame([row])
        else:
            # Otherwise use concat with matching columns
            new_row_df = DataFrame([row], columns=self.data.columns)
            self.data = pd.concat([self.data, new_row_df], ignore_index=True)

    def write(self, basedir, prefix):
        filename = "{}_raw_{}.csv".format(prefix, datetime.now().strftime("%Y%m%d_%H%M%S"))
        full_path = path.join(basedir, filename)
        export_rows = self.data.drop_duplicates()
        if export_rows.shape[0]:
            print(f"Saved raw data: {path.basename(full_path)}")
            self.data.drop_duplicates().to_csv(full_path)
            return full_path
        else:
            print("No data to save")
            return None

    def plot(self, **args):
        return self.data.plot(**args)

    def lastval(self, key):
        return self.lastrow[key]
