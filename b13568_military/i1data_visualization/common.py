def set_js_file(orderedlist):


	js_txt = '''

	var DATA = {
	'''

	print("\n1. Heat comparison")
	compare_txt = ''
	for m in orderedlist:
		if m['name'] not in compare_txt:
			compare_txt += "'" + str(m['name']) +"':" + str(m['price']) + ","

	js_txt += compare_txt

	# num_positive = 0

	# sentiment_txt = ",'num_positive':" + str(num_positive ) + ", 'num_neural':" + str(num_neural ) \
	#      + ",'num_nagtive':" + str(num_nagtive ) 

	# js_txt += sentiment_txt

	js_txt += " };\n"

	print(js_txt)
	with open("../movie/static/student.js", 'w') as file:
		file.write(js_txt.strip())

# set_js_file(0.3)
def set_js_file2(d):


	js_txt = '''

	var DATA_COUNT = {
	'''

	print("\n2. DATA_COUNT comparison")
	compare_txt = ''
	for key, value in d.items():
		if key not in compare_txt and value > 4:
			compare_txt += "'" + str(key) +"':" + str(value) + ","

	js_txt += compare_txt

	# num_positive = 0

	# sentiment_txt = ",'num_positive':" + str(num_positive ) + ", 'num_neural':" + str(num_neural ) \
	#      + ",'num_nagtive':" + str(num_nagtive ) 

	# js_txt += sentiment_txt

	js_txt += " };\n"

	print(js_txt)
	with open("../movie/static/student1.js", 'w') as file:
		file.write(js_txt.strip())