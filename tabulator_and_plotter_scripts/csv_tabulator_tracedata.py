import os
import glob
import re
import argparse
import csv

# function to tabulate the csv data into a latex table
def tabulate_csv_to_latex(csv_file):
    import csv
    rows = []
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)

    header = rows[0]
    data = rows[1:]
    col_count = len(header)
    col_format = "|".join(["c"] * col_count)

    latex_table = (
        "\\begin{table}[h!]\n"
        "\\centering\n"
        "\\rowcolors{2}{black!5}{black!10}\n"
        "\\setlength{\\arrayrulewidth}{0.3mm}\n"
        "\\setlength{\\tabcolsep}{5pt}\n"
        "\\renewcommand{\\arraystretch}{1.5}\n"
        "\\resizebox{\\textwidth}{!}{\n"
        f"\\begin{{tabular}}{{|{col_format}|}}\n\\hline\n"
        + " & ".join(header) + " \\\\ \\hline\n"
    )
    for row in data:
        latex_table += " & ".join(row) + " \\\\ \\hline\n"
    latex_table += (
        "\\end{tabular}}\n"
        "\\caption{Table CAPTION}\n"
        "\\label{tab:table}\n"
        "\\end{table}"
    )

    # Write the latex table to a .tex file
    with open("trace_data_table.tex", "w") as f:
        f.write(latex_table)

def output_csv_file():
    # 0. Write the column headers to the output csv file
    output_csv = 'trace_data.csv'
    with open(output_csv, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Application", "L1D_TOTAL_ACCESS", "L1D_TOTAL_HIT", "L1D_hit_ratio", "IPC"])

    # 1. For each trace file (every .txt file) in the current directory:
    for trace_file in glob.glob("*.txt"):
        app_name = os.path.splitext(os.path.basename(trace_file))[0]
        # remove the suffix ".champsimtrace.xz.*" from the app_name
        app_name = app_name.split(".champsimtrace.xz")[0]

        l1d_total_access = None
        l1d_total_hit = None
        ipc_value = None

        with open(trace_file, 'r') as f:
            for line in f:
                # 1.1.2 Extract the IPC
                if "CPU 0 cumulative IPC:" in line:
                    match_ipc = re.search(r"CPU 0 cumulative IPC:\s*([\d.]+)", line)
                    if match_ipc:
                        ipc_value = float(match_ipc.group(1))

                # 1.1.3 Extract L1D TOTAL ACCESS and L1D TOTAL HIT
                if "L1D TOTAL     ACCESS:" in line:
                    match_l1d = re.search(r"L1D TOTAL\s+ACCESS:\s+(\d+)\s+HIT:\s+(\d+)", line)
                    if match_l1d:
                        l1d_total_access = int(match_l1d.group(1))
                        l1d_total_hit = int(match_l1d.group(2))

        # 1.2 Calculate the L1D hit ratio
        l1d_hit_ratio = 0.0
        if l1d_total_access and l1d_total_access > 0:
            l1d_hit_ratio = l1d_total_hit / l1d_total_access

        # 1.3 Write the data to the output csv file
        with open(output_csv, mode='a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                app_name,
                l1d_total_access if l1d_total_access else 0,
                l1d_total_hit if l1d_total_hit else 0,
                f"{l1d_hit_ratio:.6f}",
                f"{ipc_value:.6f}" if ipc_value else 0
            ])

    # Reorder the csv file alphabetically based on the application name
    reorder_csv(output_csv)

def reorder_csv(csv_file):
    with open(csv_file, mode='r') as infile:
        reader = csv.DictReader(infile)
        data = sorted(reader, key=lambda row: row['Application'])

    with open(csv_file, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process trace files from specified folder')
    parser.add_argument('folder', help='Folder containing the trace files')
    args = parser.parse_args()
    folder = args.folder

    # set working directory to folder
    os.chdir(folder)

    output_csv_file()
    print("trace_data.csv created")
    tabulate_csv_to_latex("trace_data.csv")
    print("trace_data.csv tabulated to latex table")