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

    #comments.append((request.form['complex_pdb']).strip())
    complex_pdb=(request.form['complex_pdb']).strip()
    com_year_from=request.form['complex_year_from']
    com_year_to=request.form['complex_year_to']
    name=request.form['prot_name'].strip()
    is_antibody=request.form['antibody']
    prot_pdb=request.form['prot_pdb'].strip()
    prot_access=request.form['prot_access'].strip()
    scop_family=request.form['scop']
    pro_year_from=request.form['prot_year_from']
    pro_year_to=request.form['prot_year_to']
    len_A_from=request.form['lengthA_from']
    len_A_to=request.form['lengthA_to']
    len_B_from=request.form['lengthB_from']
    len_B_to=request.form['lengthB_to']
    res_from=request.form['res_from']
    res_to=request.form['res_to']
    ident_from=request.form['ident_from']
    ident_to=request.form['ident_to']
    flag=False



       # pass the list of the results
    listC,exception,theQuery=sqlalchemy_query.search_results(request) #sending to search functions in class sqlalchemy_query
    data=""
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






#            c.accession_prot_A=c.accession_prot_A.replace("-","")
#            c.accession_prot_B=c.accession_prot_B.replace("-","")
#            linkAccessionPA_1="http://www.uniprot.org/uniprot/"+c.accession_prot_A
#            linkAccessionPA_2=""
#            accA=[c.accession_prot_A,""]
#            if c.accession_prot_A.find(",")!=-1:
#                accA=c.accession_prot_A.split(",")
#            if(accA[0]!=accA[1]):
#                linkAccessionPA_1="http://www.uniprot.org/uniprot/"+accA[0]
#                linkAccessionPA_2="http://www.uniprot.org/uniprot/"+accA[1]
#            else:
#                linkAccessionPA_1="http://www.uniprot.org/uniprot/"+accA[0]
#                accA[1]=""
#                linkAccessionPB_1="http://www.uniprot.org/uniprot/"+c.accession_prot_B
#                linkAccessionPB_2=""
#                accB=[c.accession_prot_B,""]
#                if c.accession_prot_B.find(",")!=-1:
#                    accB=c.accession_prot_B.split(",")
#                    if(accB[0]!=accB[1]):
#                        linkAccessionPB_1="http://www.uniprot.org/uniprot/"+accB[0]
#                        linkAccessionPB_2="http://www.uniprot.org/uniprot/"+accB[1]
#                    else:
#                        linkAccessionPB_1="http://www.uniprot.org/uniprot/"+accB[0]
#                        accB[1]=""

#               # a dictionary for the results table at the web html
#            p={"pdb_entry":str(c.pdb_entry),"year_pub":str(c.year_pub),"resolution":str(c.resolution),
#            "link":str(c.link),"pdb_prot_A":str(c.pdb_prot_A),"linkPA":str(linkPA),"linkAccessionPA_1":str(linkAccessionPA_1),
#            "linkAccessionPA_2":str(linkAccessionPA_2),"name_prot_A":str(c.name_prot_A),"accession_prot_A_1":str(accA[0]),
#            "accession_prot_A_2":str(accA[1]),"chain_prot_A":str(c.chain_prot_A),"length_protein_A":str(c.length_protein_A),
#            "identity_prot_A":str(c.identity_prot_A),"scop_prot_A":str(c.scop_prot_A),"reso_prot_A":str(c.reso_prot_A),
#            "year_pub_prot_A":str(c.year_pub_prot_A),"res_num_prot_A":str(c.res_num_prot_A),"pdb_prot_B":str(c.pdb_prot_B),
#            "linkPB":str(linkPB),"linkAccessionPB_1":"fff","linkAccessionPB_2":str(linkAccessionPB_2),
#            "name_prot_B":str(c.name_prot_B),"accession_prot_B_1":str(accB[0]),"accession_prot_B_2":str(accB[1]),"chain_prot_B":str(c.chain_prot_B),
#            "length_protein_B":str(c.length_protein_B),"identity_prot_B":str(c.identity_prot_B),"scop_prot_B":str(c.scop_prot_B),
#            "reso_prot_B":str(c.reso_prot_B),"year_pub_prot_B":str(c.year_pub_prot_B),"res_num_prot_B":str(c.res_num_prot_B)}
#            protdata.append(p)
               #text for download:
            content = ""
            t={"pdb_entry":str(c.pdb_entry),"link":link,"year_pub":str(c.year_pub),"resolution":str(c.resolution),
            "pdb_prot_A":str(c.pdb_prot_A),"linkPA":str(linkPA),"linkAccessionPA_1":link_acc_A_1,
            "linkAccessionPA_2":link_acc_A_2,"name_prot_A":str(c.name_prot_A),"accession_prot_A_1":accession_prot_A_1,
            "accession_prot_A_2":accession_prot_A_2,"chain_prot_A":str(c.chain_prot_A),"length_protein_A":str(c.length_protein_A),
            "identity_prot_A":str(c.identity_prot_A),"scop_prot_A":str(c.scop_prot_A),"reso_prot_A":str(c.reso_prot_A),
            "year_pub_prot_A":str(c.year_pub_prot_A),"res_num_prot_A":str(c.res_num_prot_A),"pdb_prot_B":str(c.pdb_prot_B),
            "linkPB":str(linkPB),"linkAccessionPB_1":link_acc_B_1,"linkAccessionPB_2":link_acc_B_2,
            "name_prot_B":str(c.name_prot_B),"accession_prot_B_1":accession_prot_B_1,"accession_prot_B_2":accession_prot_B_2,"chain_prot_B":str(c.chain_prot_B),
            "length_protein_B":str(c.length_protein_B),"identity_prot_B":str(c.identity_prot_B),"scop_prot_B":str(c.scop_prot_B),
            "reso_prot_B":str(c.reso_prot_B),"year_pub_prot_B":str(c.year_pub_prot_B),"res_num_prot_B":str(c.res_num_prot_B)}
    #result=[]
    #for i in listC:
    #    result.append(i.pdb_entry)

            p.append(t)

    index.save_results=list(p)
    return render_template("result3.html",result = p,exception="",theQuery=theQuery,count=len(p))
    #return render_template("result2.html",result = p,exception="",theQuery="fgd",count=3)
    #return render_template("results1.html", result=result)
    #return render_template("result1.html",result = result)#,exception=exception,theQuery=theQuery,count=i)

        #return render_template("result.html",result = protdata,exception=exception,theQuery=theQuery,count=i)
    #comments,exception,theQuery=sqlalchemy_query.search_results(request)
    #return render_template("show_comments.html", comments=comments)


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
    return render_template("result2.html",result = index.save_results,exception="",theQuery="fgd",count=3)

