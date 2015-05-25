rosterra-server
===============

[![Build Status](https://travis-ci.org/sdob/rosterra-server.svg?branch=master)](https://travis-ci.org/sdob/rosterra-server)
[![Coverage Status](https://coveralls.io/repos/sdob/rosterra-server/badge.svg?branch=master)](https://coveralls.io/r/sdob/rosterra-server?branch=master)

This is the REST API backend for Rosterra.

Prerequisites
-------------

* Python 2.7
* git
* curl (for installing)
* PostgreSQL (for the db)

Installation
------------

1. Install pip. This might require sudo.

        $ curl -O https://bootstrap.pypa.io/get-pip.py
        $ sudo python get-pip.py

1. Install virtualenv and get it set up and activated.

        $ sudo pip install virtualenv
        $ mkdir ~/rosterra && cd ~/rosterra
        $ virtualenv venv
        $ source venv/bin/activate

1. Clone this repo.

        $ git clone https://github.com/sdob/rosterra-server.git

1. Install the required Python libraries.

        $ cd rosterra-server
        $ pip install -r requirements.txt

1. Create a Postgres user called `rosterra_user` with password `pass`,
grant the user `createdb` privileges (for creating the test database),
and create a database called `rosterra_db`. The following should work:

        $ sudo -u postgres psql -c "create user rosterra_user with password 'pass'"
        $ sudo -u postgres psql -c "alter user rosterra_user with createdb"
        $ sudo -u postgres psql -c "create database rosterra_db with owner rosterra_user"

1. You should now be able to run the tests.

        $ ./manage.py test

1. Before you can run the dev server, you'll need to migrate the database.

        $ ./manage.py migrate
        $ ./manage.py runserver

1. Check that the dev server is running. In another terminal:

        $ curl http://localhost:8000/authenticate -d "username=gorman@example.com&password=pass" -w "\n"
        {"token":"42b854989913c715b7548f4a781eb73bc5dc42e2","user":7}
        $ export TOKEN=42b854989913c715b7548f4a781eb73bc5dc42e2
        $ curl http://localhost:8000/companies -H "Authorization: Token $TOKEN" -w "\n"
        [{"id":2,"name":"Weyland-Yutani"},{"id":4,"name":"FrobozzCo"}]

1. That's it!
