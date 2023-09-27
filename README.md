# Kakeibo App
A kakeibo is a household ledger. The idea behind the kakeibo is to give the user insight in her or his consumming behaviour. 

At the beginning of the month the periodic bills are entered in the system by the system. 

At the beginning of the month a user adds the budget for the month 

Daily shopping and other expenditures are registered in the system by the user(s)

At the end of the month a dashboard is presented showing on what and where the money was spend, and if there is a balance left. 

## Architecture

 - The user interface is made with Nicegui
 - Fastapi is used to create an HTTP api for Nicegui to use
 - The programming logic is written in typed Python. 
 - The persistent data is stored in a lightweight sqlite database

The program follows the MVC layout. 

## Setup
```sh
# Install dependencies
pipenv install --dev

# Setup pre-commit and pre-push hooks
pipenv run pre-commit install -t pre-commit
pipenv run pre-commit install -t pre-push
```

## Credits
This package was created with Cookiecutter and the [sourcery-ai/python-best-practices-cookiecutter](https://github.com/sourcery-ai/python-best-practices-cookiecutter) project template.
