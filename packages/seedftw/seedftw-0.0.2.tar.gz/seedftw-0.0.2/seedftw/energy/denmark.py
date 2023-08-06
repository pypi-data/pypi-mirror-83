# -*- coding: utf-8 -*-
"""
Functions related to data loading in Denmark.

"""

# Import all useful libraries
import pandas as pd
import numpy as np
import json
import urllib.parse

from datetime import datetime, timedelta

# For caching
from functools import lru_cache

# Loading data from Energinet
@lru_cache(maxsize=10)
def __dk_energinet_dataservice_call(sql_query,output_format='Dataframe'):
    
    # Determine the URL to use for the call
    url = 'https://www.energidataservice.dk/proxy/api/datastore_search_sql?sql=' + \
        urllib.parse.quote(sql_query)
    
    # Read data in Json format
    api_data = pd.read_json(url)
            
    if any(api_data.success)==False:
        print("Failure in the API call")
        
    if output_format=='Dataframe':
        api_data = pd.DataFrame.from_records(api_data["result"].records)
    
    return api_data

def electricity_average_co2_intensity(area='', start_time=(datetime.now()-timedelta(hours=168)).strftime("%Y-%m-%dT%H:%M:%SZ"), end_time=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")):
    
    if area=='DK1':
        condition2use = """WHERE "PriceArea" = 'DK1' AND"""
        
    elif area=='DK2':
        condition2use = """WHERE "PriceArea" = 'DK2' AND"""
        
    else:
        condition2use = '''WHERE'''
        
    condition2use = condition2use + """ "Minutes5UTC" >= '""" + start_time + \
        """' AND "Minutes5UTC" <= '""" + end_time + "'"
            
    query2use = '''SELECT "Minutes5UTC", "PriceArea", "CO2Emission" FROM "co2emis" ''' + \
        condition2use + ' ORDER BY "Minutes5UTC" ASC'
    
    co2_data = __dk_energinet_dataservice_call(sql_query=query2use, output_format='Dataframe')                    
    return co2_data


def electricity_average_co2_intensity_forecast(area='', start_time=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"), end_time=(datetime.now()+timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")):
    
    if area=='DK1':
        condition2use = """WHERE "PriceArea" = 'DK1' AND"""
        
    elif area=='DK2':
        condition2use = """WHERE "PriceArea" = 'DK2' AND"""
        
    else:
        condition2use = '''WHERE'''
        
    condition2use = condition2use + """ "Minutes5UTC" >= '""" + start_time + \
        """' AND "Minutes5UTC" <= '""" + end_time + "'"
            
    query2use = '''SELECT "Minutes5UTC", "PriceArea", "CO2Emission" FROM "co2emisprog" ''' + \
        condition2use + ' ORDER BY "Minutes5UTC" ASC'
            
    co2_data = __dk_energinet_dataservice_call(sql_query=query2use, output_format='Dataframe')                    
    return co2_data
        