#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sympy.interactive import printing
printing.init_printing(use_latex=True)
sns.set(rc={'figure.figsize':(8,6)})
from IPython.display import Image
import os
import numpy as np
from scipy import stats
import csv
all_colors=["orange", "blue","red","black","#2ecc71", "#2e0071",  "#2efdaa"]
subset_colors =  ["red","black","#2ecc71", "#2e0071",  "#2efdaa", "#200daa","#2ffd00"]
include_plots = ['arc','alecar3']
import os.path as path
import xlwt 
from xlwt import Workbook 

#np.random.seed(12345678)


# In[7]:


def writeHeader(sheet1, our_algo, other_algo):
    row = 0
    col= 1
    sheet1.write(row, col, "dataset") 
    col= col+ 1
    sheet1.write(row, col,  "algorithm")
    col= col+ 1
    sheet1.write(row, col,   "cache_size") 
    col= col+ 1
    sheet1.write(row, col, "our_algo_mean") 
    col= col+ 1
    sheet1.write(row, col, "other_algo_mean") 
    col= col+ 1
    sheet1.write(row, col, "other_algo_std") 
    col= col+ 1 
    sheet1.write(row,  col,  "other_algo_std") 
    col= col+ 1 
    sheet1.write(row,col , "p_value")
    col= col+ 1 
    sheet1.write(row, col,  "color") 
    col= col+ 1 
    sheet1.write(row, col,  "effect_size") 
    
from numpy import mean
from numpy import var
from math import sqrt

# function to calculate Cohen's d for independent samples
def cohend(d1, d2):
    # calculate the size of samples
    n1, n2 = len(d1), len(d2)
    # calculate the variance of the samples
    s1, s2 = var(d1, ddof=1), var(d2, ddof=1)
    # calculate the pooled standard deviation
    s = sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    # calculate the means of the samples
    u1, u2 = mean(d1), mean(d2)
    # calculate the effect size
    return (u1 - u2) / s
    
def writeInCsv(sheet1,row, df_cache, our_algo, other_algo, datas, cache_size):
    #print(self.df_cache)
    df_our_algo=df_cache[(df_cache['algo']==our_algo)].hit_rate.to_numpy()
    
    df_other_algo=df_cache[(df_cache['algo']==other_algo)].hit_rate.to_numpy()
    print(len(df_our_algo))
    print(len(df_other_algo))
    effect_size = cohend(df_our_algo,df_other_algo )
    
#     print(self.df_our_algo)
#     print(self.df_other_algo)
    
    t2, p2  = stats.ttest_rel(df_our_algo, df_other_algo)
#             df_cache[['ALeCaR', 'ScanALeCaR']].plot(kind='box')
    our_algo_mean = np.mean(np.array(df_our_algo))
    other_algo_mean = np.mean(np.array(df_other_algo))
    # Calculate the standard deviation
    our_algo_std = np.std(np.array(df_our_algo), ddof=1)
    other_algo_std = np.std(np.array(df_other_algo), ddof=1)

    our_algo_sem =  stats.sem(np.array(df_our_algo))
    other_algo_sem =  stats.sem(np.array(df_other_algo))
    print( "*****Dataset:" , datas , "*****Cache Size:" , cache_size , "*******")
    print(our_algo ," Average = " , our_algo_mean, "Standard deviation = " , our_algo_std)
    print("Standard error estimated =", our_algo_sem)
    
    print(other_algo, " Average = " , other_algo_mean, "Standard deviation = " , other_algo_std)
    print("Standard error estimated = ", other_algo_sem)

    print("t-test with respect to", other_algo)
    print("t = " + str(t2))
    print("p-value = " + str(p2))
    print("Effect size = ",effect_size)

    color = 0 if round(p2, 2) >0.05  else (1 if our_algo_mean> other_algo_mean  else -1)

    col= 1
    sheet1.write(row, col, datas) 
    col= col+ 1
    sheet1.write(row, col,  other_algo)
    col= col+ 1
    sheet1.write(row, col,   cache_size) 
    col= col+ 1
    sheet1.write(row, col, our_algo_mean) 
    col= col+ 1
    sheet1.write(row, col, other_algo_mean) 
    col= col+ 1
    sheet1.write(row, col, other_algo_std) 
    col= col+ 1 
    sheet1.write(row,  col,  other_algo_std) 
    col= col+ 1 
    sheet1.write(row,col , round(p2,3))
    col= col+ 1 
    sheet1.write(row, col,  color) 
    col= col+ 1 
    sheet1.write(row, col,  effect_size)
    
    


# In[9]:

class CacheusPlugin:
 def input(self, inputfile):
  self.df = pd.read_csv(inputfile, header=None)
 def run(self):
     pass
 def output(self, outputfile):
  self.df.columns = ['traces', 'trace_name', 'algo', 'hits', 'misses', 'writes', 'filters', 
                   'size', 'cache_size', 'requestcount', 'hit_rate', 'time', 'dataset']

  self.df = self.df.sort_values(['dataset', 'cache_size', 
                    'traces', 'hit_rate'], ascending=[True, True, True, False])

  our_algo = "lirsalecar"
  our_algos = ["lirsalecar", 'arcalecar', 'cacheus']
  other_algos = [ "arc", "lirs", "lecar", "dlirs"]


  # self.df = pd.read_excel('data/final_results.xlsx')
  # our_algo = "ScanALeCaR"
  # other_algos = [ 'ARC', "LIRS", "DLIRS", "LeCaR", "ALeCaR2N", "ALeCaRN"]


  # our_algo = "ALeCaRN"
  # other_algos = [ 'ARC', "LIRS", "DLIRS", "LeCaR", "ALeCaR2N", "ScanALeCaR"]
  # #print(self.df_all)
  for our_algo in our_algos:
    wb = Workbook() 

    # add_sheet is used to create sheet. 
    filename = our_algo + '_t-test_results'
    #filename = our_algo + ' t-test results'
    sheet1 = wb.add_sheet(filename) 
    datasets = self.df["dataset"].unique()
    row=1
    writeHeader(sheet1, our_algo, "Other Algorithm")
    for other_algo in other_algos:
    #     sheet1.write(row, 0, other_algo) 
    #     row= row+1
        for datas in datasets:
            self.df_data= self.df[ self.df["dataset"] == datas]
            cache_sizes = self.df_data["cache_size"].unique()
            for cache_size in cache_sizes:
                self.df_cache = self.df_data[(self.df_data["cache_size"] == cache_size) ]
                print(cache_size, datas, other_algo)
    #             t_test_results.append(l)
                writeInCsv(sheet1,row, self.df_cache, our_algo, other_algo, datas, cache_size)
                row= row+1

    #sheet1.write(row, datas, cache_size, alecar_mean, alecar_std,scanalecar_mean, scanalecar_std,t2, p2) 

    wb.save(our_algo+'_t-test_results.xls')
    os.system("mv "+our_algo+"_t-test_results.xls "+outputfile+"/")


  test = np.arange(20).reshape(5, 4)
  print(test)

  print(stats.sem(test))


  # In[ ]:




