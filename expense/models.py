from django.db import models

# Create your models here.
class Expense(models.Model):
    transaction_name = models.CharField(max_length=100,blank=True,null=True)
    amount = models.CharField(max_length=100,blank=True,null=True)
    date = models.DateTimeField(auto_now_add = True)
    

    def __str__(self):
        return self.transaction_name

    def sign(self):
        return self.amount[:1]

    def datepretty(self):
        return self.date.strftime('%b %e,%Y')

    def month(self):
        return self.date.strftime('%b')


