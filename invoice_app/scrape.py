from flask import request, Flask, render_template

import selenium
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from .__init__ import db, app
from datetime import date

from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

import sys

sys.path.append('C:/Users/mak.leks') # necessary to import password from separate directory

from utils import password

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')

from .models import invoice_tracker
# db.create_all()
# db.session.commit()

f = 'link'
def gf():
	g = f
	return g


def scrape(driver):
	driver.get('http://erpapps2.etisalatng.com:8007/OA_HTML/RF.jsp?function_id=28636&resp_id=-1&resp_appl_id=-1&security_group_id=0&lang_code=US&params=CPYPyBAphz6mSqY84ZkFa9CXwdteotULAyPZ08oWV5OyDx56runG5TMwsLoyvdZOJdbWWAjl0gBc0Eiswu4RGQI-tfazo0hh8ETjvkZ.m3UEFx5uRepRIUkJyNBr5jVhniFOsfu757M2o8nAd-SX4S07i6wbUdGZ85p3ZpRVtVXOe-iCwpRVTwdN3.tRBEZqy2YDnvt61g1qTNiriayF94D9TwsEWur9F7ZiZEMfH3pYO8w6bycgklglxBMil4GwSwJ3Hu5TJmqn32fkWO3QHtApd3doEMIHG7jWhg2JNIwJxkaKEO7kFcu.HG5W8o1TCq.5gYAQ-Wh-HqWJfa7RZBCZSwgi.cAzs-zDHj3odxZjYaeEgH2IkPV-4e2gR-BNFMt4OZpKuRfaqU-tyAOVaWskgBXV3p1A5nS8GM58xNJRCqCzJXmaVYk.Sdfe6dhC0JfB216i1QsDI9nTyhZXk7IPHnqu6cblMzCwujK91k4l1tZYCOXSAFzQSKzC7hEZaAfV-hWKIwKlWsxPxjFRrzB-8jSp6Wra02ESHi13Il.R-t9tmJZNN9MSnf4fKdqHUn2-3ZeHwsjxx-NnELWdjvShmkPIkbqJzAWmmjdVkkM&oas=mAJMKA5Ir-JtSrW5S-U6IQ..')
	driver.find_element_by_id('usernameField').clear()
	driver.find_element_by_id('usernameField').send_keys('mak.leks')
	driver.find_element_by_id ('passwordField').send_keys(password)
	driver.find_element_by_id('SubmitButton').click()
	driver.find_element_by_link_text('EMTS Project_iProcurement').click()

	global f

	f = 'uploading files...'
	inv = request.form.getlist('invoice_no')
	# convert each pct_penalty input received from the form into a float
	pct_pen = list(map(float,request.form.getlist('pct_penalty')))
	# 
	pen_file = request.files.getlist('penalty_file')

	# scrape status message
	f ='file upload complete...'

	driver.find_element_by_link_text('Notifications Summary').click()
	driver.find_element_by_id('wfSwitchUser').click()
	driver.find_element_by_xpath("//input[@type='radio']").click()
	driver.find_element_by_css_selector('#switchUser > u:nth-child(1)').click()
	d = driver.page_source
	soup = BeautifulSoup(d,'html.parser')
	tmp1 = soup.find('table', {'class':'x1h'}).find('tbody').find_all('tr')

	# penfile = request.files["penalty_file"]
	print(pen_file)
	for pfile in pen_file:		
		if not pfile:
			pass
		else:
			pfile.save(os.path.join('C:/Users/mak.leks/Desktop/',pfile.filename))
	info = dict(zip(inv,list(zip(pct_pen,pen_file))))

	
	for row1 in tmp1[1:]:
		b = row1.find_all("td")[3]  #grab invoice cell from table
		driver.get('http://erpapps2.etisalatng.com:8007/OA_HTML/'+b.find('a')['href']) #click on erp invoice link
		c = driver.page_source
		soup = BeautifulSoup(c,'html.parser')
		data = soup.find_all('span',{'class','x2'})
		if data[6].text in info:   ### data[6].text is the invoice number
			driver.find_element_by_link_text('View Additional Invoice Details').click()
			driver.find_element_by_xpath('//button[text()="Add"]').click()
			if info[data[6].text][1].filename =='':
				driver.find_element_by_id('FileInput_oafileUpload').send_keys('C:/Users/mak.leks/Desktop/txt.txt')
			else:
				driver.find_element_by_id('FileInput_oafileUpload').send_keys('C:/Users/mak.leks/Desktop/'+info[data[6].text][1].filename) #convert path from windows syntax
			print(list(info.keys()).index(data[6].text),  "looook herererer wap")
			print(info)
			driver.find_element_by_id('FileName').send_keys('Payment Calculation')
			driver.find_element_by_id('AkDescription').send_keys(data[6].text) #file description on erp
			Select(driver.find_element_by_id('AkAttachmentCategory')).select_by_visible_text('Miscellaneous')
			driver.find_element_by_id('Okay_uixr').click()
			f = 'upload to erp..'
			driver.find_element_by_id('ReturnTo').click()
			# below, response comment is sent depending on if there is a penalty, bonus or neither.
			if info[data[6].text][0] == 0:
				driver.find_element_by_id('Response').send_keys('Invoice processed. No penalty applicable. ')#, info[data[6].text][2])
			elif info[data[6].text][0] > 0:
				driver.find_element_by_id('Response').send_keys('Invoice processed and availability/payment calculation attached. Finance to deduct service credit of ', str(info[data[6].text][0]), '% from total cost. ')#, info[data[6].text][2])
			elif info[data[6].text][0] < 0:
				driver.find_element_by_id('Response').send_keys('Invoice processed and availability/payment calculation attached. Finance to award a bonus of ', str(info[data[6].text][0]*-1), '% of total cost. ')#, info[data[6].text][2])
			f = 'Invoice penalty for '+data[6].text+' uploaded successfully..'
			#Update penalty percent and date_processed to DB
			print(inv)
			pct_ind = list(info.keys()).index(data[6].text) #get index from the "info" file to retrieve the correct penalty inputted from form 
			db.session.query(invoice_tracker).filter(invoice_tracker.invoice_number==str(data[6].text)).first().date_processed = date.today()
			db.session.query(invoice_tracker).filter(invoice_tracker.invoice_number==str(data[6].text)).first().penalty_percent = float(pct_pen[pct_ind])/100
			db.session.commit()
			driver.find_element_by_id('Ok').click()
		else:
			pass
	print(invoice_tracker.query.filter_by(invoice_number='D20031').all())
	f = 'Done!'

