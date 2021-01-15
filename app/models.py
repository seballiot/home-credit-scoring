from app import db


class HomeCreditColumnsDescription(db.Model):
    field1 = db.Column(db.Integer, primary_key=True)
    Table = db.Column(db.String(120))
    Row = db.Column(db.String(120))
    Description = db.Column(db.String(120))
    Special = db.Column(db.String(120))
