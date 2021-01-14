# Digital Healthcare Booking Platform
## Setup

At first, you need to install postgres database engine.

1- For linux:
```sh
sudo apt-get install libpq-dev
sudo apt install postgresql postgresql-contrib
sudo service postgresql restart
sudo -u postgres psql
ALTER USER postgres PASSWORD 'postgres';
CREATE DATABASE seapp;
GRANT ALL PRIVILEGES ON DATABASE seapp TO postgres;
```
2- You can follow the same steps through windows by downloading [postgres](https://www.postgresql.org/download/).

Then you need to clone the repository for our project:
```sh
$ git clone https://github.com/AmrAhmed11/Software-Engineering-Project
$ cd Software-Engineering-Project
```

Make sure you have python and pip installed

```sh
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ sudo apt install python3.8
$ python3 get-pip.py
```


Create a virtual environment to install dependencies in and activate it:

```sh
$ pip3 install pipenv
$ pipenv shell
```

Then install the dependencies:

```sh
cd seProject
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `pipenv`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```
, navigate to `http://127.0.0.1:8000/` and enjoy our website.

to create an admin account
```sh
(env)$ python manage.py createsuperuser
```
, navigate to `http://127.0.0.1:8000/admin`.
	1- enter users table
	2- choose your user in Groups section add admin group
	3- complete your personal information 
	4- click save
## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
(env)$ python manage.py test
```
You can also visit our deployed version of the website on heroku [here](https://seapp-ainshams.herokuapp.com/).

For more details about the [website](https://github.com/AmrAhmed11/Software-Engineering-Project) and our [user guide](https://github.com/AmrAhmed11/Software-Engineering-Project/blob/master/seProject/README.MD)