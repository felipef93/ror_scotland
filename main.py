
import pandas as pd
import multiprocessing
from functools import partial

from station import workflow

def main():
    continous_data= ### your path here/sample_inputs/
    nrfa_meta= ### your path to nrfa_metadata here    
        
    station_list=list(nrfa_meta.id)

    func=partial(workflow,
                 nrfa_meta=nrfa_meta,
                 continous_data_location=continous_data)

    pool = multiprocessing.Pool(processes=16)


    pool.map(func,station_list)
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()