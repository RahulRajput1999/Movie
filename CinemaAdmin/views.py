from django.shortcuts import render_to_response,redirect,render
from datetime import datetime
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from login.models import *
from django.contrib.auth import *
from login.forms import *
from django.contrib.auth.forms import PasswordChangeForm
def home(request):
    c={}
    if request.user.is_authenticated:
        id = request.user.id
        user = User.objects.get(id = id)
        if user is not None:
            cinema_id = user.username
            request.session['cinema_id'] = cinema_id
            movies = {}
            mov = Movie.objects.filter(cinema_id = cinema_id)
            offers = {}
            off = Offers.objects.filter(cinema_id = cinema_id)
    if mov is not None:
        for i in mov:
            movies[i.movie_name] = i.movie_details
        c['movies'] = mov
    if off is not None:
        for j in off:
            offers[j.offer_name] = j.offer_details
        c['offers'] = offers
    c.update(csrf(request))
    if request.user.is_authenticated:
        return render(request,'cinema-home.html',c)
    else:
        return HttpResponseRedirect('/login/invalidlogin')
def about(request):
    c={}
    c.update(csrf(request))
    if request.user.is_authenticated:
        return render(request,'about_cin.html',c)
    else:
        return HttpResponseRedirect('/login/invalidlogin')
def contact(request):
    c={}
    c.update(csrf(request))
    if request.user.is_authenticated:
        return render(request,'contact_cin.html',c)
    else:
        return HttpResponseRedirect('/login/invalidlogin')
def profile(request):
    c={}
    c.update(csrf(request))
    if request.user.is_authenticated:
        id = request.user.id
        user = User.objects.get(id = id)
        if user is not None:
            username = user.username
            list2 = Cinema.objects.filter(cinema_id = username)
            count = list2.count()
            if int(count)>0:
                user_name = list2[0].cinema_id
                full_name = list2[0].cinema_name
                email = list2[0].email
                phoneno = list2[0].phoneno
                addr = list2[0].address
                c['user_name'] = user_name
                c['full_name'] = full_name
                c['email'] = email
                c['phoneno'] = phoneno
                c['addr'] = addr
            c['count'] = username
        return render(request,'profile2.html',c)
    else:
        return HttpResponseRedirect('/login/invalidlogin')
def editPassword(request):
    c = {}
    c.update(csrf(request))
    return render(request,'update_password_cin.html',c)
def editProfile(request):
    c={}
    c.update(csrf(request))
    if request.user.is_authenticated:
        id = request.user.id
        user = User.objects.get(id = id)
        if user is not None:
            username = user.username
            request.session['cinema_id'] = username
            list2 = Cinema.objects.filter(cinema_id = username)
            count = list2.count()
            if int(count)>0:
                cin_name = list2[0].cinema_name
                phoneno = list2[0].phoneno
                addr = list2[0].address
                c['cin_name'] = cin_name
                c['phoneno'] = phoneno
                c['addr'] = addr
        return render(request,'edit_profile_cin.html',c)
    else:
        return HttpResponseRedirect('/login/invalidlogin')
def addNewMovie(request):
    c = {}
    c.update(csrf(request))
    return render(request,'add_new_movie.html',c)
def addNewOffer(request):
    c = {}
    c.update(csrf(request))
    return render(request,'add_new_offer.html',c)
def addNewShow(request):
    c = {}
    c.update(csrf(request))
    mid = request.GET.get('mid','')
    cid = request.session['cinema_id']
    mname = request.GET.get('mname','')
    request.session['movie_id'] = mid
    show = Show.objects.filter(cinema_id = cid,movie_id = mid)
    print(mid+'  '+cid)
    c['show'] = show
    c['mname'] = mname
    return render(request,'add_new_show.html',c)
def add(request):
    c = {}
    c.update(csrf(request))
    name = request.POST.get('name','')
    details = request.POST.get('detail','')
    user = User.objects.get(id = request.user.id)
    if user is not None:
        cinema = user.username
        cin = Cinema.objects.filter(cinema_id = cinema)
        if int(cin.count())>0:
            movie = Movie(cinema_id=cin[0],movie_name=name,movie_details=details)
            movie.save()
        else:
            HttpResponseRedirect('/CinemaAdmin/addNewMovie/')
    else:
        HttpResponseRedirect('/CinemaAdmin/addNewMovie/')
    return HttpResponseRedirect('/CinemaAdmin/home')
def add2(request):
    c = {}
    c.update(csrf(request))
    user = User.objects.get(id = request.user.id)
    name = request.POST.get('name','')
    details = request.POST.get('detail','')
    if user is not None:
        cinema = user.username
        cin = Cinema.objects.filter(cinema_id = cinema)
        if int(cin.count())>0:
            offer = Offers(cinema_id=cin[0],offer_name=name,offer_details=details)
            offer.save()
    return HttpResponseRedirect('/CinemaAdmin/home')
def add3(request):
    c = {}
    c.update(csrf(request))
    time = request.POST.get('time','')
    pex = request.POST.get('price_ex','')
    ppr = request.POST.get('price_pr','')
    c_id = request.session['cinema_id']
    m_id = request.session['movie_id']
    cinema = Cinema.objects.filter(cinema_id = c_id)
    movie = Movie.objects.filter(movie_id = m_id)
    if int(movie.count())>0:
        show = Show(cinema_id = cinema[0],movie_id = movie[0], time = time, price_ex = pex, price_pr = ppr)
        show.save()
        print('added')
    else:
        print('failed')
    return HttpResponseRedirect('/CinemaAdmin/home')
