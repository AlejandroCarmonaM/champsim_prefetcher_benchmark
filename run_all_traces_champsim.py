
# This script runs all traces in the specified directory using Champsim simulator.
# Command to run ./run_champsim.sh hashed_perceptron-no-next_line-no-no-lru-1core 10 50 [trace_folder]/[trace_file]
# trace_file values = {602.gcc_s-2226B.champsimtrace.xz, 623.xalancbmk_s-202B.champsimtrace.xz, 649.fotonik3d_s-1176B.champsimtrace.xz, 654.roms_s-1390B.champsimtrace.xz}
# How to run: python run_all_traces_champsim.py

import os
import subprocess

# Configuration
trace_files = [
    '602.gcc_s-2226B.champsimtrace.xz',
    '623.xalancbmk_s-202B.champsimtrace.xz',
    '649.fotonik3d_s-1176B.champsimtrace.xz',
    '654.roms_s-1390B.champsimtrace.xz'
]
command_template = './run_champsim.sh hashed_perceptron-no-CPLXstride_ConfCnt_PD3-no-no-lru-1core 10 50 {trace_path}'

# Run Champsim for each trace file
for trace_file in trace_files:
    trace_path = trace_file
    command = command_template.format(trace_path=trace_path)
    print(f'Running command: {command}')
    subprocess.run(command, shell=True, check=True)