from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Swag(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='swags/', blank=True, null=True)
    company = models.CharField(max_length=100)
    conference = models.CharField(max_length=100)
    year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        help_text="Year of the conference",
        null=True,
        blank=True
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    comments = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swags')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} from {self.company} ({self.conference})"

    def average_rating(self):
        avg = self.ratings.aggregate(Avg('rating'))['rating__avg']
        return avg if avg else self.rating

    class Meta:
        ordering = ['-created_at']

class SwagComment(models.Model):
    swag = models.ForeignKey(Swag, on_delete=models.CASCADE, related_name='user_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.swag.name}"

class SwagRating(models.Model):
    swag = models.ForeignKey(Swag, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('swag', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Rating of {self.rating} by {self.user.username} for {self.swag.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
