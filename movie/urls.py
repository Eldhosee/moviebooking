from django.urls import path

from movie import views

urlpatterns = [
    path('',views.homepage,name="homepage"),
    path('login',views.login,name="login"),
    path('register',views.register,name="register"),
    path('description/<int:id>', views.description, name="description" ),
    path('theater/<str:id>',views.theater,name="theater"),
    path('showtime',views.showtime,name="showtime"),
    path('seatselect',views.seatselect,name="seatselect"),
    path('seatselected',views.seatselected,name="seatselected"),
    path('history',views.history,name="history"),
     path('logout',views.logout,name="logout"),


]

