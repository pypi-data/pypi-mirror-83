# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 14:14:13 2020
@author: Rohit Gandikota
"""
import numpy as np
import re
import requests
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from dateparser.search import search_dates
import os
import urllib
from multiprocessing.pool import ThreadPool
def serverFilterBhoonidhi(parameters,user_pos):
    user_pos = np.array(user_pos)
    resolution_specific = False
    for filt in parameters:
        if filt[-1] in ['latitude']:
            filt[-1] = 'lat'
        if filt[-1] in ['longitude']:
            filt[-1] = 'lon'
        if filt[-1] in ['resolution']:
            resolution_specific = True
            comp = filt[0][0]
            num = int(re.search(r'\d+',  filt[0]).group())
            if comp == '+':
                num+=10
            if comp == '-':
                num-=9
            if 'kilometer' in filt[0] or 'km' in filt[0] or 'kilo' in filt[0]:
                num = num*1000
            elif 'miles' in filt[0] or 'mile' in filt[0]:
                num = num*1609.34
            elif 'meter' in filt[0] or 'mts' in filt[0] or 'm' in filt[0]:
                num = num
            
            
            if num < 10:
                filt[0] = 'High'
            elif num < 50:
                filt[0] ='Medium'
            elif num < 200:
                filt[0] = 'Low'
            elif num < 1000:
                filt[0] = 'Coarse'
            else:
                filt[0] = 'Medium'
                
            
            
        if filt[-1] in ['radius','area','swath','spread']:
            num = int(re.search(r'\d+',  filt[0]).group())
            if filt[-1]=='area':
                num = int(num**0.5)
            if 'kilometer' in filt[0] or 'km' in filt[0] or 'kilo' in filt[0]:
                pass
            elif 'miles' in filt[0] or 'mile' in filt[0]:
                num = num*1609.34
            elif 'meter' in filt[0] or 'mts' in filt[0] or 'm' in filt[0]:
                num = num*0.001
            filt[0] = str(num)
            filt[-1] = 'radius'
            
            
        if filt[-1] == 'cloud':
            filt[-1] = 'cloudThresh'
            filt[0] = int(re.search(r'\d+',  filt[0]).group())
    if resolution_specific == False and 'resolution' in user_pos[:,0]:
        if 'medium' in user_pos[:,0]:
            parameters.append(['Medium','resolution'])
        elif 'low' in user_pos[:,0]:
            parameters.append(['Low','resolution'])
        elif 'high' in user_pos[:,0]:
            parameters.append(['High','resolution'])
        elif  'coarse' in user_pos[:,0]:
            parameters.append(['Coarse','resolution'])
        else:
            pass
    return parameters

def getBhoonidhiSat(names):
    def logic(name):
        if name in ['l8','landsat8','every']:
            return 'LandSat-8','Standard'
        elif name in ['sentinel1A']:
            return 'Sentinel-1A','GRD'
        elif name in ['sentinel2A']:
            return 'Sentinel-2A','Level-1C'
        elif name in ['sentinel1B']:
            return 'Sentinel-1B','GRD'
        elif name in ['sentinel2B']:
            return 'Sentinel-2B','Level-1C'
        elif name in ['oceansat2']:
            return 'OceanSat-2','L1B'
        else:
            raise Exception('Satellite not available on bhoonidhi')
            
        
    if len(names)>1:
        output = []
        i = 0
        for name in names:
            sat,prod = logic(name)
            if i != 0:
                if sat not in np.array(output)[:,0]:
                    output.append((sat,prod))
            else:
                output.append((sat,prod))
            i+=1
        return output
    else:
        if names[0] == 'every':
            output = []
            all_sats = ['landsat8','sentinel1A','sentinel2A','sentinel1B','sentinel2B','oceansat2']
            for name in all_sats:
                sat,prod = logic(name)
                output.append((sat,prod))
            return output
            
        else:
            return [logic(names[0])]
    
def getBhoonidhiSatSen(user_sat,user_sen):
    output = []
    def logicSat(name):
        if name in ['l8','landsat8','every']:
            return 'LandSat-8','OLI%2BTIRS','Standard'
        elif name in ['sentinel1a']:
            return 'Sentinel-1A','SAR(IW)','GRD'
        elif name in ['sentinel2a']:
            return 'Sentinel-2A','MSI','Level-1C'
        elif name in ['sentinel1b']:
            return 'Sentinel-1B','SAR(IW)','GRD'
        elif name in ['sentinel2b']:
            return 'Sentinel-2B','MSI','Level-1C'
        elif name in ['oceansat2']:
            return 'OceanSat-2','OCM','L1B'
        else:
            raise Exception('Satellite not available on bhoonidhi')
        
    if 'optical' in user_sen:
        user_sat.append('landsat8')
        user_sat.append('sentinel2a')
        user_sat.append('sentinel2b')
    if 'microwave' in user_sen:
        user_sat.append('sentinel1a')
        user_sat.append('sentinel1b')
        
    if 'sentinel' in user_sat:
        user_sat.pop(user_sat.index('sentinel'))
        user_sat.append('sentinel2a')
        user_sat.append('sentinel2b')
        user_sat.append('sentinel1a')
        user_sat.append('sentinel1b')
    if 'landsat' in user_sat:
        user_sat.pop(user_sat.index('landsat'))
        user_sat.append('landsat8')
    if 'oceansat' in user_sat:
        user_sat.pop(user_sat.index('oceansat'))
        user_sat.append('oceansat2')
        
        
    if len(user_sat)>0 or len(user_sen)>0:
        i = 0
        for name in user_sat:
            sat,sen,prod = logicSat(name.lower())
            if i != 0:
                if (sat,sen,prod) not in output:
                    output.append((sat,sen,prod))
            else:
                output.append((sat,sen,prod))
            i+=1
        
        if len(user_sen)>0:
            user_sat = []
            for name in user_sen:
                if name in ['oli','OLI+TIRS']:
                    user_sat.append('l8')
                elif name in ['msi','MSI']:
                    user_sat.append('sentinel2a')
                    user_sat.append('sentinel2b')
                elif name in ['sar','SAR']:
                    user_sat.append('sentinel1a')
                    user_sat.append('sentinel1b')
                elif name in ['ocm','OCM']:
                    user_sat.append('oceansat2')
            for name in user_sat:
                sat,sen,prod = logicSat(name.lower())
                if len(output) != 0:
                    if (sat,sen,prod) not in output:
                            output.append((sat,sen,prod))
                else:
                    output.append((sat,sen,prod))
        return output
    else:
        return [logicSat('l8')]
   
def getBhoonidhiSen(name,sat):
    if name == 'every':
        if sat == 'LandSat-8':
            return 'OLI%2BTIRS'
        if sat == 'Sentinel-1A':
            return 'SAR(IW)'
        if sat == 'Sentinel-2A':
            return 'MSI'
        if sat == 'Sentinel-1B':
            return 'SAR(IW)'
        if sat == 'Sentinel-2B':
            return 'MSI'
        if sat == 'OceanSat-2':
            return 'OCM'
    if name in ['oli','OLI+TIRS']:
        return 'OLI%2BTIRS'
    elif name in ['msi','MSI']:
        return 'MSI'
    elif name in ['sar','SAR']:
        return 'SAR(IW)'
    elif name in ['ocm','OCM']:
        return 'OCM'
    else:
        raise Exception(f'Given sensor configuration not available: {name}')
    
def getBhoonidhiDates(string):
    terms = string.split(' ')
    date = terms[0]
    month = terms[1][:3].upper()
    year = terms[2]
    return month+'%2F'+date+'%2F'+year
def hitBhoonidhi(jsons):
    output = []
    i=0
    for j in jsons:
        i=i+1
        response = requests.post('https://bhoonidhi.nrsc.gov.in/bhoonidhi/ProductSearch', json=j, timeout=10)
        try:
            if i == 1:
                output = response.json()['Results']
            else:
                output.extend(response.json()['Results'])
        except:
            pass
    return output
def getCitiesBhoonidhi():
    response = requests.post('https://bhoonidhi.nrsc.gov.in/bhoonidhi/GetLocations', timeout=5) 
    locs =  response.json()['Results']
    cities = []
    for loc in locs:
        cities.append([loc['Location'].split(',')[0].lower(),loc['Lat'],loc['Lon']])
    return cities
def getEventsBhoonidhi():
    response = requests.post('https://bhoonidhi.nrsc.gov.in/bhoonidhi/Events', json={"action":"GetAllEvents"}, timeout=5) 
    events =  response.json()['Results']
    EVENTS = {}
    for event in events:
        event2 = event['events']
        for event1 in event2:
            EVENTS[event1['Name'].lower()] = ([event['type'],event1['points'],event1['areaAroundPoint'],event1['distinctSen'],event1['startDate'],event1['endDate']])
    return EVENTS
def getGeoLocationBhoonidhi(user_text):
    '''
    Returns: Shapefile name or lat lon, code (0 if no match, 1 if shapefile, 2 if lat lon)
    '''
    user_tokens = word_tokenize(user_text.lower())
#    countries = []
#    states = []
    cities = np.array(getCitiesBhoonidhi())
    lemmatizer = WordNetLemmatizer() 
    #    pst = PorterStemmer()
    for i in range(len(user_tokens)):
        user_tokens[i] = lemmatizer.lemmatize(user_tokens[i])
    
    user_pos = nltk.pos_tag(user_tokens)
    results = []
    for word in user_pos:
        probable = word[0]
    #            if probable in countries[:,0]:
    #                return countries[np.where(probable in Countries[:,0]),1][0] , 1
    #            elif probable in states[:,0]:
    #                return states[np.where(probable==states[:,0]),1][0] , 1
        if probable in cities[:,0]:
            results.append(cities[np.where(probable == cities[:,0])][0])
        else:
            pass
    return results
def getBhoonidhiEventDate(string):
    date = search_dates(string)[0][-1]
    return date.strftime("%d %B, %Y")
def getBhoonidhiProductTypefromResolution(parameters):
    parameters = np.array(parameters)
    for parm in parameters:
        if parm[1] == 'resolution':
            if parm[0] == 'Low':
                return 'Level-1C'
            if parm[0] == 'Medium':
                return 'Standard'
            if parm[0] == 'High':
                return 'null'
            if parm[0] == 'Coarse':
                return 'L1B'

def bhoonidhiLogin(user_id, password):
    url = 'https://bhoonidhi.nrsc.gov.in/bhoonidhi/LoginServlet'
    json = {}
    json['userId'] = user_id
    json['password'] = password
    json['oldDB'] = 'false'
    json['action'] = 'VALIDATE_LOGIN'
    
    response = requests.post(url, json=json)
    
    return response.json()["Results"][0]['JWT']


def bhoonidhiDownload(product_obj, user_id, password, output_path=''):
    token = bhoonidhiLogin(user_id, password)
    sat = product_obj['OTS_SATELLITE']
    if sat == 'L8':
        sen = 'O'
    else:
         sen = product_obj['OTS_SENSOR']
    year = product_obj['OTS_DATE_OF_DUMPING'].split('-')[-1]
    month = product_obj['OTS_DATE_OF_DUMPING'].split('-')[1].upper()
    prdId = product_obj['OTS_OTSPRODUCTID']
    
    try:
        path = "https://bhoonidhi.nrsc.gov.in/bhoonidhi/data/" + sat + "/" + sen + "/" + year + "/" + month + "/" + prdId + ".zip?token=" + token + "&product_id=" + prdId
        urllib.request.urlretrieve(path, os.path.join(output_path,prdId + ".zip"))
        return f'Downloaded the product succefully at {os.path.join(output_path,prdId + ".zip")}'
    except Exception as e:
        return str(e)
def bhoonidhiBatchDownload(products, user_id, password, output_path=''):
    def download(product):
        product_obj = product[0]
        user_id= product[1]
        password = product[2]
        token = bhoonidhiLogin(user_id, password)
        sat = product_obj['OTS_SATELLITE']
        if sat == 'L8':
            sen = 'O'
        else:
             sen = product_obj['OTS_SENSOR']
        year = product_obj['OTS_DATE_OF_DUMPING'].split('-')[-1]
        month = product_obj['OTS_DATE_OF_DUMPING'].split('-')[1].upper()
        prdId = product_obj['OTS_OTSPRODUCTID']
        
        try:
            path = "https://bhoonidhi.nrsc.gov.in/bhoonidhi/data/" + sat + "/" + sen + "/" + year + "/" + month + "/" + prdId + ".zip?token=" + token + "&product_id=" + prdId
            urllib.request.urlretrieve(path, os.path.join(output_path,prdId + ".zip"))
            return f'Downloaded the product succesfully at {os.path.join(output_path,prdId + ".zip")}'
        except Exception as e:
            return str(e)
    edited_products = []
    for product in products:
        edited_products.append([product,user_id,password])
    results = ThreadPool(5).imap_unordered(download, edited_products)
    Not_happened = []
    i=0
    for result in results:
        if 'succesfully' in result:
            pass
        else:
            Not_happened.append(products[i]['OTS_OTSPRODUCTID'])
        i+=1
    if Not_happened == []:
        return('Downloaded all the products')
    else:
        return(f'The following products could not download {Not_happened}')
    
def getShapefilesBhoonidhi():
    response = requests.post('https://bhoonidhi.nrsc.gov.in/bhoonidhi/LocLibServlet', json ={'action': "GETSHPNAMES"}, timeout=20)
    shapes =  response.json()
    for shape in shapes:
        print(shape)