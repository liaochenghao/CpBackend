#!/bin/bash
ps -aux | grep 800 | awk '{print $2}' | xargs kill -9
gunicorn CpBackend.wsgi:application -b 0.0.0.0:8000 -w 4 -t 300 --reload