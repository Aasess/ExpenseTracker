from django.shortcuts import render,redirect,get_object_or_404
from .models import Expense

# Create your views here.
def home(request):
    sumincome = 0
    sumexpense = 0
    for i in Expense.objects.all():
        if(i.amount[:1] == '+'):
            sumincome += int(i.amount[1:])
        
        if(i.amount[:1] == '-'):
            sumexpense += int(i.amount[1:])

    balance = sumincome - sumexpense    
        

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
                "balance":balance
                })
    else:       
        return render(request,'expense\home.html',{
            "expense":Expense.objects.order_by("-date")[:6],
            "income":sumincome,
            "exp":sumexpense,
            "balance":balance})


def history(request):
    return render(request,'expense\history.html',{"expense":Expense.objects.order_by("-date")})


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
