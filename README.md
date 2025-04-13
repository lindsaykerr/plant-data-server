# AHCI PAAC data-server

Basic data server 

## Install: 
pip install -r requirements.txt

run: python3 pant_server.py

### On a fresh install:
Might have to create a 'instance' folder in project root and then create an empty plant_data.db

Then, if I can remember? Either using POSTMAN or SoupUI send a delete request to http://127.0.0.1/ap1/v1/new/db and this should rebuild the database. The other option is simply open up db file with sqlite3 terminal and run script db_schema.sql

Will update with better instructions if I have time.
