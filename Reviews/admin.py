from django.contrib import admin

from .models import College, Review, PendingQuery, AnsweredQueries, StudentUser, IndustryUser, Department, Category, Cutoff


class ReviewAdmin(admin.ModelAdmin):
	model= Review
	list_display=('college','dept','rating','description','user_name','pub_date')
	list_filter=['pub_date','user_name']
	search_fields=['college']


class StudAdmin(admin.ModelAdmin):
	model=StudentUser
	list_display = ('user','college','category')
	list_filter = ['college']


class DeptAdmin(admin.ModelAdmin):
	model=Department
	list_display = ('college', 'department')
	list_filter = ['college']


class CutAdmin(admin.ModelAdmin):
	model=Cutoff
	list_display = ('college', 'dept', 'caste', 'score', 'rank')
	list_filter = ['college']


admin.site.register(College)
admin.site.register(Review, ReviewAdmin)
admin.site.register(PendingQuery)
admin.site.register(AnsweredQueries)
admin.site.register(StudentUser, StudAdmin)
admin.site.register(IndustryUser)
admin.site.register(Department, DeptAdmin)
admin.site.register(Category)
admin.site.register(Cutoff, CutAdmin)

