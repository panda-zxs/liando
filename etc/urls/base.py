from django.urls import include, path

urlpatterns = [
    path("users/", include("common.users.urls"),
         name="user"),
    path("accounts/", include("common.user_accounts.urls"),
         name="account"),
    path(r'groups/', include('common.user_groups.urls'),
         name='group'),
]
