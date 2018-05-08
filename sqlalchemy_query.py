#from sqlalchemy_declarative import Complex
#from sqlalchemy import create_engine
#engine = create_engine('mysql://mhacker:2utenLsi@mhacker.mysql.pythonanywhere-services.com/mhacker$complex_data')
#Base.metadata.bind = engine
#from sqlalchemy.orm import sessionmaker
#DBSession = sessionmaker()
#DBSession.bind = engine
from complex_declare import db
from complex_declare import Complex
session = db.session()



# filter the complex results by the aearch query fields:

def filterByComplexPDB(prevList,complex_pdb,theQuery):
    listNew=[]
    theQuery+="complex PDB entry: "+complex_pdb+"   ;  "
    for c in prevList:
        if(c.pdb_entry.lower().find(complex_pdb.lower())!=-1 or c.pdb_entry.lower().find(complex_pdb.lower())!=-1):
            listNew.append(c)
    return listNew,theQuery

def filterByComplexPubYear(prevList,com_year_from,com_year_to,theQuery):
    listNew=[]
    theQuery+="pub.year complex from: "+com_year_from+" to: "+com_year_to+"   ;  "
    if(com_year_from==""):
        for c in prevList:
            if(c.year_pub<=int(com_year_to)):
                listNew.append(c)
    elif(com_year_to==""):
        for c in prevList:
            if(c.year_pub>=int(com_year_from)):
                listNew.append(c)
    else:
        for c in prevList:
            if(c.year_pub<=int(com_year_to) and c.year_pub>=int(com_year_from)):
                listNew.append(c)
    return listNew,theQuery

def filterByAntibody(prevList,is_antibody,theQuery):
    listNew=[]
    theQuery+="only antobodies: "+str(is_antibody)+"   ;  "
    for c in prevList:
        if(c.isAntiBody):
            listNew.append(c)
    return listNew,theQuery

def filterByProtPubYear(prevList,pro_year_from,pro_year_to,theQuery):
    listNew=[]
    theQuery+="pub.year protein from: "+pro_year_from+" to: "+pro_year_to+"   ;  "
    if(pro_year_from==""):
        for c in prevList:
            if(c.year_pub_prot_A<=int(pro_year_to) or c.year_pub_prot_B<=int(pro_year_to)):
                listNew.append(c)
    elif(pro_year_to==""):
        for c in prevList:
            if(c.year_pub_prot_A>=int(pro_year_from) or c.year_pub_prot_B>=int(pro_year_from)):
                listNew.append(c)
    else:
        for c in prevList:
            if((c.year_pub_prot_A<=int(pro_year_to) and c.year_pub_prot_A>=int(pro_year_from)) or
               (c.year_pub_prot_B<=int(pro_year_to) and c.year_pub_prot_B>=int(pro_year_from))):
                listNew.append(c)
    return listNew,theQuery

def filterByProtName(prevList,name,theQuery):
    listNew=[]
    theQuery+="protein name: "+name+"   ;  "
    for c in prevList:
        if(c.name_prot_A.lower().find(name.lower())!=-1 or c.name_prot_B.lower().find(name.lower())!=-1):
            listNew.append(c)
    return listNew,theQuery

def filterByProtPDB(prevList,prot_pdb,theQuery):
    listNew=[]
    theQuery+="protein PDB entry: "+prot_pdb+"   ;  "
    for c in prevList:
        if(c.pdb_prot_A.lower().find(prot_pdb.lower())!=-1 or c.pdb_prot_B.lower().find(prot_pdb.lower())!=-1):
            listNew.append(c)
    return listNew,theQuery

def filterByProtAccession(prevList,prot_access,theQuery):
    listNew=[]
    theQuery+="protein Accession num.: "+prot_access+"   ;  "
    for c in prevList:
        if(c.accession_prot_A.lower().find(prot_access.lower())!=-1 or c.accession_prot_B.lower().find(prot_access.lower())!=-1):
            listNew.append(c)
    return listNew,theQuery


def filterByProtScopFamily(prevList,scop,theQuery):
    listNew=[]
    theQuery+="protein scop family: "+scop+"   ;  "
    for c in prevList:
        if(c.scop_prot_A.lower().find(scop.lower())!=-1 or c.scop_prot_B.lower().find(scop.lower())!=-1):
            listNew.append(c)
    return listNew,theQuery

