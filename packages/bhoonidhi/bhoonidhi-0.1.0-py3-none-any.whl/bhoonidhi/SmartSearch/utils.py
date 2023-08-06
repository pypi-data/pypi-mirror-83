# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 14:34:43 2020
@author: Rohit Gandikota
"""
import re 
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
import datetime
from dateparser.search import search_dates
#from geotext import GeoText
from quantulum3 import parser
from word2number import w2n
#import speech_recognition as sr
# from jellyfish import soundex
from .bhoonidhi_helper import getGeoLocationBhoonidhi, getBhoonidhiSatSen
# Configuration variables
TAGS_JSON = ['radius', 'buffer', 'swath', 'resolution', 'lat', 'latitude', 'lon','longitude', 'cloud','area','swath','spread']
SATS_AVAIL = ['c3','c2e','l8', 'rs2','r1a','r1b','r2a','r2b','cartosat3', 'cartosat2s', 'cartosat2e', 'resourcesat2', 'risat1b', 'risat1a', 'risat2b', 'landsat8', 'sentinel2A', 'sentinel1A', 'sentinel2B', 'sentinel1B','oceansat2' ]
SENS_AVAIL = ['pan', 'mx', 'l3', 'oli','msi','sar','ocm']
SATS_STRONG = ['resourcesat', 'risat', 'risat', 'risat', 'landsat', 'sentinel','oceansat']
SATS_WEAK = ['l8','sentinel','oceansat']
SENS_STRONG = [ 'oli','msi','sar','ocm','tirs','optical','sar','microwave','liss']
# Functions
def findCities(user_text,text_based,bhoonidhi=True):
    if bhoonidhi:
        location = getGeoLocationBhoonidhi(user_text)
    else:
        location = ['Hyderabad']
#        if text_based:
#            user_tokens = word_tokenize(user_text.lower())
#            
#            lemmatizer = WordNetLemmatizer() 
#            #    pst = PorterStemmer()
#            for i in range(len(user_tokens)):
#                user_tokens[i] = lemmatizer.lemmatize(user_tokens[i])
#            
#            user_pos = nltk.pos_tag(user_tokens)
#            
#            user_text_new=''
#            for word in user_pos:
#                if 'NN' in word[-1] :
#                    user_text_new += f'{word[0][0].upper()}{word[0][1:]}, '
#                else:
#                    user_text_new += f'{word[0].lower()} '
#        else:
#            user_text_new = user_text
#        places = GeoText(user_text_new)
#        cities = places.cities
#        if 'March' in cities:
#            cities= list(cities)
#            cities.remove('March')
#        cities = np.unique(cities)
#        
#        location = (list(cities))
    return location

    
def findDates(user_text,feature_count):
    user_text_new = user_text
    def hasNumbers(inputString):
        return bool(re.search(r'\d', inputString))
    if '%' in user_text:
        user_text = user_text.replace('%','')
    if re.search(r'\s+m\s+', user_text):
        user_text = user_text.replace(re.search(r'\s+m\s+', user_text).group(),'mts')
    if re.search(r'\s+km\w\s+', user_text):
        user_text = user_text.replace(re.search(r'\s+km\s+', user_text).group(),'km ')
    if re.search(r'\s+mt\w\s+', user_text):
        user_text = user_text.replace(re.search(r'\s+km\s+', user_text).group(),'mts ')
    if re.search(r'\s+km\w\s+', user_text):
        user_text = user_text.replace(re.search(r'\s+km\s+', user_text).group(),'km ')
    if re.search(r'[0-9]+m\s+', user_text):
        user_text = user_text.replace(re.search(r'[0-9]*m', user_text).group(),re.search(r'[0-9]*m', user_text).group()+'ts')
    user_text= user_text.replace(' meter ','meter ')
    user_text= user_text.replace(' meters ','meters ')
    user_text= user_text.replace(' kilometer ','kilometers ')
    user_text= user_text.replace('Lat ','Lattitude ')
    user_text= user_text.replace('lat ','lattitude ')
    user_text= user_text.replace('Lon ','Longitude ')
    user_text= user_text.replace('lon ','longitude ')
    user_text= user_text.replace(' abu ',' ')
    
    
    
    dates = search_dates(user_text)
    if dates != None:
        dates = np.array(dates)
        for date in dates:
            if date[0].isdigit():
                user_text = user_text.replace(date[0],'')
            if (int(date[1].strftime('%y-%m-%d').split('-')[-1]) == int(datetime.datetime.today().strftime('%y-%m-%d').split('-')[-1]) and date[1].strftime('%y-%m-%d').split('-')[-1] not in user_text) and ((date[0] not in ['today', 'yesterday','tomorrow']) and ('month' not in date[0] and 'week' not in date[0] and 'day' not in date[0]) and ((date[1].strftime('%B').lower() in date[0] or date[0] in date[1].strftime('%B').lower()))):
                user_text = user_text.replace(date[0],'')
                d = date[1].strftime(' %B, %Y')
                user_text = '01'+d+ ' to '+'30'+d +' date range '+ user_text
        dates = search_dates(user_text)
#        print(dates)
        if dates != None:
            dates = np.array(dates)
            for date in dates:
                user_text_new = user_text_new.replace(date[0],'')
            dates = np.unique(dates[:,-1])
            dates = list(dates)
            if 'today' in user_text.lower():
                dates.append(datetime.datetime.now())
            if 'yesterday' in user_text.lower():
                dates.append(datetime.datetime.now() - datetime.timedelta(days=1))
            if 'tomorrow' in user_text.lower():
                dates.append(datetime.datetime.now() + datetime.timedelta(days=1))
            
                
            dates = np.unique(dates)
            
            if len(dates) > 1:
                init_date = dates.min()
                final_date = dates.max()
                feature_count+=2
            elif len(dates) == 1:
                init_date = dates[0]
                final_date = dates[0]
                feature_count+=1
            else:
                init_date = (datetime.datetime.now() - datetime.timedelta(days=10))
                final_date =(datetime.datetime.now())
        else:
            init_date = (datetime.datetime.now() - datetime.timedelta(days=10))
            final_date = (datetime.datetime.now()) 
    elif 'recent' in user_text.lower() or 'latest' in user_text.lower():
        init_date = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%d %B, %Y")
        final_date = (datetime.datetime.now()).strftime("%d %B, %Y")
        feature_count += 2
        return init_date, final_date, feature_count
    else:
        init_date = (datetime.datetime.now() - datetime.timedelta(days=10))
        final_date = (datetime.datetime.now())
    if (final_date-init_date).days > 90:
        init_date = (final_date - datetime.timedelta(days=90))
    init_date = init_date.strftime("%d %B, %Y")
    final_date = final_date.strftime("%d %B, %Y")          
    return init_date, final_date, user_text_new, feature_count
def preprocess(user_text):
    # symbology to symnatic
    user_text = user_text.lower()
    user_text = user_text.replace('<',' less than ')
    user_text = user_text.replace('>',' greater than ')
    user_text = user_text.replace('!', 'not')
    user_text = user_text.replace('=', ' ')
    user_text = user_text.replace('-', '')
    user_text_new = ''
    words = user_text.split(' ')
    for word in words:
        try:
            user_text_new+=str(w2n.word_to_num(word))+' '
        except:
            user_text_new += word+' '
       
    user_text  = user_text_new[:-1]
    
    if len(user_text.strip())== 0:
        return 'Ping pong'
    
    if ' me ' in user_text:
        user_text = user_text.replace(' me ', ' ')
    if 'morethan' or 'more than' in user_text:
        user_text = user_text.replace('more', 'greater')
    if ' no ' in user_text:
        user_text = user_text.replace(' no ', ' 0 % ')
    if ' m ' in user_text:
        user_text = user_text.replace(' m ', ' meters ')
    if re.search(r'\[*\s*\d+.*\s*,\s*\d+.*\s*\]*',  user_text) :
        if re.search(r'location',  user_text) or re.search(r'lat\w*\s*lon\w*',  user_text):
            a = re.search(r'\[*\s*\d+.*\s*,\s*\d+.*\s*\]*',  user_text).group()
            nums = re.findall('\d+\.*\d*',a)
            user_text = user_text.replace(a,f'lat {nums[0]} and lon {nums[1]}')
   
    if re.search(r'from\s*\w*\s*\wast',  user_text):
        user_text = user_text.replace(re.search(r'from\s*\w*\s*\wast',  user_text).group(), 'till today '+re.search(r'from\s*\w*\s*\wast',  user_text).group() )
    
    if re.search(r'since\s*\w*\s*\wast',  user_text):
        user_text = user_text.replace(re.search(r'since\s*\w*\s*\wast',  user_text).group(),'till today '+re.search(r'since\s*\w*\s*\wast',  user_text).group() )
        
    if re.search(r'\wast\s*month',  user_text):
        user_text = user_text.replace(re.search(r'\wast\s*month',  user_text).group(),re.search(r'\wast\s*month',user_text).group()[:-5]+' 1 month') 
    
    if re.search(r'\wast\s*week',  user_text):
        user_text = user_text.replace(re.search(r'\wast\s*week',  user_text).group(), re.search(r'\wast\s*week',  user_text).group()[:-4]+' 1 week' )
      
    if re.search(r'\wast\s*day',  user_text):
        user_text = user_text.replace(re.search(r'\wast\s*day',  user_text).group(), re.search(r'\wast\s*day',  user_text).group()[:-3]+' 1 day')
    if re.search(r'for\s*\w*\s*\wast',  user_text):
        user_text = user_text.replace(re.search(r'for\s*\w*\s*\wast',  user_text).group(), 'till today '+re.search(r'for\s*\w*\s*\wast',  user_text).group() )
    if re.search(r'month',user_text) or re.search(r'week',user_text) or re.search(r'days',user_text):
        if not re.search('ago',user_text) and not re.search('today',user_text) and not re.search('till',user_text):
            user_text = user_text+' till today'
            
   
#    if re.search(r'from',  user_text):
#        if re.search(r'from\s*\w*\s*\w*\s*\w*\s*to',  user_text) or  re.search(r'from\s*\w*\s*\w*\s*\w*\s*until',  user_text) or  re.search(r'from\s*\w*\s*\w*\s*\w*\s*till',  user_text):
#            pass
#        else:
#            user_text = user_text.replace(re.search(r'from',  user_text).group(), 'till today from')
#    if re.search(r'since',  user_text):
#        if re.search(r'since\s*\w*\s*\w*\s*\w*\s*to',  user_text) or  re.search(r'since\s*\w*\s*\w*\s*\w*\s*until',  user_text) or  re.search(r'since\s*\w*\s*\w*\s*\w*\s*till',  user_text):
#            pass
#        else:
#            user_text = user_text.replace(re.search(r'since',  user_text).group(),'till today since')
        
    
    if re.search(r'cloud\s*percent\w*',  user_text):
        user_text = user_text.replace(re.search(r'cloud\s*percent\w*',  user_text).group(), 'cloud')
    elif re.search(r'cloud\s*cover\w*',  user_text):
        user_text = user_text.replace( re.search(r'cloud\s*cover\w*',  user_text).group(), 'cloud')
    elif re.search(r'cloud\s*spread\w*',  user_text):
        user_text = user_text.replace(re.search(r'cloud\s*spread\w*',  user_text).group(), 'cloud')
    elif re.search(r'cloud\s*thres\w*',  user_text):
        user_text = user_text.replace(re.search(r'cloud\s*thres\w*',  user_text).group(), 'cloud')
    else:
        pass
    return user_text.lower()
def findParameters(user_pos):
    user_pos = np.array(user_pos)
    params = []
    length = len(user_pos)
    for i in range(len(user_pos)):
        if user_pos[i][-1] == 'CD':
#            print('Entered CD condition' + user_pos[i][0])
            skip = False
            tags = []
            if i > 1:
                if user_pos[i-2][-1] in ['NN', 'VBP','VBD', 'NNS','JJ']:     
                    
                    if  user_pos[i-1][0] in ['le', 'lessthan', 'finer', 'fine','less', 'lesser', 'better']:
                        user_pos[i][0] = '-'+user_pos[i][0]
                        tags.append(user_pos[i-2][0])
                        skip = True
                        
                    elif user_pos[i-1][0] in ['great', 'greatthan', 'greater', 'coarse','coarser','more','worse']:
                        user_pos[i][0] = '+'+user_pos[i][0]
                        tags.append(user_pos[i-2][0])
                        skip = True
                    else:
                        tags.append(user_pos[i-2][0])
                
            if i > 0 and not skip:
                if user_pos[i-1][-1] in ['NN', 'VBP','VBD', 'NNS','JJ']:
                    tags.append(user_pos[i-1][0])    
            
            ######################## Finding tags and values by parsing through user_pos ###########        
            gotUnits = 0
        
            if i<length-1:
                 
                if user_pos[i+1][-1] in ['NN', 'VBP','VBD', 'NNS','JJ'] and len(parser.parse(user_pos[i][0]+' '+user_pos[i+1][0]))>0:
                    if parser.parse(user_pos[i][0]+' '+user_pos[i+1][0])[0].surface ==  user_pos[i][0]+' '+user_pos[i+1][0]:
                        tags.append(user_pos[i][0]+user_pos[i+1][0])
                    else:
                        tags.append(user_pos[i][0])
                        if user_pos[i+1][-1] in ['NN', 'VBP','VBD', 'NNS','JJ']:
                            tags.append(user_pos[i+1][0])
                    gotUnits = 1
                
            if i>0 and gotUnits == 0:
                if user_pos[i-1][-1]in ['NN', 'VBP','VBD', 'NNS','JJ'] and len(parser.parse(user_pos[i][0]+' '+user_pos[i-1][0]))>0:
                    if parser.parse(user_pos[i][0]+' '+user_pos[i-1][0])[0].surface ==  user_pos[i][0]+' '+user_pos[i-1][0]:
                        tags.append(user_pos[i][0]+user_pos[i-1][0])
                    else:
                        tags.append(user_pos[i][0])
                    gotUnits = 1 
            if len(parser.parse(user_pos[i][0]))>0 and gotUnits == 0:
                tags.append(user_pos[i][0])
                gotUnits = 1
            if gotUnits == 0:
#                print('Got Nothing')
                continue            
            if i<length-2:
                if user_pos[i+2][-1] in ['NN', 'VBP','VBD', 'NNS','JJ']:
                    tags.append(user_pos[i+2][0])
          
            if len(tags)>1:
                params.append(tags)
    ############## Filtering all the extracted parameters
    filtered = []
    length = len(params)
    for i in range(length):
        if i == 0 :
            for j in range(len(params[i])):
                if len(parser.parse(params[i][j]))==0:
                   if params[i][j].lower() in TAGS_JSON:
                       if j < len(params[i])-1:
                            if len(parser.parse(params[i][j+1]))==1:
                                filtered.append([params[i][j+1],params[i][j]])
                                break
                        
                else:
                    if j < len(params[i])-1:
                        if params[i][j+1].lower() in TAGS_JSON:
                            if params[i][j+1] == 'cloudThresh':
                                filtered.append([(re.search(r'\d+', params[i][j]).group()),params[i][j+1]])
                            else:
                                filtered.append([params[i][j],params[i][j+1]])
                        
                            break
    
                    
        else:
            over_write = True
            for j in range(len(params[i])):
                if len(parser.parse(params[i][j]))==0:
                    if len(filtered)>0:
                        if params[i][j] in np.array(filtered)[:,-1]:
                            pass
                        else:
                            if params[i][j].lower() in TAGS_JSON:
                                if over_write:
                                    unit = params[i][j]
                                    over_write = False
                    else:
                        if params[i][j].lower() in TAGS_JSON:
                            if over_write:
                                unit = params[i][j]
                                over_write = False
                        
                else:  
                    val =  params[i][j]
            try:
                if unit == 'cloud':
                    filtered.append([(re.search(r'\d+', val).group()),unit])
                else:
                    filtered.append([val,unit])  
                del(unit,val)
            except:
                pass
    return filtered
def getTokensPOS(user_text):
    user_tokens = word_tokenize(user_text)
    
    lemmatizer = WordNetLemmatizer() 
    #    pst = PorterStemmer()
    for i in range(len(user_tokens)):
        user_tokens[i] = lemmatizer.lemmatize(user_tokens[i])
    a = set(stopwords.words('english'))
    filtered = [x for x in user_tokens if x not in a]
    user_tokens =  filtered 
    for i in range(len(user_tokens)):
        if user_tokens[i]=='le':
            user_tokens[i]='less'
    user_pos = nltk.pos_tag(user_tokens)
    return user_pos, user_tokens
def findSatSen(user_text, user_pos, feature_count):
    def user_pos_pop(user_pos,sat):
        user_pos_new = []
        for i in range(len(user_pos)):
            if user_pos[i][0] not in sat.lower():
                user_pos_new.append(user_pos[i])
        return user_pos_new
    user_text = re.sub(' ','',user_text)
    
    user_sat = []
    user_sen = []
    
    user_sat_guess = []
    user_sen_guess = []
    
    for sat in SATS_AVAIL:
        if re.search(sat.lower(),user_text):
            user_sat.append(sat)
            user_text = user_text.replace(sat.lower(),'')
            
            user_pos = user_pos_pop(user_pos,sat)      
            feature_count+=1
    for sat in SATS_STRONG:
        if re.search(sat.lower(),user_text) and (sat not in user_sat_guess or sat not in user_sat):
            user_sat_guess.append(sat)
            user_text = user_text.replace(sat.lower(),'')
            user_pos = user_pos_pop(user_pos,sat)  
    for sat in SATS_WEAK:
        if re.search(sat.lower(),user_text) and sat not in user_sat:
            user_sat_guess.append(sat)
            user_text = user_text.replace(sat.lower(),'')
            user_pos = user_pos_pop(user_pos,sat)  
    for sen in SENS_AVAIL:
        if re.search(sen.lower(),user_text):
            user_sen.append(sen)
            user_text = user_text.replace(sen.lower(),'')
            user_pos = user_pos_pop(user_pos,sat)  
            feature_count+=1
    for sen in SENS_STRONG:
        if re.search(sen.lower(),user_text) and sen not in user_sen:
            user_sen_guess.append(sen)
            user_text = user_text.replace(sen.lower(),'')
            user_pos = user_pos_pop(user_pos,sat)  
            
    if user_sat == []:
        user_sat = user_sat_guess
        feature_count+=len(user_sat)
        
    else:
        if user_sat_guess != []:
            for sat in user_sat_guess:
                for user_s in user_sat:
                    if sat not in user_s:
                        b = 0
                    else:
                        b = 1 
                        break
                if b == 0:
                    user_sat.append(sat)
                    feature_count+=1
                
    if user_sen == []:
        user_sen = user_sen_guess
        feature_count+=len(user_sen)
    else:
        if user_sen_guess!=[]:
            for sen in user_sen_guess:
                for user_s in user_sen:
                    if sen not in user_s:
                        a = 0
                    else:
                        a = 1 
                        break
            if a == 0:
                user_sen.append(sen)
                feature_count+=1
    output = getBhoonidhiSatSen(user_sat, user_sen)
    return output, user_pos, feature_count