@app.route("/tt", methods=["GET", "POST"])
def index1():
    comments=["moshe mo"]
    return render_template("results1.html", result=comments)


#------------------------------------------------------------------------------------

@app.route("/cdb/search", methods=["GET", "POST"])
def cdbindex():
    if request.method == "GET":
        return render_template("search.html")

    #comments.append((request.form['complex_pdb']).strip())
    complex_pdb=(request.form['complex_pdb']).strip()
    com_year_from=request.form['complex_year_from']
    com_year_to=request.form['complex_year_to']
    name=request.form['prot_name'].strip()
    is_antibody=request.form['antibody']
    prot_pdb=request.form['prot_pdb'].strip()
    prot_access=request.form['prot_access'].strip()
    scop_family=request.form['scop']
    pro_year_from=request.form['prot_year_from']
    pro_year_to=request.form['prot_year_to']
    len_A_from=request.form['lengthA_from']
    len_A_to=request.form['lengthA_to']
    len_B_from=request.form['lengthB_from']
    len_B_to=request.form['lengthB_to']
    res_from=request.form['res_from']
    res_to=request.form['res_to']
    ident_from=request.form['ident_from']
    ident_to=request.form['ident_to']
    flag=False



       # pass the list of the results
    listC,exception,theQuery=sqlalchemy_query.search_results(request) #sending to search functions in class sqlalchemy_query
    data=""
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
            content = ""
            t={"pdb_entry":str(c.pdb_entry),"link":link,"year_pub":str(c.year_pub),"resolution":str(c.resolution),
            "pdb_prot_A":str(c.pdb_prot_A),"linkPA":str(linkPA),"linkAccessionPA_1":link_acc_A_1,
            "linkAccessionPA_2":link_acc_A_2,"name_prot_A":str(c.name_prot_A),"accession_prot_A_1":accession_prot_A_1,
            "accession_prot_A_2":accession_prot_A_2,"chain_prot_A":str(c.chain_prot_A),"length_protein_A":str(c.length_protein_A),
            "identity_prot_A":str(c.identity_prot_A),"scop_prot_A":str(c.scop_prot_A),"reso_prot_A":str(c.reso_prot_A),
            "year_pub_prot_A":str(c.year_pub_prot_A),"res_num_prot_A":str(c.res_num_prot_A),"pdb_prot_B":str(c.pdb_prot_B),
            "linkPB":str(linkPB),"linkAccessionPB_1":link_acc_B_1,"linkAccessionPB_2":link_acc_B_2,
            "name_prot_B":str(c.name_prot_B),"accession_prot_B_1":accession_prot_B_1,"accession_prot_B_2":accession_prot_B_2,"chain_prot_B":str(c.chain_prot_B),
            "length_protein_B":str(c.length_protein_B),"identity_prot_B":str(c.identity_prot_B),"scop_prot_B":str(c.scop_prot_B),
            "reso_prot_B":str(c.reso_prot_B),"year_pub_prot_B":str(c.year_pub_prot_B),"res_num_prot_B":str(c.res_num_prot_B)}


            p.append(t)

    index.save_results=list(p)
    return render_template("result3.html",result = p,exception="",theQuery=theQuery,count=len(p))


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
    return render_template("result2.html",result = index.save_results,exception="",theQuery="fgd",count=3)

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

