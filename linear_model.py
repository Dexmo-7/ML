import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn.linear_model
from sklearn import linear_model
import os

def prepare_country_stats(oecd_bli, gdp_per_capita):
    oecd_bli = oecd_bli[oecd_bli["INEQUALITY"]=="TOT"]
    oecd_bli = oecd_bli.pivot(index="Country", columns="Indicator", values="Value")
    gdp_per_capita.rename(columns={"2015": "GDP per capita"}, inplace=True)
    gdp_per_capita.set_index("Country", inplace=True)
    full_country_stats = pd.merge(left=oecd_bli, right=gdp_per_capita,
                                  left_index=True, right_index=True)
    full_country_stats.sort_values(by="GDP per capita", inplace=True)
    remove_indices = [0, 1, 6, 8, 33, 34, 35]
    keep_indices = list(set(range(36)) - set(remove_indices))
    
    return full_country_stats[["GDP per capita", 'Life satisfaction']].iloc[keep_indices]

datapath = os.path.join("datasets", "lifesat", "")

#Load the data
oecd_bli = pd.read_csv("oecd_bli_2015.csv", thousands=',')
gdp_per_capita = pd.read_csv("gdp_per_capita.csv", thousands=',', delimiter='\t',
                            encoding='latin1', na_values='na')

#Preparing the data
country_stats = prepare_country_stats(oecd_bli, gdp_per_capita)
X = np.c_[country_stats["GDP per capita"]]
y = np.c_[country_stats["Life satisfaction"]]

#More for data preparing
lin1 = linear_model.LinearRegression()
lin1.fit(X, y)
t0, t1 = lin1.intercept_[0], lin1.coef_[0][0]
#Data visualization
country_stats.plot(kind='scatter', x="GDP per capita", y="Life satisfaction")
plt.axis([0, 60000, 0, 10])
X2 = np.linspace(0, 60000, 1000)
plt.plot(X2, t0 + t1*X2, "b")
plt.text(5000, 3.1, r"$\theta_0 = 4.85$", fontsize=14, color="b")
plt.text(5000, 2.2, r"$\theta_1 = 4.91 \times 10^{-5}$", fontsize=14, color="b")
plt.show()

#Choosing the linear model
model = sklearn.linear_model.LinearRegression()

#Model training
model.fit(X, y)

#Results for Cyprus (prediction)
X_new = [[22587]] #GDP per capita for Cyprus
print(model.predict(X_new))
