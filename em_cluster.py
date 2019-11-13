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

    # Membership weights - probability that x_j was generated by Gaussian n_i
    # p[i][j] where i is the gaussian number and j is the data number
    # For each input, set one p value to 1, and the rest to 0
    p = np.zeros((k, rows))

    # Mean and for each gaussian, and in each gaussian, a mean for each dimension.
    mean = [[0 for i in range(columns)] for j in range(k)]
    weight = [0 for i in range(k)]

    # Covariance matrix array - i-th Gaussian, row r, column c of the covariance matrix
    std = [[[0 for i in range(columns)] for j in range(columns)] for k in range(k)]

    # Randomly assign each point to a cluster
    for j in range(rows):
        # Random gaussian is set to 1 for each j
        p[np.random.randint(low=0, high=k)][j] = 1

    for _ in range(iterations):

        # M-step - For each p_ij, so for each k * rows
        # i-th Gaussian, j-th input
        for i in range(k):
            temp = 0
            temp2 = 0
            
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

        # E-step - For each u_i, o_irc, and w_i, update p_ij
        # i-th Gaussian, j-th input
        pxj = 0
        n = 0

        for i in range(k):
            for j in range(rows):
                for l in range(k):
                    pxj += (1 / np.sqrt((2 * np.pi)**columns * np.linalg.det(std[l]))) * np.exp(-1/2 * (data[j] - mean[l]).T @ np.linalg.pinv(std[l]) @ (data[j] - mean[l])) * weight[l]
                # n = (1 / np.sqrt((2 * np.pi)**columns * np.linalg.det(std[i]))) * np.exp(-(np.linalg.solve(std[i], mean[i]).T.dot(mean[i])) / 2)
                n += (1 / np.sqrt((2 * np.pi)**columns * np.linalg.det(std[i]))) * np.exp(-1/2 * (data[j] - mean[i]).T @ np.linalg.pinv(std[i]) @ (data[j] - mean[i])) * weight[i]
                p[i][j] = n * weight[i] / pxj

        # Output
        print('After iteration %d:' % (_ + 1))
        for i in range(k):
                print('weight %d = %.4f, mean %d = (' % (i + 1, weight[i], i + 1), end = '')
                for j in range(columns):
                    print('%.4f' % mean[i][j], end = '')
                    if (j != columns - 1):
                        print(', ', end='')
                    else:
                        print(')')

    print('After final iteration:')
    for i in range(k):
        print('weight %d = %.4f, mean %d = (' % (i + 1, weight[i], i + 1), end = '')
        for j in range(columns):
            print('%.4f' % mean[i][j], end = '')
            if (j != columns - 1):
                print(', ', end='')
            else:
                print(')')

        for r in range(columns):
            print('Sigma %d row %d = ' % (i + 1, r + 1), end = '')
            for c in range(columns):
                print('%.4f' % std[i][r][c], end = '')
                if (c != columns - 1):
                    print(', ', end='')
                else:
                    print()
    
em_cluster(argv[1], argv[2], argv[3])