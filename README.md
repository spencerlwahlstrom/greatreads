# Step 4 Draft Version Update

### What works
All CRUD steps for the Books entity are functional and wired up to the DB. Read, Update, and Delete
work for the M:M intersection table Authors_Books as a bonus (everything but Create). 

### What doesn't work
All other entities (Authors, Reviews, Genres, Books_Genres) are not wired up to the DB yet and
consist of sample data from the previous draft. The Authors_Books page has a filter dropdown and a 
form for adding a new Author to Book relationship, both of which are not yet functional.

### Where/why you are blocked
No blockers, we are excited to implement CRUD for the remaining entities and to make the app prettier!

# Quick start guide

### Create a .env like the below, fill username and password
```
340DBHOST=classmysql.engr.oregonstate.edu
340DBUSER=cs340_username
340DBPW=XXXX
340DB=cs340_username
```

### Create a virtual environment

`pip3 install --user virtualenv`

`python3 -m venv ./venv`

### Start the venv
`source ./venv/bin/activate`

### While venv is running, install requirements
`pip3 install -r requirements.txt`

### To run/debug locally
`python3 app.py`

### To run with gunicorn in the background (forever)
`gunicorn -b 0.0.0.0:56879 -D app:app`

### To kill gunicorn
`pkill -u <username> gunicorn`

### Connect to VPN and view site at 
http://flip1.engr.oregonstate.edu:{port}

### To stop venv
`deactivate`

## To create new requirements
`pip3 freeze > requirements.txt`
