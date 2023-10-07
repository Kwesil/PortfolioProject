import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    data = pd.read_csv('epa-sea-level.csv')
    # Create scatter plot
    x = data['Year']
    y = data['CSIRO Adjusted Sea Level']
    plt.scatter(x, y)

    # Create first line of best fit
    fit1 = linregress(x, y)
    intercept = fit1.intercept
    slope = fit1.slope
    line_x = np.arange(1880, 2051)
    line_y = slope * line_x + intercept


    plt.plot(line_x, line_y, 'r', label='Best fit line 1')
      
    # Create second line of best fit
    new_data = data[data['Year'] >= 2000]
    x1 =  new_data['Year']
    y1 =  new_data['CSIRO Adjusted Sea Level']
    fit2 = linregress(x1, y1)
    intercept1 = fit2.intercept
    slope1 = fit2.slope
    line_x1 = np.arange(2000, 2051)
    line_y1 = slope1 * line_x1 + intercept1
      
    plt.plot(line_x1, line_y1, 'b', label='Best fit line 2')
  
    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')
  
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()
