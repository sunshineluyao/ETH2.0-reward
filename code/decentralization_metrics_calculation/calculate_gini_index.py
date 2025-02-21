import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import date

def calculate_gini_index(df, column_name):
    """
    Calculate the Gini coefficient of a specified column in a DataFrame.
    df: DataFrame containing the column to calculate the Gini coefficient.
    column_name: str, the name of the column.
    Returns: float, the Gini coefficient.
    """
    if df.empty or column_name not in df.columns:
        return None
    values = sorted(df[column_name].tolist())
    if len(values) == 0:
        return None
    n = len(values)
    numer = sum([(i+1) * values[i] for i in range(n)])
    denom = n * sum(values)
    if denom == 0:
        return None  
    gini = (2 * numer) / denom - (n + 1) / n
    return gini

if __name__ == "__main__":
    start = date(2022,9,15)
    end = date(2023,9,16)
    # please change the file path to your local path
    reward=pd.read_parquet('data/raw_reward_data/daily_validator_index_reward/total_validator_reward.parquet')
    reward['date']=pd.to_datetime(reward['date']).dt.date
    reward=reward.sort_values(by=['date'])
    reward.set_index('date',inplace=True)
    reward1=reward[['Total reward','Proposer reward','Attestation reward','Sync committee reward']]
    index_name='gini'
    for j in tqdm(reward1.columns):
        reward1[j]=reward1[j].astype(float)
        # change the negative value to 0
        if j in ['Total reward','Attestation reward']:
            reward1[j]=np.where(reward1[j]<0,0,reward1[j])
            reward1.reset_index(inplace=True)
            data=reward1
        else:
            data=reward1[reward1[j] > 0]
        file_name="_".join([i.lower() for i in j.split(' ')])
        with open(f'data/decentralization_metrics_data/{index_name}_{j}.csv', 'a') as file:
            file.write(f'date,{j}\n')
            for day in tqdm(pd.date_range(start, end)):
                daily_data = data[(data['date'] == day.date())]
                if not daily_data.empty:
                    gini_value = calculate_gini_index(daily_data, j)
                    file.write(f'{day.date()},{gini_value}\n')

        
   