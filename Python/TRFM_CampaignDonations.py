import os
import shutil
import pandas
import PandasTransforms as PTX
import sys
sys.path.insert(0, '/workspaces/vscode-remote-try-python/PostgreSQL')
import SQLCommands as SQL

############################################
# TRANSFORM Candidate Campaign Donations
# Perform any data transformations here before loading to database
# fileNameIn =  DATA/State Races/2022HD - Florida State House District Candidate Contributions
#               DATA/State Races/2022SD  - Florida State Senate District Candidate Contributions
# dirOut = DBFiles   
#    This creates a copy of the original into the DBFiles subfolder with a _DBFile.csv extension
############################################

TAB = "\t"
EOL = '\n'
COMMA = ','



# Candidate/Committee,Date,Amount,Typ,Contributor Name,City State Zip,Occupation,Inkind Desc,donortype
dictRenameColumns = {
    "Candidate/Committee": "candidate",
    "Date": "date",
    "Amount": "amount",
    "Typ": "contrib_type",
    "Contributor Name": "contributor",
    "City State Zip": "city_sate_zip",
    "Occupation": "occupation",
    "Inkind Desc" : "inkind_desc"
}


def ContributionsTransforms(pandasTX) :
    print(pandasTX.fileNameIn)
    pandasTX.removeNonAscii()
    pandasTX.removeBinary()
    pandasTX.removeColumn("Address")
    pandasTX.renameColumn(dictRenameColumns)
    GetCandidateInfo(pandasTX)
    TransformAddress(pandasTX)
    pandasTX.removeColumn("city_sate_zip")
    pandasTX.addColumn("donortype", "IND")
    pandasTX.addColumn("donorindex", "0")
    pandasTX.write()

# end ContributionsTransforms  
    
def ParseCityStateZip(cityStateZip) :
    city = ""
    state = ""
    zipCode = ""

    # ********************, FL if withheld
    if (cityStateZip.startswith("*")) :
        city = "WITHHELD"
        state = ""
        zipCode = "00000"
    else :
        # FORT WALTON BEACH, FL 32548
        # "FT. MYERS, FL "  (no zip code)
        ix1 = cityStateZip.find(", ")
        ix2 = cityStateZip.rfind(" ")
        city = cityStateZip[0:ix1]
        state = cityStateZip[ix1+2:ix2]
        zipCode = cityStateZip[ix2+1:]
        if ("" == zipCode) :
            zipCode = "00000"
    # end if withheld
    listOut = [city, state, zipCode]
    return listOut
# end ParseCityStateZip

def TransformAddress(pandasTX) :
    # Read as pandas data frame
    #df = pandas.read_csv(pandasTX.fileNameIn,sep=pandasTX.delim,header=0,index_col=False)
    df2 = pandasTX.df['city_sate_zip'].apply(lambda x: pandas.Series(ParseCityStateZip(x), index=['city', 'state', 'zipcode']))
    fileNameOut = pandasTX.fileNameIn.replace(".", "_TransformAddress.")

    # merge rows
    frames = [pandasTX.df, df2]
    dfOut = pandas.concat(frames, axis=1)

    # reload df from temp file to reset columns
    # write to temp file
    dfOut.to_csv(fileNameOut, encoding='utf-8', index=False, header=pandasTX.headers, sep=pandasTX.delim)
    pandasTX.read_from(fileNameOut)
    # replace in File with temp file
    os.remove(fileNameOut)
# end TransformAddress

def ParseCandidateFromContrib(candidate) :
    cand_fname= ""
    cand_lname = ""
    cand_party = ""
    cand_office = ""
    cand_year = "2022"

    # Rudman, Joel  (REP)(STR)
    ix1 = candidate.find(", ")
    cand_lname = candidate[0:ix1]
    ix2 = candidate.rfind("(")
    cand_office = candidate[ix2+1:].replace(')',"").strip()
    temp = candidate[ix1+2:ix2-1]
    # Joel  (REP)
    ix2 = temp.rfind("(")
    cand_party = temp[ix2+1:].strip()
    cand_fname = temp[0:ix2-1].strip()
    # end if withheld
    dictCandidate = {}
    dictCandidate["cand_fname"] = cand_fname
    dictCandidate["cand_lname"] = cand_lname
    dictCandidate["cand_party"] = cand_party
    dictCandidate["cand_office"] = cand_office
    dictCandidate["cand_year"] = cand_year
    return dictCandidate
