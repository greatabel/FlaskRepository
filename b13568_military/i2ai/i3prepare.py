import os
import pickle
import pprint
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import csv





def csv_writer_places_to_local(records, filename):
    with open(filename, 'a') as csvfile:
        fieldnames = [ 'id', 'num']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for p in records:
            print(p)
            writer.writerow({
                'id': p[0],
                'num': p[1]
                            })


def csv_reader(filename, directory='./'):
    with open(os.path.join(directory, filename), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        mylist = []
        i = 0
        for row in reader:
            items = row[0].split(',')
            if items[1] != 'Number':
                print(i, items[1] )
                mylist.append([i, items[1]])
                i += 1

            # mylist.append(row[0].split(','))    
        return mylist


if __name__ == "__main__":
    mylist = csv_reader('i1steel_price.csv', '../data/')
    print('#'*20)
    csv_writer_places_to_local(mylist, '../data/i1processed_steel_price.csv')