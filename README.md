# Company-management
A company management system that allow a general admin to create and remove companies and allow company admins to add or remove employees to the company or to teams.


### Requirements to run locally:

* Linux-based system
* [Python 3.6](https://www.python.org/)

### Installation:
##### System Dependencies:
1. Install pip and vitualenv:  
`sudo apt-get install -y virtualenv`  
`sudo apt-get install -y python3-pip`
2. Create a virtual environment:  
`virtualenv -p python3 ~/.virtualenvs/company_management`
3. Activate `company_management` virtual environment:  
`source ~/.virtualenvs/company_management/bin/activate`
4. Install requirements in the virtual environment:  
`pip3 install -r requirements.txt`
5. Run the project:  
`python manage.py runserver`

##### Relational database dependencies (PostgreSQL):
1. Install components for Ubuntu:  
`sudo apt-get update`  
`sudo apt-get install python-dev libpq-dev postgresql postgresql-contrib`
2. Switch to **postgres** (PostgreSQL administrative user):  
`sudo su postgres`
3. Log into a Postgres session:  
`psql`
4. Create database with name **company_management**:  
`CREATE DATABASE company_management;`
5. Create a database user which we will use to connect to the database:  
`CREATE USER company_management_user WITH PASSWORD 'company_management_pass';`
6. Modify a few of the connection parameters for the user we just created:  
`ALTER ROLE company_management_user SET client_encoding TO 'utf8';`  
`ALTER ROLE company_management_user SET default_transaction_isolation TO 'read committed';`  
`ALTER ROLE company_management_user SET timezone TO 'UTC';` 
7. Give our database user access rights to the database we created:  
`GRANT ALL PRIVILEGES ON DATABASE company_management TO company_management_user;`
8. Exit the SQL prompt and the postgres user's shell session:  
`\q` then `exit`
9. Activate the virtual environment:  
`source ~/.virtualenvs/company_management/bin/activate`
10. Make Django database migrations:
`python manage.py makemigrations`  
then: `python manage.py migrate`

##### Use admin interface:
1. Create an admin user:  
`python manage.py createsuperuser`
2. Run the project locally:  
`python manage.py runserver`
3. Navigate to: `http://localhost:8000/admin/`