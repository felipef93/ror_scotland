# Rates of Rise - Scotland: Code and Data

This repository contains the code and data used in the study **"Characteristics of Gauged Abrupt Wave Fronts (Walls of Water) in Flash Floods in Scotland."**

## Contents

- **`data`**: Includes annual maximum flow and level rates of rise for each station in the study.
- **`sample inputs`**: sample of inputs to the code 
- **`station.py`** and **`main.py`**: Code used to extract the annual maximum rates of rise for flow and level for every station in Scotland.
- **`final_extracted_ror.csv`**: Lists the events considered in the analysis after the removal of winter events and visual checks for spurious data.

## Raw data availability 

- **15-Minute Flow and Level Time Series**: The 15-minute time series data used in this study are available for download via the [SEPA Time Series Data Service (API)](https://timeseriesdoc.sepa.org.uk/).
- **NRFA data**: NRFA data, used to converting stations local IDs and identifying the stations is avilable at the [NRFA website](https://nrfa.ceh.ac.uk/data/search)

## Usage of the Code

A sample of flow and level inputs has been provided for ease of use with the code. The primary script for extracting the rates of rise (RoRs) for each station is located at **`station.py`**. For batch processing of multiple stations, parallelized code is available at **`main.py`**. To run, update the variables `continous_data` and `nrfa_meta` in main.