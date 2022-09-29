from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout as django_logout
import uuid
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Url
from django.contrib.auth.decorators import login_required

# Create your views here.
class Home(View):

    def get(self,request):
        return render(request,'home.html')

    def post(self,request):
        if not request.user.is_authenticated:
            messages.error(request,"You must be logged in to shorten a Url!")
            return redirect('login')
        url = request.POST['link']
        uid = str(uuid.uuid4())[:5]
        user = User.objects.filter(username=request.user).first()
        try:
            url_exist = Url.objects.get(link=url,creator=user)
            uid = url_exist.uuid
            print(url_exist)
        except:
            new_url = Url(link=url,uuid=uid,creator=user)
            new_url.save()
        data={
            'link':url,
            'url':'Your Link: &nbsp;&nbsp; qurl.pythonanywhere.com/'+uid,
        }
        return render(request,"home.html",data)

def go(request, pk):
    url_details = Url.objects.get(uuid=pk)
    return redirect('http://'+ url_details.link)

@login_required(login_url='/login')
def myAccount(request):
    user = User.objects.get(username= request.user)
    links = Url.objects.filter(creator = user).all()
    context={
        'links':links
    }
    return render(request,'myaccount.html',context)

@login_required(login_url='/login')
def deleteUrl(request,id):
    url_item = Url.objects.get(id=id)
    url_item.delete()
    messages.warning(request,"Url deleted!")
    return redirect('/account')


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        postData = request.POST
        email = postData.get('email')
        password1 = postData.get('password1')
        password2 = postData.get('password2')
        username = postData.get('username')
        agree = postData.get('agree')

        data={
            'username':username,
            'password':password1,
            'email':email,
        }

        try:
            User.objects.get(email=email)
            messages.error(request,"Email already exists!")
            return redirect('register')
        except:
            try:
                if len(username) < 4:
                    messages.error(request,"Username must be at least 4 characters")
                    return render(request,'register.html',data)

                User.objects.get(username=username)
                messages.error(request,"Username alredy taken!")
                return render(request,'register.html',data)
            except:
                if password1 == password2:
                    if agree is None:
                        messages.warning(request,"You must agree to terms and conditions of Q_Url 2022")
                        return render(request,'register.html',data)
                        
                    new_user = User.objects.create_user(username,email,password1)
                    new_user.save()
                    messages.success(request,"User account created successfully now login")
                    return redirect('login')

                else:
                    messages.error(request,"Passwords doesn't match! ")
                    return redirect('register')
    return render(request,'register.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST['username']
        password= request.POST['password']
        data={
            'username':username,
            'password':password,
        }
        try:
            User.objects.get(username=username)
        except:
            messages.error(request,"Username not found!")
            return render(request,'login.html',data)
        try:    
            user = authenticate(request,username=username,password=password)
            login(request,user)
            return redirect('/')
        except:
            messages.error(request, "Invalid Password!")
            return render(request,'login.html',data)

    return render(request,'login.html')
    
def logout(request):
    try:
        django_logout(request)
        return redirect('login')
    except Exception as e:
        messages.error(request,e)

