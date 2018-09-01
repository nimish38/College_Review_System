from django.contrib.auth import authenticate,logout,login
from django.shortcuts import render,get_object_or_404,redirect
from .models import Review,College
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import ReviewForm,UserForm
import datetime


def review_list(request):
	if(request.user.is_authenticated==False):
		return render(request, 'Reviews/login.html')
	else:	
		latest_review_list=Review.objects.order_by('-pub_date')[:9]
		context={'latest_review_list':latest_review_list}
		return render(request,'Reviews/review_list.html',context)
	
def review_detail(request,review_id):
	review=get_object_or_404(Review,pk=review_id)
	return render(request,'Reviews/review_detail.html',{'review':review})
	
def college_list(request):
	college_list=College.objects.order_by('-name')
	context={'college_list':college_list}
	return render(request,'Reviews/college_list.html',context)
	
def college_detail(request,college_id):
	college=get_object_or_404(College,pk=college_id)
	form=ReviewForm()
	return render(request,'Reviews/college_detail.html',{'college':college, 'form':form})

def add_review(request,college_id):
	college = get_object_or_404(College, pk=college_id)
	form = ReviewForm(request.POST)
	if form.is_valid():
		rating = form.cleaned_data['rating']
		description = form.cleaned_data['description']
		user_name = form.cleaned_data['user_name']
		review = Review()
		review.college = college
		review.user_name = request.user.username
		review.rating = rating
		review.description = description
		review.pub_date = datetime.datetime.now()
		review.save()
        # returning an HttpResponseRedirect prevents data from being posted twice if a
        # user hits the Back button.
		return HttpResponseRedirect(reverse('Reviews:add_review', args=(college.id,)))
	return render(request, 'Reviews/college_detail.html', {'college': college, 'form': form})
	
def login_user(request):
	if(request.method=="POST"):
		username=request.POST['username']
		password=request.POST['password']
		user=authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('Reviews:review_list')
		else:
			return render(request,'Reviews/login.html')
	return render(request,'Reviews/login.html')

def create_new_user(request):
	form=UserForm(data=request.POST)	
	if form.is_valid():
		user=form.save(commit=False)
		username=form.cleaned_data['username']
		password=form.cleaned_data['password']
		user.set_password(password)
		user.save()
		login(request,user)
		return redirect('Reviews:review_list')
	context={
		"form":form,
	}
	return render(request, 'Reviews/create_new_user.html',context)
	
def logout_user(request):
	logout(request)
	form=UserForm(request.POST or None)
	return render(request, 'Reviews/login.html',{"form":form,})