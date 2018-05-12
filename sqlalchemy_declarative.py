from sqlalchemy import Column, Integer, String,Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True



SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format( username="mhacker", password="malki1996", hostname="mhacker.mysql.pythonanywhere-services.com", databasename="mhacker$complex_data")
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class Complex(db.Model):
    #  __tablename__ = 'complex'
    pdb_entry = db.Column(db.String(100), primary_key=True)
    year_pub=db.Column(db.Integer)
    chains = db.Column(db.String(100))
    #    not yet implemented
    interface_area = db.Column(db.Integer)
    interface_area_seq = db.Column(db.String(100))
    #    >>
    resolution=db.Column(db.Float(20))
    isAntiBody=db.Column(db.Boolean(20))
    link = db.Column(db.String(100))
    pdb_prot_A=db.Column(db.String(100))
    name_prot_A=db.Column(db.String(100))
    chain_prot_A=db.Column(db.String(100))
    length_protein_A = db.Column(db.Integer)
    scop_prot_A=db.Column(db.String(100))
    super_fam_A=db.Column(db.String(100))
    reso_prot_A=db.Column(db.Float(20))
    year_pub_prot_A = db.Column(db.Integer)
    accession_prot_A=db.Column(db.String(20))
    identity_prot_A=db.Column(db.Integer)
    seq_prot_A=db.Column(db.String(100))
    res_num_prot_A = db.Column(db.Integer)#   not yet implemented
    pdb_prot_B=db.Column(db.String(100))
    name_prot_B=db.Column(db.String(100))
    chain_prot_B=db.Column(db.String(100))
    length_protein_B = db.Column(db.Integer)
    scop_prot_B=db.Column(db.String(100))
    super_fam_B=db.Column(db.String(100))
    reso_prot_B=db.Column(db.Float(20))
    year_pub_prot_B = db.Column(db.Integer)
    accession_prot_B=db.Column(db.String(100))
    identity_prot_B=db.Column(db.Integer)
    seq_prot_B=db.Column(db.String(100))
    res_num_prot_B = db.Column(db.Integer)#   not yet implemented
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~NEW FEATURES 15/04/18
    stoichiometry_prot_A = db.Column(db.String(100))
    method_prot_A = db.Column(db.String(100))
    chains_in_interface_prot_A = db.Column(db.String(100))
    rmsd_prot_A = db.Column(db.Float(20))
    #num_interface_residues_prot_A = db.Column(db.Float(20))
    stoichiometry_prot_B = db.Column(db.String(100))
    method_prot_B = db.Column(db.String(100))
    chains_in_interface_prot_B = db.Column(db.String(100))
    rmsd_prot_B = db.Column(db.Float(20))
    #num_interface_residues_prot_B = db.Column(db.Float(20))

    stoichiometry_complex = db.Column(db.String(100))
    method_complex = db.Column(db.String(100))
    chains_in_interface_complex = db.Column(db.String(100))
    indentical_complexes = db.Column(db.String(100))
    num_interface_residues_complex = db.Column(db.Float(20))

    def __str__(self):
        s=str(self.pdb_entry[0:4])+"\t"+str(self.resolution)+"\t"+str(self.year_pub)+"\t"+str(self.pdb_prot_A[0:4])+"\t"+str(self.identity_prot_A)+"\t"+str(self.year_pub_prot_A)+"\t"+str(self.length_protein_A)+"\t"+str(self.reso_prot_A)+"\t"+str(self.pdb_prot_B[0:4])+"\t"+str(self.identity_prot_B)+"\t"+str(self.year_pub_prot_B)+"\t"+str(self.length_protein_B)+"\t"+str(self.reso_prot_B)
        # feature addition
        #s = s.strip() + "\t" + str(stoichiometry_prot_A) + str(method_prot_A) + str(chains_in_interface_prot_A) + str(rmsd_prot_A) + str(stoichiometry_prot_B) + str(method_prot_B) + str(chains_in_interface_prot_B) + str(rmsd_prot_B) + str(stochiometry_complex) + str(method_complex) + str(chains_in_interface_complex) + str(num_interface_residues_complex) +str(indentical_complexes)
        return s

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
#engine = create_engine('sqlite:///complex_database1.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
#Base.metadata.create_all(engine)
db.create_all()

