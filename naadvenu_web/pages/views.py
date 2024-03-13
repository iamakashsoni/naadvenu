from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Gallery, Contact, Event, Student, MediaCoverage
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.core.files.base import ContentFile
import base64
import os
from django.conf import settings
from django.forms.utils import ErrorDict

def home(request):
    return render(request, "pages/home.html", {})

def events_workshops(request):
    events = Event.objects.all()
    return render(request, "pages/events-workshops.html", {'events': events})

def gallery(request):
    gallery_items = Gallery.objects.all()
    if request.method == 'POST' and request.user.is_authenticated:
        post_id = request.POST.get('post_id')
        post = Gallery.objects.get(id=post_id)
        if request.user in post.users_liked.all():
            post.users_liked.remove(request.user)
        else:
            post.users_liked.add(request.user)
    return render(request, "pages/gallery.html", {'gallery_items': gallery_items})

def media_coverage(request):
    media_items = MediaCoverage.objects.all()
    if request.method == 'POST' and request.user.is_authenticated:
        post_id = request.POST.get('post_id')
        post = MediaCoverage.objects.get(id=post_id)
        if request.user in post.users_liked.all():
            post.users_liked.remove(request.user)
        else:
            post.users_liked.add(request.user)
    return render(request, "pages/media-coverage.html", {'media_items': media_items})


def galleryitem(request, slug):
    item = get_object_or_404(Gallery, slug=slug)
    return render(request, 'pages/gallery-item.html', {'item': item})

def media_coverage_item(request, slug):
    item = get_object_or_404(MediaCoverage, slug=slug)
    return render(request, 'pages/media-coverage-item.html', {'item': item})

def serve_media_file(request, path):
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        return FileResponse(open(file_path, 'rb'), content_type='image/jpg')
    except FileNotFoundError:
        raise Http404

def contactUs(request):
    contacts = Contact.objects.all()
    return render(request, "pages/contact-us.html",{'contacts': contacts})

def aboutUs(request):
    return render(request, "pages/about-us.html", {})

@login_required
def studentRegistration(request):
    try:
        student = Student.objects.get(user=request.user)
        if request.method == 'POST':
            student.email = request.POST.get('email')
            student.phone_number = request.POST.get('phone_number')
            student.address = request.POST.get('address')
            # Save the updated student instance
            student.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('studentRegistration')
        else:
            # Render the form with the existing student data for updating
            return render(request, "pages/student-registrations.html", {'student': student})
    except Student.DoesNotExist:
        if request.method == 'POST':
            # Retrieve user information from the request
            user = request.user
            email = user.email
            name = user.username
            date_of_birth = request.POST.get('date_of_birth')
            occupation = request.POST.get('occupation')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            
            photo_file = request.FILES.get('photo')

            try:
                # Ensure all required fields are provided
                if name and date_of_birth and occupation and phone_number and address:
                    # Create a new Student instance with the current user
                    student = Student.objects.create(
                        user=user,
                        date_of_birth=date_of_birth,
                        phone_number=phone_number,
                        email=email,
                        address=address,
                        occupation=occupation,
                        level='level1'
                    )

                    # Save profile photo if provided
                    if photo_file:
                        student.photo.save(photo_file.name, photo_file, save=True)

                    messages.success(request, 'Registration successful!')
                    return redirect('home')
                else:
                    error_message = "Please provide the following required field(s): "
                    error_fields = []
                    if not name:
                        error_fields.append("Name")
                    if not date_of_birth:
                        error_fields.append("Date of Birth")
                    if not occupation:
                        error_fields.append("Occupation")
                    if not phone_number:
                        error_fields.append("Phone Number")
                    if not address:
                        error_fields.append("Address")

                    error_message += ", ".join(error_fields)
                    messages.error(request, error_message)
                    return redirect('studentRegistration')
            except Exception as e:
                messages.error(request, f'Error occurred: {e}')
                return redirect('studentRegistration')
        else:
            # Render the registration form
            username = request.user.username
            email = request.user.email
            return render(request, "pages/student-registrations.html", {'username': username, 'email': email})

@login_required
def generate_sargam(swar_notation):
    swar=["सा","रे","ग","म","प","ध","नि","सां"]
    sub=""
    sub1=""
    sub2=""
    inp=str(swar_notation)
    aroh,index,avroh=[],[],[]
    count=0

    for i in inp:
        index.append(int(i))

    if 7 in index:
        ind1=index[:(len(index)//2)]
        ind2=index[(len(index)//2):]

        ar1,ar2=[],[]

        while count<=7:
        
            for i in ind1:
                sub1+=swar[i]
            ar1.append(sub1)

            if "सां" in sub1 or "सा" in sub2:
                def lastswar():
                    temps=""
                    for i in ind2:
                        temps+=swar[i]
                    if "सा" in temps:
                        ar2.append(temps)
                lastswar()
                break

            sub1=""

            for i in ind2:
                sub2+=swar[i]
            ar2.append(sub2)
        
            sub2=""
        
            for i in range(0,len(ind1)):
                if i>7:
                    break
                ind1[i]+=1

            for i in range(0,len(ind2)):
                if i<0:
                    break        
                ind2[i]-=1

            count+=1

        n=0
        for i in ar1:
            for j in range(n,len(ar2)):
                aroh.append(i+ar2[j])
                avroh.append(ar2[j]+i)
                break
            n+=1

        print("aroh= ",aroh)
        print("avroh= ",avroh)

    else:    
        while count<=7:
        
            for i in index:  #aroh
                if i>7 :
                    break
                sub+=swar[i]
            aroh.append(sub)

        
            rev=""
            for i in index:       #avroh
                rev+=swar[::-1][i]
            avroh.append(rev)

            if "सां" in sub:
                break

            sub=""
            for i in range(0,len(index)):
                index[i]+=1
            
            count+=1
    
    return aroh, avroh
@login_required
def alankarGenerator(request):
    aroh, avaroh = [], []
    if request.method == 'POST':
        swar_notation = request.POST.get('hidden_swar_notation')
        if swar_notation:
            aroh, avaroh = generate_sargam(swar_notation)
    else:
        aroh, avaroh = [], [] 
    return render(request, "pages/alankar-generator.html", {'aroh': aroh, 'avaroh': avaroh})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'You have been successfully registered.')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'You have been successfully logged in.')
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})
def logout(request):
    auth_logout(request)
    return redirect('login')
