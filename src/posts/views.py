from urllib import  quote_plus 
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect,Http404
from .forms import PostForm
from .models import  Post
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone


# Create your views here.
def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form=PostForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	context={"form":form,}
	return render(request,"post_form.html",context)
def post_detail(request,slug=None):
	instance=get_object_or_404(Post,slug=slug)
	if instance.draft or instance.publish>timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404

	
		
	instance=get_object_or_404(Post,slug=slug)
	share_string=quote_plus(instance.content)
	context={"title":instance.title,"object":instance,"share_string":share_string}
	
	return render(request,"post_detail.html",context)
def post_list(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	queryset_list=Post.objects.active()

	query=request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 2)
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context={"title":"List","object_list":queryset}
	return render(request,"post_list.html",context) 

   



def post_update(request,slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(Post,slug=slug)
	form=PostForm(request.POST or None,request.FILES or None,instance =instance)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.user=request.user
		instance.save()
		messages.success(request,"successfully updated")
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		messages.success(request,"not updated")

	
	context={"title":instance.title,"object":instance,"form":form}
	
	return render(request,"post_form.html",context)
def post_delete(request,slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(Post,slug=slug)
	instance.delete()
	return redirect("posts:list")



  
    	

    	
    
    	
        
        
    
        # If page is out of range (e.g. 9999), deliver last page of results.
        

	
	