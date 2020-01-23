from django.db import models

class Uptake(models.Model):
    title = models.CharField(
        default="Cogito har opptak!",
        blank=False,    
        max_length=255,
    )
    text = models.TextField()
    active_uptake = models.BooleanField(default=True)
    button_link = models.URLField()

    def __str__(self):
        return "Uptake Banner"
