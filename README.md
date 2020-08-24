# DEAL AT DIRROX SERVER
* get google token
* get hubspot token (in development)
* fetch data from hubspot (in development)

## Requirement
* python 3.8
* django 
* authlib
* requests

## Usage
* Clone project from git.dirox.net:
```
git clone https://git.dirox.net/phuocnl/deal-dirox.git
```
* Switch to branch Server:
```
$ cd deal-dirox
$ git checkout Server
```
* Install dependencies and create a virtual environment:
```
$ pipenv install
$ pipenv shell --three
```
* Run server:
```
$ cd server
$ python3 manage.py runserver
```
* Open browser
* Enter http://127.0.0.1:8000/google/auth to get google access token
* Enter http://127.0.0.1:8000/hubspot/deals/makeoffer/all to fetch all make offer deals from hubspot (make sure you had updated a new token at line 43 in file views.py in ./deal-dirox/server/django_server/dealatdirox/)