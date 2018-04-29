from sqlalchemy import Column, Integer, String,Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_declarative import Complex
import os
import sys
from time import sleep
from optparse import OptionParser

__author__ = 'Malki Aker'

app = Flask(__name__)
app.config["DEBUG"] = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#database definition:
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format( username="mhacker", password="malki1996", hostname="mhacker.mysql.pythonanywhere-services.com", databasename="mhacker$complex_data", )
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

db = SQLAlchemy(app)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def split_string(string, delim, lits_columns):
    l = string.split(delim)
    return [l[c] for c in list_columns]



def update_feature(feature, file_name, data_table):
    data = open(file_name, 'r')
    err = open('update_errors_' + feature + '.txt', 'w+')
    if(feature == 'indentical_complexes'):
        #just to be sure that the feature is added to the correct record, mapping the entry to the new feature
        complex_grouping_dict = {(line.split('\t')[0]).split('_')[0]:(line.split('\t')[-1]) for line in data}
        #adding the feature to the table
        for cmplx in data_table:
            cmplx.indentical_complexes = complex_grouping_dict[cmplx.pdb_entry]
        db.session.commit()
    elif(feature == 'method'):
        #print(data.readline())
        complex_methods_dict = {line.split(',')[0]:[line.split(',')[1], line.split(',')[3], line.split(',')[5]] for line in data}
        for cmplx in data_table:
            cmplx.method_complex = complex_methods_dict[cmplx.pdb_entry][0]
            cmplx.method_prot_A = complex_methods_dict[cmplx.pdb_entry][1]
            cmplx.method_prot_B = complex_methods_dict[cmplx.pdb_entry][2]
        db.session.commit()
    elif(feature == 'chains_in_interface'):
        #print(data.readline())
        complex_chains_dict = {}
        for line in data:
            tmp = line.split(',')
            if('!' not in line):
                complex_chains_dict[tmp[0].split('_')[0]] = [tmp[0].split('_')[1], tmp[1].split(':')[1], tmp[2].split(':')[1]]
            else:
                complex_chains_dict[tmp[0].split('_')[0]] = ['','','']
                err.write(line)
        for cmplx in data_table:
            cmplx.chains_in_interface_complex = complex_chains_dict[cmplx.pdb_entry][0]
            cmplx.chains_in_interface_prot_A = complex_chains_dict[cmplx.pdb_entry][1]
            cmplx.chains_in_interface_prot_B = complex_chains_dict[cmplx.pdb_entry][2]
        db.session.commit()
    elif(feature == 'stochiometry_complex'):
        complex_sto_dict = {line.split('\t')[0]:[line.split('\t')[1], line.split('\t')[3], line.split('\t')[5]] for line in data}
        for cmplx in data_table:
            cmplx.stoichiometry_complex = complex_sto_dict[cmplx.pdb_entry][0]
            cmplx.stoichiometry_prot_A = complex_sto_dict[cmplx.pdb_entry][1]
            cmplx.stoichiometry_prot_B = complex_sto_dict[cmplx.pdb_entry][2]
        db.session.commit()
    elif(feature == 'rmsd'):
        #to complete this task when my laptop will be repaired
        r=0
    elif(feature == 'residues'):
        #todo - shirly's task
        r=0

    err.close()
    data.close()



def update_table(options):
    """update the features in the table"""
    listC=db.session.query(Complex).all()
    if(options.similar_complexes != None):
        update_feature('indentical_complexes', options.similar_complexes, listC)
    if(options.methods != None):
        update_feature('method', options.methods, listC)
    if(options.contact_chains != None):
        update_feature('chains_in_interface', options.contact_chains, listC)
    if(options.stoichio != None):
        update_feature('stochiometry_complex', options.stoichio, listC)
    if(options.rms != None):
        update_feature('rmsd', options.rms, listC)
    if(options.residues != None):
        update_feature('residues', options.residues, listC)
    db.session.commit()

#insert the data from the files to the Data Base
if(__name__ == "__main__"):
    parser = OptionParser()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #  usege:
    # -sim: input complexes grouped by similarities file
    # -met: input detection method file
    # -con: input contact chains file
    # -sto: input stochiometry file
    # -rms: rmsd file
    # -res: residues in interface file
    # example: python sqlalchemy_add_features.py -s additional_features/data_grouping.txt -m additional_features/MethodsdataTabSeparate.csv -c additional_features/RMSDcontact_chains.txt -S additional_features/With_stoichiometrydataTabSeparate_V2.txt
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # -sim: input complexes grouped by similarities file
    parser.add_option("-s", "--sim", type = "string", action="store", dest="similar_complexes", default = None)
    # -met: input detection method file
    parser.add_option("-m", "--met", type = "string", action="store", dest="methods", default = None)
    # -con: input contact chains file
    parser.add_option("-c", "--con", type = "string" , action="store", dest="contact_chains", default = None)
    # -sto: input stochiometry file
    parser.add_option("-S", "--sto", type = "string", action="store", dest="stoichio", default = None)
    # -rms: rmsd file
    parser.add_option("-r", "--rms", type = "string", action="store", dest="rms", default = None)
    # -res: residues in interface file
    parser.add_option("-R", "--res", type = "string", action="store", dest="residues", default = None)
    (options, args) = parser.parse_args(sys.argv)

    update_table(options)
    listC=db.session.query(Complex).all()
    for c in listC:
        print(c.stoichiometry_complex)
        print("\n***")

