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
def split_string(string, delim, lists_columns):
    """
    split_string-
    split string and extract only the requested elements
    input:
        string - the original string
        delim - some delim which separate the string into parts
        list_columns - the wanted columns from the string
    output:
        list of elements
    """
    #split the string
    l = string.split(delim)
    #choose the specific elements
    return [l[c] for c in lists_columns]

def not_is_number(s):
    """
    not_is_number-
    input:
        s - some object
    output:
        if the object is number return true
        otherwise, return false
    """
    try:
        float(s)
        return False
    except ValueError:
        return True


def update_feature(feature, file_name, data_table):
    """
    update_feature-
    input:
        feature - string, indicate which feature to update this time
        file_name - the file where the new values are
        data_table - pointer to the oldest dataset
    output:
        void
    """
    data = open(file_name, 'r')
    err = open('update_errors_' + feature + '.txt', 'w+')

    #check feature, then update the specific feature:
    #------------------------------------------------------------------
    # if the feature to update is identical complexes (complexes that are like the complex in the database) then do:
    if(feature == 'indentical_complexes'):
        #just to be sure that the feature is added to the correct record, mapping the entry to the new feature
        complex_grouping_dict = {(line.strip().split('\t')[0]).split('_')[0]:(line.strip('\n').strip().split('\t')[-1]) for line in data if(not_is_number(line.strip().split('\t')[-1]))}
        #adding the feature to the table
        for cmplx in data_table:
            if(cmplx.pdb_entry in complex_grouping_dict):
                cmplx.indentical_complexes = complex_grouping_dict[cmplx.pdb_entry]
            else:
                err.write(cmplx.pdb_entry + '\t')
        db.session.commit()
    #------------------------------------------------------------------
    # if the feature to update is method (update the method are used to detect the complex) then do:
    elif(feature == 'method'):
        #just to be sure that the feature is added to the correct record, mapping the entry to the new feature
        complex_methods_dict = {line.strip().split(',')[0]:[line.split(',')[1], line.strip().split(',')[3], line.split(',')[5]] for line in data}
        #adding the feature to the table
        for cmplx in data_table:
            cmplx.method_complex = complex_methods_dict[cmplx.pdb_entry][0].strip()
            cmplx.method_prot_A = complex_methods_dict[cmplx.pdb_entry][1].strip()
            cmplx.method_prot_B = complex_methods_dict[cmplx.pdb_entry][2].strip()
        db.session.commit()
    #------------------------------------------------------------------
    # if the feature to update is chains in interface (chains that are in the interface area for both, the complex and the subunits) then do:
    elif(feature == 'chains_in_interface'):
        #just to be sure that the feature is added to the correct record, mapping the entry to the new feature
        complex_chains_dict = {}
        for line in data:
            tmp = line.strip().split(',')
            if('!' not in line):
                complex_chains_dict[tmp[0].strip('\n').split('_')[0]] = [tmp[0].strip('\n').split('_')[1], tmp[1].strip('\n').split(':')[1], tmp[2].strip('\n').split(':')[1]]
            else:
                complex_chains_dict[tmp[0].split('_')[0]] = ['','','']
                err.write(line)
        #adding the feature to the table
        for cmplx in data_table:
            if (cmplx.pdb_entry in complex_chains_dict):
                cmplx.chains_in_interface_complex = complex_chains_dict[cmplx.pdb_entry][0].strip('\n')
                cmplx.chains_in_interface_prot_A = complex_chains_dict[cmplx.pdb_entry][1].strip('\n')
                cmplx.chains_in_interface_prot_B = complex_chains_dict[cmplx.pdb_entry][2].strip('\n')
            else:
                err.write(cmplx.pdb_entry + '\t')
        db.session.commit()
    #------------------------------------------------------------------
    # if the feature to update is stoichiometry (the stoichiometry of the complex and the subunits) then do:
    elif(feature == 'stochiometry_complex'):
        #just to be sure that the feature is added to the correct record, mapping the entry to the new feature
        complex_sto_dict = {line.split('\t')[0]:[line.split('\t')[1], line.split('\t')[3], line.split('\t')[5]] for line in data}
        #adding the feature to the table
        for cmplx in data_table:
            if (cmplx.pdb_entry in complex_sto_dict):
                cmplx.stoichiometry_complex = complex_sto_dict[cmplx.pdb_entry][0].strip()
                cmplx.stoichiometry_prot_A = complex_sto_dict[cmplx.pdb_entry][1].strip()
                cmplx.stoichiometry_prot_B = complex_sto_dict[cmplx.pdb_entry][2].strip()
            else:
                err.write(cmplx.pdb_entry + '\t')
        db.session.commit()
    #------------------------------------------------------------------
    # if the feature to update is rmsd (computed rmsd for the chains in the interface) then do:
    elif(feature == 'rmsd'):
        #to complete this task when my laptop will be repaired
        complex_rmsd_dict = {}
        #just to be sure that the feature is added to the correct record, mapping the entry to the new feature
        for line in data:
            details = line.strip().split(',')
            rms1 = details[1].split(':') + ['-']
            rms2 = details[2].split(':') + ['-']
            complex_rmsd_dict[details[0].split('_')[0]] = [rms1[2], rms2[2]]
        #adding the feature to the table
        for cmplx in data_table:
            if (cmplx.pdb_entry in complex_rmsd_dict):
                cmplx.rmsd_prot_A = complex_rmsd_dict[cmplx.pdb_entry][0].strip('\n')
                cmplx.rmsd_prot_B = complex_rmsd_dict[cmplx.pdb_entry][1].strip('\n')
            else:
                err.write(cmplx.pdb_entry + '\t')
        db.session.commit()
    #------------------------------------------------------------------
    # if the feature to update is residues (number of residues that are in the interface area) then do:
    elif(feature == 'residues'):
        complex_res_dict = {}
        data.readline()
        #just to be sure that the feature is added to the correct record, mapping the entry to the new feature
        for line in data:
            details = line.strip().split('\t')
            residues = details[4]# should be 3 but there is double tab
            complex_res_dict[details[0].split('_')[0]] = residues
        #adding the feature to the table
        for cmplx in data_table:
            if(cmplx.pdb_entry in complex_res_dict):
                cmplx.num_interface_residues_complex = complex_res_dict[cmplx.pdb_entry].strip('\n')
            else:
                err.write(cmplx.pdb_entry + '\t')
        db.session.commit()

    err.close()
    data.close()



