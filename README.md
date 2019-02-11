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

# Setup DB schema

```sh
$ python manager migrate
```

# Running the project
```sh
$ python manager runserver
```
# Running the tests

```sh

```