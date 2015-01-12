#!/bin/bash

# Build static CSS files from less

python manage.py collectstatic --noinput
lessc serve_static/less/base.less static/css/base.css
rm -rf serve_static/*
