import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'medfund_talha_secret_key_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ----------------- DATABASE MODEL -----------------
class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    disease_en = db.Column(db.String(200), nullable=False)
    disease_hi = db.Column(db.String(200), nullable=True)
    disease_ur = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=False)
    
    target_amount = db.Column(db.Float, nullable=False)
    raised_amount = db.Column(db.Float, default=0.0)
    
    # Direct Bank Details
    account_holder = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(50), nullable=False)
    ifsc_code = db.Column(db.String(20), nullable=False)
    upi_id = db.Column(db.String(100), nullable=True)
    
    # Medical Proof Document
    document_file = db.Column(db.String(200), nullable=False)

    @property
    def progress_percentage(self):
        if self.target_amount > 0:
            percent = (self.raised_amount / self.target_amount) * 100
            return min(round(percent, 1), 100)
        return 0

# ----------------- ROUTES -----------------
@app.route('/')
def home():
    campaigns = Campaign.query.order_by(Campaign.id.desc()).all()
    return render_template('index.html', campaigns=campaigns)

@app.route('/create', methods=['GET', 'POST'])
def create_campaign():
    if request.method == 'POST':
        p_name = request.form.get('patient_name')
        d_en = request.form.get('disease_en')
        d_hi = request.form.get('disease_hi')
        d_ur = request.form.get('disease_ur')
        desc = request.form.get('description')
        target = float(request.form.get('target_amount'))
        
        acc_holder = request.form.get('account_holder')
        acc_num = request.form.get('account_number')
        ifsc = request.form.get('ifsc_code')
        upi = request.form.get('upi_id')
        
        file = request.files.get('document')
        filename = "default.pdf"
        if file and file.filename != '':
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_campaign = Campaign(
            patient_name=p_name,
            disease_en=d_en,
            disease_hi=d_hi if d_hi else d_en,
            disease_ur=d_ur if d_ur else d_en,
            description=desc,
            target_amount=target,
            account_holder=acc_holder,
            account_number=acc_num,
            ifsc_code=ifsc,
            upi_id=upi,
            document_file=filename
        )
        
        db.session.add(new_campaign)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('create_campaign.html')

@app.route('/donate/<int:campaign_id>', methods=['POST'])
def donate(campaign_id):
    amount = float(request.form.get('amount'))
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.raised_amount += amount
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)