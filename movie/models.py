from email.mime import image
from random import choices
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import ImageTk, Image
# Create your models here.

class User(AbstractUser):
    pass



class movie(models.Model):
    movie_name=models.CharField(max_length=40)
    image= models.ImageField(upload_to='images/' ,blank=True,null=True)
    description=models.TextField(null=True,default='')
    latest=models.BooleanField(default=0)
    trailer=models.URLField(null=True,blank=True)

    def __str__(self):
        return f"{self.movie_name}"

    def get_movies(id):
        return movie.objects.get(id=id)
    
    def get_random():
        return movie.objects.order_by("?").first()



class theaterlist(models.Model):
    showtime=(('9:30AM','9:30AM'),('12:00PM','12:00PM'),('2:30PM','2:30PM'),('4:30PM','4:30PM'),('6:30PM','6:30PM'),('8:30PM','8:30PM'))
    show_time1=models.CharField(choices=showtime,null=True,blank=True,max_length=10)
    show_time2=models.CharField(choices=showtime,null=True,blank=True,max_length=10)
    show_time3=models.CharField(choices=showtime,null=True,blank=True,max_length=10)
    show_time4=models.CharField(choices=showtime,null=True,blank=True,max_length=10)
    show_time5=models.CharField(choices=showtime,null=True,blank=True,max_length=10)
    show_time6=models.CharField(choices=showtime,null=True,blank=True,max_length=10)
    theater=models.CharField(max_length=20)


    
    def __str__(self):
        return f"{self.theater}"



class dates(models.Model):
    date=models.DateField(null=True,help_text = "show date1")
    movies=models.ForeignKey(movie,on_delete=models.CASCADE,null=True)
    theaterlist=models.ManyToManyField(theaterlist,blank=True)


    def __str__(self):
        return f"{self.date}"

    def get_dates(movies):
        date= dates.objects.filter(movies=movies)
        return date





class booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    movie=models.ForeignKey(movie,on_delete=models.CASCADE,null=True)
    time=models.CharField(max_length=40,null=True,blank=True)
    theater=models.CharField(max_length=100,null=True,blank=True)
    date=models.CharField(max_length=50,null=True,blank=True)
    all_seat=models.CharField(max_length=400,null=True,blank=True)
    price=models.IntegerField(null=True)

    def __str__(self):
        return  f"{self.user}"

    def get_movie(movie,theater,date,time):
        return booking.objects.filter(movie=movie,theater=theater,date=date,time=time)

