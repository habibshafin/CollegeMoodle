# Generated by Django 3.0.6 on 2020-07-09 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clgStudent', '0002_studentsubjects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsubjects',
            name='comSub_11',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='com11', to='clgStudent.Subjects'),
        ),
        migrations.AlterField(
            model_name='studentsubjects',
            name='comSub_12',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='com12', to='clgStudent.Subjects'),
        ),
        migrations.AlterField(
            model_name='studentsubjects',
            name='comSub_21',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='com21', to='clgStudent.Subjects'),
        ),
        migrations.AlterField(
            model_name='studentsubjects',
            name='comSub_22',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='com22', to='clgStudent.Subjects'),
        ),
        migrations.AlterField(
            model_name='studentsubjects',
            name='comSub_31',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='com31', to='clgStudent.Subjects'),
        ),
        migrations.AlterField(
            model_name='studentsubjects',
            name='comSub_32',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='com32', to='clgStudent.Subjects'),
        ),
        migrations.AlterField(
            model_name='studentsubjects',
            name='opSub_11',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='op12', to='clgStudent.Subjects'),
        ),
    ]
