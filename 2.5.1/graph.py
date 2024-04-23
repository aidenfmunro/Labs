
##############################################################################
#                 USE GOOGLE COLAB TO RUN PROGRAM                            #
##############################################################################

import matplotlib.pyplot as plt                         #include libs  
from scipy.optimize import curve_fit    
from IPython.display import display, Math, Latex
import numpy as np
from math import *

plt.rcParams["font.family"] = "monospace"

def mapping(x, k, b):                #Function of approximating give to curve_fit 
    return b + k*x

plt.figure(figsize=(11,11))                                #Create graphic in matplotlib  
plt.title(r"зависимость $h(t)$")  #Labels of coordinates 
plt.xlabel(r"t, $^{\circ}$C")
plt.ylabel(r"$h$, дел")

#-------------------------------------------------------------------------------------

#processing data

x = []
y = []

#FILE "data.txt" !!!!!!!!!!!! YOU NEED TO UPLOAD IT TO COLAB 

file = open('2.5.1/data.txt', 'r')                 #open file with data
while (line := file.readline()):              # every line have x, y, y1 ...
  s = line.split()
  if (len(s) != 0):
    x.append(float(s[0].replace(',','.')))    #collect in x[] y1[] y2[] with change "," -> "." (if excel)
    y.append(float(s[1].replace(',','.')))

k = 0                                        #create coeffs all in function
b = 0

coeffs,_ = curve_fit(mapping, x, y)          #give func and our measurements
k = coeffs[0]                                   #it returns array of aproximating coeffs 
b = coeffs[1]
y_fit = []
for i in range(len(x)):
  y_fit.append(b + k * x[i])                    #with coeffs make array of Approximating data
#                 ^
#                 |
#                 function need to write 
#                 """"""""""""""""""""""

plt.plot(x, y, 'gs', label='')    #triangles with measurments
plt.plot(x, y_fit, color = 'b', label = f"Прямая с аппроксимацией) " r'' f", k = {k:.3f}, a = {b:.3f}") #approximating praphic
                                                                                                                                  #
#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

plt.grid(visible = True, which='major', axis='both', alpha=1)           #end of matplotlib
plt.grid(visible = True, which='minor', axis='both', alpha=1)           #show graphic
plt.legend()
plt.show()
file.close()