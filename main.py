
import pandas as pd
import multiprocessing
from functools import partial

from station import workflow

def main():
    continous_data_felipe='C:/Users/c1026040/OneDrive - Newcastle University/15_min_data/scotland_all/import_from_sepa/'
    nrfa_meta=pd.read_csv('C:/Users/c1026040/OneDrive - Newcastle University/15_min_data/england_all/standardized/nrfa-station-metadata.csv', parse_dates=True)   
    nrfa_amax=r'C:\Users\c1026040\OneDrive - Newcastle University\NRFA_amax/'             
    station_list=list(nrfa_meta.id)

    func=partial(workflow,
                 nrfa_meta=nrfa_meta,
                 continous_data_location=continous_data_felipe,
                 export_location=r'C:\Users\c1026040\OneDrive - Newcastle University\Scottish_ror_dataset/',
                 nrfa_amax_series=nrfa_amax)

    pool = multiprocessing.Pool(processes=16)


    pool.map(func,station_list)
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()