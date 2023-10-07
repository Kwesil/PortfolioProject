import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Clean data
df = df.drop(df[(df['value'] < df['value'].quantile(0.025)) | 
                        (df['value'] > df['value'].quantile(0.975))].index)


def draw_line_plot():
    # Draw line plot
    x = df.index
    y = df['value']
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(x, y, 'b')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Year'] = pd.DatetimeIndex(df_bar.index).year
    df_bar['Month'] = pd.DatetimeIndex(df_bar.index).month

    df_bar = df_bar.groupby(['Year', 'Month'])['value'].mean()
    df_bar = df_bar.unstack()
    month_labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Draw bar plot
    fig = df_bar.plot(kind='bar', figsize=(15,10)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', fontsize=15, labels=month_labels)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box.sort_values(by=['year','date'], ascending=[False, True], inplace=True)
  
    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(10,10))
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
  
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
