import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

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

# Create Tables Automatically
with app.app_context():
    db.create_all()

# Home Page Route
@app.route('/')
def index():
    campaigns = Campaign.query.order_by(Campaign.id.desc()).all()
    return render_template('index.html', campaigns=campaigns)

# Create Campaign Route (Isi ki wajah se 404 aa raha tha)
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        patient_name = request.form.get('patient_name')
        disease_en = request.form.get('disease_en')
        disease_hi = request.form.get('disease_hi')
        disease_ur = request.form.get('disease_ur')
        description = request.form.get('description')
        target_amount = request.form.get('target_amount')
        account_holder = request.form.get('account_holder')
        account_number = request.form.get('account_number')
        ifsc_code = request.form.get('ifsc_code')
        upi_id = request.form.get('upi_id')

        file = request.files.get('document_file')
        filename = ''
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_campaign = Campaign(
            patient_name=patient_name,
            disease_en=disease_en,
            disease_hi=disease_hi,
            disease_ur=disease_ur,
            description=description,
            target_amount=float(target_amount) if target_amount else 0.0,
            account_holder=account_holder,
            account_number=account_number,
            ifsc_code=ifsc_code,
            upi_id=upi_id,
            document_file=filename
        )
        db.session.add(new_campaign)
        db.session.commit()
        return redirect(url_for('index'))
             return render_template('create_campaign.html')
    @app.route('/donate/<int:id>', methods=['POST'])
    def donate(id):
        campaign = Campaign.query.get_or_404(id)
        amount = float(request.form.get('amount', 0))
        campaign.raised_amount += amount
        db.session.commit()
        return redirect(url_for('index'))

   

       
