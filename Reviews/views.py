from django.contrib.auth import authenticate,logout,login
from django.shortcuts import render,get_object_or_404,redirect
from .models import Review,College,PendingQuery,AnsweredQueries, StudentUser, IndustryUser,Department,Cutoff, Category
from django.urls import reverse
from django.http import HttpResponseRedirect,JsonResponse
from .forms import ReviewForm,StudUserForm, UserForm, IndUserForm
import datetime
from textblob import TextBlob


def get_deps(request):
	if request.is_ajax():
		q=request.GET.get('clg', None)
		c=College.objects.filter(name=q)[0]
		queryset = Department.objects.filter(college=c)
		list = []
		for i in queryset:
			if i.department!='TnP':
				list.append(i.department)
		data = {
			'list': list,
		}
		return JsonResponse(data)
	return render(request,'Reviews/create_new_user.html',{})


def recommend(request):
    if request.method == "POST":
        marks=int(request.POST['marks'])
        rank=int(request.POST['rank'])
        dep=request.POST.getlist('dep')
        caste=Category.objects.filter(caste=request.POST['caste'])
        best_clgs=Cutoff.objects.filter(dept__in=dep, caste=caste[0], score__lte=marks, rank__gte=rank).order_by('-score')
        print(best_clgs)
        if len(best_clgs)>5:
            best_clgs=best_clgs[:5]
        return render(request,'Reviews/rec_result.html',{'best_clgs': best_clgs})
    return render(request,'Reviews/recommender.html')


def answer_query(request):
    qsn=request.POST['qstn']
    col=request.POST['colg']
    context={
        'qsn': qsn,
        'col': col,
    }
    return render(request,'Reviews/answer.html',context)


def submit_query(request):
    qsn = request.POST['qstn']
    col = request.POST['colg']
    ans = request.POST['ans']
    aq=AnsweredQueries()
    aq.qsn=qsn
    aq.ans=ans
    pq = PendingQuery.objects.filter(qsn=qsn).delete()
    clge = College.objects.filter(name=col)
    clg = clge[0]
    aq.college=clg
    aq.save()
    deps = Department.objects.filter(college=clg)
    form = ReviewForm()
    user_clg = 'none'
    if not request.user.is_anonymous:
        if StudentUser.objects.filter(user=request.user).exists():
            user_clg = StudentUser.objects.filter(user=request.user)[0].college
        if IndustryUser.objects.filter(user=request.user).exists():
            user_clg = clg.name
    return render(request, 'Reviews/college_detail.html',{'college': clg, 'deps': deps, 'form': form, 'user_clg': user_clg})


def add_college(request):
	college_name=request.POST['clg']
	col = College()
	col.name = college_name
	col.save()
	form = ReviewForm()
	return render(request, 'Reviews/college_detail.html', {'college': col, 'form': form})


def req_query(request):
    qry = request.POST['qry']
    college_nm=request.POST['col']
    clge = College.objects.filter(name=college_nm)
    clg = clge[0]

    pq = PendingQuery()
    pq.college = clg
    pq.qsn = qry
    pq.save()
    deps = Department.objects.filter(college=clg)
    form = ReviewForm()
    user_clg = 'none'
    if not request.user.is_anonymous:
        if StudentUser.objects.filter(user=request.user).exists():
            user_clg = StudentUser.objects.filter(user=request.user)[0].college
        if IndustryUser.objects.filter(user=request.user).exists():
            user_clg = clg.name
    return render(request, 'Reviews/college_detail.html',{'college': clg, 'deps': deps, 'form': form, 'user_clg': user_clg})



def searched(request):
	if request.method == "POST":
		clg_name = request.POST['autocomplete-college']
		if College.objects.filter(name=clg_name).exists():
			clge = College.objects.filter(name=clg_name)
			clg=clge[0]
			form = ReviewForm()
			return render(request, 'Reviews/college_detail.html', {'college': clg, 'form': form, 'user_clg':'none'})
		else:
			return render(request, 'Reviews/add_clg.html', {'name': clg_name})
	return render(request, 'Reviews/Search.html')


