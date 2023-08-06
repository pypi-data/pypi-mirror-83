from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from appchance.sections import views

urlpatterns = [
    path("admin/", admin.site.urls),
]

router = SimpleRouter()
router.register("sections", views.SectionViewSet, basename="sections")

urlpatterns += router.urls
