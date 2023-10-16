# Generated by Django 4.1.3 on 2023-09-13 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hmdb', '0009_empstatistic_dayofweek'),
    ]

    operations = [
        migrations.CreateModel(
            name='timeshift',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('emp_type', models.CharField(blank=True, max_length=20, null=True)),
                ('workdate', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'emp_timeshift',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblLeave',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('leavecode', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('leavename', models.CharField(blank=True, max_length=150, null=True)),
                ('pay', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'tbl_leave',
            },
        ),
        migrations.AddField(
            model_name='empstatistic',
            name='emp_type',
            field=models.ForeignKey(blank=True, db_column='emp_type', max_length=20, null=True, on_delete=django.db.models.deletion.CASCADE, to='hmdb.employeetype', to_field='cde'),
        ),
        migrations.CreateModel(
            name='TblOT',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cde', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('desc', models.CharField(blank=True, db_column='Desc', max_length=100, null=True)),
                ('num', models.CharField(blank=True, max_length=10, null=True)),
                ('defaultvalue', models.CharField(blank=True, max_length=1, null=True)),
                ('refcode', models.ForeignKey(blank=True, db_column='ref_code', null=True, on_delete=django.db.models.deletion.SET_NULL, to='hmdb.empctldb', to_field='cde')),
            ],
            options={
                'db_table': 'tbl_ot_type',
            },
        ),
    ]