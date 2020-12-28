from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Expenses Income API",
      default_version='v1',
      description="This is an Expense Income API app",
      terms_of_service="https://www.ourapp.com/policies/terms/",
      contact=openapi.Contact(email="djangotestingemail-7@gmail.com"),
      license=openapi.License(name="Sukh License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('expenses/', include('expenses.urls')),
    path('income/', include('income.urls')),
    path('userstats/', include('userstats.urls')),
]
