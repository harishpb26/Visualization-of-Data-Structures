import os
import json
import subprocess
from flask import Flask, render_template, request
from flask_cors import CORS
from cgrammar import cgrammarfunc

app = Flask(__name__)
CORS(app)
complist = []

@app.route('/')
def index():
	return render_template('home.html')

#final dictionary containing both type and value
var_dict = {}

#dictionary of types
var_type = {}

text = ""
input_text = []
flag = {"dflag" : 0}
counter = {"dcount"	:	0}

@app.route('/', methods = ['POST'])
def upload():

	global text
	text = request.form['insert_code']
	global complist
	complist = []
	input_text.clear()
	f = open("input.c","w")
	for i in text.split('\n'):
		if(i.strip()):
			print(i)
			input_text.append(i)
			f.write(i + '\n')
			complist.append(json.loads(cgrammarfunc(i, var_dict, var_type, counter, flag)))
			print('\n')
	var_dict.clear()
	var_type.clear()
	f.close()

	'''
	p = subprocess.run(["python","cgrammar.py"],stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE,check = True)
	p = subprocess.Popen(['python','cgrammar.py'], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	p = subprocess.check_output(['python','cgrammar.py'])
	stdout, stderr = p.communicate()
	#rc = p.returncode
	print(p,type(p))
	my_json = stdout.decode("utf8").replace("'",'"')
	print(my_json)
	#return json.dumps(my_json)
	'''
	return render_template('about.html')


@app.route('/anime')
def anime():
	with open("var_type.json") as f:
		data = json.load(f)
	return json.dumps(data)


@app.route('/animek')
def animek():
	iter = 0
	xpos = 120
	ypos = 60
	height = 50
	width = 120
	xppos = xpos + width * 4
	yppos = ypos
	xvpos = xppos + width * 2
	yvpos = ypos
	xtemp = xpos
	ytemp = ypos
	xptemp = xppos
	yptemp = yppos
	xvtemp = xvpos
	yvtemp = yvpos
	#data = {'s': ['struct node*', {'link': ['struct node*', '?'], 'i': ['int', '?']}], 'p': ['int*', {'p': ['int*', 1]}], 'q': ['int*', 'p'], 'r': ['int*', 'p']}
	temp = {}
	for data in complist:
		for key in data:
			if(key in temp):
				if(isinstance(data[key][1], dict) and isinstance(temp[key][1], str)):
					data[key].insert(2,temp[key][2])
					data[key].insert(3,temp[key][3])
					for content in data[key][1]:
						ytemp = ytemp + height
						data[key][1][content].insert(3, iter)
						data[key][1][content].insert(2, [xtemp,ytemp])
						if("struct" in data[key][0]):
							iter += 2
						else:
							iter+=1
					ytemp = ytemp + height * 2
					xtemp = xpos
					temp[key] = data[key]
				elif("*" in data[key][0]):
					data[key].insert(2,temp[key][2])
					data[key].insert(3,temp[key][3])
					if(isinstance(data[key][1], dict)):
						#print(data[key][1])
						for content in data[key][1]:
							#print(content)
							data[key][1][content].insert(3, temp[key][1][content][3])
							data[key][1][content].insert(2, temp[key][1][content][2])

				else:
					data[key].insert(2,temp[key][2])
					data[key].insert(3, temp[key][3])
			else:
				if("*" in data[key][0]):
					data[key].insert(2, [xptemp, yptemp])
					if(isinstance(data[key][1], dict)):
						for content_key in data[key][1]:
							ytemp = ytemp + height
							data[key][1][content_key].insert(3, iter)
							data[key][1][content_key].insert(2, [xtemp,ytemp])
							if("struct" in data[key][0]):
								iter += 2
							else:
								iter+=1
						ytemp = ytemp + height * 2
						xtemp = xpos
					yptemp = yptemp + height * 2
					data[key].insert(3, iter)
					iter += 2

				else:
					data[key].insert(2, [xvtemp,yvtemp])
					yvtemp = yvtemp+ height*2.5
					data[key].insert(3, iter)
					iter += 2
				temp[key] = data[key]
	print(complist)
	return json.dumps(complist)


@app.route('/QueueArray')
def QueueArray():
	return render_template('QueueArray.html')


@app.route('/Structure')
def Structure():
	return render_template('S.html',text = input_text)


if __name__ == '__main__':
    app.run(debug = True,port = 8080, use_reloader = False)
