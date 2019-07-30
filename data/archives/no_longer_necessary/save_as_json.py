import sys
import json

with open('dataset_ids.txt', 'r') as inf:
    datasets = eval(inf.read())

with open('dataset_ids.json', 'w') as outfile:
    json.dump(datasets, outfile)
