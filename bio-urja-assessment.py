'''
According to me this problem provided all contraints is feasible upto a certain degree of error
processing the data has given the closes output of 12000.48 with only 8% error.

Getting exactly 12000 with 0% error in ratio of zonal wind farms may or may not be possible
as the processing of 100 factorial permutations can take a long time
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from colorama import Fore, Style, init
init()
from prettytable import PrettyTable
GREEN = "\033[92m"  # Green
BLUE = "\033[94m"   # Blue
RED = "\033[91m"    # Red
YELLOW = "\033[93m" # Yellow
RESET = "\033[0m"  
csv_file_path = "input_data.csv"
data = pd.read_csv(csv_file_path)
dataStructure = []
'''
Generate A datastructure with:
1. Id as WindFarm-Name (eg: E1,E2 etc.)
2. Weight forecast/capacity. Fixed for a Farm
3. Capacity
4. Forecast
'''
for row in data.values:
    dataStructure.append({"id": row[0], "weight": row[1] / row[2], "forecast": row[1], "capacity": row[2]})

ids = [item['id'] for item in dataStructure]
capacities = [item['capacity'] for item in dataStructure]
cur_forecast_sums = []
'''
Creating a limit
'''
LIMIT = int(input("Enter the range in which you want to keep it valid. Eg: Enter 500 for +/- 500 from 12000 (recommended 150):  "))
'''
Error in percentage ratio limit 
'''
PERCENTAGE_DIFFERENCE_RATIO_LIMIT = int(input("Enter the range in which you want to keep percentage ratio of N,E,W,S. Eg: Enter 5 for 5per error margin (recommended 8per):  "))

'''
Swap the element
'''
def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

'''
Function that ask the user for continuation of the process
'''
def continue_or_not():
    while True:
        a = input("Press Enter to continue or type 'q' to quit: ").strip()
        if not a:
            return True  # User pressed Enter to continue
        elif a.lower() == 'q':
            return False  # User typed 'q' to quit

'''
Function that calculate the sum of each regions for calcualting the ratio of the regions
And calculates the desired target ratio and calculates the difference between them
'''
def calculate_region_statistics(data_objects):
    west_sum = 0
    east_sum = 0
    south_sum = 0
    north_sum = 0

    for obj in data_objects:
        first_char = obj["id"][0]

        if first_char == 'E':
            east_sum += obj["forecast"]
        elif first_char == 'N':
            north_sum += obj["forecast"]
        elif first_char == 'W':
            west_sum += obj["forecast"]
        elif first_char == 'S':
            south_sum += obj["forecast"]

    # Total sum of all regions 
    total = west_sum + east_sum + south_sum + north_sum

    west_region = (west_sum * 100) / total
    east_region = (east_sum * 100) / total
    south_region = (south_sum * 100) / total
    north_region = (north_sum * 100) / total


    # Desired target values
    targetWest = 2000
    targetEast = 2800
    targetSouth = 6500
    targetNorth = 1500
    totalOri = targetEast + targetNorth + targetSouth + targetWest

    # Calculated original ratio percentage
    Oriwest = (targetWest * 100) / totalOri
    Orieast = (targetEast * 100) / totalOri
    Orisouth = (targetSouth * 100) / totalOri
    Orinorth = (targetNorth * 100) / totalOri

    print(Oriwest)
    print(Orieast)
    print(Orisouth)
    print(Orinorth)


    # Difference in original ratio percentage and sample ratio percentage
    diffEast = Orieast - east_region
    diffWest = Oriwest - west_region
    diffSouth = Orisouth - south_region
    diffNorth = Orinorth - north_region
    curr_PER_DIFF = abs(diffWest) + abs(diffEast) + abs(diffSouth) + abs(diffNorth)
    print("Difference East",diffEast)
    print("Difference West",diffWest)
    print("Difference South",diffSouth)
    print("Difference North",diffNorth)
    print(f"{Fore.GREEN}West Region Sum: {west_sum}{Style.RESET_ALL} west Original Sum:{Oriwest}")
    print(f"{Fore.GREEN}WEST % contribution: {west_region}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}East Region Sum: {east_sum}{Style.RESET_ALL} east Original Sum:{Orieast}")
    print(f"{Fore.BLUE}EAST % contribution: {east_region}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}North Region Sum: {north_sum}{Style.RESET_ALL} north Original Sum:{Orinorth}")
    print(f"{Fore.YELLOW}NORTH % contribution: {north_region}{Style.RESET_ALL}")
    print(f"{Fore.RED}South Region Sum: {south_sum}{Style.RESET_ALL} south Original Sum:{Orisouth}")
    print(f"{Fore.RED}SOUTH % contribution: {south_region}{Style.RESET_ALL}")
    print(f"Total: {total}")

    #checking whether error is minimal
    if(curr_PER_DIFF >= PERCENTAGE_DIFFERENCE_RATIO_LIMIT*4):
       print(Fore.RED + Style.BRIGHT + "FAILED RATIO MISMATCH")
    else:
        print(Fore.GREEN + Style.BRIGHT + "SUCCESSFUL!!!!")
    print(Style.RESET_ALL)


'''
Function that generates the permuations of all the input data's
'''
def generate_permutations(arr, start=0):
    if start == len(arr) - 1:
        yield arr.copy() 
    else:
        for i in range(start, len(arr)):
            swap(arr, start, i)
            
            yield from generate_permutations(arr, start + 1)
            
            swap(arr, start, i)

'''
User has to tell that how much limit and error has to be given to satisfied the ouput condition
Validate function which shows the closest permutation and desired output
'''
def validate(ds,cs):
    if(cs >= 12000 - LIMIT and cs <= 12000 + LIMIT):
        table = PrettyTable()
        table.field_names = ds[0].keys()

        # Add ds to the table
        for row in ds:
            table.add_row(row.values())
        print(table)
        print(cs)
        calculate_region_statistics(ds)
        if(not continue_or_not()):
            return False
    return True
for perm in generate_permutations(capacities):
    cur_forecast_sum = 0
    for i in range(len(perm)):
        dataStructure[i]["capacity"] = perm[i]
        dataStructure[i]["forecast"] = dataStructure[i]["weight"]*perm[i] 
        cur_forecast_sum += dataStructure[i]["weight"]*perm[i]
    cur_forecast_sums.append(cur_forecast_sum)
    out = validate(dataStructure, cur_forecast_sum)
    if(not out):
        plt.plot(cur_forecast_sums)
        plt.show()
        df = pd.DataFrame(dataStructure)
        df.to_csv("output_data.csv", index=False)
        break