from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('accounts', '0001_initial')]
    operations = [
        migrations.AddField(
            model_name='userprofile', name='security_question',
            field=models.CharField(blank=True, choices=[
                ('first_school', 'What was the name of your first school?'),
                ('childhood_friend', 'What was the first name of your childhood best friend?'),
                ('birth_city', 'In which city were you born?'),
                ('favorite_teacher', 'What was the surname of a favorite teacher?'),
                ('memorable_place', 'What was the name of a memorable place from your childhood?'),
            ], default='', max_length=32),
        ),
        migrations.AddField(
            model_name='userprofile', name='security_answer_hash',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
    ]
