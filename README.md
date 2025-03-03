# ChampSim Benchmarking with Custom Prefetchers

This readme explains how to use ChampSim to benchmark the custom prefetchers located in the `custom_prefetchers/` directory, and how to tabulate and plot the resulting data using the scripts in `tabulator_and_plotter_scripts/`.

Results for the custom prefetchers' performance using the `hashed_perceptron` branch predictor, no L1I prefetcher, `CPLXstride_ConfCnt_PD3` as the L1D prefetcher, no L2C prefetcher, no LLC prefetcher, and `lru` as the LLC replacement policy are in the folder `results_50M/` with all the traces' outputs, csv files and plots.

## 1. Building ChampSim with a Custom Prefetcher

ChampSim uses `.l1i_pref`, `.l1d_pref`, `.l2c_pref`, and `.llc_pref` files to define the configuration.

*   **Copy your prefetcher code:** Place the chosen custom prefetcher code (e.g., `CPLXstride_ConfCnt_PD3.l1d_pref`) into the appropriate directory (`prefetcher`).

*   **Run `build_champsim.sh`:** Run the `build_champsim.sh` script to use the custom prefetchers. You'll need to specify the base name of the prefetcher file (without the `.l1d_pref` extension) as arguments to the script. For example:

    ```bash
    ./build_champsim.sh hashed_perceptron no CPLXstride_ConfCnt_PD3 no no lru 1
    ```

    This command builds a single-core ChampSim binary using the `hashed_perceptron` branch predictor, no L1I prefetcher, `CPLXstride_ConfCnt_PD3` as the L1D prefetcher, no L2C prefetcher, no LLC prefetcher, and `lru` as the LLC replacement policy.

    **Important:** Ensure that the specified `.l1i_pref`, `.l1d_pref`, `.l2c_pref`, `.llc_pref` and `.llc_repl` files exist in their respective directories (`prefetcher`, `replacement`, and `branch`). The script `build_champsim.sh` performs checks to ensure these files exist.

## 2. Running Simulations

*   **Traces:** Make sure you have the trace files you want to use for benchmarking. The default trace directory is `dpc3_traces`. You can download the DPC-3 traces used indicated in the file `trace_files.txt`

*   **Run `run_champsim.sh`:** Execute the `run_champsim.sh` script to run the simulation. Specify the binary name (created in step 1), the number of warmup instructions, the number of simulation instructions, the trace file, and any extra options.

    ```bash
    ./run_champsim.sh hashed_perceptron-no-CPLXstride_ConfCnt_PD3-no-no-lru-1core 10 50 602.gcc_s-2226B.champsimtrace.xz
    ```

    This command runs the `hashed_perceptron-no-CPLXstride_ConfCnt_PD3-no-no-lru-1core` binary with 10 million warmup instructions, 50 million simulation instructions, and the `602.gcc_s-2226B.champsimtrace.xz` trace file.

    Simulation results will be stored in the `results_50M/` directory (or a directory with a name matching the `${N_SIM}` variable). The results file will be named according to the `${TRACE}-${BINARY}-${OPTION}.txt` pattern.

# Original Champsim README

