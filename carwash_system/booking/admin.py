from django.contrib import admin
from .models import WashType, TimeSlot, DayStatus, Booking, Notification


@admin.register(WashType)
class WashTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("label", "order")
    ordering = ("order",)


@admin.register(DayStatus)
class DayStatusAdmin(admin.ModelAdmin):
    list_display = ("date", "status")
    list_filter = ("status",)

def mark_processing(modeladmin, request, queryset):
    queryset.update(status="pending")

def mark_washing(modeladmin, request, queryset):
    queryset.update(status="washing")


def mark_completed(modeladmin, request, queryset):
    for booking in queryset:
        booking.status = "completed"
        booking.save()

        Notification.objects.create(
            booking=booking,
            message="Your car wash is completed. Please pick up your vehicle."
        )

mark_completed.short_description = "Mark selected as Completed"

def mark_collected(modeladmin, request, queryset):
    for booking in queryset:
        booking.status = "collected"
        booking.save()
        Notification.objects.filter(booking=booking).delete()


def mark_collected(modeladmin, request, queryset):
    queryset.update(status="collected")
    
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "car_number", "date", "time_slot", "wash_type", "status")
    search_fields = ("name", "car_number", "phone")
    list_filter = ("status", "wash_type", "date")
    actions = [mark_processing, mark_washing, mark_completed, mark_collected]



@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("booking", "message", "seen", "created_at")
    list_filter = ("seen",)


