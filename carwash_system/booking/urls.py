from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("book/", views.book, name="book"),
    path("available-slots/", views.get_available_slots, name="available_slots"),
    path("success/<int:booking_id>/", views.booking_success, name="booking_success"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("update-status/", views.update_booking_status, name="update_booking_status"),

]
