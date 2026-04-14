from django.contrib import admin

# Register your models here.
#user_login, designation_type, staff_details, student_details, staff_student_map
#staff_messages, student_assignment, assignment_details_1, assignment_details_2, assignment_details_3


from .models import user_login, user_details
from.models import designation_type, staff_details, student_details, staff_student_map
from.models import staff_messages, student_assignment, assignment_details_1, assignment_details_2, assignment_details_3


admin.site.register(user_login)
admin.site.register(user_details)
admin.site.register(designation_type)
admin.site.register(staff_details)
admin.site.register(student_details)
admin.site.register(staff_student_map)
admin.site.register(staff_messages)
admin.site.register(student_assignment)
admin.site.register(assignment_details_1)
admin.site.register(assignment_details_2)
admin.site.register(assignment_details_3)
