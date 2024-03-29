# Generated by Django 3.0.8 on 2021-01-02 08:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Academic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Qualification', models.CharField(max_length=70)),
                ('Percentage', models.CharField(max_length=10)),
                ('Course', models.CharField(max_length=10)),
                ('Program', models.CharField(max_length=10)),
                ('Created', models.DateField(auto_now=True)),
                ('Qual_Doc', models.FileField(upload_to='Qualification Document')),
                ('Std_Image', models.ImageField(upload_to='Candidates/')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('Stud_Id', models.TextField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=70, null=True)),
                ('DOB', models.DateField(null=True)),
                ('Gender', models.CharField(max_length=10)),
                ('Country', models.CharField(max_length=20, null=True)),
                ('Addr_1', models.CharField(max_length=70, null=True)),
                ('Addr_2', models.CharField(max_length=70, null=True)),
                ('Addr_3', models.CharField(max_length=70, null=True)),
                ('Pincode', models.CharField(max_length=10, null=True)),
                ('Mobile', models.IntegerField()),
                ('image', models.ImageField(default='default.png', null=True, upload_to='Profile Pics')),
                ('Email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.AddField(
            model_name='academic',
            name='Stud_Id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.Student'),
        ),
    ]
