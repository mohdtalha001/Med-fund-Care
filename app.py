import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Database Model
class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100))
    disease_en = db.Column(db.String(100))
    disease_hi = db.Column(db.String(100))
    disease_ur = db.Column(db.String(100))
    description = db.Column(db.Text)
    target_amount = db.Column(db.Float)
    raised_amount = db.Column(db.Float, default=0.0)
    account_holder = db.Column(db.String(100))
    account_number = db.Column(db.String(50))
    ifsc_code = db.Column(db.String(20))
    upi_id = db.Column(db.String(50))
    document_file = db.Column(db.String(200))

# Create Tables Automatically before the first request
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    campaigns = Campaign.query.order_by(Campaign.id.desc()).all()
    return render_template('index.html', campaigns=campaigns)
