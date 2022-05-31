import datetime

from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=False)

    def is_free(self):
        today = datetime.datetime.today()
        return not Reservation.objects.filter(date=today, room_id=self).exists()


class Reservation(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(null=True)

    class Meta:
        unique_together = ('room_id', 'date',)