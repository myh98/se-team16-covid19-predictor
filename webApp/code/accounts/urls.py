from django.urls import path
from . import views

urlpatterns = [
    path('',views.signin,name='signin'),
    path('signin',views.signin,name='signin'),
    # path('register',views.register,name='register'),
    path('signup_hospital',views.signup_hospital,name='signup_hospital'),
    path('signup_government',views.signup_government,name='signup_government'),
    path('homehospital',views.homehospital,name='homehospital'),

    # path('add',views.add,name='add'),
]

