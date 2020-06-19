from django.shortcuts import render,HttpResponse
from expense.models import Expense

# Create your views here.
def analysis(request):
    expense = Expense.objects.all()
    print(expense)
    return HttpResponse("hello")