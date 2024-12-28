import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define the Advertisement model
class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    society = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    website = db.Column(db.String(200))
    offer = db.Column(db.String(200))
    visit_details = db.Column(db.String(200))

# Initialize the database
with app.app_context():
    db.create_all()

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def homepage():
    selected_society = request.args.get('society', '')
    index = int(request.args.get('index', 0))

    # Filter ads based on the selected society
    if selected_society:
        ads = Advertisement.query.filter_by(society=selected_society).all()
    else:
        ads = Advertisement.query.all()

    # Determine the ad to display
    ad_count = len(ads)
    if ad_count == 0:
        ad = None
    else:
        ad = ads[index % ad_count]

    # Prepare indices for navigation
    next_index = (index + 1) % ad_count if ad_count > 0 else 0
    previous_index = (index - 1) % ad_count if ad_count > 0 else 0

    # Get unique societies for the filter dropdown
    societies = [ad.society for ad in Advertisement.query.distinct(Advertisement.society)]
    current_year = datetime.now().year

    return render_template(
        'homepage.html',
        ad=ad,
        societies=societies,
        selected_society=selected_society,
        next_index=next_index,
        previous_index=previous_index,
        current_year=current_year
    )

@app.route('/add-ad', methods=['GET', 'POST'])
def add_ad():
    ADD_AD_PASSWORD = "securepassword123"

    if request.method == 'POST':
        # Validate password
        password = request.form.get('password')
        if password != ADD_AD_PASSWORD:
            return "Unauthorized: Invalid password", 403

        # Get form data
        society = request.form['society']
        title = request.form['title']
        description = request.form['description']
        website = request.form['website']
        offer = request.form['offer']
        visit_details = request.form['visit_details']

        # Handle image upload
        img_file = request.files.get('img')
        if img_file and img_file.filename != '':
            filename = secure_filename(img_file.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img_file.save(img_path)
            img_url = f"{app.config['UPLOAD_FOLDER']}/{filename}"
        else:
            img_url = None

        # Save ad to the database
        new_ad = Advertisement(
            society=society,
            title=title,
            description=description,
            img_url=img_url,
            website=website,
            offer=offer,
            visit_details=visit_details
        )
        db.session.add(new_ad)
        db.session.commit()

        return redirect(url_for('homepage'))

    return render_template('add_ad.html')

if __name__ == '__main__':
    app.run(debug=True)
