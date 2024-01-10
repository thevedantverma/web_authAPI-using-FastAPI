# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 03:36:42 2024

@author: theve
"""

import uvicorn
from fastapi import FastAPI
import numpy as np
import pickle
import pandas as pd

from pydantic import BaseModel

class url(BaseModel):
    url: str
    
app = FastAPI()
pickle_in = open("classifier.pkl","rb")
classifier = pickle.load(pickle_in)

#test api1
@app.get('/')
def index():
    return{'message': 'Hello ALL HOW ARE YOU?'}

#test api 2
@app.get('/{name}')
def get_name(name:str):
    return{'message': f'hello, {name}'}


# main api of ml model
@app.post('/predict')
def predict_url(data:url):
    data= data.dict()
    type_url= data['url']
    prediction = classifier.predict([[type_url]])
    if((prediction[0]) == 0):
        prediction = "SAFE"
    elif((prediction[0]) == 1.0):
        prediction = "DEFACEMENT"
    elif((prediction[0]) == 2.0):
        prediction = "PHISHING"
    elif((prediction[0]) == 3.0):
        prediction = "MALWARE"
    return {
        'prediction': prediction}

#running API with UVICORN
#will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
#for making it run type
##uvicorn app:app --reload##
#in the cmd
    
    
    