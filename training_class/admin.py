from django.contrib import admin
from .models import Client, Group, Exercise, Solution


class ClientAdmin(admin.ModelAdmin):
    fields = []


admin.site.register(Client, ClientAdmin)
admin.site.register(Group, ClientAdmin)
admin.site.register(Exercise, ClientAdmin)
admin.site.register(Solution, ClientAdmin)


