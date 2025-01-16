from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wilayah.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model Database
class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    districts = db.relationship('District', backref='region', lazy=True)

class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    subdistricts = db.relationship('Subdistrict', backref='district', lazy=True)

class Subdistrict(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)

# Endpoint untuk melihat semua data
@app.route('/', methods=['GET'])
def documentation():
    return render_template('index.html')

@app.route('/regions', methods=['GET'])
def get_regions():
    regions = Region.query.all()
    result = [
        {
            'id': region.id,
            'name': region.name,
        } for region in regions
    ]
    return jsonify(result)

@app.route('/regions/<int:id>', methods=['GET'])
def get_region_by_id(id):
    region = Region.query.get(id)
    if not region:
        return jsonify({'message': 'Region not found'}), 404

    result = {
        'id': region.id,
        'name': region.name,
    }
    return jsonify(result)

@app.route('/districts', methods=['GET'])
def get_districts():
    districts = District.query.all()
    result = [
        {
            'id': district.id,
            'name': district.name,
            'region_id': district.region_id,
        } for district in districts
    ]
    return jsonify(result)

@app.route('/districts/<int:id>', methods=['GET'])
def get_district_by_id(id):
    district = District.query.get(id)
    if not district:
        return jsonify({'message': 'District not found'}), 404

    result = {
        'id': district.id,
        'name': district.name,
        'region_id': district.region_id,
    }
    return jsonify(result)

@app.route('/subdistricts', methods=['GET'])
def get_subdistricts():
    subdistricts = Subdistrict.query.all()
    result = [{'id': sub.id, 'name': sub.name, 'district_id': sub.district_id} for sub in subdistricts]
    return jsonify(result)

@app.route('/subdistricts/<int:id>', methods=['GET'])
def get_subdistrict_by_id(id):
    subdistrict = Subdistrict.query.get(id)
    if not subdistrict:
        return jsonify({'message': 'Subdistrict not found'}), 404

    result = {'id': subdistrict.id, 'name': subdistrict.name, 'district_id': subdistrict.district_id}
    return jsonify(result)

# Initializer untuk membuat database
with app.app_context():
    db.create_all()