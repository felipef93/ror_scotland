# Rates of Rise - Scotland: Code and Data

This repository contains the code and data used in the study **"Characteristics of Gauged Abrupt Wave Fronts (Walls of Water) in Flash Floods in Scotland."**

## Contents

- **`code/`**: Contains the code used to extract the annual maximum rates of rise for flow and level for every station in Scotland.
- **`data/`**: Includes annual maximum flow and level rates of rise for each station in the study.
- **`final_extracted_ror.csv`**: Lists the events considered in the analysis after the removal of winter events and visual checks for spurious data.

## Availability of Raw 15-Minute Flow and Level Time Series

The 15-minute time series data used in this study are available for download via the [SEPA Time Series Data Service (API)](https://timeseriesdoc.sepa.org.uk/).

## Usage of the Code

A sample input file (`input_sample.csv`) has been provided for ease of use with the code. 

### Main Code
- The primary script for extracting the rates of rise (RoRs) for each station is located at **`xxxxxx.py`**.

### Parallel Processing
- For batch processing of multiple stations, parallelized code is available at **`xxxxxxx.py`**.