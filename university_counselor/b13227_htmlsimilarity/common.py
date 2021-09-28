def set_js_file(score):
	not_p = 5
	p = 4

	num_positive = 3
	num_neural = 1
	num_nagtive = 3

	# judage the pass this assignment by similrity 80%
	if score >= 0.8:
		p += 1
	else:
		not_p += 1 

	if score  >= 0.8:
		num_positive += 1
	elif (score < 0.8 and score > 0.6):
		num_neural += 1
	else:
		num_nagtive += 1

	js_txt = '''

	var DATA = {
	'''

	print("\n1. Heat comparison")

	compare_txt = "'not_pass':" + str(not_p) + ", 'pass':" + str(p)
	js_txt += compare_txt

	sentiment_txt = ",'num_positive':" + str(num_positive ) + ", 'num_neural':" + str(num_neural ) \
	     + ",'num_nagtive':" + str(num_nagtive ) 

	js_txt += sentiment_txt

	js_txt += " };\n"

	print(js_txt)
	with open("movie/static/student.js", 'w') as file:
		file.write(js_txt.strip())

# set_js_file(0.3)