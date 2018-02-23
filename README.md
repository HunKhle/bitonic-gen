
# Synthesisable Sorting Network Hardware Generator

This repository contains generator scripts and associated verilog files required to create a syntesizable sorting hardware for a Batcher Bitonic sort network with any required size. The generated hardware currently supports sorting unsigned integers only. 


Consult the Wikipedia article for details about Bitonic sort networks. 
https://en.wikipedia.org/wiki/Bitonic_sorter

## Generating RTL for a Synthesizable Sorting Network

1. Open params.py and set the parameters for your network. 
    - SORT_SIZE: the number of elements the sort unit can process. 
    - DATA_WIDTH: the width of the integer inputs. This typically would be 64 bits. 
    - PIPELINE_STAGES: set this to 0 if you do not need to pipeline the design.

2. run python gen_pipelined_bitonic.py; this will generate two files, bitonic.v and sys_defs.vh. 

3. The rest of the required files (compare-and-swap unit and a skeletal test bench) are already in the rtl/ folder. Move the generated files(bitonic.v and sys_defs.vh) into the folder rtl/ and you are ready to synthesize and test. 
