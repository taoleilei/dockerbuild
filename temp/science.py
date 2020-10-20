# -*- encoding: utf-8 -*-
'''
@File    :   science.py
@Time    :   2020/07/09 15:44:37
@Author  :   taoleilei 
@Version :   1.0
@Contact :   taoleilei6176@163.com
@License :   (C)Copyright 2019-2020
@Desc    :   None
'''

# from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import numpy.matlib
import pandas as pd
import torch
from sklearn import datasets, svm

print(torch.__version__)
# x = torch.ones(2, 2, requires_grad=True)
# y = x + 2
# print(y)
# z = y * y * 3
# out = z.mean()
# print(z, out)
# out.backward()
# print(x.grad)
a = torch.randn(4, 4)
print(a.size())
print(a.reshape(-1).numpy())

# X, y = datasets.load_iris(return_X_y=True)
# # data = digits.images[0]
# print(X.shape)
# print(y.shape)
# # print(type(data))
# # print(data.shape)

# clf = svm.SVC()
# clf.fit(X[:-1], y[:-1])
# print(clf.predict(X[-1:]))
# a = np.array([[1, 2], [3, 4]])
# print(a.ndim)
# print(np.tile(a, (2, 2)))
# print(torch.randn(1, 3, 3))
# torch.randn()