def filterByLengthA(prevList,len_A_from,len_A_to):
    listNew=[]
    if(len_A_from==""):
        for c in prevList:
            if(c.length_protein_A<=int(len_A_to)):
                listNew.append(c)
    elif(len_A_to==""):
        for c in prevList:
            if(c.length_protein_A>=int(len_A_from)):
                listNew.append(c)
    else:
        for c in prevList:
            if(c.length_protein_A<=int(len_A_to) and c.length_protein_A>=int(len_A_from)):
                listNew.append(c)
    return listNew

def filterByLengthB(prevList,len_B_from,len_B_to):
    listNew=[]
    if(len_B_from==""):
        for c in prevList:
            if(c.length_protein_B<=int(len_B_to)):
                listNew.append(c)
    elif(len_B_to==""):
        for c in prevList:
            if(c.length_protein_B>=int(len_B_from)):
                listNew.append(c)
    else:
        for c in prevList:
            if(c.length_protein_B<=int(len_B_to) and c.length_protein_B>=int(len_B_from)):
                listNew.append(c)
    return listNew

def filterByLengths(listC,len_A_from,len_A_to,len_B_from,len_B_to,theQuery):
    listNew=[]
    if(len_A_from!="" or len_A_to!="" ):# len_A not null
        theQuery+="length protein A from: "+len_A_from+" to: "+len_A_to+"   ;  "
        listA=filterByLengthA(listC,len_A_from,len_A_to)
        listB=filterByLengthB(listC,len_A_from,len_A_to)
    else:
        listA=listC
        listB=listC
    if(len_B_from!="" or len_B_to!=""):# len_B not null
        theQuery+="length protein B from: "+len_B_from+" to: "+len_B_to+"   ;  "
        listA=filterByLengthB(listA,len_B_from,len_B_to)
        listB=filterByLengthA(listB,len_B_from,len_B_to)
    for a in listA:
        listNew.append(a);
    for b in listB:#insert only new objects
        flag=1
        for c in listNew:
            if b.pdb_entry==c.pdb_entry:
                flag=0
                break#this complex wont append to the list
        if flag==1:
            listNew.append(b)
    return listNew,theQuery

def filterByResolution(prevList,res_from,res_to,theQuery):
    listNew=[]
    theQuery+="resolution from: "+res_from+" to: "+res_to+"   ;  "
    if(res_from==""):
        for c in prevList:
            if(c.resolution<=float(res_to)):
                listNew.append(c)
    elif(res_to==""):
        for c in prevList:
            if(c.resolution>=float(res_from)):
                listNew.append(c)
    else:
        for c in prevList:
            if(c.resolution<=float(res_to) and c.resolution>=float(res_from)):
                listNew.append(c)
    return listNew,theQuery

def filterByInterface(prevList,interface_from,interface_to,theQuery):
    listNew=[]
    theQuery+="Interface area from: "+interface_from+" to: "+interface_to+"   ;  "
    if(interface_from==""):
        for c in prevList:
            if(c.interface_area<=int(interface_to)):
                listNew.append(c)
    elif(interface_to==""):
        for c in prevList:
            if(c.interface_area>=int(interface_from)):
                listNew.append(c)
    else:
        for c in prevList:
            if(c.interface_area<=int(interface_to) and c.interface_area>=int(interface_from)):
                listNew.append(c)
    return listNew,theQuery

def filterByRMSD(prevList , cutoff , theQuery):
    listNew=[]
    theQuery +="RMS cutoff:" + cutoff + "   ;  "
    for c in prevList:
        if(c.rmsd_prot_A <= int(cutoff) and c.rmsd_prot_B <= int(cutoff)):
            listNew.append(c)
    return listNew,theQuery

def filterByMethod(prevList , method , theQuery):
    listNew=[]
    theQuery +="Method (complex): " + method + "   ;  "
    for c in prevList:
        if(c.method_complex == method):
            listNew.append(c)
    return listNew,theQuery

def filterByStoichiometry(prevList , stoichiometry , theQuery):
    listNew=[]
    theQuery +="Stoichiometry (complex):" + stoichiometry + "   ;  "
    for c in prevList:
        if(c.stoichiometry_complex == stoichiometry):
            listNew.append(c)
        elif(c.stoichiometry_complex  in stoichiometry):
            listNew.append(c)
    return listNew,theQuery

