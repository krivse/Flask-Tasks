# Flask-Tasks

#### Flask-Tasks is a simple web application that allows users to create, view and update tasks. The application is written in Python using the Flask framework and the MySQL database.

#### The following methods are implemented
~~~
[GET] /tasks: This method is used to get a list of all tasks from the database.

[GET] /tasks/{id}: This method is used to get information about a specific task by its ID.

[POST] /tasks: This method is used to create a new task in the database.

[PUT] /tasks/{id}: This method is used to update information about a task by its ID.

[DELETE] /tasks/{id}: This method is used to delete a task by its ID.
~~~

#### The default path to the swagger documentation:
~~~
The default path to the swagger documentation: http://127.0.0.1:8000/docs
~~~

#### Launch the application with docker-compose:
~~~~
docker-compose up -d
~~~~

#### Local launch of the application
~~~
flask run --host=0.0.0.0 --port=8000
~~~

##### Author 
*__Ivan Krasnikov__*