#insert the data from the files to the Data Base
i=1
f=open("additional_features/data_grouping.txt","r")  ## to insert  the twices
#f=open("data.txt","r")  ## to insert  the twices ----old version
for c in f.readlines():
#    print("load "+str(i))
    #c=c.split("$")
    c=c.split("\t")
    new_complex=Complex()
    new_complex.pdb_entry = c[0].split('_')[0]
    new_complex.year_pub=c[1]
    new_complex.chains=c[2]
    #    default- not yet implemented
    new_complex.interface_area = c[3]
    new_complex.interface_area_seq = c[4]
    #    >>
    new_complex.resolution=c[5]
    new_complex.isAntiBody=bool(c[6])
    new_complex.link =c[7]
    new_complex.pdb_prot_A=c[8]
    new_complex.name_prot_A=c[9].replace(',',' ')
    new_complex.chain_prot_A=c[10]
    new_complex.length_protein_A = c[11]
    new_complex.scop_prot_A=c[12]
    new_complex.super_fam_A=c[13]
    new_complex.reso_prot_A=c[14]
    new_complex.year_pub_prot_A = c[15]
    new_complex.accession_prot_A=c[16]
    new_complex.identity_prot_A=c[17]
    new_complex.seq_prot_A=c[18]
    new_complex.res_num_prot_A = c[19]
    new_complex.pdb_prot_B=c[20]
    new_complex.name_prot_B=c[21].replace(',',' ')
    new_complex.chain_prot_B=c[22]
    new_complex.length_protein_B = c[23]
    new_complex.scop_prot_B=c[24]
    new_complex.super_fam_B=c[25]
    new_complex.reso_prot_B=c[26]
    new_complex.year_pub_prot_B = c[27]
    new_complex.accession_prot_B=c[28]
    new_complex.identity_prot_B=c[29]
    new_complex.seq_prot_B=c[30]
    new_complex.res_num_prot_B = c[31]
    db.session.add(new_complex)
    i=i+1

#session.commit()
f.close()

