from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Choices
SELECT_CATEGORY_CHOICES = [
    ("Food", "Food"),
    ("Travel", "Travel"),
    ("Shopping", "Shopping"),
    ("Necessities", "Necessities"),
    ("Entertainment", "Entertainment"),
    ("Other", "Other"),
]

ADD_EXPENSE_CHOICES = [
    ("Expense", "Expense"),
    ("Income", "Income"),
]

PROFESSION_CHOICES = [
    ("Employee", "Employee"),
    ("Business", "Business"),
    ("Student", "Student"),
    ("Other", "Other"),
]


class Addmoney_info(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    add_money = models.CharField(max_length=10, choices=ADD_EXPENSE_CHOICES)
    quantity = models.BigIntegerField()
    Date = models.DateField(default=now)
    Category = models.CharField(max_length=20, choices=SELECT_CATEGORY_CHOICES, default='Food')

    class Meta:
        db_table = 'addmoney'
        ordering = ['-Date']

    def __str__(self):
        return f"{self.user.username} - {self.add_money} - {self.Category} - {self.quantity} on {self.Date}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=10, choices=PROFESSION_CHOICES)
    Savings = models.IntegerField(null=True, blank=True, default=0)
    income = models.BigIntegerField(null=True, blank=True, default=0)
    image = models.ImageField(upload_to='profile_image', blank=True, null=True)

    def __str__(self):
        return self.user.username


# Signal to auto-create UserProfile on User creation
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

   

