from inviterefer.models import Organisation, ExtendedUser, Invite, InviteNew, Refer
from inviterefer.serializers import OrganisationSerializer
from inviterefer.serializers import InviteSerializer
from inviterefer.serializers import MyInviteSerializer
from inviterefer.serializers import InviteNewSerializer
from rest_framework import generics
from inviterefer.serializers import UserSerializer,ReferSerializer
from inviterefer.serializers import ExtendedUserSerializer
from inviterefer.permissions import IsOwnerOrReadOnly, IsUserOrReadOnly
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from django.core.mail import send_mail
from django.http import Http404
from django.contrib.sessions.models import Session


@api_view(['GET'])
def api_root(request, format=None):
	return Response()


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (IsUserOrReadOnly,)

"""
def get_user(request):
	return request.user
"""

class ExtendedUserViewSet(viewsets.ModelViewSet):
	queryset = ExtendedUser.objects.all()
	serializer_class = ExtendedUserSerializer

"""class InviteViewSet(viewsets.ReadOnlyModelViewSet):
	user = get_user()
	queryset = Invite.objects.all(user=request.user)
	serializer_class = InviteSerializer
"""

@api_view(['GET'])
def current_user(request):
	user = request.user

class MyInviteViewSet(viewsets.ModelViewSet):
	def get_queryset(self):
		return Invite.objects.filter(user=self.request.user)
	serializer_class = MyInviteSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
							IsOwnerOrReadOnly)

	def perform_create(self, serializer):
		try:
			invitedby = ExtendedUser.objects.get(user=self.request.user)
			serializer.save(owner=self.request.user,company=invitedby.organisation)
		except:
			serializer.save()

	

class InviteViewSet(viewsets.ModelViewSet):
	
	queryset = Invite.objects.all()
	serializer_class = InviteSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
							IsOwnerOrReadOnly)

	def perform_create(self, serializer):
		try:
			invitedby = ExtendedUser.objects.get(user=self.request.user)
			serializer.save(owner=self.request.user,company=invitedby.organisation)
		except:
			serializer.save()


class InviteNewViewSet(viewsets.ModelViewSet):
	queryset = InviteNew.objects.all()
	serializer_class = InviteNewSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
							IsOwnerOrReadOnly)

	def perform_create(self, serializer):
		try:
			invitedby = ExtendedUser.objects.get(user=self.request.user)
			serializer.save(owner=self.request.user,company=invitedby.organisation)
		except:
			serializer.save()
			return
		msg = "Hi!\nYou have a new invite to become %s at %s from %s\n\nRegister for Startupbyte at localhost:8000/users with your emailId" % (
																		serializer.data['postoffered'], 
																			invitedby.organisation.name, 
																				invitedby.user.username)
		send_mail("New Invite",msg,'sanketmarkan',[serializer.data['emailid'],])

class ReferViewSet(viewsets.ModelViewSet):
	queryset = Refer.objects.all()
	serializer_class = ReferSerializer
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
		try:
			referby = ExtendedUser.objects.get(user=self.request.user)
			msg = "Hi!\nYou have been reffered to join Startupbyte by %s, %s at %s.\n\n" %(referby.user.username,
																						referby.role,
																						referby.organisation.name)
		except:
			msg = "Hi!\nYou have been reffered to join Startupbyte by %s.\n\n" %(self.request.user.username)
		msg = msg + "Join By registering at localhost:8000/users with your emailid."
		send_mail("New Refer",msg,'sanketmarkan',[serializer.data['emailid'],])

class OrganisationViewSet(viewsets.ModelViewSet):
	queryset = Organisation.objects.all()
	serializer_class = OrganisationSerializer

"""
class MyInviteViewSet(viewsets.ModelViewSet):
	queryset = Invite.objects.all()
	serializer_class = InviteSerializer
"""