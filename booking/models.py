from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# Branch model (unchanged)
class Branch(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    phone_number = models.CharField(max_length=20)
    opening_hours = models.TextField()
    image = models.ImageField(upload_to='uploads/branches')
    description = models.TextField()

    def __str__(self):
        return self.name

# Service model (unchanged)
class Service(models.Model):
    name = models.CharField(max_length=255)
    branch = models.ManyToManyField(Branch)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    has_free_cancellation = models.BooleanField(default=False)
    included = models.TextField()

    def __str__(self):
        return self.name

# Client model (no User connection)
class Client(models.Model):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=False, null=False)
    additional_details = models.TextField(blank=True, null=True)
    receive_special_offers = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Booking model (unchanged, already uses Client)
class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    booking_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} - {self.service.name} at {self.branch.name} on {self.booking_datetime}"

    class Meta:
        unique_together = ('client', 'service', 'branch', 'booking_datetime')

    def clean(self):
        if self.branch not in self.service.branch.all():
            raise ValidationError("The selected branch does not offer this service.")
        

# admin model here
class Admin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username