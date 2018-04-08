from django.shortcuts import render_to_response,redirect,render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from login.models import *
from django.contrib.auth import *
from login.forms import *
from django.contrib.auth.forms import PasswordChangeForm

def login1(request): #view for login page...
	c ={}
	c.update(csrf(request))
	return render(request,'index.html',c)
def restore(request): #view for password recovery page...
        c={}
        c.update(csrf(request))
        return render(request,'restore.html',c)
def updateProfile(request): #view for inserting profile data in to databse...
        c = {}
        c.update(csrf(request))
        name= request.POST.get('name','')
        phone= request.POST.get('phone', '')
        date= request.POST.get('date', '')
        if request.user.is_authenticated:
                id = request.user.id
                user = User.objects.get(id = id)
                if user is not None:
                        username = user.username
                        list2 = Puser.objects.filter(user_id = username)
                        count = list2.count()
                        if int(count)>0:
                                pUser = list2[0]
                                pUser.user_name = name
                                pUser.phoneno = phone
                                pUser.bdate = date
                                pUser.save()
                        else:
                                return render(request,'edit_profile.html',c)
                return HttpResponseRedirect('/home/profile')
        else:
                return HttpResponseRedirect('/login/invalidlogin')
def updateCinemaProfile(request): #view for updating the cinema profile in databse...
        c = {}
        c.update(csrf(request))
        name= request.POST.get('name','')
        phone= request.POST.get('phone', '')
        address= request.POST.get('address', '')
        if request.user.is_authenticated:
                id = request.user.id
                user = User.objects.get(id = id)
                if user is not None:
                        username = user.username
                        list2 = Cinema.objects.filter(cinema_id = username)
                        count = list2.count()
                        if int(count)>0:
                                cUser = list2[0]
                                cUser.cinema_name = name
                                cUser.phoneno = phone
                                cUser.address = address
                                cUser.save()
                        else:
                                return render(request,'edit_cin.html',c)
                return HttpResponseRedirect('/CinemaAdmin/profile')
        else:
                return HttpResponseRedirect('/login/invalidlogin')
def updatePassword(request): #view to update the password in database...
	c={}
	c.update(csrf(request))
	id = request.user.id
	cuser = User.objects.get(id=id)
	form = PasswordChangeForm(request.user, request.POST)
	c['form']=form
	if form.is_valid():
		profile= Cinema.objects.get(cinema_id=cuser.username);
		profile.password=request.POST.get('new_password1','');
		profile.save()
		user = form.save()
		update_session_auth_hash(request, user)  # Important!
		#messages.success(request, 'Your password was successfully updated!')
	else:
                return render(request,'cinema-home.html',c)
		#return render(request,'home.hmtl',c)
	return render(request,'cinema-home.html',c)

def update(request): #view to update the password in databse...
	c={}
	c.update(csrf(request))
	id = request.user.id
	puser = User.objects.get(id=id)
	form = PasswordChangeForm(request.user, request.POST)
	c['form']=form
	if form.is_valid():
		profile= Puser.objects.get(user_id=puser.username);
		profile.password=request.POST.get('new_password1','');
		profile.save()
		user = form.save()
		update_session_auth_hash(request, user)  # Important!
		#messages.success(request, 'Your password was successfully updated!')
	else:
                return render(request,'home.html',c)
		#return render(request,'home.hmtl',c)
	return render(request,'home.html',c)
def recover(request): #view to diaspalay the password after successfull recovery...
        c={}
        c.update(csrf(request))
        username = request.POST.get('username')
        bdate = request.POST.get('date')
        l = [bdate]
        list = Puser.objects.filter(user_id = username)
        password = ' '
        if int(list.count())>0:
                date = [list[0].bdate];
                d1 = str(l[0])
                d2 = str(date[0])
                cmp = d2.find(d1)
                if int(cmp>=0):
                        password = 'Your password is:'+str(list[0].password)
                else:
                        password = password+'Invalid details!'
        else:
                password = password+'Invalid details!'
        c['msg'] = password
        return render(request,'restore.html',c)

def auth_view(request): #view to aquthenticate the user...
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	cuser = Cinema.objects.filter(cinema_id=username)
	count = cuser.count()
	if user is not None:
		auth.login(request, user)
		if int(count)>0:
                        return HttpResponseRedirect('/CinemaAdmin/home/')
		return HttpResponseRedirect('/login/loggedin/')
	else:
		return HttpResponseRedirect('/login/invalidlogin/')

@login_required(login_url = '/login/')

def loggedin(request): #view for redirecting valid user to home page...
	if request.user.is_authenticated:
		return HttpResponseRedirect('/home/location/')
	else:
		return HttpResponseRedirect('/login/invalidlogin/')

def invalidlogin(request): #view to redirect the invalid user to login page...
	c ={}
	c.update(csrf(request))
	c['q']="Invalid UserName or PassWord"
	return render(request,'index.html',c)
	
def signUp(request): #view to show the signup page...
	c ={}
	c.update(csrf(request))
	c['role'] = 'member'
	return render(request,'signup.html',c)

def store(request): #view to store the new user data in to datbase...
	username= request.POST.get('username', '')
	name= request.POST.get('name','')
	password1= request.POST.get('password1', '')
	password2= request.POST.get('password2', '')
	email= request.POST.get('email','')
	phone= request.POST.get('phone', '')
	date= request.POST.get('date', '')
	c ={}
	c.update(csrf(request))
	form = SignUpForm(request.POST)
	c['form']=form;
	c['role'] = 'member'
	if form.is_valid():
			profile= Puser(user_id=username,user_name=name,email=email,phoneno=phone,bdate=date,password=password1)
			profile.save()
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return render(request,'home.html')
	return render(request,'signup.html',c)

def cinstore(request): #view to store the new cinema profile in to the databse...
	username = request.POST.get('username', '')
	name = request.POST.get('name','')
	password1 = request.POST.get('password1', '')
	password2 = request.POST.get('password2', '')
	email = request.POST.get('email','')
	phone = request.POST.get('phone', '')
	city = request.POST.get('city','')
	address= request.POST.get('address','')
	c={}
	c.update(csrf(request))
	form = SignUpForm(request.POST)
	c['form']=form;
	c['role'] = 'manager'
	if form.is_valid():
			profile= Cinema(cinema_id=username,cinema_name=name,email=email,phoneno=phone,password=password1,address=address,city=city)
			profile.save()
			offer = Offers(cinema_id=profile,offer_name="default",offer_details="default")
			form.save()
			offer.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			city_ob = City.objects.filter(city = city)
			if int(city_ob.count())<=0:
                                ci = City(city = city)
                                ci.save()                                        
			login(request, user)
			return render(request,'cinema-home.html')
	return render(request,'signup.html',c)
	
def logout(request): #view for log out the user...
	auth.logout(request)
	return render(request,'index.html')
