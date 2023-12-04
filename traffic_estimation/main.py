import pandas as pd
import sys
import trafficOperations as to

sys.path.append("scraper/")
import dataOperations as do
import fileOperations as fo

def main():
    restaurants = {
        "Cotton Club" : 0,
        "August Restaurant" : 0,
        "Cafe Techno" : 0,
        "Restaurant W33" : 0,
        "Juvenes Mathilda" : 0,
        "Juvenes Alma" : 0,
        "Juvenes Alere" : 0,
        "Juvenes Serveri" : 0
    }

    date_from = "2024-02-10"
    date_to = "2024-02-20"

    class_file_path = 'calendars/all_classes.json'
    all_classes_df = do.get_all_classes(class_file_path)
    total_traffic_df = to.get_traffic_df(f"results/traffic/{date_from}_to_{date_to}.csv", all_classes_df)

    if total_traffic_df is not None:
        for date in total_traffic_df:
            traffic_at_date = [0, 0, 0, 0, 0, 0, 0, 0]
            traffic_at_date = to.get_traffic_at_date(all_classes_df, total_traffic_df, traffic_at_date, date, restaurants)
            print(traffic_at_date)
    else:
        print("Warning - Unable to get total traffic...")


if __name__ == '__main__':
    main()