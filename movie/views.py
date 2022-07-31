from django.shortcuts import redirect, render
from .models import movie,dates,  theaterlist,User,booking
from django.contrib.auth import login as auth_login, authenticate, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings 
from django.http.response import JsonResponse 
from django.views.decorators.csrf import csrf_exempt 

# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY

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
           
            

        except:
            print(True)
           
        
        print(booked_seats)   
        seats=[i.split(',') for i in booked_seats]
        
        
        a=[]
        for i in seats:
            a+=i

        

        request.session["booked_seats"]=a
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
        # movie_id=movie.objects.get(movie_name=movie_name)
        seatselected=request.POST.get('seatselected')
        
        seats=seatselected.split(',')
        request.session['date']=date
        request.session['movie_name']=movie_name
        request.session['theater']=theater
        request.session['date']=date
        request.session['time']=time
        request.session['seatselected']=seatselected
        
        selected_seats=seatselected.split(',')
        request.session['selected_seats']=selected_seats
        
        


        count=0
        for i in seats:
            count+=1
        price=count*100
        if time is None:
            return redirect('homepage')
        if seatselected:
            
           
            request.session['price']=price
            

            
            return render(request,"movies/ticket.html",{
                "movie_name":movie_name,
                "theater":theater,
                "date":date,
                "time":time,
                "seatselected":seatselected,
                "price":price,
                "message":"please pay to confirm your booking "
            })
        else:
                    movie_name=request.session.get('movie_name')
                    theater=request.session.get('theater')
                    time=request.session.get('time')
                    seatselected=request.session.get('seatselected')
                    date=request.session.get('date')
                    a=request.session.get('booked_seats')
                    return render(request,"movies/seatselect.html",{
                        "date":date,
                        "theater":theater,
                        "time":time,
                        "movie_name":movie_name,
                        "booked_seats":seatselected,
                        "booked_seats":a,
                        "error":"True",
        })

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


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

    
@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        price=request.session.get('price')
        price*=100
        movie_name=request.session.get('movie_name')
        theater=request.session.get('theater')
        print(price,movie_name,theater)
        domain_url = 'https://moviebooking123.herokuapp.com/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
           


            checkout_session = stripe.checkout.Session.create(
                    line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                        'name': movie_name,
                        
                        },
                        'unit_amount': price,
                    },
                    'quantity': 1,
                    }],
                    mode='payment',
                    success_url=domain_url+'success',
                    cancel_url=domain_url+'cancel',
                )
           
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def success(request):
    if request.method=='GET':
            
                    user=request.user
                    try:
                    
                        user=User.objects.get(username=user)
                    except:
                        message="Invalid user"
                        return render(request,"movies/login_2.html",{
                        "error":message
                    })
                    
          
               

           
                    movie_name=request.session.get('movie_name')
                    theater=request.session.get('theater')
                    request.session.get('date')
                    time=request.session.get('time')
                    seatselected=request.session.get('seatselected')
                    booked_seats=request.session.get('booked_seats')
                    selected_seats_array=request.session.get('selected_seats')
                    price=request.session.get('price')
                    date=request.session.get('date')
                    movie_id=movie.objects.get(movie_name=movie_name)
                    
                    try:
                        booked_seats=[]
                        already_booked=booking.get_movie(movie_id,theater,date,time)
                        for i in already_booked:
                            booked_seats.append(i.all_seat)
                        
                        seats=[i.split(',') for i in booked_seats]
                        a=[]
                        for i in seats:
                            a+=i
                        print(a)
                        

                    except:
                        pass

                    flag=0
                    try:
                        for i in a:
                            for j in selected_seats_array:
                                print(i,j)
                                if i==j:
                                    flag=1
                    except:
                        pass

                    if flag==0:
                        movie_booking=booking.objects.create(user=user,movie=movie_id,all_seat=seatselected,price=price,time=time,date=date,theater=theater)
                        movie_booking.save()
                        return render(request,"movies/ticket.html",{
                            "movie_name":movie_name,
                            "theater":theater,
                            "date":date,
                            "time":time,
                            "seatselected":seatselected,
                            "price":price,
                            "history":"show history"
                            
                        })
                    else:
                        return render(request,"movies/ticket.html",{
                            "movie_name":movie_name,
                            "theater":theater,
                            "date":date,
                            "time":time,
                            "seatselected":seatselected,
                            "price":price,
                            "history":"show history"
                            
                        })







                    
def cancel(request):
    if request.method=='GET':
            
            user=request.user
            try:
            
                user=User.objects.get(username=user)
            except:
                message="Invalid user"
                return render(request,"movies/login_2.html",{
                "error":message
            })

           
            movie_name=request.session.get('movie_name')
            theater=request.session.get('theater')
            request.session.get('date')
            time=request.session.get('time')
            seatselected=request.session.get('seatselected')
            price=request.session.get('price')
            date=request.session.get('date')
        
            return render(request,"movies/ticket.html",{
                "movie_name":movie_name,
                "theater":theater,
                "date":date,
                "time":time,
                "seatselected":seatselected,
                "price":price,
                "message":"payment failed please try again"
                
            })

