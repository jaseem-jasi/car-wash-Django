from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from datetime import date, timedelta

from .models import Booking, WashType, TimeSlot, DayStatus, Notification
from .forms import BookingForm
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def admin_dashboard(request):
    day_offset = request.GET.get("day", "0")

    try:
        day_offset = int(day_offset)
    except ValueError:
        day_offset = 0

    today = date.today()
    selected_date = today + timedelta(days=day_offset)

    bookings = Booking.objects.filter(date=selected_date).order_by("time_slot")

    context = {
        "selected_date": selected_date,
        "day_offset": day_offset,
        "is_today": selected_date == today,   # ✅ GUARANTEED BOOLEAN

        "total_count": bookings.count(),
        "processing_count": bookings.filter(status="pending").count(),
        "washing_count": bookings.filter(status="washing").count(),
        "completed_count": bookings.filter(status="completed").count(),
        "collected_count": bookings.filter(status="collected").count(),

        "bookings": bookings,
    }

    return render(request, "booking/admin_dashboard.html", context)

@staff_member_required
@require_POST
def update_booking_status(request):
    booking_id = request.POST.get("booking_id")
    new_status = request.POST.get("status")

    booking = get_object_or_404(Booking, id=booking_id)

    allowed_statuses = ["pending", "washing", "completed", "collected"]
    if new_status in allowed_statuses:
        booking.status = new_status
        booking.save()

    return redirect("admin_dashboard")


def home(request):
    car_number = request.GET.get("car_number")
    message = None

    if car_number:
        # get latest booking
        booking = Booking.objects.filter(
            car_number__iexact=car_number
        ).order_by("-id").first()

        if booking:
            if booking.status == "pending":
                message = "Your car wash is in processing."
            elif booking.status == "washing":
                message = "Your vehicle is currently being washed."
            elif booking.status == "completed":
                message = "Your wash is completed. Please pick up your vehicle."
            elif booking.status == "collected":
                message = None  # show no status
        else:
            message = None

    return render(request, "booking/home.html", {
        "car_number": car_number,
        "message": message,
    })




def get_available_slots(request):
    selected_date = request.GET.get("date")

    if not selected_date:
        return JsonResponse({"slots": []})

    # Leave day check
    if DayStatus.objects.filter(date=selected_date, status="leave").exists():
        return JsonResponse({"slots": [], "leave": True})

    all_slots = TimeSlot.objects.all()
    booked = Booking.objects.filter(date=selected_date).values_list("time_slot_id", flat=True)

    available = all_slots.exclude(id__in=booked)

    return JsonResponse({
        "leave": False,
        "slots": list(available.values("id", "label"))
    })


def book(request):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    allowed_dates = [today, tomorrow]

    # Prepare date + availability message
    day_messages = []
    for d in allowed_dates:
        msg = "Available"
        if DayStatus.objects.filter(date=d, status="leave").exists():
            msg = "Leave Day — No booking"
        day_messages.append({"date": d, "msg": msg})

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            car_number = form.cleaned_data["car_number"]
            booking_date = form.cleaned_data["date"]

            # 🔒 DUPLICATE ACTIVE BOOKING CHECK
            active_booking_exists = Booking.objects.filter(
                car_number__iexact=car_number,
                status__in=["pending", "washing", "completed"],
                date__in=[today, tomorrow],
            ).exists()

            if active_booking_exists:
                form.add_error(
                    "car_number",
                    "This vehicle already has an active booking."
                )
            else:
                booking = form.save()

                # Optional email
                if booking.email:
                    send_mail(
                        "Car Wash Booking Confirmed",
                        f"Your booking is confirmed for {booking.date} at {booking.time_slot.label}.",
                        settings.DEFAULT_FROM_EMAIL,
                        [booking.email],
                    )

                return redirect("booking_success", booking.id)

    else:
        form = BookingForm()

    return render(request, "booking/book.html", {
        "form": form,
        "day_messages": day_messages,
    })



def booking_success(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    return render(request, "booking/booking_success.html", {"booking": booking})
