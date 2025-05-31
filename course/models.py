from django.db import models
from django.contrib.auth.models import User

class CourseMaterial(models.Model):
    MATERIAL_TYPES = [
        ('lesson', 'Lesson Slides'),
        ('homework', 'Homework Assignment'),
        ('lecture', 'Lecture Recording'),
        ('other', 'Other Material'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPES, default='other')
    file = models.FileField(upload_to='course_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, help_text="Instructor who uploaded this material")

    def __str__(self):
        return f"{self.get_material_type_display()}: {self.title}"

    class Meta:
        ordering = ['-uploaded_at']

class UserPayment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='payment_profile') # Changed related_name for clarity
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True) # To store Stripe Customer ID
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True, null=True) # For specific payment attempts
    has_paid_for_course = models.BooleanField(default=False)
    payment_date = models.DateTimeField(blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True) # e.g., 200.00

    def __str__(self):
        return f"{self.user.username} - {'Paid' if self.has_paid_for_course else 'Not Paid'}"
