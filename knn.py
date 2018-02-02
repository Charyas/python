#coding=utf-8

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

np.random.seed(42)

n_samples, n_features = 50, 200

X = np.random.randn(n_samples, n_features)

print X
coef = 3 * np.random.randn(n_features)
inds = np.arange(n_features)
np.random.shuffle(inds)
coef[inds[10:]] = 0
y = np.dot(X, coef)

y += 0.01 * np.random.normal(size=n_samples)
n_samples = X.shape[0]
X_train, y_train = X[:n_samples//2], y[:n_samples//2]
X_test, y_test = X[n_samples//2:], y[n_samples//2:]

from sklearn.linear_model import Lasso

alpha = 0.1
lasso = Lasso(alpha=alpha)
y_pred_lasso = lasso.fit(X_train, y_train).predict(X_test)
r2_score_lasso = r2_score(y_test, y_pred_lasso)
print lasso
print r2_score_lasso

from sklearn.linear_model import ElasticNet

enet = ElasticNet(alpha=alpha, l1_ratio=0.7)
y_pred_enet = enet.fit(X_train,y_train).predict(X_test)
r2_score_enet = r2_score(y_test, y_pred_enet)

plt.plot(enet.coef_, color='lightgreen', linewidth=2,
         label='Elastic net coefficients')
plt.plot(lasso.coef_, color='gold', linewidth=2,
         label='Lasso coefficients')
plt.plot(coef, '--', color='navy', label='original coefficients')
plt.legend(loc='best')
plt.title("Lasso R^2: %f, Elastic Net R^2: %f"
          % (r2_score_lasso, r2_score_enet))
plt.show()


