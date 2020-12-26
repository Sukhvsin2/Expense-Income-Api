from django.db import models
from authentication.models import User

class Income(models.Model):
    SOURCE_OPTIONS = [
        ('ONLINE_SERVICE', 'ONLINE_SERVICE'),
        ('RENT', 'RENT'),
        ('SALARY','SALARY'),
        ('TRAVEL', 'TRAVEL'),
        ('FOOD', 'FOOD'),
        ('OTHERS', 'OTHERS'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(choices=SOURCE_OPTIONS, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField()
    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering: ['-date']

    def __str__(self):
        return str(self.user) + 's income'
