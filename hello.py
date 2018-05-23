#from flask import Flask, redirect, render_template, request, url_for
from flask import Flask,request,render_template,flash, redirect, url_for
#import try_sql
import sqlalchemy_query
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
import os.path
from flask_sqlalchemy import SQLAlchemy

from complex_declare import db
from complex_declare import Complex
session = db.session()

app=Flask(__name__)


app = Flask(__name__)
app.config["DEBUG"] = True


theQuery,protdata=[],[]



@app.route("/search", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("search.html")
       # pass the list of the results
    listC,exception,theQuery=sqlalchemy_query.search_results(request) #sending to search functions in class sqlalchemy_query
    # data=""
    i=0
    p=[]
    if(listC):
        for c in listC:
            i=i+1
            linkPA="http://www.rcsb.org/pdb/explore/explore.do?structureId="+c.pdb_prot_A[0:4]
            linkPB="http://www.rcsb.org/pdb/explore/explore.do?structureId="+c.pdb_prot_B[0:4]
            link="http://www.rcsb.org/pdb/explore/explore.do?structureId="+c.pdb_entry[0:4]

            # delete the * signs
            c.pdb_prot_A=c.pdb_prot_A.replace("*","")
            c.pdb_prot_B=c.pdb_prot_B.replace("*","")

            if len(c.accession_prot_A)>10:
                accession_prot_A_1=c.accession_prot_A.split(",")[0].replace(",","").replace("-","")
                accession_prot_A_2=c.accession_prot_A.split(",")[1].replace(",","").replace("-","")
                link_acc_A_1="http://www.uniprot.org/uniprot/"+accession_prot_A_1
                link_acc_A_2="http://www.uniprot.org/uniprot/"+accession_prot_A_2
            else:
                accession_prot_A_1=c.accession_prot_A.replace(",","").replace("-","")
                link_acc_A_1="http://www.uniprot.org/uniprot/"+accession_prot_A_1
                accession_prot_A_2=""
                link_acc_A_2=""
            if len(c.accession_prot_B)>10:
                accession_prot_B_1=c.accession_prot_B.split(",")[0].replace(",","").replace("-","")
                accession_prot_B_2=c.accession_prot_B.split(",")[1].replace(",","").replace("-","")
                link_acc_B_1="http://www.uniprot.org/uniprot/"+accession_prot_B_1
                link_acc_B_2="http://www.uniprot.org/uniprot/"+accession_prot_B_2
            else:
                accession_prot_B_1=c.accession_prot_B.replace(",","").replace("-","")
                accession_prot_B_2=""
                link_acc_B_1="http://www.uniprot.org/uniprot/"+accession_prot_B_1
                link_acc_B_2=""
            img_loc = "/static/images/"+str(c.pdb_entry)+".png"
            #text for download:
            t={"pdb_entry":str(c.pdb_entry),"link":link,"year_pub":str(c.year_pub),"resolution":str(c.resolution),
            "pdb_prot_A":str(c.pdb_prot_A),"linkPA":str(linkPA),"linkAccessionPA_1":link_acc_A_1,
            "linkAccessionPA_2":link_acc_A_2,"name_prot_A":str(c.name_prot_A),"accession_prot_A_1":accession_prot_A_1,
            "accession_prot_A_2":accession_prot_A_2,"chain_prot_A":str(c.chain_prot_A),"length_protein_A":str(c.length_protein_A),
            "identity_prot_A":str(c.identity_prot_A),"scop_prot_A":str(c.scop_prot_A.replace(',',' ')),"reso_prot_A":str(c.reso_prot_A),
            "year_pub_prot_A":str(c.year_pub_prot_A),"res_num_prot_A":str(c.res_num_prot_A),"pdb_prot_B":str(c.pdb_prot_B),
            "linkPB":str(linkPB),"linkAccessionPB_1":link_acc_B_1,"linkAccessionPB_2":link_acc_B_2,
            "name_prot_B":str(c.name_prot_B),"accession_prot_B_1":accession_prot_B_1,"accession_prot_B_2":accession_prot_B_2,"chain_prot_B":str(c.chain_prot_B),
            "length_protein_B":str(c.length_protein_B),"identity_prot_B":str(c.identity_prot_B),"scop_prot_B":str(c.scop_prot_B.replace(',',' ')),
            "reso_prot_B":str(c.reso_prot_B),"year_pub_prot_B":str(c.year_pub_prot_B),"res_num_prot_B":str(c.res_num_prot_B),
            "stoichiometry_prot_A":str(c.stoichiometry_prot_A),"method_prot_A":c.method_prot_A,"chains_in_interface_prot_A":str(c.chains_in_interface_prot_A),"rmsd_prot_A":str(c.rmsd_prot_A),"stoichiometry_prot_B":str(c.stoichiometry_prot_B),
            "method_prot_B":str(c.method_prot_B),"chains_in_interface_prot_B":str(c.chains_in_interface_prot_B),"rmsd_prot_B":str(c.rmsd_prot_B),"stoichiometry_complex": str(c.stoichiometry_complex),
            "method_complex":str(c.method_complex),"chains_in_interface_complex":str(c.chains_in_interface_complex),"indentical_complexes":str(c.indentical_complexes),"num_interface_residues_complex":str(c.num_interface_residues_complex),"cmplx_img":str(img_loc)}
            p.append(t)

    index.save_results=list(p)

    return render_template("result7.html",result = p,exception="",theQuery=theQuery,count=len(p))



@app.route("/")
def home():
    return render_template('intro.html')

@app.route("/home")
def home1():
    return render_template('home.html')

@app.route("/citingUs")
def contactUs():
    return render_template('citingUs.html')

@app.route("/help")
def help():
    return render_template('help.html')
@app.route("/result_txt")
def result_txt():
    return render_template("text_result.html",result = index.save_results,exception="",theQuery="fgd",count=3)

@app.route("/result_table")
def result_table():
    return render_template("table_result.html",result = index.save_results,exception="",theQuery="fgd",count=3)

@app.route("/tt", methods=["GET", "POST"])
def index1():
    comments=["moshe mo"]
    return render_template("results1.html", result=comments)


#------------------------------------------------------------------------------------

@app.route("/cdb/search", methods=["GET", "POST"])
def cdbindex():
    if request.method == "GET":
        return render_template("search.html")

       # pass the list of the results
    listC,exception,theQuery=sqlalchemy_query.search_results(request) #sending to search functions in class sqlalchemy_query
    i=0
    p=[]
    if(listC):
        for c in listC:
            i=i+1
            linkPA="http://www.rcsb.org/pdb/explore/explore.do?structureId="+c.pdb_prot_A[0:4]
            linkPB="http://www.rcsb.org/pdb/explore/explore.do?structureId="+c.pdb_prot_B[0:4]
            link="http://www.rcsb.org/pdb/explore/explore.do?structureId="+c.pdb_entry[0:4]

            # delete the * signs
            c.pdb_prot_A=c.pdb_prot_A.replace("*","")
            c.pdb_prot_B=c.pdb_prot_B.replace("*","")

            if len(c.accession_prot_A)>10:
                accession_prot_A_1=c.accession_prot_A.split(",")[0].replace(",","").replace("-","")
                accession_prot_A_2=c.accession_prot_A.split(",")[1].replace(",","").replace("-","")
                link_acc_A_1="http://www.uniprot.org/uniprot/"+accession_prot_A_1
                link_acc_A_2="http://www.uniprot.org/uniprot/"+accession_prot_A_2
            else:
                accession_prot_A_1=c.accession_prot_A.replace(",","").replace("-","")
                link_acc_A_1="http://www.uniprot.org/uniprot/"+accession_prot_A_1
                accession_prot_A_2=""
                link_acc_A_2=""
            if len(c.accession_prot_B)>10:
                accession_prot_B_1=c.accession_prot_B.split(",")[0].replace(",","").replace("-","")
                accession_prot_B_2=c.accession_prot_B.split(",")[1].replace(",","").replace("-","")
                link_acc_B_1="http://www.uniprot.org/uniprot/"+accession_prot_B_1
                link_acc_B_2="http://www.uniprot.org/uniprot/"+accession_prot_B_2
            else:
                accession_prot_B_1=c.accession_prot_B.replace(",","").replace("-","")
                accession_prot_B_2=""
                link_acc_B_1="http://www.uniprot.org/uniprot/"+accession_prot_B_1
                link_acc_B_2=""

               #text for download:
            #content = ""
            t={"pdb_entry":str(c.pdb_entry),"link":link,"year_pub":str(c.year_pub),"resolution":str(c.resolution),
            "pdb_prot_A":str(c.pdb_prot_A),"linkPA":str(linkPA),"linkAccessionPA_1":link_acc_A_1,
            "linkAccessionPA_2":link_acc_A_2,"name_prot_A":str(c.name_prot_A),"accession_prot_A_1":accession_prot_A_1,
            "accession_prot_A_2":accession_prot_A_2,"chain_prot_A":str(c.chain_prot_A),"length_protein_A":str(c.length_protein_A),
            "identity_prot_A":str(c.identity_prot_A),"scop_prot_A":str(c.scop_prot_A),"reso_prot_A":str(c.reso_prot_A),
            "year_pub_prot_A":str(c.year_pub_prot_A),"res_num_prot_A":str(c.res_num_prot_A),"pdb_prot_B":str(c.pdb_prot_B),
            "linkPB":str(linkPB),"linkAccessionPB_1":link_acc_B_1,"linkAccessionPB_2":link_acc_B_2,
            "name_prot_B":str(c.name_prot_B),"accession_prot_B_1":accession_prot_B_1,"accession_prot_B_2":accession_prot_B_2,"chain_prot_B":str(c.chain_prot_B),
            "length_protein_B":str(c.length_protein_B),"identity_prot_B":str(c.identity_prot_B),"scop_prot_B":str(c.scop_prot_B),
            "reso_prot_B":str(c.reso_prot_B),"year_pub_prot_B":str(c.year_pub_prot_B),"res_num_prot_B":str(c.res_num_prot_B),
            "stoichiometry_prot_A":c.stoichiometry_prot_A,"method_prot_A":c.method_prot_A,"chains_in_interface_prot_A":str(c.chains_in_interface_prot_A),"rmsd_prot_A":str(c.rmsd_prot_A),"stoichiometry_prot_B": str(c.stoichiometry_prot_B.replace('\n','')),
            "method_prot_B":c.stoichiometry_prot_B.replace('\n',''),"chains_in_interface_prot_B":str(c.chains_in_interface_prot_B),"rmsd_prot_B":str(c.rmsd_prot_B),"stoichiometry_complex": c.stoichiometry_complex,
            "method_complex":str(c.method_complex),"chains_in_interface_complex":str(c.chains_in_interface_complex),"indentical_complexes":c.indentical_complexes,"num_interface_residues_complex":str(c.num_interface_residues_complex)}
            t={}
            p.append(t)

    index.save_results=list(p)
    return render_template("result7.html",result = p,exception="",theQuery=theQuery,count=len(p))


#@app.route("/tt", methods=["GET", "POST"])
#def index1():
#    comments=["moshe mo"]
#    return render_template("results1.html", result=comments)


@app.route("/cdb/citingUs")
def cdbcontactUs():
    return render_template('citingUs.html')

@app.route("/cdb/help")
def cdbhelp():
    return render_template('help.html')

@app.route("/cdb/result_txt")
def cdbresult_txt():
    return render_template("text_result.html",result = index.save_results,exception="",theQuery="fgd",count=3)

@app.route("/cdb/table_txt")
def cdbresult_table():
    return render_template("table_result.html",result = index.save_results,exception="",theQuery="fgd",count=3)

@app.route("/tools")
def tools():
    return render_template('tools.html')

@app.route("/cdb/home")
def cdbhome():
    return render_template('cdbhome.html')

@app.route("/intro")
def intro():
    return render_template('intro.html')


if __name__ == '__main__':
    app.run()

