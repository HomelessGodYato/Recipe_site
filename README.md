~~# Pancakes

## Useful and powerful links:

* [Trello](https://trello.com/b/OrTDRL2A/projekt-przepi%C5%9Bnik)

## Technologies
* Python 3.10.2
* Django 4.0.3
* Docker 20.10.13 

## Prerequisite

1. Python
2. pip
3. Docker
4. Your favorite IDE
5. Optional pgAdmin environment

## First steps

1. clone repository

         git clone https://github.com/PRz-IO/p01gr02-przepisy-zespol-gr02.git

2. Start container

         docker-compose up -d

3. When it is done, you have to open second terminal and make migrations

          python manage.py makemigrations

4.  Apply migration:

          python manage.py migrate

## Run

1. Change path to project path:
      
       cd .\..\..\pancakes\

2. Start db container:
   
         docker-compose up 
3. Start application:

         python manage.py runserver

4. App is listening on address "http://localhost:8000/"

## Migration
When you change structure of models(adding a field, deleting a model, etc.). You have to to make migration.

1. Make migration:

        python manage.py makemigrations

2. Apply migration:

        python manage.py migrate

