from django.db import models

# Create your models here.

class ishospital(models.Model):
    username=models.CharField(max_length=50,primary_key=True)
    hospital=models.BooleanField()
    class Meta:
        db_table="ishospital"


class hospitalinfo(models.Model):
    username=models.CharField(max_length=50,primary_key=True)
    hospitalname=models.CharField(max_length=50)
    pincode=models.IntegerField()
    class Meta:
        db_table="hospitalinfo"


