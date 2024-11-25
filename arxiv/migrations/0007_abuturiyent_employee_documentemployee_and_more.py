# Generated by Django 4.2.16 on 2024-11-25 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arxiv', '0006_remove_document_location_student_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Abuturiyent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100, null=True)),
                ('employe_id', models.CharField(max_length=20)),
                ('graduation_year', models.IntegerField()),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='arxiv.location')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100, null=True)),
                ('employe_id', models.CharField(max_length=20)),
                ('graduation_year', models.IntegerField()),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='arxiv.location')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_type', models.CharField(choices=[('shaxsiy_varaqa', 'Shaxsiy varaqa'), ('turdavoy', 'Turdavoy'), ('t-2', 'T-2')], max_length=20)),
                ('is_available', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='arxiv.employee')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentAbuturiyent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_type', models.CharField(choices=[('diplom', 'Diplom'), ('atestatsiya', 'Atestatsiya')], max_length=20)),
                ('is_available', models.BooleanField(default=False)),
                ('abuturiyent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='arxiv.abuturiyent')),
            ],
        ),
    ]