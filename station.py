
# Create a station object with the hydrometric station

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import csv

class station:
    def __init__(self, 
                 station_id,
                 local_id,
                 data_level,
                 data_flow,
                 start_date,
                 end_date,
                 #nrfa_max_med
                 ):
        self.station_id = station_id
        self.local_id = local_id
        self.data_level = data_level
        self.data_flow = data_flow
        self.start_date = start_date
        self.end_date = end_date

        self.amax_level_ror=pd.DataFrame()
        self.amax_flow_ror=pd.DataFrame()

        self.amax_ror=pd.DataFrame()


    def rors_level_and_flow(self):
        self.data_level=compute_rors(self.data_level,'level')
        self.data_flow=compute_rors(self.data_flow,'flow')
        
        # compute threshold ror
        self.amax_level_ror=compute_amax(self.data_level,'ror_level')
        self.amax_flow_ror=compute_amax(self.data_flow,'ror_flow')

    def merge_datasets(self):
        self.amax_level_ror['date']=self.amax_level_ror.index
        self.amax_flow_ror['date']=self.amax_flow_ror.index
        # Get amax flow and level data in the same panda dataframe by using the water year as the key whilist keeping the index
        self.amax_ror=pd.merge(self.amax_level_ror,self.amax_flow_ror,how='inner',on='water_year',suffixes=('_level','_flow'))
        #water year as index
        self.amax_ror.set_index('water_year',inplace=True)
        # reorer as [date_level, valuel_level, ror_level, date_flow, value_flow, ror_flow]
        self.amax_ror=self.amax_ror[['date_level','ror_level','ror_rel_level','date_flow','ror_flow','ror_rel_flow']]

    def export_dataset(self):
        # If data folder does not exist, create it
        if not os.path.exists('data'):
            os.makedirs('data')
        self.amax_ror.to_csv(f'data/{self.station_id}.csv')


def compute_amax(data,column_name):
    water_year = [ele.year if ele.month<10 else ele.year+1 for ele in data.index]
    date_1 = data.groupby(water_year)[column_name].idxmax()        
    amax=data.loc[date_1]
    # add the water year to the dataframe
    amax['water_year'] = list(set(water_year))
    return amax

def compute_rors(any_data, data_type='level'):
    #Resmple the data to 15 minutes
    any_data = any_data.resample('15T').mean()
    #Fill missing timesteps with NA values
    any_data = any_data.asfreq('15T')
    #Compute the rate of rise
    any_data[f'ror_{data_type}'] = any_data['value'].diff()
    def t_minus_1_ror(any_data):
    #Compute relative ror in regard to the previous timestep if the current timestep is above the 10th percentile
        ror_rel_t1 = any_data[f'ror_{data_type}'].copy()
        ror_rel_t1[any_data['value'] <= any_data['value'].quantile(0.9)] = np.nan
        ror_rel_t1 = ror_rel_t1 / any_data['value'].shift(1)
        return ror_rel_t1.values
    
    any_data[f'ror_rel_{data_type}']=t_minus_1_ror(any_data)
    return any_data


def read_data(nrfa_station_nbr,nrfa_meta,continous_data_location):

    local_station_nbr=str(nrfa_meta[nrfa_meta['id']==nrfa_station_nbr]['measuring-authority-station-id'].values[0]).lower()

    station_meta=nrfa_meta[nrfa_meta['id']==nrfa_station_nbr]
    if 'SEPA' in station_meta['measuring-authority-id'].values[0]:
        if os.path.exists(f'{continous_data_location}/mergedlevel/{str(local_station_nbr)}.txt') and os.path.exists(f'{continous_data_location}/mergedflow/{str(local_station_nbr)}.txt'):    
            level_data=pd.read_csv(f'{continous_data_location}/mergedlevel/{str(local_station_nbr)}.txt',index_col=0,parse_dates=True,usecols=['datetime','value'])
            flow_data=pd.read_csv(f'{continous_data_location}/mergedflow/{str(local_station_nbr)}.txt',index_col=0,parse_dates=True,usecols=['datetime','value'])
            start_date=level_data.index[0]
            end_date=level_data.index[-1]
        else:
            level_data=pd.DataFrame()
            flow_data=pd.DataFrame()
            start_date=np.nan
            end_date=np.nan

        station_x=station(station_id=nrfa_station_nbr,
                    local_id=local_station_nbr,
                    data_level=level_data,
                    data_flow=flow_data,
                    start_date=start_date,
                    end_date=end_date,
                    #nrfa_max_med=list_nrfa
                    )

        return station_x    
    else:
        pass

def workflow(station_id,nrfa_meta,continous_data_location,export_location,nrfa_amax_series):
        #try:
        station = read_data(station_id,nrfa_meta,continous_data_location)
        export_location=r'C:\Users\c1026040\OneDrive - Newcastle University\Scottish_ror_dataset/'
        #pot_stations=list(pd.read_csv(r'C:\Users\c1026040\OneDrive - Newcastle University\Scottish_ror_dataset/POT_60_80.txt',header=None)[0])
        if station is not None and not station.data_level.empty:
            station.rors_level_and_flow()
            #station.export_stations(path=export_location)
            station.merge_datasets()
            station.export_dataset()