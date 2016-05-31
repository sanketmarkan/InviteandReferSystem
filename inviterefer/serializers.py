from rest_framework import serializers
from inviterefer.models import Organisation, ExtendedUser, Invite, InviteNew, Refer
from django.contrib.auth.models import User

class OrganisationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organisation
        fields = ('url', 'name', 'typeof')


class ExtendedUserSerializer(serializers.ModelSerializer):
    refercode = serializers.ReadOnlyField()
    referby = serializers.ReadOnlyField()
    class Meta:
        model = ExtendedUser
        fields = ('url', 'user', 'organisation', 'role', 'refercode', 'referby')

    def create(self,validated_data):
        user = validated_data['user']
        refercode = user.username
        refercode = str(refercode).upper()+str(user.id*user.id)
        euser = ExtendedUser(user=user, organisation=validated_data['organisation'],
                                role=validated_data['role'],refercode=refercode )
        for refers in Refer.objects.all():
            if euser.user.email == refers.emailid:
                euser.referby = refers.user.username
        euser.save()
        return euser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email','password')
        write_only_password_fields = ('password',)

    def create(self, validated_data):
        user = User(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        for invites in InviteNew.objects.all():
            if user.email == invites.emailid:
                newinvite = Invite()
                newinvite.owner = invites.owner
                newinvite.company = invites.company
                newinvite.accept = False
                newinvite.user = user
                newinvite.postoffered = invites.postoffered
                newinvite.save()
                invites.delete()
        return user


class InviteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    company = serializers.ReadOnlyField(source='company.name')
    accept = serializers.BooleanField()
    
    class Meta:
        model = Invite
        fields = ('url','user','owner','postoffered','company','accept')

    def create(self, validated_data):
        try:
            obj = ExtendedUser.objects.get(user=validated_data['owner'])
        except:
            raise serializers.ValidationError('Not Eligible to offers post')
        if obj.role not in ['FOUNDERS','ADMIN']:
            raise serializers.ValidationError('Not Eligible to offers post')
        invite = Invite(user=validated_data['user'], postoffered= validated_data['postoffered'], owner=validated_data['owner'],
                            company=validated_data['company'])
        invite.save()
        return invite

    def update(self, instance, validated_data):
        current_user = self.context['request'].user
        if current_user == instance.owner:
            instance.user = validated_data.get('user',instance.user)
            instance.postoffered = validated_data.get('postoffered',instance.postoffered)
        if current_user == instance.user:
            instance.accept = validated_data.get('accept',instance.accept)
        instance.save()
        if instance.accept == True:
            try:
                euser = ExtendedUser.objects.get(user=current_user)
                euser.organisation = instance.company
                euser.role = instance.postoffered
            except:
                euser = ExtendedUser()
                euser.user = current_user
                euser.organisation = instance.company
                euser.role = instance.postoffered
            euser.save()
            instance.delete()
            return
        return instance

class InviteNewSerializer(serializers.ModelSerializer):    
    owner = serializers.ReadOnlyField(source='owner.username')
    company = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = InviteNew
        fields = ('url','emailid','owner','postoffered','company')

    def create(self, validated_data):
        try:
            obj = ExtendedUser.objects.get(user=validated_data['owner'])
            obj.role in ['FOUNDERS','ADMIN']
        except:
            raise serializers.ValidationError('Not Eligible to offers post')
        invite = InviteNew(emailid=validated_data['emailid'], postoffered= validated_data['postoffered'], owner=validated_data['owner'],
                            company=validated_data['company'])
        invite.save()
        return invite


class ReferSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Refer
        fields = ('user', 'emailid')


class MyInviteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    company = serializers.ReadOnlyField(source='company.name')
    accept = serializers.BooleanField()

    class Meta:
        model = Invite
        fields = ('url','user','owner','postoffered','company','accept')

    def create(self, validated_data):
        try:
            obj = ExtendedUser.objects.get(user=validated_data['owner'])
            
        except:
            raise serializers.ValidationError('Not Eligible to offers post')
        if obj.role not in ['FOUNDERS','ADMIN']:
            raise serializers.ValidationError('Not Eligible to offers post')
        invite = Invite(user=validated_data['user'], postoffered= validated_data['postoffered'], owner=validated_data['owner'],
                            company=validated_data['company'])
        invite.save()
        return invite