def update_table(options):
    """
    update_table-
    update the features in the table
    input:
        - options- list of features to update (file names)
    output:
        void
    """
    # fetch the old table from the server
    listC=db.session.query(Complex).all()
    #check which features to update:
    if(options.similar_complexes != None):
        print("update identical complexes...")
        update_feature('indentical_complexes', options.similar_complexes, listC)
    if(options.methods != None):
        print("update methods...")
        update_feature('method', options.methods, listC)
    if(options.contact_chains != None):
        print("update contact chains...")
        update_feature('chains_in_interface', options.contact_chains, listC)
    if(options.stoichio != None):
        print("update stoichiometry...")
        update_feature('stochiometry_complex', options.stoichio, listC)
    if(options.rms != None):
        print("update rmsd...")
        update_feature('rmsd', options.rms, listC)
    if(options.residues != None):
        print("update residues...")
        update_feature('residues', options.residues, listC)
    # commit changes
    db.session.commit()
    # update antibodies, its from the older script, just in case
    antibodies=['1G7M','1QFU','1QFW','1R3I','1R3J','1R3K','1R3L','1RZJ','1RZK','1S78','1TET','1TPX','1TQB','1TQC','1TZH','1TZI','1UA6','1UAC','1UJ3','1VFB','1MHP','1MLC','1N8Z','1NAK','1NBY','1NBZ','1NCA','1NCB','1NCC','1NCD','1NDG','1NDM','1NL0','1NMA','1NMB','1NMC','1NSN','1OAK','1OAZ','1OB1','1OSP','1P2C','1PG7','1PKQ','1Q1J','2BDN','2BOB','2BOC','2CMR','2DD8','2DQC','2DQD','2DQE','2DQF','2DQG','2DQH','2DQI','2DQJ','2DWD','2DWE','2EIZ','2EKS','2FD6','2FJG','2FJH','1WEJ','1XCQ','1XCT','1XF5','1XGP','1XGQ','1XGR','1XGT','1XGU','1YQV','1Z3G','1ZTX','1ZWI','2ADF','2AEP','2AEQ','2ATK','2B0S','2B1A','2B2X','2B4C','1YYL','1YYM','2I5Y','2I60','3VE0','4HG4','4FFY','4R4N','4FQR','2Q8A','2Q8B','2QAD','2QQK','2QQL','2QQN','2QR0','2R0K','2R0L','2R4R','2R4S','2R56','2R9H','2UZI','2VC2','2VDK','2VDL','2VDM','2VH5','2VIR','2VIS','2VIT','2VWE','2VXQ','2VXS','2VXT','2W0F','2W9E','2WUB','2H8P','2HFE','2HFG','2HG5','2HJF','2HLF','2HVJ','2HVK','2I9L','2IFF','2IGF','2IH1','2IH3','2ITC','2ITD','2J4W','2J5L','2J6E','2J88','2JEL','2JIX','2JK5','2NR6','2NXY','2NXZ','2NY0','2NY1','2NY2','2NY3','2NY4','2NY5','2NY6','2NY7','2NYY','2NZ9','2OZ4','2P7T','2XRA','2YBR','2YC1','2YPV','2YSS','2ZJS','3A67','3A6B','3A6C','3BAE','3BDY','3BE1','3BGF','3BKJ','3BN9','3BQU','3BSZ','3LQA','3LZF','3MA9','3MAC','3MJ9','3MLT','3MLW','3MLX','3MNZ','3MXW','3N85','3NCY','3NGB','3NH7','3NID','3NIF','3NIG','3NPS','3O0R','3O2D','3O41','3O45','3OGC','3OPZ','3OR6','3OR7','3P11','3P30','3PGF','3PJS','3PNW','3Q1S','3Q3G','3GI8','3GI9','3H0T','3H42','3HB3','3HFM','3HI1','3HI6','3HMX','3HPL','3I50','3IDX','3IDY','3IFN','3IGA','3IXT','3JWD','3JWO','3K2U','3KJ4','3KJ6','3KR3','3L5W','3L5X','3L95','3LD8','3LDB','3LEV','3LIZ','3V4P','3V4V','3V6Z','3V7A','3VG9','3VGA','3VI3','3W2D','3W9E','3WFB','3WFC','3WFD','3WFE','3WIH','3WLW','3WSQ','3ZTJ','3ZTN','4AEI','4AL8','4ALA','4AM0','3QA3','3R1G','3RAJ','3RKD','3RU8','3RVV','3RVW','3RVX','3SDY','3SE8','3SE9','3SKJ','3SO3','3SOB','3SQO','3STL','3STZ','3T2N','3T3M','3T3P','3TT1','3TT3','3TYG','3U2S','3U30','3U4E','3U7Y','3U9U','3UAJ','3UBX','3UJI','4G6F','4G6J','4G6M','4G7Y','4G80','4GMS','4GXU','4H8W','4HC1','4HCR','4HF5','4HFU','4HIX','4I18','4I77','4I9W','4JB9','4JDT','4JKP','4JO1','4JPV','4JPW','4D9Q','4D9R','4DGI','4DKE','4DKF','4DN4','4DQO','4DTG','4DVR','4DW2','4ENE','4ETQ','4FFV','4FFW','4FFZ','4FP8','4FQI','4FQK','4FQV','4FQY','4PP2','4PY8','4QCI','4QEX','4QNP','4QTI','4R0L','4R4F','4R4H','4R8W','4RFN','4RRP','4RWY','4S1Q','4S1R','4S1S','4U6H','4UBD','4UT6','4UT9','4UTA','4UTB','4UUJ','4L5F','4LSP','4LSQ','4LSR','4LST','4LSU','4LSV','4MHH','4MHJ','4MSW','4NM8','4OGX','4OGY','4OII','4OLU','4OLV','4OLW','4OLX','4OLY','4OLZ','4OM0','4OM1','4ONG','4ORZ','5D93','5D96','5DHV','5DUR','5E1A','5E8D','5EBL','5EBM','5EBW','5EC1','5EC2','5F3B','5F3H','5F6J','5F96','5F9W','5FB8','4WFE','4WFF','4WFG','4WFH','4XAK','4XMP','4XNY','4XNZ','4XZU','4YBL','4YC2','4YDJ','4YDK','4YDL','4YE4','4YWG','4Z5R','4ZSO','5T29','5T5B','5T5F','5T6L','5T80','5T85','5TFW','5TIH','5V2A','5VCO','5FHX','5GJS','5GJT','5GZN','5GZO','5HDB','5HJ3','5JHL','5KAQ','5KN5','5KVD','5KVE','5KVF','5KVG','5LBS','5LCV','1A14','1A2Y','1ACY','1ADQ','1AFV','1AHW','1AI1','1AR1','1BGX','1BJ1','1BQL','1BVK','1C08','1CIC','1CZ8','1DEE','1DQJ','1DVF','1E6J','1EGJ','1EO8','1F58','1FBI','1FDL','1FE8','1FJ1','1FNS','1FSK','1G7H','1G7I','1G7J','1G7L','1G9M','1G9N','1GC1','1GGI','1H0D','1I9R','1IAI','1IGC','1IQD','1J1O','1J1P','1J1X','1JHL','1JPS','1K4C','1K4D','1KEN','1KIP','1KIQ','1KIR','4V1D','4V1D_','4ZYP','4ZYP_','5C7K','5C7K_','5FHC','5FHC_','5FYL','5FYL_','5JS9','5JS9_','5JSA','5JSA_','1QFW_']

    listC=db.session.query(Complex).all()
    for c in listC:
        if(not c.pdb_entry in antibodies):
            c.isAntiBody=False

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
    # example: python sqlalchemy_add_features.py -s additional_features/data_grouping.txt -m additional_features/MethodsdataTabSeparate.csv -c additional_features/translate_data_with_contact_chains_3.9_09.05.18.txt -S additional_features/With_stoichiometrydataTabSeparate_V2.txt -r additional_features/RMSD.csv -R additional_features/aa_in_contact_4.0.txt
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #----------------------------------------------------------------------------------------------------
    # notice:                                                                                           |
    # The major of the features are updated in the script sqlalchemy_declarative.py, this script imports|
    # sqlalchemy_declarative.py, thus the latter run *before* this script run.                          |
    #----------------------------------------------------------------------------------------------------
    #options:
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
    print('Done\n')

