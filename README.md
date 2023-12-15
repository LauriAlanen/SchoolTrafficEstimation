# School Traffic Estimation

## Overview
This repository contains two main programs for managing and analyzing school class schedules. The `scraper.py` script scrapes the current week's schedules from the VAMK Lukkarit website, while the `estimation.py` module estimates upcoming restaurant traffic based on class attendance. The `estimate.py` module is called from `endpoint/listener.py`, which uses the Django framework to set up a REST API.


Please note that the scraper must be run before fetching data, and currently, data is available only for the ongoing week.

## Dependencies Installation
1. Install the required dependencies by running the following command:
    ```bash
    apt install -e .
    ```

## Class Schedule Scraper (`scraper.py`)
1. Run the scraper script to gather the current week's class schedule.
    ```bash
    ./scraper.py
    ```
2. The scraper will save individual class calendars as CSV files in the "calendars" directory.
   
   ![image](https://github.com/LauriAlanen/SchoolTrafficEstimation/assets/80245457/4821f96f-9641-44ce-9a41-a8f547df4b15)


## Traffic Estimation (`estimation/estimate.py`)
1. After successfully scraping all classes, use the `estimate.py` program for estimating upcoming traffic.
2. The estimation is based on the number of people in each class, and each class is assigned a list with weights that affect how people are distributed to the restaurants.
3. The program is currently tailored for estimating restaurant occupancy but is modular enough for customization.

## REST API (`endpoint/listener.py`)
After starting the listener, you can easily fetch data using GET requests from the provided endpoints. For example:
- Retrieve all dates with "attending" classes: `http://localhost:5000/getDates`
- Get estimated traffic for a specific date and time: `http://localhost:5000/getTraffic?fdate=2023-12-13 13:15`

### Demo App Made Using React and the REST API `listener.py`
https://github.com/LauriAlanen/SchoolTrafficEstimation/assets/80245457/af37275d-85b0-4417-b35e-517963fde6dd

## High-Level Overview
![High Level Overview](https://github.com/LauriAlanen/SchoolTrafficEstimation/assets/80245457/51435b5e-3c70-4c90-8811-92012ad36290)

## Scraper Flowchart
![Scraper Flowchart](https://github.com/LauriAlanen/SchoolTrafficEstimation/assets/80245457/d51bb3e1-3163-4bfe-a33b-fdd3e932b158)

## Estimation Flowchart
![Estimation Flowchart](https://github.com/LauriAlanen/SchoolTrafficEstimation/assets/80245457/dfb80e63-fb2d-46e1-8ca6-bbfc41990d27)

## Customization
- The code is modular and can be easily adapted for estimating other metrics or behaviors beyond restaurant occupancy.
- Explore the code and adjust the weights and parameters in the `estimation.py` program according to your specific requirements.

## Issues 
There is no handling for failed scrapes. If you get the following output the program will finish but when using the estimation program it will result in a crash.

![image](https://github.com/LauriAlanen/SchoolTrafficEstimation/assets/80245457/6c403c2a-fcbd-475e-b804-d7bbadb643d8)
****
