# Generated by Django 3.0.6 on 2020-06-25 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inte_lists", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArvDrugs",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        help_text="This is the stored value, required",
                        max_length=250,
                        unique=True,
                        verbose_name="Stored value",
                    ),
                ),
                (
                    "display_name",
                    models.CharField(
                        db_index=True,
                        help_text="(suggest 40 characters max.)",
                        max_length=250,
                        unique=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "display_index",
                    models.IntegerField(
                        db_index=True,
                        default=0,
                        help_text="Index to control display order if not alphabetical, not required",
                        verbose_name="display index",
                    ),
                ),
                (
                    "field_name",
                    models.CharField(
                        blank=True,
                        editable=False,
                        help_text="Not required",
                        max_length=25,
                        null=True,
                    ),
                ),
                (
                    "version",
                    models.CharField(default="1.0", editable=False, max_length=35),
                ),
            ],
            options={
                "verbose_name": "Arv Drugs",
                "verbose_name_plural": "Arv Drugs",
                "ordering": ["display_index", "display_name"],
                "abstract": False,
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
            },
        ),
        migrations.CreateModel(
            name="ClinicServices",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        help_text="This is the stored value, required",
                        max_length=250,
                        unique=True,
                        verbose_name="Stored value",
                    ),
                ),
                (
                    "display_name",
                    models.CharField(
                        db_index=True,
                        help_text="(suggest 40 characters max.)",
                        max_length=250,
                        unique=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "display_index",
                    models.IntegerField(
                        db_index=True,
                        default=0,
                        help_text="Index to control display order if not alphabetical, not required",
                        verbose_name="display index",
                    ),
                ),
                (
                    "field_name",
                    models.CharField(
                        blank=True,
                        editable=False,
                        help_text="Not required",
                        max_length=25,
                        null=True,
                    ),
                ),
                (
                    "version",
                    models.CharField(default="1.0", editable=False, max_length=35),
                ),
            ],
            options={
                "verbose_name": "Clinic Services",
                "verbose_name_plural": "Clinic Services",
                "ordering": ["display_index", "display_name"],
                "abstract": False,
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
            },
        ),
        migrations.CreateModel(
            name="DiabetesTreatments",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        help_text="This is the stored value, required",
                        max_length=250,
                        unique=True,
                        verbose_name="Stored value",
                    ),
                ),
                (
                    "display_name",
                    models.CharField(
                        db_index=True,
                        help_text="(suggest 40 characters max.)",
                        max_length=250,
                        unique=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "display_index",
                    models.IntegerField(
                        db_index=True,
                        default=0,
                        help_text="Index to control display order if not alphabetical, not required",
                        verbose_name="display index",
                    ),
                ),
                (
                    "field_name",
                    models.CharField(
                        blank=True,
                        editable=False,
                        help_text="Not required",
                        max_length=25,
                        null=True,
                    ),
                ),
                (
                    "version",
                    models.CharField(default="1.0", editable=False, max_length=35),
                ),
            ],
            options={
                "verbose_name": "Diabetes Treatments",
                "verbose_name_plural": "Diabetes Treatments",
                "ordering": ["display_index", "display_name"],
                "abstract": False,
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
            },
        ),
        migrations.CreateModel(
            name="HealthServices",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        help_text="This is the stored value, required",
                        max_length=250,
                        unique=True,
                        verbose_name="Stored value",
                    ),
                ),
                (
                    "display_name",
                    models.CharField(
                        db_index=True,
                        help_text="(suggest 40 characters max.)",
                        max_length=250,
                        unique=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "display_index",
                    models.IntegerField(
                        db_index=True,
                        default=0,
                        help_text="Index to control display order if not alphabetical, not required",
                        verbose_name="display index",
                    ),
                ),
                (
                    "field_name",
                    models.CharField(
                        blank=True,
                        editable=False,
                        help_text="Not required",
                        max_length=25,
                        null=True,
                    ),
                ),
                (
                    "version",
                    models.CharField(default="1.0", editable=False, max_length=35),
                ),
            ],
            options={
                "verbose_name": "Health Services",
                "verbose_name_plural": "Health Services",
                "ordering": ["display_index", "display_name"],
                "abstract": False,
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
            },
        ),
        migrations.CreateModel(
            name="HypertensionTreatments",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        help_text="This is the stored value, required",
                        max_length=250,
                        unique=True,
                        verbose_name="Stored value",
                    ),
                ),
                (
                    "display_name",
                    models.CharField(
                        db_index=True,
                        help_text="(suggest 40 characters max.)",
                        max_length=250,
                        unique=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "display_index",
                    models.IntegerField(
                        db_index=True,
                        default=0,
                        help_text="Index to control display order if not alphabetical, not required",
                        verbose_name="display index",
                    ),
                ),
                (
                    "field_name",
                    models.CharField(
                        blank=True,
                        editable=False,
                        help_text="Not required",
                        max_length=25,
                        null=True,
                    ),
                ),
                (
                    "version",
                    models.CharField(default="1.0", editable=False, max_length=35),
                ),
            ],
            options={
                "verbose_name": "Hypertension Treatments",
                "verbose_name_plural": "Hypertension Treatments",
                "ordering": ["display_index", "display_name"],
                "abstract": False,
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
            },
        ),
        migrations.CreateModel(
            name="RxModificationReasons",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        help_text="This is the stored value, required",
                        max_length=250,
                        unique=True,
                        verbose_name="Stored value",
                    ),
                ),
                (
                    "display_name",
                    models.CharField(
                        db_index=True,
                        help_text="(suggest 40 characters max.)",
                        max_length=250,
                        unique=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "display_index",
                    models.IntegerField(
                        db_index=True,
                        default=0,
                        help_text="Index to control display order if not alphabetical, not required",
                        verbose_name="display index",
                    ),
                ),
                (
                    "field_name",
                    models.CharField(
                        blank=True,
                        editable=False,
                        help_text="Not required",
                        max_length=25,
                        null=True,
                    ),
                ),
                (
                    "version",
                    models.CharField(default="1.0", editable=False, max_length=35),
                ),
            ],
            options={
                "verbose_name": "Treatment Modification Reasons",
                "verbose_name_plural": "Treatment Modification Reasons",
                "ordering": ["display_index", "display_name"],
                "abstract": False,
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
            },
        ),
        migrations.CreateModel(
            name="RxModifications",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        help_text="This is the stored value, required",
                        max_length=250,
                        unique=True,
                        verbose_name="Stored value",
                    ),
                ),
                (
                    "display_name",
                    models.CharField(
                        db_index=True,
                        help_text="(suggest 40 characters max.)",
                        max_length=250,
                        unique=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "display_index",
                    models.IntegerField(
                        db_index=True,
                        default=0,
                        help_text="Index to control display order if not alphabetical, not required",
                        verbose_name="display index",
                    ),
                ),
                (
                    "field_name",
                    models.CharField(
                        blank=True,
                        editable=False,
                        help_text="Not required",
                        max_length=25,
                        null=True,
                    ),
                ),
                (
                    "version",
                    models.CharField(default="1.0", editable=False, max_length=35),
                ),
            ],
            options={
                "verbose_name": "Treatment Modifications",
                "verbose_name_plural": "Treatment Modifications",
                "ordering": ["display_index", "display_name"],
                "abstract": False,
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
            },
        ),
        migrations.DeleteModel(name="DiabetesTreatment",),
        migrations.DeleteModel(name="HypertensionTreatment",),
        migrations.AddIndex(
            model_name="rxmodifications",
            index=models.Index(
                fields=["id", "display_name", "display_index"],
                name="inte_lists__id_9e0101_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="rxmodificationreasons",
            index=models.Index(
                fields=["id", "display_name", "display_index"],
                name="inte_lists__id_eeabfd_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="hypertensiontreatments",
            index=models.Index(
                fields=["id", "display_name", "display_index"],
                name="inte_lists__id_34d395_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="healthservices",
            index=models.Index(
                fields=["id", "display_name", "display_index"],
                name="inte_lists__id_af9927_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="diabetestreatments",
            index=models.Index(
                fields=["id", "display_name", "display_index"],
                name="inte_lists__id_5eae8d_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="clinicservices",
            index=models.Index(
                fields=["id", "display_name", "display_index"],
                name="inte_lists__id_c9cbba_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="arvdrugs",
            index=models.Index(
                fields=["id", "display_name", "display_index"],
                name="inte_lists__id_8c8bae_idx",
            ),
        ),
    ]
