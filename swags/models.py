from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Swag(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='swags/', blank=True, null=True)
    company = models.CharField(max_length=100)
    conference = models.CharField(max_length=100)
    rating = models.DecimalField(
        max_digits=2, 
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        help_text="Rating from 1 to 5 stars (half-star increments allowed)"
    )
    comments = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swags')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} from {self.company} ({self.conference})"

    class Meta:
        ordering = ['-created_at']
