# DEAL@DIROX 
## SERVER
* Admin page
* Login
* Logout
* Register google and hubspot token
* get google token
* fetch data from hubspot
### Requirement
* python 3.8
* django 

### Usage
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
* Setting up server:
```
$ cd server
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```
* Create superuser
```
$ python3 manage.py createsuperuser
```
* Run server:
```
$ python3 manage.py runserver
```
* Open web browser and go to admin page to manage server: 
http://127.0.0.1:8000/accounts/user/admin
* Send http request to server to call service

### API document
#### 1. Login
```
POST /accounts/user/login HTTP/1.1
Content-Type: multipart/form-data

user_id: username or email
password: password
```
#### 2. Logout (login require)
```
GET /accounts/user/logout HTTP/1.1
Cookie: sessionid=LOGIN_SESSION_ID
```
#### 3. Register google and hubspot token (login require)
```
GET /accounts/google/auth HTTP/1.1
Cookie: sessionid=LOGIN_SESSION_ID
GET /accounts/hubspot/auth HTTP/1.1
Cookie: sessionid=LOGIN_SESSION_ID
```
#### 4. Get google token (login require)
```
GET /google/services/token HTTP/1.1
Cookie: sessionid=LOGIN_SESSION_ID
```
#### 5. Fetch make offer deals (login require)
```
GET /hubspot/deals/makeoffer/all HTTP/1.1
Cookie: sessionid=LOGIN_SESSION_ID
```
## UI

### Install dependencies
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).