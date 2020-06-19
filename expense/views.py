from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.db.models import Q
import datetime
from .models import Expense

# Create your views here.
def home(request):
    sumincome = 0
    sumexpense = 0

    #for this month logic 
    sumincomemonth = 0
    sumexpensemonth = 0 

    #today month
    mnth = datetime.date.today().strftime("%B")

    for i in Expense.objects.all():
        if(i.amount[:1] == '+'):
            sumincome += int(i.amount[1:])
        
        if(i.amount[:1] == '-'):
            sumexpense += int(i.amount[1:])

        balance = sumincome - sumexpense 
        #for monthly calculation
        if(int(i.month()) == datetime.date.today().month):
            if(i.amount[:1] == '+'):
                sumincomemonth += int(i.amount[1:])
        
            if(i.amount[:1] == '-'):
                sumexpensemonth += int(i.amount[1:])

            balancemonth = sumincomemonth - sumexpensemonth 
    

    remaining = balance - balancemonth


    if(request.method == 'POST'):
        if request.POST['transaction_name'] and request.POST['amount']:
            expense = Expense()
            expense.transaction_name = request.POST['transaction_name']
            expense.amount = request.POST['amount']
            expense.save()
            return redirect('home')
        else:
            return render(request,'expense\home.html',{
                "error":"Missing Field !! Add New Transaction ",
                "expense":Expense.objects.order_by("-date")[:6],
                "income":sumincome,
                "exp":sumexpense,
                "balance":balance,
                "monthbal":balancemonth,
                "monthinc":sumincomemonth,
                "monthexp":sumexpensemonth,
                "month":mnth,
                "remaining":remaining,
                })
    else:       
        return render(request,'expense\home.html',{
            "expense":Expense.objects.order_by("-date")[:6],
            "income":sumincome,
            "exp":sumexpense,
            "balance":balance,
            "monthbal":balancemonth,
            "monthinc":sumincomemonth,
            "monthexp":sumexpensemonth,
            "month":mnth,
            "remaining":remaining})




def history(request):
    return render(request,'expense\history.html',{
        "expense":Expense.objects.order_by("-date")
        })




def edit(request,transaction_id):
    transaction = get_object_or_404(Expense,pk=transaction_id)
    if(request.method=="POST"):
        #submit data
        if(request.POST["transactionname"] and request.POST["amount"]):
            print(transaction.transaction_name)
            transaction.transaction_name = request.POST["transactionname"]
            transaction.amount = request.POST["amount"]
            print(transaction.transaction_name)
            transaction.save()
            return redirect("history")
        else:
            return render(request,'expense\edit.html',{"transaction":transaction,"error":"Missing Fields!!!"})

    else:
        return render(request,'expense\edit.html',{"transaction":transaction })


def delete(request,transaction_id):
    transaction = get_object_or_404(Expense,pk=transaction_id)
    if(request.method =="POST"):
        transaction.delete()
        return redirect('history')
    else:
        return render(request,'expense\delete.html',{"transaction":transaction})



def search(request):
    query = request.GET['query']
    #logic for search
    expense = Expense.objects.filter(
        Q(transaction_name__icontains=query) | Q(amount__icontains=query)).order_by('-date')
    if(len(expense) == 0):
        return render(request,'expense\search.html',{'error':'There are no results for keywords:','query':query})
    else:
        return render(request,'expense\search.html',{'expense':expense})