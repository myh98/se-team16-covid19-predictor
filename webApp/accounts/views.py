from accounts.database_func import mongo_DB
from django.shortcuts import render
from django.contrib.auth.models import auth,User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from accounts.models import ishospital,hospitalinfo
from django.http import HttpResponse
from django.contrib import messages
from pymongo import MongoClient, errors

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
        user1=ishospital.objects.get


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
def zonaldata(request):
    
    if request.method=='POST':
        zonename=request.POST['zone']
        date=request.POST['date']

        print(" zonename ",zonename)
        print("date ",date)

        # TO DO  fetch data(active,recovered,deaths,beds,ventilator,ppc) corresponding to particular zone..
        md = mongo_DB()
        check_entry = {'zone':zonename, 'date':date}
        dict_values = md.retrieveZoneData("zone_data",check_entry)
        active = dict_values['active']
        recovered = dict_values['recovered']
        deaths = dict_values['death']
        beds = dict_values['empty_beds']
        ventilators = dict_values['empty_ven']
        ppe = dict_values['ppe_stock']

        x =  {"zonename":zonename,"active":active, "recovered":recovered, "deaths":deaths,"beds":beds,"ventilators":ventilators,"ppc":ppe}

        return render(request,'zonaldata1.html',x)
    else:
        return render(request,'zonaldata.html')

@csrf_exempt
def showrequest(request):
    # TO DO fetch requests data  here
    # here l is the no of database rows
    db=mongo_DB()
    db_rows=db.entire_collection("request_details")
    obj=[]
    
    for x in db_rows:
    	zone=x['zone']
    	hospital_name=x['hospit_name']
    	beds=x['beds']
    	vent=x['vent']
    	ppe_stock=x['ppe_stock']
    	date=x['date']
    	obj1={'zone':zone,'hospital':hospital_name,'beds':int(beds),'ventilators':int(vent),'ppe':int(ppe_stock),'date':date}
    	obj.append(obj1)

    request_data={'iterator':[]}
    request_data['iterator']=obj


    # TO DO populate your data in obj









    return render(request,'showrequest.html',request_data)


@csrf_exempt
def homehospital(request):
    return render(request,'homehospital.html')

@csrf_exempt
def homegovernment(request):
    return render(request,'homegovernment.html')

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
            zone_entry = {'zone':zone, 'date':date,'active':active_cases,'recovered':recovered_cases, 'death':deaths}
            
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
            zone_entry = {'zone':zone, 'date':date,'empty_beds':empty_beds,'empty_ven':unoccupied_vent, 'ppe_stock':ppe_kit_count}
            
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


@csrf_exempt
def weeklypre(request):
    if request.method=="POST":
        zonename=request.POST['zone']
        date=request.POST['date']

        # use zonename and date to retrieve data from data base
        print("zonename1",zonename)
        print("date1",date)

        md = mongo_DB()
        new_list = []
        death_list = []
        check_entry = {'zone':zonename}
        cursor_rcvd = md.retrieveZoneData("output_details", check_entry)

        for entry in cursor_rcvd:
            for i in range(1,8):
                col = str(i)+"_x"
                new_list.append(entry[col])
                # col = str(i)+"_y"
                # death_list.append(entry[col])
        print(new_list)
        # print(death_list)

        x={"zonename":zonename,"data_list":new_list}
        # y={"zonename":zonename,"data_list":death_list}

        # update dictionary x's data_list field and put real data from database

        return render(request,'weeklypre1.html',x)


    else:
        return render(request,'weeklypre.html')  


db.output_details.insert({'zone':'Alwal','1_x':2,'2_x':3,'3_x':3,'4_x':4,'5_x':5,'6_x':6,'7_x':2,'1_y':2,'2_y':3,'3_y':3,'4_y':4,'5_y':5,'6_y':6,'7_y':2})