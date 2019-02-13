# Consumer Affairs - Backend practical test

-- Acceptance Criteria

 - The completed assignment must be hosted in a git repository
 - The repository must include commit history (e.g., more than one commit)
 - Users are able to submit reviews to the API
 - Users are able to retrieve reviews that they submitted
 - Users cannot see reviews submitted by other users
 - Use of the API requires a unique auth token for each user
 - Submitted reviews must include, at least, the following attributes:
   - Rating - must be between 1 - 5
   - Title - no more than 64 chars
   - Summary - no more than 10k chars
   - IP Address - IP of the review submitter
   - Submission date - the date the review was submitted
   - Company - information about the company for which the review was submitted, can be simple text (e.g., name, company id, etc.) or a separate model altogether
   - Reviewer Metadata - information about the reviewer, can be simple text (e.g., name, email, reviewer id, etc.) or a separate model altogether
 - Unit tests must be included providing 100% code coverage
 - Include instructions on local setup details for both “app setup” and “data setup”
 - Document the API

 -- Optional: 
 - Provide an authenticated admin view that allows me to view review submissions

# Instalation

Requeriments: **Python 3.7**

-- Using with ```pyenv``` and ```pipenv``` go to the root of the project:
```sh
$ pipenv install --dev
```

-- Using with `virtualenv` make sure you are with the environment activated:
```sh
$ pip install -r requirements.txt
```


All the projects dependeces will be installed


**If you are using `pipenv`just add before the commands `pipenv run` or run `pipenv shell` to load the `virtualenv`**

# Running the tests
```sh
$ pytest
```

# Setup DB schema
```sh
$ python manager migrate
```

# Creating superuser to access admin page
```sh
$ python manage.py createsuperuser
```

# Running the project
```sh
$ python manager runserver
```

# Access to admin page
Open your browser and access the url `http://<project host:port>/admin` and use the credentials created before

# Setup basic informations
After logged at admin with the user created before, click on `Tokens` link inside the `AUTH TOKEN` session.

 - To create new tokens for existent users, click on the top righ link `ADD TOKEN +`, select the user and click on save
 - To create new tokens for a new user, click on the top righ link `ADD TOKEN +`, setup a new user and click on save

 In that session is possible see all the tokens allowed for the users in the requests.
 **Use this page to get token info used to authorize the API** 

# API

**Make sure to have a token already generated at admin (previews step)**

**List all the APIs available** 
```sh
$ curl -H "Content-type: application/json" -H 'Authorization: Token <user token from admin>' 'http://127.0.0.1:8000/'
```
this will return
```javascript
{"company":"http://127.0.0.1:8000/company/","review":"http://127.0.0.1:8000/review/"}
```

**Create new review**
```sh
$ curl -XPOST -H "Content-type: application/json" -H 'Authorization: Token <user token from admin>' -d '{
    "rating": 4,
    "title": "My first review",
    "summary": "This is my first review for this API",
    "company": {
        "name": "google",
        "description": "provide add everywhere"
    }
 }' 'http://127.0.0.1:8000/review/'
```
this will return the review created
```javascript
{
    "rating":4,
    "title":"My first review",
    "summary":"This is my first review for this API",
    "ip_address":"127.0.0.1",
    "submission_date":"2019-02-13T11:31:11.322733Z",
    "company":{
        "name":"google",
        "description":"provide add everywhere"},
    "reviewer":{
        "user":{
            "username":"test",
            "email":""},
    "key":<user token from admin>}}
```

**List all reviews create by the user**
```sh
$ curl -H "Content-type: application/json" -H 'Authorization: Token <user token from admin>' 'http://127.0.0.1:8000/review/'
```
This will return the list of reviews created by the user
```javascript
[{
    "rating":4,
    "title":"My first review",
    "summary":"This is my first review for this API",
    "ip_address":"127.0.0.1",
    "submission_date":"2019-02-13T11:31:11.322733Z",
    "company":{
        "name":"google",
        "description":"provide add everywhere"},
    "reviewer":{
        "user":{
            "username":"test",
            "email":""},
    "key":<user token from admin>}}]
```

# Bonus task
If enable the user to use admin with review access, the user will just see yours reviews, although if the user is a superuser, in that case the user will see all reviews created.
