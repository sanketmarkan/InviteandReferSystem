# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 23:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('FOUNDERS', 'Founders'), ('ADMIN', 'Admin'), ('MENTORS', 'Mentors'), ('ADVISORS', 'Advisors'), ('EMPLOYEE', 'Employee'), ('NORMALUSER', 'Normal Users')], default='NORMALUSER', max_length=15)),
                ('refercode', models.CharField(max_length=10)),
                ('referby', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postoffered', models.CharField(choices=[('FOUNDERS', 'Founders'), ('ADMIN', 'Admin'), ('MENTORS', 'Mentors'), ('ADVISORS', 'Advisors'), ('EMPLOYEE', 'Employee'), ('NORMALUSER', 'Normal Users')], default='NORMALUSER', max_length=15)),
                ('accept', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='InviteNew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailid', models.EmailField(max_length=254)),
                ('postoffered', models.CharField(choices=[('FOUNDERS', 'Founders'), ('ADMIN', 'Admin'), ('MENTORS', 'Mentors'), ('ADVISORS', 'Advisors'), ('EMPLOYEE', 'Employee'), ('NORMALUSER', 'Normal Users')], default='NORMALUSER', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('typeof', models.CharField(choices=[('STARTUP', 'Startup'), ('INCUBATOR', 'Incubator'), ('ACCELERATOR', 'Accelerator')], default='STARTUP', max_length=10)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Refer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailid', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='invitenew',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inviterefer.Organisation'),
        ),
        migrations.AddField(
            model_name='invitenew',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offeredby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='invite',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inviterefer.Organisation'),
        ),
        migrations.AddField(
            model_name='invite',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='invite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='extendeduser',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inviterefer.Organisation'),
        ),
        migrations.AddField(
            model_name='extendeduser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]