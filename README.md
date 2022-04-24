# Pancakes

## Useful and powerful links:

* [Trello](https://trello.com/b/OrTDRL2A/projekt-przepi%C5%9Bnik)

## Technologies
* Python 3.10.2
* Django 4.0.3


## Prerequisite

1. Python
2. pip
3. Your favorite IDE

## First steps

1. clone repository

## Run

1. Change path to project path:
      
       cd .\..\..\pancakes\  

2. Activate virtual environment: 

        .\.venv\Scripts\activate 

3. Start application:
   
         python .\manage.py runserver

4. Deactivate environment:

         deactivate

## Migration
When you change structure of models(adding a field, deleting a model, etc.). You have to to make migration.

1. Make migration:

        python .\manage.py makemigrations mainApp

2. Apply migration:

        python .\manage.py migreate


## TODO

* split unit and integration tests
