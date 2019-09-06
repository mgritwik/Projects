from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
import numpy as np

X = [[0.44, 0.68], [0.99, 0.23]]
vector = [109.85, 155.72]
predict= np.array([0.49, 0.18]).reshape(1,-1)

poly = PolynomialFeatures(degree=2)
X_ = poly.fit_transform(X)
predict_ = poly.fit_transform(predict)

clf = linear_model.LinearRegression()
clf.fit(X_, vector)
prediction=clf.predict(predict_)
print(prediction)


'''
#working of PolynomialFeatures
>>> from sklearn.preprocessing import PolynomialFeatures
>>> import numpy as np
>>> X = np.arange(6).reshape(3, 2)
>>> X
array([[0, 1],
       [2, 3],
       [4, 5]])
>>> poly = PolynomialFeatures(degree=2)
>>> poly.fit_transform(X)
array([[ 1,  0,  1,  0,  0,  1],
       [ 1,  2,  3,  4,  6,  9],
       [ 1,  4,  5, 16, 20, 25]])
'''