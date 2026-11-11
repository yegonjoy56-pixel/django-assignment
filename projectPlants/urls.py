
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Green Haven Administration"
admin.site.site_title = "Green Haven Admin"
admin.site.index_title = "Plant Shop Management"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("accounts/", include("accounts.urls")),
    path("plants/", include("plants.urls")),
    path("shop/", include("shop.urls")),
]
