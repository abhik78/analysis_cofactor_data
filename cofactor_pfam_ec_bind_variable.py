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
db_user = ''
db_pass = ''
db_sid  = ''

engine = create_engine('oracle://'+db_user+':'+db_pass+'@'+db_sid)
connection = engine.connect()
unp_list = []
idlist = []
c = csv.writer(open("cofactor_pfam_ec_out_28-06-17.csv","wb"))
with open(sys.argv[1]) as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        pdbid = row['pdbid']
        bm = row['bm']
        resid = row['resid']
        hetcode = row['hetcode']
        
        
        sql1 = """select distinct  q.pdb_id, ec.ec, ec.accession, ebm.name, es.organism_scientific, p.pfam_accession, p.clan_name as pfam_clan_name, p.description as pfam_description, :hetcode
                    from ( select distinct a.pdb_id, n.code, n.entity_id, n.struct_asym_orig, n.residue_id
                        from motif_bond a,  motif_atom_plane_ring n, residue r,
                                (select distinct b.id
                                      from motif_ligand a, motif_atom_plane_ring b
                                      where a.pdb_id = b.pdb_id and a.seqnum = b.residue_id and a.struct_asym = b.struct_asym and a.pdb_id = :pdb_id
                                           and boundmolecule_id = :boundmolecule_id and b.residue_id = :residue_id) e
                        where a.type != 'undefined' and a.atom1 =e.id and n.pdb_id = a.pdb_id and a.atom2 = n.id and n.pdb_id = r.entry_id
                                  and n.struct_asym = r.struct_asym_id and n.residue_id = r.id and n.code = r.chem_comp_id and a.pdb_id = :pdb_id
                              ) q, entity_pfam s, pfam_clan_data p, pdb_ec ec, entity_best_name ebm, entity_src es
                    where q.pdb_id = s.entry_id and q.entity_id = s.entity_id and  s.accession = p.pfam_accession
                    and q.residue_id between s."START" and s."END"
                    and q.pdb_id = ec.entry_id and q.entity_id = ec.entity_id
                    and q.pdb_id = ebm.entry_id and q.entity_id = ebm.entity_id
                    and q.pdb_id = es.entry_id and q.entity_id = es.entity_id""" 
        
        #print sql1
        db_query1 = connection.execute(sql1, (hetcode, pdbid, bm, resid, pdbid))
        
        if db_query1:
            for x in db_query1:
                
                c.writerow(x)
                logging.error(x)


connection.close()
