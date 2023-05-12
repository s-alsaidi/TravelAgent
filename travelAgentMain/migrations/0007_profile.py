# Generated by Django 3.2.9 on 2021-11-26 03:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('travelAgentMain', '0006_alter_customer_examination_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tel', models.CharField(max_length=20, verbose_name='رقم الهاتف')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='travelAgentMain.branch', verbose_name='الفرع')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='اسم المستخدم')),
            ],
            options={
                'verbose_name': 'بروفايل المستخدم',
                'verbose_name_plural': 'بروفايل المستخدمين',
            },
        ),
    ]
