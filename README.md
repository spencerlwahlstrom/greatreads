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
`gunicorn -b 0.0.0.0:56798 -D app:app`

### To kill gunicorn
`pkill -u <username> gunicorn`

### Connect to VPN and view site at 
http://flip1.engr.oregonstate.edu:{port number}

### To stop venv
`deactivate`

## To create new requirements
`pip3 freeze > requirements.txt`