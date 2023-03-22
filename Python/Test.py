import os
import shutil
import pandas
import Python.PandasTransforms_Old as PTX
import sys
sys.path.insert(0, '/workspaces/vscode-remote-try-python/PostgreSQL')
import SQLCommands as SQL

wrksp = "/workspaces/vscode-remote-try-python/DATA//State Races"
dirHDContrib = os.path.join(wrksp, "2022HD")

os.chdir(wrksp)

print(os.getcwd())

with SQL.Connect() as conn :
    SQL.SelectCountWhere(conn, "contributions", "")
# end with conn
