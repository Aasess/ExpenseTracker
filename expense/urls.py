from django.contrib import admin
from django.urls import path
from . import views

urlpatterns =[
    path('',views.home,name="home"),
    path('history/',views.history,name="history"),
    path('history/edit/<int:transaction_id>',views.edit,name="edit"),
    path('history/<int:transaction_id>/delete',views.delete,name="delete")
]