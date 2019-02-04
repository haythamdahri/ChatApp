from datetime import timedelta, date

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import lower
from django.utils.timezone import now
from django_countries.fields import CountryField


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="MSG")
    country = CountryField()
    isOnline = models.BooleanField(default=False)
    lastOnline = models.DateTimeField(default=now())

    def __str__(self):
        return self.user.username

    def connect(self):
        print("connected from model")
        self.isOnline = True
        self.save()

    def disconnect(self):
        self.isOnline = False
        self.lastOnline = now()
        self.save()

    def full_name(self):
        full_name = self.user.first_name + ' ' + self.user.last_name
        if len(full_name) > 15:
            return lower(full_name)
        return full_name

    def last_online_status(self):
        connected_since = now() - self.lastOnline
        print(connected_since.days)
        print("Now: "+str(now().hour))
        print("Since: "+str(self.lastOnline.hour))
        print(f"connected since: {connected_since.seconds}")
        if connected_since.days <= 365 or connected_since <= 366:
            if connected_since.days <= 31 or connected_since.days <= 30 or connected_since.days <= 27 or connected_since <= 28:
                if connected_since.days < 1:
                    if connected_since.seconds <= 60*60:
                        return (abs(now().minute - self.lastOnline.minute)).__str__() + " m"
                    return (abs(now().hour - self.lastOnline.hour)).__str__() + " h"
                return (abs(now().day - self.lastOnline.day)).__str__() + " d"
            return (abs(now().month - self.lastOnline.month)).__str__() + " M"
        return (abs(now().year - self.lastOnline.year)).__str__() + " Y"




class RoomMM(models.Model):
    profiles = models.ManyToManyField(Profile)

    def __str__(self):
        cumm = "Profiles:"
        for profile in self.profiles.all():
            cumm += ' | ' + profile
        return cumm


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=10000)
    sent_date = models.DateTimeField(default=now)
    isRead = models.BooleanField(default=False)

    def __str__(self):
        return 'Sender: ' + self.sender.user.username + ' | Receiver: ' + self.receiver.user.username


class FriendRequest(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='RequestSender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='RequestReceiver')
    isAccepted = models.BooleanField(default=False)

    def __str__(self):
        return 'Sender: ' + self.sender.user.username + " | Receiver: " + self.receiver.user.username