def filterByIdentity(prevList,ident_from,ident_to,theQuery):
    listNew=[]
    theQuery+="Identity % from: "+ident_from+"% to: "+ident_to+"%   ;  "
    if(ident_from==""):
        for c in prevList:
            if(c.identity_prot_A<=int(ident_to) and c.identity_prot_B<=int(ident_to)):
                listNew.append(c)
    elif(ident_to==""):
        for c in prevList:
            if(c.identity_prot_A>=int(ident_from) and c.identity_prot_B>=int(ident_from)):
                listNew.append(c)
    else:
        for c in prevList:
            if((c.identity_prot_A<=int(ident_to) and c.identity_prot_A>=int(ident_from)) and
              (c.identity_prot_B<=int(ident_to) and c.identity_prot_B>=int(ident_from))):
                listNew.append(c)
    return listNew,theQuery

def search_results(request):
    #get the searched fields from the search form html:
    complex_pdb=(request.form['complex_pdb']).strip()
    #com_year_from=request.form['complex_year_from']
    #com_year_to=request.form['complex_year_to']
    name=request.form['prot_name'].strip()
    is_antibody=request.form['antibody']
    prot_pdb=request.form['prot_pdb'].strip()
    prot_access=request.form['prot_access'].strip()
    scop_family=request.form['scop']
    #pro_year_from=request.form['prot_year_from']
    #pro_year_to=request.form['prot_year_to']
    len_A_from=request.form['lengthA_from']
    len_A_to=request.form['lengthA_to']
    len_B_from=request.form['lengthB_from']
    len_B_to=request.form['lengthB_to']
    res_from=request.form['res_from']
    res_to=request.form['res_to']
    ident_from=request.form['ident_from']
    ident_to=request.form['ident_to']

    #addition 06.05.18
    cutoff = request.form['cutoff']
    stoichiometry = request.form['stoichiometry']
    method = request.form['method']
    #listC=session.query(Complex).all()
    listC=Complex.query.all()
    session.close()
    theQuery="The query was -   "
    exception=""
    if(ident_from=="" and ident_to=="" and is_antibody=="no" and complex_pdb=="" and prot_pdb=="" and prot_access=="" and name=="" and scop_family==""  and len_A_from=="" and len_A_to=="" and len_B_from=="" and len_B_to=="" and res_from=="" and res_to=="" and cutoff=="" and stoichiometry=="" and method==""):
        exception="please insert search fields"
        return None,exception,theQuery
    if(complex_pdb!="" ):# complex pdb not null
        listC,theQuery=filterByComplexPDB(listC,complex_pdb,theQuery)
    # if(com_year_from!="" or com_year_to!="" ):# protein pub.year not null
    #     listC,theQuery=filterByComplexPubYear(listC,com_year_from,com_year_to,theQuery)
    if(name!="" ):# protein name not null
        listC,theQuery=filterByProtName(listC,name,theQuery)
    if(is_antibody=="yes" ):# only antibodies
        listC,theQuery=filterByAntibody(listC,is_antibody,theQuery)
    if(prot_pdb!="" ):# protein pdb not null
        listC,theQuery=filterByProtPDB(listC,prot_pdb,theQuery)
    if(prot_access!="" ):# protein pdb not null
        listC,theQuery=filterByProtAccession(listC,prot_access,theQuery)
    if(scop_family!="" ):# protein name not null
        listC,theQuery=filterByProtScopFamily(listC,scop_family,theQuery)
    # if(pro_year_from!="" or pro_year_to!="" ):#protein pub.year not null
    #     listC,theQuery=filterByProtPubYear(listC,pro_year_from,pro_year_to,theQuery)
    if(method!=''):
        listC,theQuery=filterByMethod(listC, method ,theQuery)
    if(stoichiometry!=''):
        listC,theQuery=filterByStoichiometry(listC , stoichiometry , theQuery)
    if(cutoff!=''):
            listC,theQuery=filterByRMSD(listC , cutoff , theQuery)
    if(ident_from!="" or ident_to!="" ):#identity not null
        listC,theQuery=filterByIdentity(listC,ident_from,ident_to,theQuery)
    listC,theQuery=filterByLengths(listC,len_A_from,len_A_to,len_B_from,len_B_to,theQuery)
#    if(interface_from!="" or interface_to!=""):# interface not null
#        listC,theQuery=filterByInterface(listC,interface_from,interface_to,theQuery)
    if(res_from!="" or res_to!=""):# resolution not null
        listC,theQuery=filterByResolution(listC,res_from,res_to,theQuery)
    return listC,exception,theQuery
