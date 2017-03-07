from urllib import  quote_plus 
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect,Http404
from .forms import PostForm
from .models import  Post
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Create your views here.
def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form=PostForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
	context={"form":form,}
	return render(request,"post_form.html",context)
def post_detail(request,id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(Post,id=id)
	share_string=quote_plus(instance.content)
	context={"title":instance.title,"object":instance,"share_string":share_string}
	
	return render(request,"post_detail.html",context)
def post_list(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	queryset_list=Post.objects.all()
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

   



def post_update(request,id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(Post,id=id)
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
def post_delete(request,id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(Post,id=id)
	instance.delete()
	return redirect("posts:list")



     
    	

    	
    
    	
        
        
    
        # If page is out of range (e.g. 9999), deliver last page of results.
        

	
	