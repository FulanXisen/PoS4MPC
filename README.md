# PoS4SMPC

experimental result of PoS4SMPC

- examples/: the folder contains security policy examples of programs
- benchmark/: the folder contains source files of benchmark using Obliv-C and MPyC
- performance.pdf: detail performance data in Obliv-C and MPyC

## Executing programs
### Using Obliv-C
The measurements of benchmark in Obliv-C rely on Absentminded Crypto Kit. We only provide the function implementation here.
#### Requirements
- install `Obliv-C` from https://github.com/samee/obliv-c 
- install `Absentminded Crypto Kit` from https://bitbucket.org/jackdoerner/absentminded-crypto-kit/src/master

#### Step
1. put the files you want to execute in benchmark/oblivc into absentminded-crypto-kit/src/
2. measurements using absentminded-crypto-kit's template in absentminded-crypto-kit/test/
3. update makefile
### Using MPyc
#### Requirements
- install `Python`, version 3.x
- install Python's `mpyc` package using `pip`
### Step
run command `python LinS.py --opt -e 10 -s 1 -i 5 -M 2` (resp. `BinS.py`, `AlmS.py`) to run v2 of LinS (resp. BinS, AlmS) with 10 input array length, 1 search element, 5 repeation in 2 party setting, take out `--opt` to run v1.

run command `python QS.py --opt -n 10 -i 5` (resp. `PSI.py`) to run v2 of QS (resp. PSI) with 10 input array length (half for each party), 5 repeation in 2 party setting, take out `--opt` to run v1.
