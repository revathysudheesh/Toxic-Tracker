from django.shortcuts import render,redirect
import easyocr
from PIL import Image
import openai
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
import os
from django.conf import settings
from toxicscan.models import clientDB
from django.contrib import messages


# Create your views here.
def scanpage(request):
    if 'username' in request.session:
        em = request.session["username"]
        data = clientDB.objects.get(Email=em)
        return render(request,"scan1.html",{'data':data})
    else:
        return render(request,"scan1.html")

def inputdata(request):
    if request.method=="POST":
        product = request.POST.get("productname")
        if product!="":
            openai.api_key='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'
            prompt=f"what are the toxic ingredients of '{product}' and its side effects"
            response=openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=300,
                temperature=0.1,
                )
            side_effects=response.choices[0].text.strip()
        else:
            side_effects = "You have not entered a product. Enter a Product Name to check"
        em = request.session["username"]
        data = clientDB.objects.get(Email=em)
        return render(request,"scan1.html",{"side_effects":side_effects,'data':data})

def inputimage(request):
    if request.method=="POST":
        try:
            product = request.FILES["image"]

            filename = product.name

            # Define the media directory path
            media_path = os.path.join(settings.MEDIA_ROOT, filename)

            # Check if a file with the same name already exists, and if it does, modify the filename
            while os.path.exists(media_path):
                name, ext = os.path.splitext(filename)
                filename = f"{name}_1{ext}"
                media_path = os.path.join(settings.MEDIA_ROOT, filename)

            # Open the media directory in binary write mode and save the uploaded file
            with open(media_path, 'wb') as destination:
                for chunk in product.chunks():
                    destination.write(chunk)
            reader = easyocr.Reader(['en'], gpu=True)
        # image_path = r'C:\Users\shilp\OneDrive\Documents\Luminar\Internship\61qvMq1Pd0L.jpg'
            image = Image.open(media_path)
            results = reader.readtext(media_path)
            name=''
            for detection in results:
                text = detection[1]
                name=name+" "+text
            print(name)

            openai.api_key='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'
            prompt=f"what are the toxic ingredients in '{name}' and its side effects"
            response=openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=300,
                temperature=0.1,
                )
            side_effects=response.choices[0].text.strip()
        except MultiValueDictKeyError:
            side_effects = "No image added"
        em = request.session["username"]
        data = clientDB.objects.get(Email=em)
        return render(request,"scan1.html",{"side_effects":side_effects,'data':data,'name':name})


def loginpage(request):
    return render(request,"loginpage.html")

def saveuser(request):
    if request.method=="POST":
        email = request.POST.get("email")
        user = request.POST.get("username")
        passw = request.POST.get("password")
        confpass = request.POST.get("cpassword")
        if clientDB.objects.filter(Email = email).exists():
            messages.error(request,"Email ID already taken")
            return redirect(loginpage)
        else:
            if passw==confpass :
                obj = clientDB(Email=email,Username=user,Password=passw)
                obj.save()
                messages.success(request,"Sign Up Success")
                return redirect(loginpage)
            else:
                messages.error(request,"Passwords does not match")
                return redirect(loginpage)

def login(request):
    if request.method=="POST":
        email= request.POST.get("email")
        passw= request.POST.get("password")
        if clientDB.objects.filter(Email=email,Password=passw).exists():
            request.session["username"] = email
            request.session["password"] = passw
            messages.success(request,"Login Success")
            return redirect(scanpage)
        else:
            messages.error(request,"incorrect Email or Password")
            return redirect(loginpage)

def logout(request):
    del request.session["username"]
    del request.session["password"]
    messages.success(request,"Log out Success")
    return redirect(loginpage)