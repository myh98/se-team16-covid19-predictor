from django.shortcuts import render
from django.contrib.auth.models import auth,User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from accounts.models import ishospital,hospitalinfo
from django.http import HttpResponse
from django.contrib import messages
from pymongo import MongoClient, errors
Domain='127.0.0.1'
port=27017

class mongo_DB:

    def __init__(self):
        self.connection=MongoClient("mongodb://hospit:1234@127.0.0.1/hospit_db")
        self.db=self.connection.hospit_db

    def insert(self,cl_name,db_entry):
        # self.db.cl_name.insert_one(db_entry)

        if cl_name=="patient_details":
            self.db.patient_details.insert_one(db_entry)

        elif cl_name=="equipment_details":
            self.db.equipment_details.insert_one(db_entry)

        elif cl_name=="request_details":
            self.db.request_details.insert_one(db_entry)

        elif cl_name=="output_details":
            self.db.output_details.insert_one(db_entry)

        else:
            return False 


    def check_perDayEntry(self,cl_name,check_entry): # for check entry enter hospit_name zone and date 
        
        if cl_name=="patient_details":
            
            return (self.db.patient_details.count_documents(check_entry)==1)
            
        if cl_name=="equipment_details":
            
            return (self.db.equipment_details.count_documents(check_entry)==1)

        if cl_name=="request_details": # Check_entry{'hospit_name':'','zone':,''}
            
            return (self.db.request_details.count_documents(check_entry)==1) 
        


    def update(self,cl_name,entry_type,updated_entry):

        if cl_name=="zone_data" and entry_type=='patient_update':
            #received values
            
            zone=updated_entry['zone']
            

            #find old values
            db_values=self.db.zone_data.find({'zone':zone})
            
            for x in db_values:
                new_active=int(x['active'])+int(updated_entry['active'])
                new_recovered=int(x['recovered'])+int(updated_entry['recovered'])
                new_death=int(x['death'])+int(updated_entry['death'])

            print("new active \n",new_active)
            #update
            self.db.zone_data.update_one({"zone":zone},{"$set":{"active":str(new_active),"recovered":str(new_recovered),"death":str(new_death)}})

        elif cl_name=="zone_data" and entry_type=='equipment_update':
            #received values
            
            zone=updated_entry['zone']
            

            #find old values
            db_values=self.db.zone_data.find({'zone':zone})
            for x1 in db_values:
                new_beds=int(x1['empty_beds'])+int(updated_entry['empty_beds'])
                new_ven=int(x1['empty_ven'])+int(updated_entry['empty_ven'])
                new_ppe=int(x1['ppe_stock'])+int(updated_entry['ppe_stock'])

            #update
            self.db.zone_data.update_one({"zone":zone},{"$set":{"empty_beds":str(new_beds),"empty_ven":str(new_ven),"ppe_stock":str(new_ppe)}})

        else:
            return False


    def entire_collection(self,cl_name): # returns cursor object
        if cl_name=="patient_details":
            return self.db.patient_details.find()

        elif cl_name=="equipment_details":
            return self.db.equipment_details.find()

        elif cl_name=="request_details":
            return self.db.request_details.find()

        elif cl_name=="output_details":
            return self.db.output_details.find()

        elif cl_name=="zone_data":
            return self.db.zone_data.find()

        else:
            return False 
        
    def drop_collection(self,cl_name):
        
        if cl_name=='output_details':
            self.db.output_details.drop()

        elif cl_name=="zone_data":
            self.db.zone_data.drop()
            zone_list=['z1','z2','z3','z4']

            for z in zone_list:
                db_entry={'zone':z,'active':0,'recovered':0,'death':0,'empty_beds':0,'empty_ven':0,'ppe_stock':0}
                self.db.zone_data.insert_one(db_entry)

        else:
            return False

    def delete(self,cl_name,db_entry):
        if cl_name=="patient_details":
            return self.db.patient_details.delete_many(db_entry)


        elif cl_name=="equipment_details":
            return self.db.equipment_details.delete_many(db_entry)


        elif cl_name=="request_details":
            return self.db.request_details.delete_many(db_entry)


        elif cl_name=="output_details":
            return self.db.output_details.delete_many(db_entry)


        elif cl_name=="zone_data":
            return self.db.zone_data.delete_many(db_entry)

        else:
            return False 

# Create your views here.
@csrf_exempt
def signup_hospital(request):
    if request.method=='POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        hospitalname=request.POST['hospitalname']
        lastname=request.POST['lastname']
        pincode=request.POST['pincode']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        repassword=request.POST['repassword']

        if password != repassword:
            messages.info(request,'retyped password is not matching')
            return redirect('signup_hospital')


        query=User.objects.filter(username=username)
        if query.exists():
            messages.info(request,'User name already exists')
            return redirect('signup_hospital')
            # return HttpResponse("user already exist")


        entry=ishospital(username=username,hospital=True)
        entry.save()

        entry1=hospitalinfo(username=username,hospitalname=hospitalname,pincode=pincode)
        entry1.save()



        user=User.objects.create_user(username=username,email=email,password=password,first_name=firstname,last_name=lastname)
        user.save()
        
        messages.info(request,'Account Created Successfully! You can now Sign In')
        return render(request,'signup_hospital.html')

    else:
        return render(request,'signup_hospital.html')


    

