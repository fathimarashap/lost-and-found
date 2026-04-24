
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserTable, ItemTable, Complaints, Found

admin.site.register(UserTable)
admin.site.register(ItemTable)
admin.site.register(Complaints)
admin.site.register(Found)