# Generated by Django 4.2.4 on 2023-08-09 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0004_questionbank"),
    ]

    operations = [
        migrations.CreateModel(
            name="CandidateResponse",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("answer", models.TextField()),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="home.questionbank",
                    ),
                ),
            ],
        ),
    ]