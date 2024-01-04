#!/bin/bash

# Start the Django application
gunicorn -c task/gunicorn_config.py task.wsgi:application