def autocomplete_college(request):
	if request.is_ajax():
		q=request.GET.get('search', None)
		queryset = College.objects.filter(name__startswith=q)
		list = []
		for i in queryset:
			list.append(i.name)
		data = {
			'list': list,
		}
		return JsonResponse(data)
	return render(request,'Reviews/Search.html',{})


def review_list(request):
	if request.user.is_authenticated==False:
		return render(request, 'Reviews/Search.html')
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
	deps=Department.objects.filter(college=college)
	form=ReviewForm()
	user_clg = 'none'
	if not request.user.is_anonymous:
		if StudentUser.objects.filter(user=request.user).exists():
			user_clg = StudentUser.objects.filter(user=request.user)[0].college
		if IndustryUser.objects.filter(user=request.user).exists():
			user_clg = college.name
	return render(request,'Reviews/college_detail.html',{'college':college,'deps':deps, 'form':form, 'user_clg':user_clg})


def add_review(request,college_id):
	college = get_object_or_404(College, pk=college_id)
	deps = Department.objects.filter(college=college)
	form = ReviewForm(request.POST)
	user_clg = 'none'
	if not request.user.is_anonymous:
		if StudentUser.objects.filter(user=request.user).exists():
			user_clg = StudentUser.objects.filter(user=request.user)[0].college
		if IndustryUser.objects.filter(user=request.user).exists():
			user_clg = college.name
	if form.is_valid():
		description = form.cleaned_data['description']
		anonymous=form.cleaned_data['anonymous']
		acad = int(form.cleaned_data['academic_rate'])
		place = int(form.cleaned_data['placement_rate'])
		infra = int(form.cleaned_data['infra_rate'])
		val=TextBlob(description)
		rate=val.sentiment.polarity

		# normalization

		rating = ((rate+1)*5)/2
		print(rate, rating)
		tot_rate = (acad + place + infra + rating)/4
		rating = round(tot_rate, 1)

		review = Review()
		review.college = college
		if StudentUser.objects.filter(user=request.user).exists():
			review.dept = StudentUser.objects.filter(user=request.user)[0].dept
		if IndustryUser.objects.filter(user=request.user).exists():
			review.dept = Department.objects.filter(college=college, department='TnP')[0]
		if anonymous:
			review.user_name = "Anonymous"
		else:
			review.user_name = request.user.username
		review.academic_rate = acad
		review.placement_rate = place
		review.infra_rate = infra
		review.rating = rating
		review.description = description
		review.pub_date = datetime.datetime.now()
		review.save()

		# returning an HttpResponseRedirect prevents data from being posted twice if a user hits the Back button.

		return HttpResponseRedirect(reverse('Reviews:add_review', args=(college.id,)))
	return render(request, 'Reviews/college_detail.html', {'college': college,'deps':deps,'user_clg': user_clg, 'form': form})


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
	Uform = UserForm(data=request.POST)
	Sform = StudUserForm(data=request.POST)
	Iform = IndUserForm(data=request.POST)
	if request.method == "POST":
		if Uform.is_valid() and Sform.is_valid():
			user = Uform.save(commit=False)
			password = Uform.cleaned_data['password']
			user.set_password(password)
			user.save()
			Sform.save(commit=False)
			stud=StudentUser()
			stud.user=user
			stud.college=Sform.cleaned_data['college']
			stud.category=Sform.cleaned_data['category']
			d=Sform.cleaned_data['depart']
			stud.dept = Department.objects.filter(department=d,college=stud.college)[0]
			print(stud.dept.department,stud.dept.college)
			stud.save()
			login(request, user)
			return redirect('Reviews:review_list')

		if Uform.is_valid() and Iform.is_valid():
			user = Uform.save(commit=False)
			password = Uform.cleaned_data['password']
			user.set_password(password)
			user.save()
			Iform.save(commit=False)
			ind=IndustryUser()
			ind.user=user
			ind.company=Iform.cleaned_data['company']
			ind.save()
			login(request, user)
			return redirect('Reviews:review_list')
	context = {
		"Uform": Uform,
		"Sform": Sform,
		"Iform": Iform,
	}
	return render(request, 'Reviews/create_new_user.html',context)


def logout_user(request):
	logout(request)
	form=StudUserForm(request.POST or None)
	return render(request, 'Reviews/login.html', {"form": form})