db.session.commit()
antibodies=['1G7M','1QFU','1QFW','1R3I','1R3J','1R3K','1R3L','1RZJ','1RZK','1S78','1TET','1TPX','1TQB','1TQC','1TZH','1TZI','1UA6','1UAC','1UJ3','1VFB','1MHP','1MLC','1N8Z','1NAK','1NBY','1NBZ','1NCA','1NCB','1NCC','1NCD','1NDG','1NDM','1NL0','1NMA','1NMB','1NMC','1NSN','1OAK','1OAZ','1OB1','1OSP','1P2C','1PG7','1PKQ','1Q1J','2BDN','2BOB','2BOC','2CMR','2DD8','2DQC','2DQD','2DQE','2DQF','2DQG','2DQH','2DQI','2DQJ','2DWD','2DWE','2EIZ','2EKS','2FD6','2FJG','2FJH','1WEJ','1XCQ','1XCT','1XF5','1XGP','1XGQ','1XGR','1XGT','1XGU','1YQV','1Z3G','1ZTX','1ZWI','2ADF','2AEP','2AEQ','2ATK','2B0S','2B1A','2B2X','2B4C','1YYL','1YYM','2I5Y','2I60','3VE0','4HG4','4FFY','4R4N','4FQR','2Q8A','2Q8B','2QAD','2QQK','2QQL','2QQN','2QR0','2R0K','2R0L','2R4R','2R4S','2R56','2R9H','2UZI','2VC2','2VDK','2VDL','2VDM','2VH5','2VIR','2VIS','2VIT','2VWE','2VXQ','2VXS','2VXT','2W0F','2W9E','2WUB','2H8P','2HFE','2HFG','2HG5','2HJF','2HLF','2HVJ','2HVK','2I9L','2IFF','2IGF','2IH1','2IH3','2ITC','2ITD','2J4W','2J5L','2J6E','2J88','2JEL','2JIX','2JK5','2NR6','2NXY','2NXZ','2NY0','2NY1','2NY2','2NY3','2NY4','2NY5','2NY6','2NY7','2NYY','2NZ9','2OZ4','2P7T','2XRA','2YBR','2YC1','2YPV','2YSS','2ZJS','3A67','3A6B','3A6C','3BAE','3BDY','3BE1','3BGF','3BKJ','3BN9','3BQU','3BSZ','3LQA','3LZF','3MA9','3MAC','3MJ9','3MLT','3MLW','3MLX','3MNZ','3MXW','3N85','3NCY','3NGB','3NH7','3NID','3NIF','3NIG','3NPS','3O0R','3O2D','3O41','3O45','3OGC','3OPZ','3OR6','3OR7','3P11','3P30','3PGF','3PJS','3PNW','3Q1S','3Q3G','3GI8','3GI9','3H0T','3H42','3HB3','3HFM','3HI1','3HI6','3HMX','3HPL','3I50','3IDX','3IDY','3IFN','3IGA','3IXT','3JWD','3JWO','3K2U','3KJ4','3KJ6','3KR3','3L5W','3L5X','3L95','3LD8','3LDB','3LEV','3LIZ','3V4P','3V4V','3V6Z','3V7A','3VG9','3VGA','3VI3','3W2D','3W9E','3WFB','3WFC','3WFD','3WFE','3WIH','3WLW','3WSQ','3ZTJ','3ZTN','4AEI','4AL8','4ALA','4AM0','3QA3','3R1G','3RAJ','3RKD','3RU8','3RVV','3RVW','3RVX','3SDY','3SE8','3SE9','3SKJ','3SO3','3SOB','3SQO','3STL','3STZ','3T2N','3T3M','3T3P','3TT1','3TT3','3TYG','3U2S','3U30','3U4E','3U7Y','3U9U','3UAJ','3UBX','3UJI','4G6F','4G6J','4G6M','4G7Y','4G80','4GMS','4GXU','4H8W','4HC1','4HCR','4HF5','4HFU','4HIX','4I18','4I77','4I9W','4JB9','4JDT','4JKP','4JO1','4JPV','4JPW','4D9Q','4D9R','4DGI','4DKE','4DKF','4DN4','4DQO','4DTG','4DVR','4DW2','4ENE','4ETQ','4FFV','4FFW','4FFZ','4FP8','4FQI','4FQK','4FQV','4FQY','4PP2','4PY8','4QCI','4QEX','4QNP','4QTI','4R0L','4R4F','4R4H','4R8W','4RFN','4RRP','4RWY','4S1Q','4S1R','4S1S','4U6H','4UBD','4UT6','4UT9','4UTA','4UTB','4UUJ','4L5F','4LSP','4LSQ','4LSR','4LST','4LSU','4LSV','4MHH','4MHJ','4MSW','4NM8','4OGX','4OGY','4OII','4OLU','4OLV','4OLW','4OLX','4OLY','4OLZ','4OM0','4OM1','4ONG','4ORZ','5D93','5D96','5DHV','5DUR','5E1A','5E8D','5EBL','5EBM','5EBW','5EC1','5EC2','5F3B','5F3H','5F6J','5F96','5F9W','5FB8','4WFE','4WFF','4WFG','4WFH','4XAK','4XMP','4XNY','4XNZ','4XZU','4YBL','4YC2','4YDJ','4YDK','4YDL','4YE4','4YWG','4Z5R','4ZSO','5T29','5T5B','5T5F','5T6L','5T80','5T85','5TFW','5TIH','5V2A','5VCO','5FHX','5GJS','5GJT','5GZN','5GZO','5HDB','5HJ3','5JHL','5KAQ','5KN5','5KVD','5KVE','5KVF','5KVG','5LBS','5LCV','1A14','1A2Y','1ACY','1ADQ','1AFV','1AHW','1AI1','1AR1','1BGX','1BJ1','1BQL','1BVK','1C08','1CIC','1CZ8','1DEE','1DQJ','1DVF','1E6J','1EGJ','1EO8','1F58','1FBI','1FDL','1FE8','1FJ1','1FNS','1FSK','1G7H','1G7I','1G7J','1G7L','1G9M','1G9N','1GC1','1GGI','1H0D','1I9R','1IAI','1IGC','1IQD','1J1O','1J1P','1J1X','1JHL','1JPS','1K4C','1K4D','1KEN','1KIP','1KIQ','1KIR','4V1D','4V1D_','4ZYP','4ZYP_','5C7K','5C7K_','5FHC','5FHC_','5FYL','5FYL_','5JS9','5JS9_','5JSA','5JSA_','1QFW_']

listC=db.session.query(Complex).all()
for c in listC:
    if(not c.pdb_entry in antibodies):
        print(str(c))
        c.isAntiBody=False
db.session.commit()