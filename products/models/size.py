from django.db import models

class Size(models.Model):
    name = models.CharField(max_length=20, unique=True)  # e.g. S, M, L, XL

    def __str__(self):
        return self.name


