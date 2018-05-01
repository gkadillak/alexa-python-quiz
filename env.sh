#!/bin/bash

workon quiz_game

export FLASK_DEBUG=1
export FLASK_APP='python_quiz/app.py'
export DATABASE_URL='postgresql://localhost:5432/python_quiz'
export APP_SETTINGS='python_quiz.config.DevelopmentConfig'