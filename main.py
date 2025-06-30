from flask import Flask, render_template, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conversion_history.db'
db = SQLAlchemy(app)

class ConversionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_value = db.Column(db.Float, nullable=False)
    input_unit = db.Column(db.String(10), nullable=False)
    output_value = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Conversion logic
def convert(value, mode):
    try:
        val = float(value)
        if mode == "miles_to_km":
            return f"{val * 1.60934:.2f} km"
        elif mode == "km_to_miles":
            return f"{val / 1.60934:.2f} miles"
        elif mode == "km_to_hours":
            return f"{val / 60:.2f} hours"
        elif mode == "hours_to_km":
            return f"{val * 60:.2f} km"
        elif mode == "miles_to_hours":
            return f"{val / 60:.2f} hours"
        elif mode == "hours_to_miles":
            return f"{val * 60:.2f} miles"
        else:
            return "Invalid conversion"
    except ValueError:
        return "Invalid input"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        value = request.form['value']
        conversion = request.form['conversion']
        result = convert(value, conversion)

        # Optional: record to DB
        record = ConversionRecord(
            input_value=value,
            input_unit=conversion,
            output_value=result
        )
        db.session.add(record)
        db.session.commit()

    return render_template('index.html', result=result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)