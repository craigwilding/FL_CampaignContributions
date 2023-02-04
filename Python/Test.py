import os
import shutil

wrksp = "/workspaces/vscode-remote-try-python/DATA//State Races"
dirHDContrib = os.path.join(wrksp, "2022HD")

os.chdir(wrksp)

print(os.getcwd())
print(dirHDContrib)

contribFile = "HD120_Candidate.csv"
nameParts = contribFile.split('_')
districtStr = nameParts[0] # get first part HD###
districtStr = districtStr[2:]  # skip first 2 chars
print(districtStr)
district = int(districtStr)

amount = 0.0
amountIn = float("15.25")
amount += amountIn
print(str(amount))
