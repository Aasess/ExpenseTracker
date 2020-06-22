from django.shortcuts import render,HttpResponse
from expense.models import Expense
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool,BasicTickFormatter,DatetimeTickFormatter
from bokeh.models import ColumnDataSource
from bokeh.layouts import row
from datetime import datetime,timedelta
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
# Create your views here.
def analysis(request):
    df = pd.DataFrame(Expense.objects.values())
    df.drop('id',axis=1,inplace=True)

    df["amount"] = df["amount"].astype(int)
   
    #sorting on date basis
    df = df.sort_values(by=['date'])
    #now I don't need time so remove time from date
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['date'] = pd.to_datetime(df['date'])
    df['datestr'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    
    #for months only logic and plotting graph
    dfmonth = df[df['date'] >= datetime.today().replace(day=1)]
    source = ColumnDataSource(dfmonth)
    
    #---------------- for prediction-------------------------
    df.drop(["transaction_name","datestr"],axis=1,inplace = True)
    #lets combine the amount by date
    dfcopy = df.groupby('date').sum()
    # working with days only
    dfcopy['days_from_start'] = (dfcopy.index - dfcopy.index[0]).days
    #calculating remaining balance after each transaction and storing in dataframe
    remaining = []
    eachamount = dfcopy.amount[0]
    remaining.append(dfcopy.amount[0])
    for i in range(len(dfcopy)-1):
        eachamount += dfcopy.amount[i+1]
        remaining.append(eachamount)
    #separating input and targets as
    X = dfcopy["days_from_start"].values
    Y= remaining
    #lets reshapre the input
    X = X.reshape([-1,1])
    #use linear regression from sklearn
    model = LinearRegression()
    model.fit(X,Y)
    
    #print(model.score(X,Y))
    
    ypredicts = model.predict(X)
    #for 10 days prediction
    endindex = len(dfcopy)-1
    days_from_start = dfcopy['days_from_start'][endindex]
    #logic for setting next 7 days input
    nextdate = dfcopy.index[endindex]
    nextdatetime = []
    nextdatedays = []

    for i in range(1,10):
        nextdatedays.append(days_from_start + i)
        nextdate += timedelta(days=1)
        nextdatetime.append(nextdate)
    
    dfpredict = pd.DataFrame({
        'days':nextdatedays,
    })
    
    yfuture = model.predict(dfpredict)
    
    for i in range(len(nextdatetime)):
        nextdatetime[i] = nextdatetime[i].strftime("%Y-%m-%d")
        yfuture[i] = round(yfuture[i])


    #-------------------------prediction done-----------------
    
    #todays month
    month = datetime.today().strftime("%B")
    
    #setup graph plot for displaying monthly income and expense
    plot1 = figure(
        title = month +' Graph',
        x_axis_type='datetime',
        x_axis_label = "Days",
        y_axis_label = "Amount",
        plot_width = 1060,
        plot_height = 500,
    )
    plot1.line(x='date',y = 'amount',line_width=1,legend_label="Daily Basis Income And Expense",source=source,line_dash ="dashed")
    plot1.circle(x='date',y='amount',fill_color='white',size=8,legend_label="Daily Basis Income And Expense",source=source)
    
    plot1.xaxis.formatter=DatetimeTickFormatter(days="%Y/%m/%d")
   
    plot1.add_tools(HoverTool(tooltips=[
        ("date","@datestr"),
        ('transaction_name',"@transaction_name"),
        ("amount",'@amount')]))
    #store components
    script1,div1 = components(plot1)

    plot2 = figure(
        title = "Remaining Balance Graph using Linear Regression",
        x_axis_type="datetime",
        x_axis_label = "Days",
        y_axis_label ="Amount",
        plot_width = 650,
        plot_height = 500,
    )
    
    #print(dfpredict)
    plot2.line(x=dfcopy.index,y=remaining,line_color="red",line_width=5,legend_label="Actual Data")
    plot2.line(x=dfcopy.index,y=ypredicts,line_color="green",line_width=3,legend_label="predicted Data",line_dash="dashed")
    script2,div2 = components(plot2)
    
    #lets zip for using two variables in jinja
    predict = zip(nextdatetime,yfuture)
    #render to analysis.html
    return render(request,'analysis/analysis.html',{
        'script1':script1,
        'div1':div1,
        'month':month,
        'script2':script2,
        'div2':div2,
        'predict':predict,
    })