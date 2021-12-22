# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
import json
import requests
import time
import re
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config.update(dict(
    DEBUG=True,
))

with open('log.txt') as f:
    my_list = list(f)
#get bad user agents
with open('bad-user-agents.txt') as f2:
    bad_list = list(f2)


@app.route("/")
def index():
  
    return render_template("index.html") # render the page

@app.route("/search")
def search():
	text = request.args['searchText'] # get the text to search for
	isCheck = request.args['isCheck']


	result = [c for c in my_list if str(text).lower() in c.lower()]
	ip_list = [None]*len(result)
	ip_list6 = [None]*len(result)
	match_list = [None]*len(result)

	for i in range(len(result)):
		try: 
			ip_list[i] = re.findall( r'[0-9]+(?:\.[0-9]+){3}', result[i])[0]
			result[i] = result[i].replace(ip_list[i],'')
		except:
			pass
		try:
			ip_list6[i] = re.findall(r'^(2.*)[\s][a]', result[i])[0] 
			result[i] = result[i].replace(ip_list6[i],'')
		except:
			pass
	'''
		for j in range(len(bad_list)):
			try:
				#seach for bad user agents j in result i 
				print("scanning in result[" + i +"]" + "for " + bad_list[j])
				if (result[i].find(bad_list[j])): 
					print("match = " + result[i].find(bad_list[j]))
			except:
				print("No match found!")

	'''	
	# return as JSON	
	return json.dumps(
		{"results":result, "isCheck": isCheck, "ip_list" : ip_list, "ip_list6": ip_list6, "searchText": text, "match" : match_list}
		, ensure_ascii=False).encode('utf8')

if __name__ == "__main__":
    app.run()