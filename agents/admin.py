from django.contrib import admin

# Register your models here.
from agents.models import BadNum, Agent

admin.site.register(BadNum)
admin.site.register(Agent)