from django.contrib import admin

# Register your models here.
from .models import College,Review
class ReviewAdmin(admin.ModelAdmin):
	model= Review
	list_display=('college','rating','description','user_name','pub_date')
	list_filter=['pub_date','user_name']
	search_fields=['college']
	
admin.site.register(College)
admin.site.register(Review,ReviewAdmin)