from django.contrib import admin
from app.models import User,Csv

# class user(admin.ModelAdmin):
#     # Define which fields to display in the admin list view
#     list_display = ('field1', 'field2', 'field3')  # Add fields from YourModel here


# Register the model with the custom admin class
admin.site.register(User)
admin.site.register(Csv)
