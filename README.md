# Florida Campaign Contributions

This collects campaign contribution data pulled from the [FL Campaign Finance Database](https://dos.elections.myflorida.com/campaign-finance/contributions/).  I have added the campaign contributions of all [FL House and Senate candidates](https://dos.elections.myflorida.com/candidates/Index.asp) in 2022.  The Python scripts go through the contribution files and counts the campaign contributions raised in each district.

## District Comparisons
This creates a .csv file in the **Results** folder which compares the money raised by DEM and REP candidates. 
The available columns are
1. District number
2. DEM Candidate Name
3. DEM Total = Total contributions received by the candidate
4. DEM Party = Total contributions given to the candidate by state-level party committees
5. REP Candidate Name
6. REP Total = Total contributions received by the candidate
7. REP Party = Total contributions given to the candidate by state-level party committees
8. Overspend = The amount the candidate with the largest contribution amount outraised the other candidate by
9. District Total = The total amount raised in the district by both DEM and REP candidates


## State Level
The state-level results for comparing candidate contributions by FL house and senate districts are completed.

[2022 FL House District comparison](https://github.com/craigwilding/FL_CampaignContributions/blob/main/Results/State%20Races/2022HD_Contrib_byDistrict.csv)

[2022 FL Senate District comparison](https://github.com/craigwilding/FL_CampaignContributions/blob/main/Results/State%20Races/2022SD_Contrib_byDistrict.csv)

### County Level
I hope to expand to county-level candidates, but this requires pulling data from each of the 67 counties.

## Data Collection

I amusing the [Selenium Web Driver](https://www.selenium.dev/documentation/webdriver/) to automatically pull data from the state website.
I have not yet added the python scripts that do the web-scraping.  I will add these if I am able to add 
Selenium and the [Chrome web-driver](https://chromedriver.chromium.org/downloads) to the codespace.

## Data Processing
This is the order I am running the scripts:
### Extract
1. Candidates: The list of FL House and Senate candidates was pulled from the [FL DOE Candidate database](https://dos.elections.myflorida.com/candidates/CanList.asp)
1. Contributions: Candidate contributions were pulled from the [Florida Contributions Database](https://dos.elections.myflorida.com/campaign-finance/contributions/)  See [CF0_GetWebFLContribHD2022.py](Python/CF0_GetWebFLContribHD2022.py)   for the Selenium web driver to automate downloading data from the website.
2. Voter Files: Provided from the [Florida Division of Elections](https://dos.myflorida.com/elections/data-statistics/voter-registration-statistics/voter-extract-disk-request/) into the DATA/VoterFiles Folder

### Transform
1. TRFM_Candidates.py   Clean non-ascii characters.  Reformat for loading to database
2. TRFM_CampaignDonations.py   Clean non-ascii, and bad characters.  Parse city, state, and zip from address.  Reformat for loading to database
3. VF_TRFM1_RemoveAddress.py   Remove address, phone, email and unneeded columns from original voter file
4. VF_TRFM2_AddHeader.py   Add column headers for later use
5. VF_TRFM3_RemoveExempt.py   Remove exempt records where voter info is hidden
### Load
1. CREATE_Candidates.py   Create Candidate database
2. LOAD_Candidates.py   Load Candidate database from transformed DB file
3. CREATE_Contributions.py   Create Contributions database
4. LOAD_Contributions.py   Load Contributions database from transformed DB file
5. CREATE_Voters2022.py   Create Voter database
6. LOAD_Voters2022.py   Load Voter database from transformed DB file

### Process
1. CF2_GetStateContrib.py - Parse the contribution files and count totals per state house district
### Results
1. [2022HD_Contrib_byDistrict.csv](https://github.com/craigwilding/FL_CampaignContributions/blob/main/Results/State%20Races/2022HD_Contrib_byDistrict.csv) - Table of contributions per state house district
2. [2022SD_Contrib_byDistrict.csv](https://github.com/craigwilding/FL_CampaignContributions/blob/main/Results/State%20Races/2022SD_Contrib_byDistrict.csv) - Table of contributions per state senate district

## Contributing

This project has been made public for prospective employers to see as an example of data that I work with.
I am not asking for code contributions, but if you have suggestions for anything else you would like to see 
from the data, please contact me at: craig.wilding.home@gmail.com 

## License

Copyright © 2023 Craig Wilding All rights reserved.<br />
