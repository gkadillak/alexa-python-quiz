#!/usr/bin/env bash

export APP_SETTINGS='python_quiz.configs.flask_configs.ProductionConfig'
export FLASK_APP='python_quiz/app.py'


export DATABASE_URL="postgresql://$DATABASE_USERNAME:$DATABASE_PASSWORD@localhost/python_quiz"
