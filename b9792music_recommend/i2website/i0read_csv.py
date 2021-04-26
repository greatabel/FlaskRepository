import os
import csv

def read_from_localfile(filename, directory='./'):
    with open(os.path.join(directory, filename), 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        all_rows = []
        for row in reader:
            if row is not None: 
                all_rows.append(row)
        print(all_rows)

if __name__ == "__main__":
    content = read_from_localfile('movie_rating.csv', '../data/')
    print(content)