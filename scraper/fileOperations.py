import pandas as pd
import pyarrow.feather as feather
import os

def save_calendar(schedule, path):
    folder_path = os.path.dirname(path)

    try:
        os.makedirs(folder_path)
        print(f"Created folder with path {folder_path}")
    
    except FileExistsError:
        print(f"Folder with path {folder_path} already exists")
    
    with open(path, "wb") as f:
        schedule.to_csv(f)
        print("Succesfully saved schedule!")


def read_calendar(path):
    with open(path, "rb") as f:
        print(f"Reading schedule {path}")

        read_df = pd.read_csv(f)
        #read_df = feather.read_feather(f)

        return read_df

