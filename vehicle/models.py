from django.db import models
from core.models import User

# -----------------------------
# VEHICLE CORE MODELS
# -----------------------------
class Vehicle(models.Model):

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Sold', 'Sold'),
        ('Pending', 'Pending'),
    ]

    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('CNG', 'CNG'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
    ]

    TRANSMISSION_CHOICES = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
    ]

    BODY_TYPE_CHOICES = [
        ('Hatchback', 'Hatchback'),
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('MUV', 'MUV'),
        ('Coupe', 'Coupe'),
        ('Convertible', 'Convertible'),
        ('Pickup', 'Pickup'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')

    # Basic details
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=80)
    variant = models.CharField(max_length=80, blank=True, null=True)
    year = models.PositiveSmallIntegerField()

    featured = models.BooleanField(default=False) 

    # Pricing
    price = models.DecimalField(max_digits=12, decimal_places=2)

    # Specs
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    km_driven = models.PositiveIntegerField(default=0)

    owner_type = models.CharField(max_length=50, default="1st Owner")
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)

    # Engine & performance
    engine_cc = models.PositiveIntegerField(blank=True, null=True)
    mileage = models.FloatField(blank=True, null=True)
    max_power = models.CharField(max_length=50, blank=True, null=True)
    torque = models.CharField(max_length=50, blank=True, null=True)
    seating_capacity = models.PositiveSmallIntegerField(default=5)

    # Features (CarWale style)
    sunroof = models.BooleanField(default=False)
    touchscreen = models.BooleanField(default=False)
    rear_camera = models.BooleanField(default=False)

    # Location
    location = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Description
    description = models.TextField(blank=True)

    # Status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    # Timestamps
    listed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-listed_at']

    def __str__(self):
        return f"{self.brand} {self.model} {self.variant or ''} ({self.year})"


# MULTIPLE IMAGES
class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='vehicle_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


# -----------------------------
# OFFERS & TRANSACTIONS
# -----------------------------
class Offer(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='offers')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_offers')
    offered_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    status = models.CharField(max_length=20, choices=[('Completed','Completed'),('Cancelled','Cancelled')])
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_transactions')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_transactions')
    final_price = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# -----------------------------
# TEST DRIVE & INSPECTION
# -----------------------------
class TestDrive(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='testdrives')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testdrive_requests')
    scheduled_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)


class VehicleInspection(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Failed', 'Failed'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    report_details = models.TextField()
    inspection_date = models.DateField()
    inspection_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


# -----------------------------
# MESSAGING
# -----------------------------
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    message_text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


# -----------------------------
# FAVOURITES
# -----------------------------
class Favourite(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('buyer', 'vehicle')


# -----------------------------
# PAYMENTS
# -----------------------------
class Payment(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=100, blank=True)
    method = models.CharField(max_length=20, choices=[('Card','Card'),('UPI','UPI'),('Cash','Cash')])
    status = models.CharField(max_length=20, choices=[('Pending','Pending'),('Success','Success'),('Failed','Failed')])
    updated_at = models.DateTimeField(auto_now=True)
