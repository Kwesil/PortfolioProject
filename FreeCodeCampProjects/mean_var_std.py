import numpy as np

def calculate(list):
    if len(list) < 9:
        raise ValueError('List must contain nine numbers.')
    else:
        pass
    data = np.reshape(list, (3, 3))
    flattened = np.matrix.flatten(data)
    print("Matrix: {}".format(data))
    
    # Mean of both axes and flattened matrix
    mean = np.mean(data, axis=0).tolist()
    mean1 = np.mean(data, axis=1).tolist()
    mean2 = np.mean(flattened).tolist()
    
    # Variance of both axes and flattened matrix
    var = np.var(data, axis=0).tolist()
    var1 = np.var(data, axis=1).tolist()
    var2 = np.var(flattened).tolist()
    
    # Standard deviation of both axes and flattened matrix
    std = np.std(data, axis=0).tolist()
    std1 = np.std(data, axis=1).tolist()
    std2 = np.std(flattened).tolist()
    
    # Max values of both axes and flattened matrix
    max = np.max(data, axis=0).tolist()
    max1 = np.max(data, axis=1).tolist()
    max2 = np.max(flattened).tolist()
    
    # Min values of both axes and flattened matrix
    min =  np.min(data, axis=0).tolist()
    min1 = np.min(data, axis=1).tolist()
    min2 = np.min(flattened).tolist()
    
    # sum of both axes and flattened matrix
    sum = np.sum(data, axis=0).tolist()
    sum1 = np.sum(data, axis=1).tolist()
    sum2 = np.sum(flattened).tolist()    
    
    calculations = {
        'mean': [mean, mean1, mean2],
        'variance': [var, var1, var2],
        'standard deviation': [std, std1, std2],
        'max': [max, max1, max2],
        'min': [min, min1, min2],
        'sum': [sum, sum1, sum2] 
    }

    return calculations
 
n = 9
number_list = list(int(num) for num in input("Enter nine numbers separated by space: ").strip().split())[:n]
project = (calculate(number_list))
print(project)
