import pandas as pd
import pyarrow.feather as feather
import json
from io import StringIO

def saveSchedule(data_to_serialize, path):
    df = pd.read_json(StringIO(data_to_serialize))
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