from django.conf.urls import url, include
from inviterefer import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'organistation', views.OrganisationViewSet)
router.register(r'extendedusers', views.ExtendedUserViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'invite', views.InviteViewSet)
router.register(r'myinvite', views.MyInviteViewSet, base_name='myinvite')
router.register(r'invitenew', views.InviteNewViewSet)
router.register(r'refer', views.ReferViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]