from django.urls import include, path

urlpatterns = [
    path('autocomplete/', include('employee_info.urls.autocomplete'))
]
