import os
import glob
import re
import csv
import argparse
import pandas as pd

def get_prefetcher_name():
    #get the name from the current last level folder name
    prefetcher_name = os.path.basename(os.getcwd())
    return prefetcher_name

def reorder_csv(csv_file):
    with open(csv_file, mode='r') as infile:
        reader = csv.DictReader(infile)
        data = sorted(reader, key=lambda row: row['Application'])

    with open(csv_file, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(data)


def read_trace(trace_file):
    prefetch_hits = prefetch_issued = l1d_load_miss = l1d_rfo_miss = ipc_value = 0
    
    try:
        with open(trace_file, 'r') as f:
            content = f.read()
            
            for line in content.split('\n'):
                if "L1D PREFETCH  REQUESTED" in line:
                    parts = line.split()
                    prefetch_issued = int(parts[parts.index("ISSUED:") + 1])
                    prefetch_hits = int(parts[parts.index("USEFUL:") + 1])
                elif "L1D LOAD" in line:
                    parts = line.split()
                    l1d_load_miss = int(parts[parts.index("MISS:") + 1])
                elif "L1D RFO" in line:
                    parts = line.split()
                    l1d_rfo_miss = int(parts[parts.index("MISS:") + 1])
                elif "CPU 0 cumulative IPC:" in line:
                    match_ipc = re.search(r"CPU 0 cumulative IPC:\s*([\d.]+)", line)
                    if match_ipc:
                        ipc_value = float(match_ipc.group(1))
                    
    except FileNotFoundError:
        print(f"Error: File {trace_file} not found")
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        
    return prefetch_hits, prefetch_issued, l1d_load_miss, l1d_rfo_miss, ipc_value

def output_csv_file():
    output_csv = 's8_trace_data.csv'
    headers = ['Prefetcher', 'Application', 'Prefetch_hits', 'Prefetch_issued', 
              'Accuracy', 'L1D_LOAD_MISS', 'L1D_RFO_MISS', 'Demand_misses', 'Coverage', 'IPC']
    
    with open(output_csv, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

    prefetcher_name = get_prefetcher_name()

    for trace_file in glob.glob("*.txt"):
        if trace_file == "prefetcher_name.txt":
            continue
            
        app_name = os.path.splitext(os.path.basename(trace_file))[0]
        app_name = app_name.split(".champsimtrace.xz")[0]

        prefetch_hits, prefetch_issued, l1d_load_miss, l1d_rfo_miss, ipc_value = read_trace(trace_file)

        demand_misses = l1d_load_miss + l1d_rfo_miss
        accuracy = prefetch_hits / prefetch_issued if prefetch_issued > 0 else 0
        coverage = prefetch_hits / (prefetch_hits + demand_misses) if (prefetch_hits + demand_misses) > 0 else 0

        with open(output_csv, mode='a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                prefetcher_name,
                app_name,
                prefetch_hits,
                prefetch_issued,
                f"{accuracy:.6f}",
                l1d_load_miss,
                l1d_rfo_miss,
                demand_misses,
                f"{coverage:.6f}",
                f"{ipc_value:.6f}"
            ])

    reorder_csv(output_csv)

def csv_tab_folder(folder):
    # set working directory to folder
    os.chdir(folder)

    output_csv_file()
    print("s8_trace_data.csv created")

    # return to original directory
    os.chdir("..")

def csv_tab_all_folders():
    for folder in glob.glob("*/"):
        csv_tab_folder(folder)
        print(f"Processed folder {folder}")

def merge_all_csv():
    # Initialize empty list to store DataFrames
    all_data = []
    
    # Find all s8_trace_data.csv files in subfolders
    for folder in glob.glob("*/"):
        csv_path = os.path.join(folder, "s8_trace_data.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            all_data.append(df)
    
    # Combine all DataFrames
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        # Sort by Prefetcher and Application
        final_df = final_df.sort_values(['Prefetcher', 'Application'])
        # Save to current directory
        final_df.to_csv('all_trace_data_s8.csv', index=False)
        print("Created all_trace_data_s8.csv")
################################

    # Obtain the data from the baseline prefetcher's IPC for each application:
    # (602.gcc_s-2226B, 623.xalancbmk_s-202B, 649.fotonik3d_s-1176B, 654.roms_s-1390B)

    # calculate the Normalized_IPC for each prefetcher 
    # and application by dividing the IPC of the prefetcher by the IPC
    #  of the baseline prefetcher for the same application

    # Add a column to the csv file with the Normalized_IPC values for each row
    # baseline: Normalized_IPC = 1.0
    # other prefetchers: Normalized_IPC = IPC_prefetcher / IPC_baseline
def calculate_normalized_ipc(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Get baseline IPC values for each application
    baseline_ipcs = df[df['Prefetcher'] == 'baseline'].set_index('Application')['IPC'].to_dict()
    
    # Calculate normalized IPC
    def normalize_ipc(row):
        if row['Prefetcher'] == 'baseline':
            return 1.0
        return row['IPC'] / baseline_ipcs[row['Application']]
    
    # Add Normalized_IPC column
    df['Normalized_IPC'] = df.apply(normalize_ipc, axis=1)
    
    # Save updated CSV
    df.to_csv(csv_file, index=False)
    print(f"Added Normalized_IPC column to {csv_file}")



# Main program
if __name__ == "__main__":
    csv_tab_all_folders()
    merge_all_csv()
    calculate_normalized_ipc('all_trace_data_s8.csv')