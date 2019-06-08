#!/bin/bash
gunicorn --config gunicorn.py 'app:create_app()'
