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
    data = np.array(data).astype(float)
    rows = data.shape[0]
    columns = data.shape[1]

    # Probability that x_j was generated by Gaussian n_i
    # p[i][j] where i is the gaussian number and j is the data number
    # For each input, set one p value to 1, and the rest to 0
    p = np.zeros((k, rows))

    # Mean and for each gaussian, and in each gaussian, a mean for each dimension.
    mean = [[0 for i in range(columns)] for j in range(k)]
    weight = [0 for i in range(k)]
    std = [[[0 for i in range(columns)] for j in range(columns)] for k in range(k)]

    # Randomly assign each point to a cluster
    for j in range(rows):
        # Random gaussian is set to 1 for each j
        p[np.random.randint(low=0, high=k)][j] = 1

    for _ in range(iterations):

        # M-step - For each p_ij, so for each k * rows
        # i-th Gaussian
        for i in range(k):
            temp = 0
            temp2 = 0
            # j-th input
            # Mean calculation
            for j in range(rows): 
                temp += (p[i][j] * data[j]) # p[dimension][input], so go down the i'th column (dimension). Think of cross multiplication when it comes to dimensionality.
            mean[i] = temp / sum(p[i])
            
            # Weight calculation
            weight[i] = sum(p[i]) / sum(sum(p))

            # Standard deviation calculation - covariance matrix
            for r in range(columns):
                for c in range(columns):
                    for j in range(rows):
                        temp2 += p[i][j] * (data[j][r] - mean[i][r]) * (data[j][c] - mean[i][c])
                    if (temp2 / sum(p[i]) < 0.0001 and r == c):
                        std[i][r][c] = 0.0001
                    else:
                        std[i][r][c] = temp2 / sum(p[i])


em_cluster(argv[1], argv[2], argv[3])