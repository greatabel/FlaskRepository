from common import set_js_file, set_js_file2

from csv_operation import csv_reader, csv_write
from itertools import groupby
import itertools
import operator

woods = csv_reader("i0manmadeboard.csv", "../data")
print('1sample', woods[0], "#" * 10, woods[1])
print('len=', len(woods),
	woods[0]['name'], woods[0]['price'])

mylist = []

# To sort the list in place...
# woods.sort(key=lambda x: x['price'], reverse=True)

# To return a new list, use the sorted() built-in function...
orderedlist = sorted(woods, key=lambda x: float(x['price']), reverse=True)[:5]

# orderedlist = sorted(woods, key=lambda t: t['price'], reverse=True)[:5]



print(orderedlist)
print('----#--------#--------#----')
set_js_file(orderedlist)

k_v = {}
# csv_write(mylist, 'i1one_to_one.csv')
for w in woods:
	if w['name'] not in k_v:
		k_v[w['name']] = 1

	else:
		k_v[w['name']] += 1
print(k_v)
set_js_file2(k_v)