from django.contrib import admin

# Register your models here.
from agents.models import BadNum, Agent, AgentIProperty, AgentStProperty

admin.site.register(BadNum)
admin.site.register(Agent)
admin.site.register(AgentIProperty)
admin.site.register(AgentStProperty)
