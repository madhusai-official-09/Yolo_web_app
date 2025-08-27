#!/bin/bash
# simple start script for local testing
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
echo "Place your model (e.g. yolo11s.pt) in this folder before running."
python app.py
