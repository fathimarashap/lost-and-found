from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.userlogin, name='login'),
    path('register/', views.register, name='register'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('userhome/', views.userhome, name='userhome'),
    path('viewuser/', views.viewuser, name='viewuser'),
    path('viewitems/', views.viewitems, name='viewitems'),
    path('viewfound/', views.viewfound, name='viewfound'),
    path('viewcomplaint/', views.viewcomplaint, name='viewcomplaint'),
    path('reply/<int:id>/', views.reply, name='reply'),
    path('viewprofile/', views.viewprofile, name='viewprofile'),
    path('changepass/', views.changepass, name='changepass'),
    path('managelost/', views.managelost, name='managelost'),
    path('addlost/', views.addlost, name='addlost'),
    path('viewlost/', views.viewlost, name='viewlost'),
    path('updatelost/<int:id>/', views.updatelost, name='updatelost'),
    path('viewreply/', views.viewreply, name='viewreply'),
    path('sendcomplaint/', views.sendcomplaint, name='sendcomplaint'),
    path('editlost/<int:id>/', views.editlost, name='editlost'),
    path('deletelost/<int:id>/', views.deletelost, name='deletelost'),
    path('logout/', views.userlogout, name='logout'),
    path('view_my_found/', views.view_my_found, name='view_my_found'),
    path('confirm_found/<int:id>/', views.confirm_found, name='confirm_found'),
]
