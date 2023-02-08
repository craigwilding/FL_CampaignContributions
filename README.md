# Florida Campaign Contributions

This collects campaign contribution data pulled from the [FL Campaign Finance Database](https://dos.elections.myflorida.com/campaign-finance/contributions/).  I have added the campaign contributions of all [FL House and Senate candidates](https://dos.elections.myflorida.com/candidates/Index.asp) in 2022.  The Python scripts go through the contribution files and counts the campaign contributions raised in each district.

## District Comparisons
It creates a .csv file in the **Results** folder which contains counts for each district and candidate. 
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
The state-level results by house district are completed.
I will be working on repeating the excercise for state senate districts.

### County Level
I hope to expand to county-level candidates, but this requires pulling data from each of the 67 counties.

## Data Collection

I amusing the [Selenium Web Driver](https://www.selenium.dev/documentation/webdriver/) to automatically pull data from the state website.
I have not yet added the python scripts that do the web-scraping.  I will add these if I am able to add 
Selenium and the [Chrome web-driver](https://chromedriver.chromium.org/downloads) to the codespace.

### Data Processing
This is the order I am running the scripts:
#### Retrieve Data
1. CF0_GetWebFLContribHD2022.py   (NOTE: Ran outside of codespace)  This uses Selenium web driver to pull data from the Florida Contributions Database
#### Clean Data
2. CF1_FixBadData.py   - Fixes contribution files that got converted to binary due to bad data.
3. CF1a_RemoveAddressInfo.py - Remove the street address for security.  I don't want to publish a person's personal address
#### Process
4. CF2_GetStateHDContrib.py - Parse the contribution files and count totals per state house district
#### Results
5. 2022HD_Contrib_byDistrict.csv - Table of contributions per state house district
## Contributing

This project has been made public for prospective employers to see as an example of data that I work with.
I am not asking for code contributions, but if you have suggestions for anything else you would like to see 
from the data, please contact me at: craig.wilding.home@gmail.com 

## License

Copyright © 2023 Craig Wilding All rights reserved.<br />
