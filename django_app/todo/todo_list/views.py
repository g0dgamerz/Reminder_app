from django.shortcuts import render,redirect
from .models import List
from .forms import ListForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.
def home(request):
	if request.method=='POST':
		form = ListForm(request.POST or None)

		if form.is_valid():
			form.save()
			all_items=List.objects.all
			messages.success(request,('Item has been added'))
			return render(request,'home.html',{'all_items':all_items})

	else:
		all_items = List.objects.all
		return render(request, 'home.html', {'all_items':all_items})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data('username')
            password = form.cleaned_data('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
         form = UserCreationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)



def delete(request,list_id):
	item = List.objects.get(pk=list_id)
	item.delete()
	messages.success(request,'Item has been deleted')
	return redirect('home')

def cross_off(request, list_id):
	item= List.objects.get(pk=list_id)
	item.completed = True
	item.save()
	return redirect('home')


def uncross(request, list_id):
	item = List.objects.get(pk=list_id)
	item.completed = False
	item.save()
	return redirect('home')

def edit(request, list_id):
	if request.method =="POST":
		item = List.objects.get(pk=list_id)
		form = ListForm(request.POST or None, instance=item)

		if form.is_valid():
			form.save()
			all_items=List.objects.all()
			messages.success(request,'Item has been Edited')
			return redirect('home')

	else:
		item = List.objects.get(pk=list_id)
		return render(request,'edit.html',{'item': item})
