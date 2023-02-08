import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

Downloads = "/workspaces/vscode-remote-try-python/DATA/Downloads"
pathToChrome = "/workspaces/vscode-remote-try-python/DATA/Downloads/chromedriver.exe"
os.environ['PATH'] += pathToChrome
print("chromePath = " + pathToChrome)
service = Service(executable_path=pathToChrome)

# browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver = webdriver.Chrome(pathToChrome)
# driver = webdriver.Chrome(pathToChrome, options=options)
# driver = webdriver.Chrome(service=service)

#service = ChromeService(executable_path=ChromeDriverManager().install())
#driver = webdriver.Chrome(service=service)