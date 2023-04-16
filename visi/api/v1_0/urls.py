from django.conf import settings
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import obtain_auth_token

from visi.api.v1_0.views.teacher_views import TeacherListCreateView, TeacherRetrieveUpdateDestroyView
from visi.api.v1_0.views.subject_views import SubjectListCreateView, SubjectRetrieveUpdateDestroyView


schema_view_v1_0 = get_schema_view(
    openapi.Info(
        title="VISI API",
        default_version='v1.0',
        description="API for Visi",
        terms_of_service="http://127.0.0.1:8000/privacy-policy/",
        contact=openapi.Contact(email="admin@example.com"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

app_name = "v1.0"

urlpatterns = [
    path("", view=schema_view_v1_0.without_ui(cache_timeout=12 * 60 * 60), name='schema-json'),
    path("swagger(?P<format>\.json|\.yaml)", view=schema_view_v1_0.without_ui(cache_timeout=None), name='schema-swagger'),

    path("login/", view=obtain_auth_token, name="login"),
    path("teachers/", view=TeacherListCreateView.as_view(), name="teacher_list"),
    path("teachers/<int:id>", view=TeacherRetrieveUpdateDestroyView.as_view(), name="teacher_retrieve"),

    path("subjects/", view=SubjectListCreateView.as_view(), name="subject_list"),
    path("subjects/<int:id>", view=SubjectRetrieveUpdateDestroyView.as_view(), name="subject_retrieve"),

    path("docs/", view=schema_view_v1_0.with_ui('redoc', cache_timeout=None), name='schema-redoc-ui')
]

if settings.DEBUG:
    urlpatterns += [
        path("swagger-ui/", view=schema_view_v1_0.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    ]