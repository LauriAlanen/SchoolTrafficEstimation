import pandas as pd
import pyarrow.feather as feather
import os

def save_df_to_file(df_to_save, path):
    folder_path = os.path.dirname(path)
    create_folder_path(folder_path)

    with open(path, "wb") as f:
        df_to_save.to_csv(f)
        print("Succesfully saved schedule!")


def read_df_from_file(path):
    with open(path, "rb") as f:
        print(f"Reading schedule {path}")

        df_to_read = pd.read_csv(f)
        #read_df = feather.read_feather(f)

        return df_to_read


def create_folder_path(folder_path):
    try:
        os.makedirs(folder_path)
        print(f"Created folder with path {folder_path}")

    except FileExistsError:
        print(f"Folder with path {folder_path} already exists")