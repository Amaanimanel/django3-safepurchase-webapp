from django.db import models
from django.contrib.auth.models import User


class Purchase(models.Model):
    title = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datereceived = models.DateTimeField(null=True, blank=True)


    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title) + ": ₵" + str(self.price)
