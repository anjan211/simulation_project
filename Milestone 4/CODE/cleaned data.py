###########--------SIMULATION PROJECT---------DATA ANALYSIS-------------##############
##############-----------------TEAM TETRAHEDRON---------------------------###############
##############-----OWNER -- RAGHAVA VINAYKANTH MUSHUNURI, ARNAB DAS, ANJAN CHETTARJEE, LAURO , KAVYA VAJJA, CHANDAN RADHAKRISHNA----#####

import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import statsmodels
from pandas import plotting
import scipy
import matplotlib.mlab as mlab
from scipy import stats
import scipy.stats as st
import seaborn as sns
import statsmodels.api as sm
from statsmodels.graphics.gofplots import qqplot
import pylab as py
from scipy.stats import lognorm, norm

# reading the excel file
data = pd.read_excel('E:/master/sem2/simproj/raw data/leipziger-str-north-raw.xlsx', sep=',')
data['Raw Data'] = data[(data['Raw Data']<40)]
data = data.dropna()
#hist = data.hist(bins=75)
#plt.show()
#print(data)
#getting minimum and maximum of the data
xmin = data['Raw Data'].min()
xmax = data['Raw Data'].max()
print(data.shape[0])
kmin = int(np.sqrt(data.shape[0]))
kmax = int(data.shape[0] / 5)
# df = pd.DataFrame()
# df1 = pd.DataFrame()
# df2 = pd.DataFrame()
# df3 = pd.DataFrame()
# print(kmin)
# k = bin multiplicity
k = 1
# t = bin width
t = []
# list to store expected values
Exp = []
# list to store observed values
counts = []
# list to store maximum and minimum values for a table
individual_list_x = []
individual_list_y = []
data['lognorm'] = np.log(data['Raw Data'])
data['j'] = pd.Series(range(1, data.shape[0] + 1))
data['f'] = (data['j'] - 0.5) / data.shape[0]
data1 = pd.Series(data['f'])
mu = data['lognorm'].mean()
s = sigma = data['lognorm'].std()
################## GETTING THE LIST OF POSSIBLE VALUES FOR NUMBER OF BINS(SQR(N) - N/5)-----------#####################T
for i in range(kmin + 1, kmax + 1):
    t.append((xmax - xmin) / i)
c = 1
##############-------------------------CALCULATING THE FREQUENCY OF OBSERVED VALUES------------------------############
for j in range(len(t)):
    k = 1
    count = []
    list_x = []
    list_y = []

    for i in data['Raw Data']:

        if xmin + (k - 1) * t[j] <= i < xmin + (k) * t[j] and i <= xmax:
            c += 1

        else:
            count.append(c)
            list_x.append(xmin + (k - 1) * t[j])
            list_y.append(xmin + (k) * t[j])
            k += 1
            c = 1
    counts.append(count)
    individual_list_x.append(list_x)
    individual_list_y.append(list_y)

# print((counts[0]))
#print((counts[0]))
#################---------------------------PLOTTING THE GRAPHS-----------------------------###############
dist_names = [st.expon, st.lognorm, st.norm]
for distribution in dist_names:
    # Set up distribution and get fitted distribution parameters
    params = distribution.fit(data['Raw Data'])
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]
    #print(distribution, params)
    data['Finv'] = distribution.ppf(data['f'], loc=loc, scale=scale, *arg) if arg else distribution.ppf(data['f'],
                                                                                                        loc=loc,
                                                                                                        scale=scale)
    sns.scatterplot(x="Finv", y="Raw Data", data=data)
    # print(data['Finv'])
    sse = np.sum(np.power(data['Raw Data'] - data['Finv'], 2.0))
    # pdf = pd.Series(pdf)
    # print(pdf)
    print(sse)
    qqplot(data['Raw Data'], fit=True, dist=distribution, line='45')
    plt.show()
########################-------------------CALCULATING EXPECTED VALUES------------------------------#
Exp = []
for distribution in dist_names:
    expected_value = []
    for i in range(len(t)):
        expected = []

        for j in range(len(individual_list_x[i])):

            params = distribution.fit(data['Raw Data'])
            arg = params[:-2]
            loc = params[-2]
            scale = params[-1]
            if arg:
                ex1 = (distribution.cdf(individual_list_y[i][j], loc=loc, scale=scale, *arg) - distribution.cdf(
                    individual_list_x[i][j], loc=loc, scale=scale, *arg)) * data.shape[0]
                expected.append(ex1)
            else:
                ex = (distribution.cdf(individual_list_y[i][j], loc=loc, scale=scale) - distribution.cdf(
                    individual_list_x[i][j], loc=loc, scale=scale)) * data.shape[0]

                expected.append(ex)
        expected_value.append(expected)
    Exp.append(expected_value)
#print((Exp[78][1][0]))
#print(len(Exp[1][1]))

#######------------------------CHI SQUARE TEST---------------------######
chi_square = []
for i in range(len(dist_names)):
    chi2 = []
    for j in range(len(t)):
        chisquare = (np.power(np.array(Exp[i][j]) - np.array(counts[j]), 2)) / np.array(Exp[i][j])
        calculated = np.sum(chisquare)
        chi2.append(calculated)
    chi_square.append(chi2)
print(chi_square)
# print(np.sum(Array))
# print(m)
# print(individual_list_x[0])
# print(individual_list_y[0])