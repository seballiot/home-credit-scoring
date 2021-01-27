from app import db


class HomeCreditColumnsDescription(db.Model):
    field1 = db.Column(db.Integer, primary_key=True)
    Table = db.Column(db.String(120))
    Row = db.Column(db.String(120))
    Description = db.Column(db.String(120))
    Special = db.Column(db.String(120))


class Bureau(db.Model):
    SK_ID_CURR = db.Column(db.Integer, primary_key=True)
    SK_ID_BUREAU = db.Column(db.Integer, primary_key=True)
    CREDIT_ACTIVE = db.Column(db.String(120))
    CREDIT_CURRENCY = db.Column(db.String(120))
    DAYS_CREDIT = db.Column(db.Integer)
    CREDIT_DAY_OVERDUE = db.Column(db.Integer)
    DAYS_CREDIT_ENDDATE = db.Column(db.String(120))
    DAYS_ENDDATE_FACT = db.Column(db.String(120))
    AMT_CREDIT_MAX_OVERDUE = db.Column(db.String(120))
    CNT_CREDIT_PROLONG = db.Column(db.Integer)
    AMT_CREDIT_SUM = db.Column(db.Float)
    AMT_CREDIT_SUM_DEBT = db.Column(db.String(120))
    AMT_CREDIT_SUM_LIMIT = db.Column(db.String(120))
    AMT_CREDIT_SUM_OVERDUE = db.Column(db.Float)
    CREDIT_TYPE = db.Column(db.String(120))
    DAYS_CREDIT_UPDATE = db.Column(db.Integer)
    AMT_ANNUITY = db.Column(db.String(120))


class ApplicationTrain(db.Model):
    SK_ID_CURR = db.Column(db.Integer, primary_key=True)
    TARGET = db.Column(db.Integer)
    NAME_CONTRACT_TYPE = db.Column(db.String(120))
    CODE_GENDER = db.Column(db.String(120))
    FLAG_OWN_CAR = db.Column(db.String(120))
    FLAG_OWN_REALTY = db.Column(db.String(120))
    CNT_CHILDREN = db.Column(db.Integer)
    AMT_INCOME_TOTAL = db.Column(db.Float)
    AMT_CREDIT = db.Column(db.Float)
    AMT_ANNUITY = db.Column(db.Float)
    AMT_GOODS_PRICE = db.Column(db.Float)
    NAME_TYPE_SUITE = db.Column(db.String(120))
    NAME_INCOME_TYPE = db.Column(db.String(120))
    NAME_EDUCATION_TYPE = db.Column(db.String(120))
    NAME_FAMILY_STATUS = db.Column(db.String(120))
    NAME_HOUSING_TYPE = db.Column(db.String(120))
    REGION_POPULATION_RELATIVE = db.Column(db.String(120))
    DAYS_BIRTH = db.Column(db.Integer)
