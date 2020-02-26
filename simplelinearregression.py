import math
import matplotlib.pyplot as plt

list_x = [1,2,3,4,5,6,7,8,9,10]
list_y = [2,5,8,11,14,18,22,26,30,34]

test_x = [12, 14, 16]
test_y = [44, 54, 65]

def mean(values):
    return sum(values) / float(len(values))

def variance (values, mean):
    return sum([(x-mean)**2 for x in values])

def covariance(x, mean_x, y, mean_y):
    covar = 0.0
    for i in range(len(x)):
        covar += (x[i] - mean_x) * (y[i] - mean_y)
    return covar

def coefficients(values_x, values_y):
    mean_x, mean_y = mean(values_x), mean(values_y)
    b1 = covariance(values_x, mean_x, values_y, mean_y) / variance(values_x, mean_x)
    b0 = mean_y - b1 * mean_x
    return [b0, b1]

def simple_linear_regression(train_x, train_y, test_x):
    predictions = []
    b0, b1 = coefficients(train_x, train_y)
    for x in test_x:
        guess = b0 + b1 * x
        predictions.append(guess)
    return predictions

def rmse_metric(actual_y, predicted_y):
    sum_error = 0.0
    for i in range(len(actual_y)):
        prediction_error = predicted_y[i] - actual_y[i]
        sum_error += prediction_error ** 2
    mean_error = sum_error / float(len(actual_y))
    return math.sqrt(mean_error)

predicted_y = simple_linear_regression(list_x, list_y, test_x)
print(predicted_y)
prediction_accuracy = rmse_metric(test_y, predicted_y)
print(prediction_accuracy)

    
