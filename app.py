import os
from .models import invoice_tracker
from flask import Flask, render_template, redirect, flash, request, url_for, Markup, send_file
from .__init__ import app, db
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
import flask_login
from flask_login import LoginManager, UserMixin, login_user, \
login_required, logout_user, current_user
from flask_socketio import SocketIO, emit, send
from flask_table import Table, Col, LinkCol

import selenium
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select


socketio = SocketIO(app)

from .scrape import scrape, gf


# status tracking variables
global de
de = ['rep']



@app.route('/download/<vendor>')
def download_file(vendor):

	if "NOKIA" in vendor:
		path = "penalty_templates/nokia.xlsx"
		return send_file(path, as_attachment=True, cache_timeout=0)
	elif "HUAWEI" in vendor:
		path = "penalty_templates/huawei.xlsx"
		print(path)
		return send_file(path, as_attachment=True, cache_timeout=0)
	elif "AVIAT" in vendor:
		path = "penalty_templates/aviat.xlsx"
		return send_file(path, as_attachment=True, cache_timeout=0)
	elif "SPROUT" in vendor:
		path = "penalty_templates/sprout.xlsx"
		return send_file(path, as_attachment=True, cache_timeout=0)
	elif "TESMARK" in vendor:
		path = "penalty_templates/tesmark.xlsx"
		return send_file(path, as_attachment=True, cache_timeout=0)
	elif "BELL-X" in vendor:
		path = "penalty_templates/bell-x.xlsx"
		return send_file(path, as_attachment=True, cache_timeout=0)




@app.route("/", methods=['GET','POST'])
def penalty_upload():
	# query the invoice_tracker database 
	object_query = invoice_tracker.query.filter_by(date_processed=None)
	
	# execute the query and return only 4 columns
	query_df = pd.read_sql(object_query.statement,object_query.session.bind)[['vendor_name','invoice_number','invoice_amount']]
	query_df['invoice_amount'] = query_df['invoice_amount'].map('{:,.2f}'.format) # convert to string format with comma thousands separators

	# create an iterable list
	rows = list(range(len(query_df)))

	# items = invoice_tracker.query.filter_by(date_processed=None).all()
	# pending = ItemTable(items)

	# pending = Markup(query_df.to_html(classes=['table','table-hover','table-sm'], id='tbh'))
	# global f
	# f = '' # track status inside the 

	# launch the scrape function if the submit button is clicked on the form
	if request.method == "POST":
		driver = webdriver.Chrome(ChromeDriverManager().install())
		driver.implicitly_wait(100)
		scrape(driver=driver)

		f = 'Done!'
		query_df = pd.read_sql(object_query.statement,object_query.session.bind)[['vendor_name','invoice_number','invoice_amount']]
		query_df['invoice_amount'] = query_df['invoice_amount'].map('{:,.2f}'.format) 
		rows = list(range(len(query_df)))
		return ('', 204)
		return render_template("index.html", rows=rows, query_df=query_df)
		

	return render_template("index.html", rows=rows, query_df=query_df)

# socket module to transfer "heartbeat" messages between client and server and also communicate progress of the scrape

@socketio.on('message')
def handleMessage(msg):
	print('Message: '+ msg)
	f = gf()
	de.append(f)
	if de[-1]=='': # checks if status has changed
		pass
	else:
		send(de[-1], broadcast=True) # sends current status to JS front-end
if __name__=='__main__':
	socketio.run(app)