from django.db import models

# Create your models here.
class Metrics(models.Model):

    date = models.DateField()
    channel = models.CharField(max_length=128)
    country = models.CharField(max_length=16)
    os = models.CharField(max_length=32)
    impressions = models.IntegerField()
    clicks = models.PositiveIntegerField()
    installs = models.PositiveIntegerField()
    spend = models.FloatField()
    revenue = models.FloatField()

    @property
    def cpi(self):
        if self.installs != 0:
            return (self.spend / self.installs)
        else:
            return None

    class Meta:
        ordering = ('id',)