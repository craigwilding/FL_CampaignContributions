import os
import shutil
import csv
from csv import DictReader
from csv import DictWriter

############################################################
# Get State Contributions
# Go through the contribution files for state house / senate candidates
# get total contributions to the candidate and those by party.
############################################################

wrksp = "/workspaces/vscode-remote-try-python/DATA/State Races"
dirHDContrib = os.path.join(wrksp, "2022HD")


os.chdir(wrksp)

print(os.getcwd())

TAB = "\t"
EOL = '\n'

############################################################
# Data Definitions
# dictDistrict[] = dict[party]
############################################################


# Candidate class to hold candidate info
class CandidateClass:
    district = 0
    name = ""
    party = ""
    party_amount = 0.0
    total = 0.0
# end CandidateClass

# Republican Donors
listREPparty = ["FLORIDA HOUSE REPUBLICAN CAMPAIGN COMMITTEE", "REPUBLICAN PARTY OF FLORIDA", "Florida Republican Senatorial Campaign Committee"]

# Democratic Donors
listDEMparty = ["Florida Democratic Legislative Campaign Committee", "Florida Democratic Party", "Senate Victory"]

# is the donor one of the political parties?
def isPartyDonor(contributor, party_code) :
    isDonor = False
    listParty = listREPparty;
    if ("DEM" == party_code) :
        listParty = listDEMparty;
    for group in listParty :
        match = group.lower()
        if (contributor.lower().find(match) > -1) :
            isDonor = True
        # end if match
    # end for each group
    return isDonor
#end isPartyDonor


############################################################
# Read through each candidate contribution file
# check for donations from Republican party
############################################################
def CountContributions(dirIn, fileNameOut) :
    dictDistrict = {}
    districtType = ""
    for contribFile in os.listdir(dirIn) :
        print(contribFile)
        # get district number from HD###_Candidate.csv
        nameParts = contribFile.split('_')
        districtStr = nameParts[0] # get first part HD###
        districtType = districtStr[0:2] 
        districtStr = districtStr[2:]  # skip first 2 chars
        district = int(districtStr)
        party = nameParts[1]
        firstName = nameParts[2]
        lastName = nameParts[3]

        # check each HD contribution
        fileNameIn = os.path.join(dirIn, contribFile)
        with open(fileNameIn, 'r') as read_obj:
            csv_dict_reader = DictReader(read_obj)

            Candidate = CandidateClass()
            Candidate.district = district
            Candidate.party = party
            Candidate.name = firstName + " " + lastName

            for row in csv_dict_reader:  
                
                amountIn = float(row["Amount"])
                Candidate.total += amountIn
                contributor = row["Contributor Name"]
                # check for party donor
                if (isPartyDonor(contributor, party)) :
                    Candidate.party_amount += amountIn
                # end isPartyDonor

                #end if
            # end for each row
            
            # Save to dictionary
            if (district in dictDistrict) :
                dictParties = dictDistrict[district]
                dictParties[party] = Candidate
                dictDistrict[district] = dictParties
            else :
                # new entry
                dictParties = {}
                dictParties[party] = Candidate
                dictDistrict[district] = dictParties
            # end add to dictionary

        # end with read csv
        del read_obj
    # end for contrib directory

    with open(fileNameOut, 'w', newline='') as write_csv:
        # field names
        fields = ['district']
        fields += ['DEM_Candidate', 'DEM_Total', 'DEM_Party']
        fields += ['REP_Candidate', 'REP_Total', 'REP_Party']
        fields += ['overspend', 'district_total']
        # write column headers 
        csvwriter = csv.DictWriter(write_csv, fieldnames = fields)
        csvwriter.writeheader()
        rowsOut = []

        for district in dictDistrict :
            dictParty = dictDistrict[district]
            DEM_Candidate = CandidateClass() # allow for no candidate that ran in the district
            if ("DEM" in dictParty) :
                DEM_Candidate = dictParty["DEM"]
            REP_Candidate = CandidateClass() # allow for no candidate that ran in the district
            if ("REP" in dictParty) :
                REP_Candidate = dictParty["REP"]

            rowOut = {}
            rowOut["district"] = district
            rowOut["DEM_Candidate"] = DEM_Candidate.name
            rowOut["DEM_Total"] = DEM_Candidate.total
            rowOut["DEM_Party"] = DEM_Candidate.party_amount
            rowOut["REP_Candidate"] = REP_Candidate.name
            rowOut["REP_Total"] = REP_Candidate.total
            rowOut["REP_Party"] = REP_Candidate.party_amount

            # calcuate overspend and total
            overspend = 0.0
            if (DEM_Candidate.total > REP_Candidate.total) :
                overspend = DEM_Candidate.total - REP_Candidate.total
            else :
                overspend = REP_Candidate.total - DEM_Candidate.total

            district_total = DEM_Candidate.total + REP_Candidate.total
                
            rowOut["overspend"] = overspend
            rowOut["district_total"] = district_total
            rowsOut.append(rowOut)

            print(districtType + str(Candidate.district) + " DEM Total: $" + str(DEM_Candidate.total)  + " REP Total: $" + str(REP_Candidate.total))
        # end for candidates

        csvwriter.writerows(rowsOut)
        print("WRITE file: " + fileNameOut)
    # end write csv

    del write_csv
    del rowsOut

    del dictDistrict
# end CountContributions

dirOut = "/workspaces/vscode-remote-try-python/Results/State Races"
if not os.path.exists(dirOut) :
    os.mkdir(dirOut)

dirDBFiles = "/workspaces/vscode-remote-try-python/DATA/State Races/DBFiles"


dirHDContrib = os.path.join(dirDBFiles, "2022HD")
fileNameOut = os.path.join(dirOut, "2022HD_Contrib_byDistrict.csv")
CountContributions(dirHDContrib, fileNameOut)

dirSDContrib = os.path.join(dirDBFiles, "2022SD")
fileNameOut = os.path.join(dirOut, "2022SD_Contrib_byDistrict.csv")
CountContributions(dirSDContrib, fileNameOut)   
