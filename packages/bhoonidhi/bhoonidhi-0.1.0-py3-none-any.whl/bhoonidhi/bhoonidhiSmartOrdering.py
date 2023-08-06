# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 22:42:51 2020
@author: Rohit Gandikota
"""

import numpy as np
import json
import re
import os
import logging
from .bhoonidhi_helper import serverFilterBhoonidhi, getBhoonidhiSat, getBhoonidhiSen, getBhoonidhiDates, getEventsBhoonidhi, getBhoonidhiEventDate, getBhoonidhiProductTypefromResolution, hitBhoonidhi
from .utils import findParameters, findCities, findDates, findSatSen, getTokensPOS, preprocess#, Voice2Text
#%% Proxy settings
#import nltk
#os.environ["https_proxy"] = "http://user_name:password@proxy.inst.com:port"
#nltk.set_proxy("http://user_name:password@proxy.inst.com:port")
logging.basicConfig(filename='bhoonidhiSmartSearch.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
#%% Smart Searching for Bhoonidhi

def bhoonidhiSmartEventSearch(user_tokens):
    events = (getEventsBhoonidhi())
    common_data = []
    specific_data = []
    found_events = []
    for event in events.keys():
#        print(event)
        f = events[event]
        f.append(event)
#        print(f)
        for token in user_tokens:
            if token in event:
                if 'flood' in token or 'avalanche' in token:
                    common_data.append(f) 
                else:
                    specific_data.append(f)
                break
    if specific_data == []:
        found_events = common_data
    else:
        found_events = specific_data
        
    unique = []
    final_events = []
    i = 0
    for f in found_events:
        if i == 0:
            unique.append(f[-1])
            final_events.append(f)
        elif f[-1] not in unique:    
            final_events.append(f)
    found_events = final_events
    del(final_events)
            
            

            
        
    found_events =(found_events)
    if len(np.shape(found_events)) == 1:
        found_events = [found_events]
    jsons = []
    for event in found_events:
        available_sens = event[3].split(',')
        sens = []
        for sen in available_sens:
            for token in user_tokens:
                if token in sen:
                    sens.append(sen)
        if sens == []:
            sens = available_sens
        for sen in sens:
            sat = getBhoonidhiSat(['every'])[0]
            json_dict = {}
            json_dict['onlySen'] = getBhoonidhiSen(sen.strip(),sat)
            json_dict["searchCritera"]="EventBased"
            json_dict["userId"]="T"
            json_dict['sat'],json_dict["prod"] = sat[0],sat[1]
            json_dict['sen'] = getBhoonidhiSen('oli','l8')
            json_dict['sdate'] =getBhoonidhiDates(getBhoonidhiEventDate(event[4])) 
            json_dict['edate'] = getBhoonidhiDates(getBhoonidhiEventDate(event[5])) 
            json_dict['cloudThresh'] = '20'
            json_dict['query']='area'
            location = event[1].split(',')
            if len(location)==2:
                json_dict['queryType']='location'
                json_dict['lat']=location[0]
                json_dict['lon']=location[1]
                json_dict['radius']=event[2]
            elif len(location)>2 :
                json_dict['queryType']='polygon'
                json_dict['brlat']=location[4]
                json_dict['brlon']=location[5]
                json_dict['tllat']=location[0]
                json_dict['tllon']=location[1]
            jsons.append(json_dict)    
    return hitBhoonidhi(jsons)
          
def bhoonidhiSmartSearch(user_text, text_based=True,write_json = False):
    feature_count = 0
    # Passing the string text into word tokenize for breaking the sentences
    #################################################################### Finding dates in the string
    user_text = preprocess(user_text) 
        
    init_date, final_date, feature_count = findDates(user_text,feature_count)
    ################################################################## tokenize and parts of speech classification
    user_pos, user_tokens = getTokensPOS(user_text)
    ################################################################# Search for event based
    if re.search(r'flood',user_text) or re.search(r'avalanche',user_text):
        return bhoonidhiSmartEventSearch(user_tokens)
    ################################################################## Get parameters from string
    parameters = findParameters(user_pos)
    parameters = serverFilterBhoonidhi(parameters,user_pos)
    feature_count+=len(parameters)
    ################################################################## Finding geo-locations in the string
    location = findCities(user_text, text_based)
    feature_count+=len(location)
   
    ######################################################################## Finding satellite in the tokens
    try:
        SatSen, feature_count = findSatSen(user_text, feature_count)
    except Exception as e:
        logging.error(str(e))
    output = np.array(SatSen)
    if init_date == 'null' and final_date =='null':    
        statement = f'Do you want {output[1]} data from any time'
    elif init_date != 'null' and final_date =='null':    
        statement = f'Do you want {output} data from the date {init_date}'
    else:
        statement = f'Do you want {output} data from the dates {init_date} till {final_date}'
    
    if len(location) >0:
        statement += f' in the region of {[city[0] for city in location]}'
    if len(parameters)>0:
        statement += ' with constraints '
        for parameter in parameters:
            statement+= f'{str(parameter[-1])} = {str(parameter[0])} and '
        statement = statement[:-5]   
    

          
    if feature_count>0:  
#        logging.info(statement)
        jsons = []
        
        skip = False
        if len(location)>0:
            for city in location:
                for output in SatSen:
                    logging.info(f'Found {feature_count} number of features in the query')
                    json_dict = {}
                    json_dict["searchCritera"]="SatelliteBased"
                    json_dict["userId"]="T"
                    json_dict['sat'],json_dict['sen'],json_dict["prod"] = output[0],output[1],output[2]
                    json_dict['sdate'] =getBhoonidhiDates(init_date) 
                    json_dict['edate'] = getBhoonidhiDates(final_date)
                    json_dict['cloudThresh'] = '30'
                    json_dict['query']='date'
                    if len(parameters)> 0:
                        if 'resolution' in np.array(parameters)[:,-1]:
                            json_dict["searchCritera"]="ResolutionBased"
                            json_dict['prod'] = getBhoonidhiProductTypefromResolution(parameters)
                            skip = True
                        if 'lat' in np.array(parameters)[:,-1]:
                            json_dict['query']='area'
                            json_dict['queryType']='location'
                    if len(city)>0:
                        json_dict['lat']=city[1]
                        json_dict['lon']=city[2]
                        json_dict['query']='area'
                        json_dict['queryType']='location'
                        try:
                            if not len(json_dict['radius'])>0:
                                json_dict['radius']= '10'
                        except:
                            json_dict['radius']= '10'
                    
                    if len(parameters)>0:
                        for parameter in parameters:
                            json_dict[parameter[-1]] = parameter[0]
                    jsons.append(json_dict)
                    if skip:
                        break
        else:
            for output in SatSen:
#                print(sat)
                logging.info(f'Found {feature_count} features in the query')
                json_dict = {}
                json_dict["searchCritera"]="SatelliteBased"
                json_dict["userId"]="T"
                json_dict['sat'],json_dict['sen'],json_dict["prod"] = output[0],output[1],output[2]
                json_dict['sdate'] =getBhoonidhiDates(init_date) 
                json_dict['edate'] = getBhoonidhiDates(final_date)
                json_dict['cloudThresh'] = '20'
                json_dict['query']='date'
                if len(parameters)> 0:
                    if 'resolution' in np.array(parameters)[:,-1]:
                        json_dict["searchCritera"]="ResolutionBased"
                        json_dict['prod'] = getBhoonidhiProductTypefromResolution(parameters)
                        skip = True
                    if 'lat' in np.array(parameters)[:,-1]:
                        json_dict['query']='area'
                        json_dict['queryType']='location'
                if len(parameters)>0:
                    for parameter in parameters:
                        json_dict[parameter[-1]] = parameter[0]
                jsons.append(json_dict)
                if skip:
                    break
        
        if write_json == True:
            json_path = "D:\\Projects\\Bhoonidhi\\SmartOrdering\\user_request.json"
            if os.path.exists(json_path):
                os.remove(json_path)
            for i in range(len(jsons)):
                with open(json_path, "w+") as outfile:  
                        json.dump(jsons[i], outfile)
        return hitBhoonidhi(jsons)
    else:   
        logging.warning('No relevant features found in the query')
        raise Exception('No relevant features found in the query')
        

if __name__ == "__main__":   
    user_text = 'Get me sentinel data from hyderabad with radius of 100 km with resolution coarser than 30 mts latitude 10.56 and longitude of 72.35 and cloud coverage of less than 5 %'
    json_obj =  bhoonidhiSmartSearch(user_text)
    json_obj
    user_text = 'Data over Jaipur from yesterday with no cloud and medium resolution'
    json_obj =  bhoonidhiSmartSearch(user_text)
    json_obj
    user_text = 'Hyderabad from 14th September radius 100 km 15% cloud l8 oli latitude = 17.33 and longitude = 78.5 '
    json_obj =  bhoonidhiSmartSearch(user_text)
    json_obj
    user_text = 'Get data greater than 30 m resolution'
    json_obj =  bhoonidhiSmartSearch(user_text)
    json_obj
    user_text = 'Hyderabad with resolution=30m'
    json_obj =  bhoonidhiSmartSearch(user_text)
    json_obj
    user_text = 'resolution more than 50 m and radius of 10 km around hyderabad landsat 8 data'
    json_obj =  bhoonidhiSmartSearch(user_text)
    json_obj
    user_text = 'Get Hyderabad pingpong with medium resolution'
    json_obj =  bhoonidhiSmartSearch(user_text)
    json_obj
    user_text = 'get satellite data more than 100 Meter Resolution'
    json_obj =  bhoonidhiSmartSearch(user_text)
    json_obj
    user_text = 'Lat 17.18 Lon 89.33 radius 300 landsat 8 oli'
    json_obj =  bhoonidhiSmartSearch(user_text)
    json_obj
    user_text = 'get landsat 8 data for past two months over hyderabad and guntur area of 400 km2'
    json_obj =  bhoonidhiSmartSearch(user_text)
    json_obj
    user_text = 'data<10 meters resolution'
    json_obj =  bhoonidhiSmartSearch(user_text)
    json_obj
    user_text = 'Recent data of LandSat-8'
    user_text = 'l8 landsat8 land sat 8 landsat 8 sentinel 2 sentinel 2A'
    json_obj =  bhoonidhiSmartSearch(user_text)
    json_obj    
    user_text= "Fetch Landsat8 MX data from 14th June to 23rd July over Mexico"
    user_text="Resourcesat Data MX 15th July to 20th September Hyderabad"
    user_text = "I want cartosat3 satellite MX sensor over the region of Hyderabad and Bangalore from today till December 30"
    user_text = "I want all the available data from today"
    user_text = "get me data from avalanche and kerala flood"
  
    json_obj =  bhoonidhiSmartSearch(user_text)
    json_obj
    
    user_text = 'get me the data from March'
    json_obj =  bhoonidhiSmartSearch(user_text)
    json_obj
    json_obj = [json_obj[0]]
    response = hitBhoonidhi(json_obj)