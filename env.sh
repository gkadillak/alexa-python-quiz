#!/bin/bash

workon quiz_game

export TESTING_DATABASE_URL='postgresql://localhost:5432/test_python_quiz'
export APP_SETTINGS='python_quiz.configs.flask_configs.DevelopmentConfig'
export FLASK_APP='python_quiz/app.py'
