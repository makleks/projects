from sqlalchemy import ForeignKey, MetaData, Table
from sqlalchemy.orm import relationship
from .__init__ import db
from sqlalchemy.ext.automap import automap_base




class table_name(db.Model):

	index = db.Column(db.Integer, primary_key=True)
	supplier = db.Column(db.String, nullable=False)
	invoice = db.Column(db.String, nullable=False)
	amount = db.Column(db.Float, ForeignKey('users.id'))
	
	def __init__(self, title, description, author_id):
		self.supplier = supplier
		self.invoice = invoice
		self.amount = amount

class invoice_tracker(db.Model):
    __tablename__ = 'invoice_tracker'
    __table_args__ = {'extend_existing': True} 
    #index = db.Column(db.Integer, primary_key=True)
    index =db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String)
    sub_type = db.Column(db.String)
    vendor_name = db.Column(db.String)
    invoice_number = db.Column(db.String)
    invoice_amount = db.Column(db.Float)
    description = db.Column(db.String)
    service_period = db.Column(db.String)
    year = db.Column(db.String)
    date_received = db.Column(db.Date)
    date_processed = db.Column(db.Date)
    sla_received = db.Column(db.Date)
    comments = db.Column(db.String)
    penalty_percent = db.Column(db.Float)
    penalty_amount = db.Column(db.Float)
    
    def __init__(self, title, description, author_id):
        self.index = index
        self.service_type = service_type
        self.sub_type = sub_type
        self.vendor_name = vendor_name
        self.invoice_number = invoice_number
        self.invoice_amount = invoice_amount
        self.description = description
        self.service_period = service_period
        self.year = year
        self.date_received = date_received
        self.date_processed = date_processed
        self.sla_received = sla_received
        self.comments = comments
        self.penalty_percent = penalty_percent
        self.penalty_amount = penalty_amount
    def __repr__(self):
        return "<User(index='%s', service_type='%s', sub_type='%s', vendor_name='%s', invoice_number='%s', invoice_amount='%s', \
        description='%s', service_period='%s', year='%s', date_received='%s', \
        date_processed='%s', sla_received='%s', comments='%s', penalty_percent='%s', penalty_amount='%s')>" % (self.index, self.service_type, self.sub_type, self.vendor_name,\
        self.invoice_number, self.invoice_amount, self.description, self.service_period, \
        self.year, self.date_received, self.date_processed, self.sla_received, self.comments, self.penalty_percent, self.penalty_amount)
