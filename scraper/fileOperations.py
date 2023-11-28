import pandas as pd
import pyarrow.feather as feather
import json
from io import StringIO

def saveSchedule(schedule, path):
    df = pd.read_json(StringIO(schedule))
    df.drop(["start_date", "event_id", "code", "visible", "color", "subject", 
             "description", "reserved_for", "location", "realizations"],
            axis=1, inplace=True),
    
    with open(path, "wb") as f:
        df.to_csv(f)
        #feather.write_feather(df, f)

def readSchedule(path):
    with open(path, "rb") as f:
        read_df = pd.read_csv(f)
        #read_df = feather.read_feather(f)
        return read_df

def getAllClasses(class_file_path):
    with open(class_file_path, "rb") as f:
        classes_json = json.load(f)
        return classes_json