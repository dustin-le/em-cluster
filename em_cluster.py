# Dustin Le
# 1001130689

from sys import argv
import numpy as np

def em_cluster(data_file, k, iterations):
    data = []

    with open(data_file, 'r') as file:
        for line in file:
            data.append(line.split()[0:2])
    

em_cluster(argv[1], argv[2], argv[3])