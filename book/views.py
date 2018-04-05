from django.shortcuts import render_to_response,redirect,render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect,HttpResponse
from django.http import JsonResponse
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from login.models import *
from django.contrib.auth import *
from login.forms import *

def seats(request):
        c={}
        c.update(csrf(request))
        sid = request.POST.get('sid','')
        request.session['sid'] = sid
        show = Show.objects.filter(show_id = int(sid))
        seat = show[0].seat
        #seat="0110100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"
        com='1'
        c['chart']=seat
        c['com']=com
        price1=show[0].price_ex;
        price2=show[0].price_pr;
        c['price1']=price1
        c['price2']=price2
        return render(request,'seats.html',c)
def ticket(request):
	c={}
	c.update(csrf(request))
	sid = request.session['sid']
	show = Show.objects.get(show_id = sid)
	show.seat = request.POST.get('chart')
	#show.save()
	user = request.user.username
	puser = Puser.objects.filter(user_id = user)
	ticket = Ticket(user_id = puser[0], show_id = show)
	#ticket.save()
	print(request.POST.get('total'))
	print(request.POST.get('count'))
	return render(request,'seats.html',c)
	
