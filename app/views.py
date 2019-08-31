from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from .models import Pet
from .forms import CreatePetForm, UpdatePetForm, SignupForm, SigninForm
from django.contrib import messages

# Create your views here.

def pet_list(request):
	pets = Pet.objects.all()
	query = request.GET.get("q")
	if query:
		pets = pets.filter(
			Q(name__icontains=query)|
			Q(age__icontains=query)|
			Q(price__icontains=query)
			).distinct()
	
	context = {
		"pets": pets,
	}
	return render(request, 'pet_list.html', context)


def pet_detail(request, pet_id):
	pet = Pet.objects.get(id=pet_id)
	context = {
		"pet": pet,
	}
	return render(request, 'pet_detail.html', context)


def pet_create(request):
	form = CreatePetForm()
	if request.user.is_anonymous:
		return redirect('signin')
	if not request.user.is_staff:
		return redirect("no-access")
	if request.method == "POST":
		form = CreatePetForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'A New Pet Has Been Added.')
			return redirect('pet-list')
	
	context = {
	'form' : form,
	}
	return render(request,'create.html',context)


def pet_update(request, pet_id):
	pet = Pet.objects.get(id=pet_id)
	form = UpdatePetForm(instance=pet)
	if request.user.is_anonymous:
		return redirect('signin')
	if not request.user.is_staff:
		return redirect("no-access")
	if request.method == "POST":
		form = UpdatePetForm(request.POST, request.FILES,instance=pet)
		if form.is_valid():
			form.save()
			messages.info(request, 'Successfully Updated.')
			return redirect('pet-detail',pet_id)

	context = {
	'form' : form,
	'pet' : pet,
	}
	return render(request,'update.html',context)


def pet_delete(request, pet_id):
	pet = Pet.objects.get(id=pet_id)
	if request.user.is_anonymous:
		return redirect('signin')
	if not request.user.is_staff:
		return redirect("no-access")
	pet.delete()
	messages.info(request, 'Successfully Deleted.')
	return redirect('pet-list')


def access(request):
    return render(request,'not-found.html')

def signup(request):
	form = SignupForm()
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)

			user.set_password(user.password)
			user.save()
			login(request, user)
			return redirect("pet-list")
	context = {
		"form":form,
	}
	return render(request, 'signup.html', context)

def signin(request):
	form = SigninForm()
	if request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect('pet-list')
	context = {
		"form":form
	}
	return render(request, 'signin.html', context)

def signout(request):
	logout(request)
	return redirect("signin")
