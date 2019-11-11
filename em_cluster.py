# Dustin Le
# 1001130689

from sys import argv
import numpy as np

def em_cluster(data_file, k, iterations):
    data = []
    k = int(k)
    iterations = int(iterations)

    with open(data_file, 'r') as file:
        for line in file:
            if ',' in line:
                data.append(line.split(', ')[0:-1])
            else:
            data.append(line.split()[0:-1])
    
    # Initialization
    data = np.array(data)
    rows = data.shape[0]
    columns = data.shape[1]

    # p[i][j] where i is the gaussian number and j is the data number
    # For each input, set one p value to 1, and the rest to 0
    p = np.zeros((k, rows))

    # Randomly assign each point to a cluster
    for j in range(rows):
        # Random gaussian is set to 1 for each j
        p[np.random.randint(low=0, high=k)][j] = 1

em_cluster(argv[1], argv[2], argv[3])