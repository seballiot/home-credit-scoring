from flask import render_template, request, redirect, url_for, jsonify
from app import app

@app.route("/")
def homepage():
    return "Homepage sa mère"