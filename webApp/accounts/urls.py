from django.urls import path
from . import views

urlpatterns = [
    path('',views.signin,name='signin'),
    path('signin',views.signin,name='signin'),
    # path('register',views.register,name='register'),
    path('signup_hospital',views.signup_hospital,name='signup_hospital'),
    path('signup_government',views.signup_government,name='signup_government'),
    path('homehospital',views.homehospital,name='homehospital'),
    path('homegovernment',views.homegovernment,name='homegovernment'),

    path('patientdetail',views.patientdetail,name='patientdetail'),
    path('equipmentdetail',views.equipmentdetail,name='equipmentdetail'),
    path('requestformdetail',views.requestformdetail,name='requestformdetail'),
    path('zonaldata',views.zonaldata,name='zonaldata'),
    path('showrequest',views.showrequest,name='showrequest'),
    path('weeklypre',views.weeklypre,name="weeklypre"),
    path('logout',views.logout,name="logout"),




    # path('add',views.add,name='add'),
]