<p align="center">
  <h1 align="center"> ChampSim </h1>
  <p> ChampSim is a trace-based simulator for a microarchitecture study. You can sign up to the public mailing list by sending an empty mail to champsim+subscribe@googlegroups.com. Traces for the 3rd Data Prefetching Championship (DPC-3) can be found from here (https://dpc3.compas.cs.stonybrook.edu/?SW_IS). A set of traces used for the 2nd Cache Replacement Championship (CRC-2) can be found from this link. (http://bit.ly/2t2nkUj) <p>
</p>

# Clone ChampSim repository
```
git clone https://github.com/ChampSim/ChampSim.git
```

# Compile

ChampSim takes five parameters: Branch predictor, L1D prefetcher, L2C prefetcher, LLC replacement policy, and the number of cores. 
For example, `./build_champsim.sh hashed_perceptron no no lru 1` builds a single-core processor with hashed_perceptron branch predictor, no L1/L2 data prefetchers, and the baseline LRU replacement policy for the LLC.
```
$ ./build_champsim.sh hashed_perceptron no no no no lru 1

$ ./build_champsim.sh ${BRANCH} ${L1I_PREFETCHER} ${L1D_PREFETCHER} ${L2C_PREFETCHER} ${LLC_PREFETCHER} ${LLC_REPLACEMENT} ${NUM_CORE}
```

# Download DPC-3 trace

Professor Daniel Jimenez at Texas A&M University kindly provided traces for DPC-3. Use the following script to download these traces (~20GB size and max simpoint only).
```
$ cd scripts

$ ./download_dpc3_traces.sh
```

# Run simulation

Execute `run_champsim.sh` with proper input arguments. The default `TRACE_DIR` in `run_champsim.sh` is set to `$PWD/dpc3_traces`. <br>

* Single-core simulation: Run simulation with `run_champsim.sh` script.

```
Usage: ./run_champsim.sh [BINARY] [N_WARM] [N_SIM] [TRACE] [OPTION]
$ ./run_champsim.sh hashed_perceptron-no-no-no-no-lru-1core 1 10 602.gcc_s-2226B.champsimtrace.xz

${BINARY}: ChampSim binary compiled by "build_champsim.sh" (hashed_perceptron-no-no-lru-1core)
${N_WARM}: number of instructions for warmup (1 million)
${N_SIM}:  number of instructinos for detailed simulation (10 million)
${TRACE}: trace name (602.gcc_s-2226B.champsimtrace.xz)
${OPTION}: extra option for "-low_bandwidth" (src/main.cc)
```
Simulation results will be stored under "results_${N_SIM}M" as a form of "${TRACE}-${BINARY}-${OPTION}.txt".<br> 

* Multi-core simulation: Run simulation with `run_4core.sh` script. <br>
```
Usage: ./run_4core.sh [BINARY] [N_WARM] [N_SIM] [N_MIX] [TRACE0] [TRACE1] [TRACE2] [TRACE3] [OPTION]
$ ./run_4core.sh hashed_perceptron-no-no-no-lru-4core 1 10 0 602.gcc_s-2226B.champsimtrace.xz \\
  401.bzip2-38B.champsimtrace.xz 403.gcc-17B.champsimtrace.xz 410.bwaves-945B.champsimtrace.xz
```
Note that we need to specify multiple trace files for `run_4core.sh`. `N_MIX` is used to represent a unique ID for mixed multi-programmed workloads. 


# Add your own branch predictor, data prefetchers, and replacement policy
**Copy an empty template**
```
$ cp branch/branch_predictor.cc branch/mybranch.bpred
$ cp prefetcher/l1d_prefetcher.cc prefetcher/mypref.l1d_pref
$ cp prefetcher/l2c_prefetcher.cc prefetcher/mypref.l2c_pref
$ cp prefetcher/llc_prefetcher.cc prefetcher/mypref.llc_pref
$ cp replacement/llc_replacement.cc replacement/myrepl.llc_repl
```

**Work on your algorithms with your favorite text editor**
```
$ vim branch/mybranch.bpred
$ vim prefetcher/mypref.l1d_pref
$ vim prefetcher/mypref.l2c_pref
$ vim prefetcher/mypref.llc_pref
$ vim replacement/myrepl.llc_repl
```

**Compile and test**
```
$ ./build_champsim.sh mybranch mypref mypref mypref myrepl 1
$ ./run_champsim.sh mybranch-mypref-mypref-mypref-myrepl-1core 1 10 bzip2_183B
```

# How to create traces

We have included only 4 sample traces, taken from SPEC CPU 2006. These 
traces are short (10 million instructions), and do not necessarily cover the range of behaviors your 
replacement algorithm will likely see in the full competition trace list (not
included).  We STRONGLY recommend creating your own traces, covering
a wide variety of program types and behaviors.

The included Pin Tool champsim_tracer.cpp can be used to generate new traces.
We used Pin 3.2 (pin-3.2-81205-gcc-linux), and it may require 
installing libdwarf.so, libelf.so, or other libraries, if you do not already 
have them. Please refer to the Pin documentation (https://software.intel.com/sites/landingpage/pintool/docs/81205/Pin/html/)
for working with Pin 3.2.

Get this version of Pin:
```
wget http://software.intel.com/sites/landingpage/pintool/downloads/pin-3.2-81205-gcc-linux.tar.gz
```

**Note on compatibility**: If you are using newer linux kernels/Ubuntu versions (eg. 20.04LTS), you might run into issues (such as [[1](https://github.com/ChampSim/ChampSim/issues/102)],[[2](https://stackoverflow.com/questions/55698095/intel-pin-tools-32-bit-processsectionheaders-560-assertion-failed)],[[3](https://stackoverflow.com/questions/43589174/pin-tool-segmentation-fault-for-ubuntu-17-04)]) with the PIN3.2. ChampSim tracer works fine with newer PIN tool versions that can be downloaded from [here](https://software.intel.com/content/www/us/en/develop/articles/pin-a-binary-instrumentation-tool-downloads.html). PIN3.17 is [confirmed](https://github.com/ChampSim/ChampSim/issues/102) to work with Ubuntu 20.04.1 LTS.

Once downloaded, open tracer/make_tracer.sh and change PIN_ROOT to Pin's location.
Run ./make_tracer.sh to generate champsim_tracer.so.

**Use the Pin tool like this**
```
pin -t obj-intel64/champsim_tracer.so -- <your program here>
```

The tracer has three options you can set:
```
-o
Specify the output file for your trace.
The default is default_trace.champsim

-s <number>
Specify the number of instructions to skip in the program before tracing begins.
The default value is 0.

-t <number>
The number of instructions to trace, after -s instructions have been skipped.
The default value is 1,000,000.
```
For example, you could trace 200,000 instructions of the program ls, after
skipping the first 100,000 instructions, with this command:
```
pin -t obj/champsim_tracer.so -o traces/ls_trace.champsim -s 100000 -t 200000 -- ls
```
Traces created with the champsim_tracer.so are approximately 64 bytes per instruction,
but they generally compress down to less than a byte per instruction using xz compression.

# Evaluate Simulation

ChampSim measures the IPC (Instruction Per Cycle) value as a performance metric. <br>
There are some other useful metrics printed out at the end of simulation. <br>

Good luck and be a champion! <br>
