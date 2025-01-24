#!/bin/bash
source /root/venv/bin/activate
gunicorn wildberries.wsgi:application -w 1 -b 127.0.0.1:8000 --chdir=/root/wildberries

