#!/bin/bash
gunicorn --config gunicorn_config.py bot.bot:main
