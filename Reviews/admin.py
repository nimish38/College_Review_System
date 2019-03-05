from django.contrib import admin

from .models import College, Review, PendingQuery, AnsweredQueries, StudentUser, IndustryUser


class ReviewAdmin(admin.ModelAdmin):
	model= Review
	list_display=('college','rating','description','user_name','pub_date')
	list_filter=['pub_date','user_name']
	search_fields=['college']


admin.site.register(College)
admin.site.register(Review, ReviewAdmin)
admin.site.register(PendingQuery)
admin.site.register(AnsweredQueries)
admin.site.register(StudentUser)
admin.site.register(IndustryUser)
