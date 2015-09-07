from django.contrib import admin

# Register your models here.
from main.models import *

admin.site.register(Author)
admin.site.register(Subject)
admin.site.register(Review)
admin.site.register(Question)
admin.site.register(Answer)