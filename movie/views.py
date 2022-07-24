from django.shortcuts import redirect, render
from .models import movie,dates,  theaterlist,User,booking
from django.contrib.auth import login as auth_login, authenticate, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import stripe

# This is your test secret API key.


# Create your views here.

def homepage(request):
    if request.method=='GET':
        latest_movies=movie.objects.filter(latest=1)
        movies=movie.objects.filter(latest=0)
        random=movie.get_random()
        

        return render(request,"movies/homepage.html",{
            "latest_movies":latest_movies,
            "movies":movies,
            "random":random
        })

def login(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            auth_login(request, user)
            a=user
            request.session['user']=a.id
            request.session['email']=a.email
            print(request.session['email'])
            return HttpResponseRedirect(reverse("homepage"))
            
        else:
            
            return render(request, "movies/login_2.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request,"movies/login_2.html")
    

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "movies/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "movies/register.html", {
                "message": "Username already taken."
            })

        return HttpResponseRedirect(reverse("login"))
    else:
        return render(request, "movies/register.html")





def description(request,id):
    # print(id)
    movie_details=movie.get_movies(id)
    
    return render(request,"movies/description.html",{
        "movie_details":movie_details
    })

def theater(request,id):
   
    
    movies=movie.get_movies(id)
    
    if movies:
        date=dates.get_dates(movies=movies)

   

    if request.session.get('user'):
    
        return render(request,"movies/theater.html",{
            "dates":date,
            "id":id
            
        })
    else:
        return redirect('login')

@login_required(login_url='login')
def showtime(request):
     if request.method=='POST':
        date=request.POST.get('date')
        id=request.POST.get('id')
        date_id=request.POST.get('date_id')
       
        movies=movie.get_movies(id)
    
        if movies:
            all_date=dates.get_dates(movies=movies)
       
        show_date=dates.objects.get(id=date_id)
        show=show_date.theaterlist.all()
        theater=[]
        
        for i in show:
            a=theaterlist.objects.get(theater=i)
            theater.append(a)
           
        return render(request,"movies/theater.html",{
            "dates":all_date,
            "show_time":theater,
            "id":id,
            "show_date":show_date
        })
     else:
        return redirect('homepage')

@login_required(login_url='login')
def seatselect(request):
    
    if request.method=='POST':
        date=request.POST.get('dates')
        theater=request.POST.get('theater')
        time=request.POST.get('time')
        id=request.POST.get('id')
        movies=movie.get_movies(id)
        name=movies.movie_name
        booked_seats=[]
        already_booked=booking.get_movie(id,theater,date,time)
      
        try:
            already_booked=booking.get_movie(id,theater,date,time)
            for i in already_booked:
                booked_seats.append(i.all_seat)
            print(booked_seats)
            

        except:
            print(True)
           
        
            
        seats=[i.split(',') for i in booked_seats]
        
        print(seats)
        a=[]
        for i in seats:
            a+=i

        print(a)


        print(id,name)
        return render(request,"movies/seatselect.html",{
            "date":date,
            "theater":theater,
            "time":time,
            "movie_name":name,
            "booked_seats":a
        })

    else:
        return redirect('homepage')
@login_required(login_url='login')
def seatselected(request):
    if request.method=='POST':
        user=request.user
        try:
            
            user=User.objects.get(username=user)
        except:
            message="Invalid user"
            return render(request,"movies/login_2.html",{
                "error":message
            })
        time=request.POST.get('time')
        theater=request.POST.get('theater')
        date=request.POST.get('date')
        movie_name=request.POST.get('movie_name')
        movie_id=movie.objects.get(movie_name=movie_name)
        seatselected=request.POST.get('seatselected')
        
        seats=seatselected.split(',')
        
        count=0
        for i in seats:
            count+=1
        price=count*100
        if time is None:
            return redirect('homepage')
        if seatselected:
           
            request.session['movie_name']=movie_name
            request.session['theater']=theater
            request.session['date']=date
            request.session['time']=time
            request.session['seatselected']=seatselected
            request.session['price']=price
            

            movie_booking=booking.objects.create(user=user,movie=movie_id,all_seat=seatselected,price=price,time=time,date=date,theater=theater)
            movie_booking.save()
            return render(request,"movies/ticket.html",{
                "movie_name":movie_name,
                "theater":theater,
                "date":date,
                "time":time,
                "seatselected":seatselected,
                "price":price
            })
        return redirect('homepage')
    return redirect('homepage')

@login_required(login_url='login')
def history(request):
    user=request.user
    try: 
        User.objects.get(username=user)
        history=list(booking.objects.filter(user=user).reverse())
        
        return render(request,"movies/history.html",{
            "history":history
        })
    except:
        return render(request,"movies/login_2.html")

def logout(request):
    request.session.clear()
    
    return redirect('login')







