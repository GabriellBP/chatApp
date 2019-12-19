from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.cache import cache
import datetime


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)


def set_customer():
    qtt_is_customer = len(UserProfile.objects.filter(is_customer=True))
    qtt_is_not_customer = len(UserProfile.objects.filter(is_customer=False))
    print(qtt_is_customer, qtt_is_not_customer)
    if qtt_is_customer <= qtt_is_not_customer:
        return True
    else:
        return False


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_customer = models.BooleanField(default=set_customer, null=False)

    def __str__(self):
        return self.user.username

    def last_seen(self):
        return cache.get('last_seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
                return False
            else:
                return True
        else:
            return False

    def verify_customer(self):
        return self.is_customer
