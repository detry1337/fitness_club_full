from django.db import models
from django.contrib.auth.models import User

class Membership(models.Model):
    MEMBERSHIP_TYPES = [
        ('BASIC', 'Базовый'),
        ('PREMIUM', 'Премиум'),
        ('VIP', 'VIP'),
    ]
    
    name = models.CharField(max_length=100, choices=MEMBERSHIP_TYPES, default='BASIC')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.get_name_display()

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True, blank=True)
    join_date = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='members/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class Service(models.Model):
    SERVICE_TYPES = [
        ('GYM', 'Тренажерный зал'),
        ('YOGA', 'Йога'),
        ('POOL', 'Бассейн'),
        ('CROSSFIT', 'Кроссфит'),
    ]
    name = models.CharField(max_length=100, choices=SERVICE_TYPES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.get_name_display()

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name} на {self.date} {self.time}"