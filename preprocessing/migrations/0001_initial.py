# Generated by Django 3.0.8 on 2020-10-15 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('datasets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProsesKDD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car', models.DecimalField(decimal_places=4, max_digits=19)),
                ('npl', models.DecimalField(decimal_places=4, max_digits=19)),
                ('roa', models.DecimalField(decimal_places=4, max_digits=19)),
                ('roe', models.DecimalField(decimal_places=4, max_digits=19)),
                ('nim', models.DecimalField(decimal_places=4, max_digits=19)),
                ('ldr', models.DecimalField(decimal_places=4, max_digits=19)),
                ('status', models.CharField(choices=[('NO', 'No Process'), ('PR', 'Processed'), ('TR', 'Transformed')], default='NO', max_length=50)),
                ('rasio_k', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.RasioKeuangan')),
            ],
            options={
                'db_table': 'proses_kdd',
            },
        ),
    ]