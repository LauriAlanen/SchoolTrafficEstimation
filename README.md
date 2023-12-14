# Class Traffic Estimation

## Overview
This repository includes two main programs for managing and analyzing school class schedules. The `scraper.py` script is responsible for scraping the current week's class schedule from the VAMK Lukkarit website. After successfully scraping the classes, the `estimation.py` program can be used to estimate upcoming traffic in restaurants based on the number of people in classes.

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

## Traffic Estimation (`estimation.py`)
1. After successfully scraping all classes, use the `estimation.py` program for estimating upcoming traffic.
2. The estimation is based on the number of people in each class, and each class is assigned a list with weights that affect how people are distributed to the restaurants.
3. The program is currently tailored for estimating restaurant occupancy but is modular enough for customization.

## High-Level Overview
![High Level Overview](https://github.com/LauriAlanen/SchoolTrafficEstimation/assets/80245457/51435b5e-3c70-4c90-8811-92012ad36290)

## Scraper Flowchart
![Scraper Flowchart](https://github.com/LauriAlanen/SchoolTrafficEstimation/assets/80245457/d51bb3e1-3163-4bfe-a33b-fdd3e932b158)

## Estimation Flowchart
![Estimation Flowchart](https://github.com/LauriAlanen/SchoolTrafficEstimation/assets/80245457/dfb80e63-fb2d-46e1-8ca6-bbfc41990d27)

## Customization
- The code is modular and can be easily adapted for estimating other metrics or behaviors beyond restaurant occupancy.
- Explore the code and adjust the weights and parameters in the `estimation.py` program according to your specific requirements.

## Issues and Contributions
If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository. Contributions are welcome!