@csrf_exempt
def signup_government(request):
    if request.method=='POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        repassword=request.POST['repassword']

        if password != repassword:
            messages.info(request,'retyped password is not matching')
            return redirect('signup_government')

        query=User.objects.filter(username=username)
        if query.exists():
            messages.info(request,'Sorry! This username already exists. Try again')
            return redirect('signup_government')
            # return HttpResponse("user already exist")

        entry=ishospital(username=username,hospital=False)
        entry.save()

        user=User.objects.create_user(username=username,email=email,password=password,first_name=firstname,last_name=lastname)
        user.save()
        
        messages.info(request,'Account Created Successfully! You can now Sign In')
        return render(request,'signup_government.html')



        # print(firstname," first name")
        # print(lastname," last name")
        # return render(request,'signup_government.html')
    else:
        return render(request,'signup_government.html')

    


@csrf_exempt
def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        obj=User.objects.filter(username=username)
        if not obj.exists():
            messages.info(request,"Register first!!")
            return redirect('signin')

        obj1=User.objects.get(username=username)
        # if obj1.password != password:
        #     messages.info(request,"Invalid credentials!!")
        #     return redirect('signin')

        # user1=auth.authenticate(username=username,password=password)
        # print("hello")

        # if user1 == None:
        #     messages.info(request,"Invalid credentials1!!")
        #     return redirect('signin')

        # auth.login(request,user1)

        # current_user=request.user
        
        # print(current_user.username," user name fetched from request")
        # print("logged in",request.user.username)
        # print(request.user,"request user1")
        # auth.logout(request)
        # print(request.user,"request user")

        # if request.user.is_authenticated:
        #     print("logged in",request.user.username)
        # else:
        #     print("logged out")






        return redirect('homehospital')
    else:
        return render(request,'signin.html')

@csrf_exempt
def homehospital(request):
    return render(request,'homehospital.html')

@csrf_exempt
def patientdetail(request):
    if request.method=='POST':
        hospital_name=request.POST['hospitalname']
        pincode=request.POST['pincode']
        zone=request.POST['zone']
        active_cases=request.POST['active']
        recovered_cases = request.POST['recovered']
        deaths=request.POST['deaths']
        date=request.POST['date']
        print("hospital: ", hospital_name)
        # messages.info(request,'In patientdetail. With hospital_name') #TODO: how will this work?

        md = mongo_DB()
        check_entry = {'name':hospital_name, 'zone':zone, 'date':date}
        # check_entry = {'name':'hosp1', 'zone':'z1', 'date':'22-04-19'}
        if md.check_perDayEntry("patient_details", check_entry):
            print("dup")
        else:
            db_entry = {'name':hospital_name, 'pincode':pincode,'zone':zone, 'active':active_cases, 'recovered':recovered_cases, 'death':deaths,'date':date}
            md.insert("patient_details", db_entry)
            zone_entry = {'zone':zone, 'active':active_cases,'recovered':recovered_cases, 'death':deaths}
            
            md.update("zone_data", 'patient_update', zone_entry)
            #TODO display saved successfully


        return redirect('patientdetail') #TODO: is this redirection correct?
    else:
        return render(request,'patientform.html')

@csrf_exempt
def equipmentdetail(request):
    if request.method=='POST':
        hospital_name=request.POST['hospitalname']
        pincode=request.POST['pincode']
        zone=request.POST['zone']
        empty_beds=request.POST['emptybeds']
        occupied_beds = request.POST['occupiedbeds']
        unoccupied_vent=request.POST['unocc_vent']
        occupied_vents=request.POST['occ_vent']
        ppe_kit_count=request.POST['ppe_kit']
        date=request.POST['date']

        #TODO: handle db part
        md = mongo_DB()
        check_entry = {'name':hospital_name, 'zone':zone, 'date':date}
        # check_entry = {'name':'hosp1', 'zone':'z1', 'date':'22-04-19'}
        if md.check_perDayEntry("equipment_details", check_entry):
            print("dup")
        else:
            db_entry = {'name':hospital_name, 'pincode':pincode,'zone':zone, 'empty_beds':empty_beds, 'occupied_beds':occupied_beds, 'empty_ven':unoccupied_vent,'occupied_vents':occupied_vents,'ppe_stock':ppe_kit_count,'date':date}
            md.insert("equipment_details", db_entry)
            zone_entry = {'zone':zone, 'empty_beds':empty_beds,'empty_ven':unoccupied_vent, 'ppe_stock':ppe_kit_count}
            
            md.update("zone_data", 'equipment_update', zone_entry)
            #TODO display saved successfully


        print("zone:", zone)

        return redirect('equipmentdetail') #TODO: is this redirection correct?
    else:
        return render(request,'equipmentform.html')

@csrf_exempt
def requestformdetail(request):
    if request.method=='POST':
        hospital_name=request.POST['hospitalname']
        pincode=request.POST['pincode']
        zone=request.POST['zone']
        bed_request = request.POST['bed_req']
        vent_request = request.POST['vent_req']
        ppe_request = request.POST['ppe_req']
        date = request.POST['date']

        #TODO: handle db part
        md = mongo_DB()
        check_entry = {'hospit_name':hospital_name, 'zone':zone,'date':date}
        # check_entry = {'name':'hosp1', 'zone':'z1', 'date':'22-04-19'}
        if md.check_perDayEntry("request_details", check_entry):
            print("dup")
        else:
            db_entry = {'hospit_name':hospital_name,'zone':zone, 'beds':bed_request, 'vent':vent_request,'ppe_stock':ppe_request,'date':date}
            md.insert("request_details", db_entry)

        print("bed_request:", bed_request)
        return redirect('requestformdetail') #TODO: is this redirection correct?
    else:
        return render(request,'requestform.html')

@csrf_exempt
def register(request):

    if request.method=='POST':
        user_name=request.POST['user_name']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        # user=User.objects.create_user(username=user_name,email=email,password=password,first_name=first_name,last_name=last_name)
        # user.save()
        test=User.objects.get(username=user_name)
        print(test.email)
        # return redirect('/')
        return render(request,'signin.html')



    else:
        return render(request,'register.html')
    

