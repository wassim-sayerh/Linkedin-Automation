#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 23:03:40 2020

@author: wassim
"""



def selectCV(languageFileCode, country):
    
    if country.lower() == 'france':
        countryFolder = "France"
    else:
        countryFolder = "Other"
        
    return "/Users/wassim/OneDrive - IE Students/Applications/- CV Stack Source Standard/" + countryFolder + "/CV - Wassim Sayerh - " + languageFileCode + ".pdf"