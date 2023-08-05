# Generated by Django 2.0 on 2018-01-03 11:51

from django.db import migrations, models
import django_crypto_fields.fields.encrypted_char_field
import django_crypto_fields.fields.encrypted_text_field
import edc_model.validators.phone


class Migration(migrations.Migration):

    dependencies = [("edc_locator", "0002_auto_20180103_1322")]

    operations = [
        migrations.AddField(
            model_name="historicalsubjectlocator",
            name="may_call_work",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=25,
                verbose_name="Has the participant given permission to contacted <b>at work</b> by telephone or cell by study staff for follow-up purposes during the study?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="subjectlocator",
            name="may_call_work",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=25,
                verbose_name="Has the participant given permission to contacted <b>at work</b> by telephone or cell by study staff for follow-up purposes during the study?",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="historicalsubjectlocator",
            name="subject_work_phone",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                help_text=" (Encryption: RSA local)",
                max_length=71,
                null=True,
                verbose_name="Work contact number",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectlocator",
            name="subject_work_place",
            field=django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(
                blank=True,
                help_text=" (Encryption: AES local)",
                max_length=250,
                null=True,
                validators=[edc_model.validators.phone.telephone_number],
                verbose_name="Name and location of work place",
            ),
        ),
        migrations.AlterField(
            model_name="subjectlocator",
            name="subject_work_phone",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                help_text=" (Encryption: RSA local)",
                max_length=71,
                null=True,
                verbose_name="Work contact number",
            ),
        ),
        migrations.AlterField(
            model_name="subjectlocator",
            name="subject_work_place",
            field=django_crypto_fields.fields.encrypted_text_field.EncryptedTextField(
                blank=True,
                help_text=" (Encryption: AES local)",
                max_length=250,
                null=True,
                validators=[edc_model.validators.phone.telephone_number],
                verbose_name="Name and location of work place",
            ),
        ),
    ]
