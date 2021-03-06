# Generated by Django 3.0.4 on 2020-06-27 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clgExam', '0002_auto_20200628_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ct',
            name='TotalMarks',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='ct',
            name='ctPercentage',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ctmarks',
            name='AchievedMarks',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='customexam',
            name='CQ',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='customexam',
            name='CustomExamPercentage',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='customexam',
            name='MCQ',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='customexam',
            name='PassMarksCQ',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='customexam',
            name='PassMarksMCQ',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='customexam',
            name='TotalMarks',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='customexammarks',
            name='AchievedMarksCQ',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='customexammarks',
            name='AchievedMarksMCQ',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='practical',
            name='PassMarks',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='practical',
            name='PracticalPercentage',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='practical',
            name='TotalMarks',
            field=models.PositiveIntegerField(default=25),
        ),
        migrations.AlterField(
            model_name='practicalmarks',
            name='AchievedMarks',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='termfinal',
            name='CQ',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='termfinal',
            name='MCQ',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='termfinal',
            name='PassMarksCQ',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='termfinal',
            name='PassMarksMCQ',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='termfinal',
            name='TermFinalPercentage',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='termfinal',
            name='TotalMarks',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='termfinalmarks',
            name='AchievedMarksCQ',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='termfinalmarks',
            name='AchievedMarksMCQ',
            field=models.PositiveIntegerField(),
        ),
    ]
