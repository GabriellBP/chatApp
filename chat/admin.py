from django.contrib import admin
from chat.models import Message, UserProfile

admin.site.register(Message)
admin.site.register(UserProfile)
