from django.db import models
from django.core.validators import RegexValidator


class WashType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    label = models.CharField(max_length=20)    # Example: "10:00 AM"
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.label


class DayStatus(models.Model):
    STATUS_CHOICES = [
        ("working", "Working Day"),
        ("leave", "Leave Day"),
    ]

    date = models.DateField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.date} → {self.status}"


class Booking(models.Model):
    STATUS_CHOICES = [
    ("pending", "Processing"),
    ("washing", "Washing"),
    ("completed", "Completed"),
    ("collected", "Car Collected"),
]


    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")


    # Customer details
    name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r"^[0-9+()-]+$")],
        blank=True,
        null=True
    )
    email = models.EmailField(blank=True, null=True)

    car_number = models.CharField(max_length=15)

    # Booking details
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT)
    wash_type = models.ForeignKey(WashType, on_delete=models.PROTECT)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car_number} ({self.date} {self.time_slot})"


class Notification(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.booking.car_number}"
