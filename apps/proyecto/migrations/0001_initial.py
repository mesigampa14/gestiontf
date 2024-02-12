# Generated by Django 5.0.1 on 2024-02-12 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sistema', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='archivos/')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_alta', models.DateTimeField(auto_created=True)),
                ('cargo', models.CharField(max_length=250)),
                ('fecha_baja', models.DateTimeField(auto_now=True)),
                ('docente', models.ManyToManyField(to='sistema.docente')),
            ],
        ),
        migrations.CreateModel(
            name='Estudiantes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_alta', models.DateTimeField(auto_created=True)),
                ('fecha_baja', models.DateTimeField(auto_now=True)),
                ('estudiante', models.ManyToManyField(to='sistema.estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=300)),
                ('descripcion', models.TextField()),
                ('presentacion', models.DateField(blank=True, null=True)),
                ('archivos', models.FileField(blank=True, null=True, upload_to='apps/proyecto/archivos/')),
                ('director', models.ManyToManyField(to='sistema.docente')),
                ('estudiantes', models.ManyToManyField(to='sistema.estudiante')),
            ],
        ),
    ]