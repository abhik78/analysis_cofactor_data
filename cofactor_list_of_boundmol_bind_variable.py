#! /usr/bin/env python

import requests
import json
import re
import csv
import sys

import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
#other logging levels are ERROR, INFO, DEBUG
#logger.setLevel(logging.DEBUG)

from sqlalchemy import create_engine
# Database connection details
db_user = '#######'
db_pass = '########'
db_sid  = '#########'

engine = create_engine('oracle://'+db_user+':'+db_pass+'@'+db_sid)
connection = engine.connect()
unp_list = []
idlist = []
c = csv.writer(open("cofactor_list_of_boundmol_output_28-06-2017.csv","wb"))

with open(sys.argv[1]) as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        hetcode = row['hetcode']
        
        sql1 ="""select a.pdb_id, a.boundmolecule_id , a.seqnum as residue_num, a.code as compound_id
                from motif_ligand a
                where a.struct_asym = a.struct_asym_orig
                    and a.code=:code""" 
        db_query1 = connection.execute(sql1, (hetcode))
        if db_query1:
            for x in db_query1:
                
                print x
                c.writerow(x)
