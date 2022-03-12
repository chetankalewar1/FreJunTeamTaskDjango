from django.contrib import admin
from .models import User, Team, TeamMember, AssignTask, Task


# class UserAdmin(admin.ModelAdmin):
#     search_fields = (
#         "username",
#         "email",
#         "phone",
#         "display_name",
#     )
#     list_display = (
#         "username",
#         "email",
#         "phone",
#         "display_name",
#         "is_phone_verified",
#         "is_email_verified",
#         "updated_at",
#     )


admin.site.register(User)
admin.site.register(Task)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(AssignTask)