# end ParseCandidate

def GetCandidateInfo(pandasTX) :
    # Have to get candidate info from the file name
    # as not all candidates have contribution entries to pull the data from


    # get district from filename
    # HD82_REP_Lauren-Uhlich_Melo_contrib_DBFile
    folders = pandasTX.fileNameIn.split("/")
    fileName = folders[len(folders)-1]
    parts = fileName.split('_')
    office = parts[0]
    district = "0"
    if (office.startswith("HD")) :
        district = office[2:]
        office = "STR"
    elif (office.startswith("SD")) :
        district = office[2:]
        office = "STS"
    # end if

    party = parts[1]
    firstName = parts[2]
    lastName = parts[3]
    year = "2022"
        
    # end district


    cand_id = ""
    with SQL.Connect() as conn:
        table = "candidates"
        sqlWhere = " WHERE "
        #sqlWhere += " (UPPER(lastname) = '" + lastName.upper() + "')"
        #sqlWhere += " AND (firstname.UPPER() LIKE '%" + firstName.upper() + "%')"
        sqlWhere += " (party = '" + party.upper() + "')"
        sqlWhere += " AND (office = '" + office.upper() + "')"
        sqlWhere += " AND (year = " + year + ")"  # integer
        if ("0" != district) :
            sqlWhere += " AND (district = " + district + ")" # integer
        # endif district

        # print(sqlWhere)
        cand_id = SQL.SelectIdWhere(conn, table, sqlWhere)
        
        #sqlWhere = " id = " + cand_id
        #colFirstName = ("firstname", firstName, "text")
        #colLastName = ("lastname", lastName, "text")
        #columns = [colFirstName, colLastName]
        #SQL.UpdateWhere(conn, table, columns, whereSql="")
    # end connection

    # add candidate columns
    pandasTX.addColumn("cand_firstname", firstName, PTX.COL_BEGIN)
    pandasTX.addColumn("cand_lastname", lastName, PTX.COL_BEGIN)
    pandasTX.addColumn("cand_id", cand_id, PTX.COL_BEGIN)
    pandasTX.removeColumn("candidate")
# end GetCandidateInfo



dirData = "/workspaces/vscode-remote-try-python/DATA/State Races"
dirDBFiles = os.path.join(dirData,  "DBFiles")
if not os.path.exists(dirDBFiles):
    os.makedirs(dirDBFiles)


##############################################
# FL House District Candidates
##############################################
dirIn = os.path.join(dirData, "2022HD")
dirOut = os.path.join(dirDBFiles, "2022HD")
if not os.path.exists(dirOut):
    os.makedirs(dirOut)

testFile = "HD101_DEM_Hillary_Cassel_contrib.csv"

for contribFile in os.listdir(dirIn) :
    #if (contribFile != testFile) :
    #    continue

    print(contribFile)
    fileNameIn = os.path.join(dirIn, contribFile)
    outName = contribFile.replace(".csv","_DBFile.csv")
    fileNameOut = os.path.join(dirOut, outName)
    shutil.copy(fileNameIn, fileNameOut)
    pandasTX = PTX.PandasTransform(fileNameOut, delim=COMMA, headers=True)
    ContributionsTransforms(pandasTX)
# end for contrib files

##############################################
# FL Senate District Candidates
##############################################
dirIn = os.path.join(dirData, "2022SD")
dirOut = os.path.join(dirDBFiles, "2022SD")
if not os.path.exists(dirOut):
    os.makedirs(dirOut)

for contribFile in os.listdir(dirIn) :
    print(contribFile)
    fileNameIn = os.path.join(dirIn, contribFile)
    outName = contribFile.replace(".csv","_DBFile.csv")
    fileNameOut = os.path.join(dirOut, outName)
    shutil.copy(fileNameIn, fileNameOut)
    pandasTX = PTX.PandasTransform(fileNameOut, delim=COMMA, headers=True)
    ContributionsTransforms(pandasTX)
# end for contrib files