from django.shortcuts import render,HttpResponse
from expense.models import Expense
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool,BasicTickFormatter,DatetimeTickFormatter
from bokeh.models import ColumnDataSource
from bokeh.layouts import row
import datetime
import pandas as pd
# Create your views here.
def analysis(request):
    df = pd.DataFrame(Expense.objects.values())
    df.drop('id',axis=1,inplace=True)

    #df.to_csv("trans.csv",index = False)
    df["amount"] = df["amount"].astype(int)
   
    positive = []
    negative = []
    #lets define the function to separate income and expense
    def PluasOrNeg(amount):
        if(amount >= 0):
            positive.append(amount)
            negative.append(0)
        else:
            negative.append(amount)
            positive.append(0)
    for amount in df['amount']:
        PluasOrNeg(amount)

    income = pd.Series(positive)
    expense = pd.Series(negative)
    #making separate columns for income and expense
    df["income"] = income
    df["expense"] = expense
    
    #sorting on date basis
    df = df.sort_values(by=['date'])
    #now I don't need time so remove time from date
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['date'] = pd.to_datetime(df['date'])
    df['y'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    dfmonth = df[df['date'] >= datetime.datetime.today().replace(day=1)]

    thismonth = print(datetime.date.today().month)
    source = ColumnDataSource(dfmonth)
    #setup graph plot for displaying
    plot = figure(
        title = 'Line Graph',

        x_axis_type='datetime',
    
        x_axis_label = "date",
        y_axis_label = "income",
        plot_width = 800,
        plot_height = 500,
    )
    print(dfmonth)
    plot.line(x='date',y = 'amount',line_width=1,legend_label="daily basis",source=source,line_dash ="dashed")
    plot.circle(x='date',y='amount',fill_color='white',size=8,legend_label="daily basis",source=source)
    plot.xaxis.formatter=DatetimeTickFormatter(days="%Y/%m/%d")
    
    plot.add_tools(HoverTool(tooltips=[
        ("date","@y"),
        ('transaction_name',"@transaction_name"),
        ("amount",'@amount')]))
    #store components
    script,div = components(plot)

    #trans
    return render(request,'analysis/analysis.html',{
        'script':script,
        'div':div
    })