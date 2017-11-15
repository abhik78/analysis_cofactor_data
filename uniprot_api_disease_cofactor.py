#! /usr/bin/env python

import requests
import json
import re
import csv


import requests, sys

uniprotid_list = []




def return_response(uniprotid):
    r = requests.get("https://www.ebi.ac.uk/proteins/api/proteins/%s.json" % uniprotid)
    if r.status_code == 200:
        uniprot_json_values = r.json()
        return uniprot_json_values
    return None

result_list = []


with open(sys.argv[1]) as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        uniprotid = row['uniprotid']
        uniprotid_list.append(uniprotid)

    for unpid in uniprotid_list:
        json_values1 = return_response(unpid)
        cofactor = ""
        disease = ""
        try:
            
        
            for row1 in json_values1['comments']:
                
                if row1['type'] =='DISEASE':
                    disease += ' '+row1['diseaseId']
                    #disease = 'yes'
                    
                    
                    #print(row1['diseaseId'])
                        
                if row1['type'] == 'COFACTOR':
                    #print(row1['cofactors'][0]['name'])
                    cofactor += ' '+row1['cofactors'][0]['name']
        
        
                        
                    
        except:
            pass

        result_list.append({'uniprot': unpid, 'disease_list': disease, 'cofactors': cofactor})
        #print(result_list)
        print disease
        print cofactor

if result_list:
    with open('unpid_information_result.csv', 'w+') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, result_list[0].keys())
        w.writeheader()
        for row2 in result_list:
            w.writerow(row2)
else:
    print('no results')
