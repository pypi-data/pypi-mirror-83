# Generated by Django 2.2.6 on 2019-10-15 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook_url', models.URLField(blank=True, help_text="Page's url in facebook", verbose_name='Facebook')),
                ('twitter_handle', models.CharField(blank=True, help_text='Without the @', max_length=255, verbose_name='Twitter handle')),
                ('twitter_url', models.URLField(blank=True, help_text="Page's url in twitter", verbose_name='Twitter')),
                ('instagram_url', models.URLField(blank=True, help_text="Page's url in instagram", verbose_name='Instagram')),
                ('linkedin_url', models.URLField(blank=True, help_text="Page's url in linkedin", verbose_name='LinkedIn')),
                ('youtube_url', models.URLField(blank=True, help_text="Page's url in youtube", verbose_name='Youtube')),
                ('vimeo_url', models.URLField(blank=True, help_text="Page's url in vimeo", verbose_name='Vimeo')),
                ('googleplus_url', models.URLField(blank=True, help_text="Page's url in google plus", verbose_name='Google Plus')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
            ],
            options={
                'verbose_name': 'Social',
                'verbose_name_plural': 'Social',
            },
        ),
        migrations.CreateModel(
            name='OtherSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentry_active', models.BooleanField(default=False, verbose_name='Activate')),
                ('sentry_dsn', models.URLField(blank=True, help_text='Get it from sentry.io', verbose_name='DSN for frontend error reporting')),
                ('google_recaptcha_public', models.CharField(max_length=255, verbose_name='Recaptcha Public Key')),
                ('google_recaptcha_secret', models.CharField(max_length=255, verbose_name='Recaptcha Secret Key')),
                ('ssl_on', models.BooleanField(default=False, verbose_name='Is SSL active?')),
                ('sending_criteria', models.CharField(choices=[('Express', 'Express'), ('Normal', 'Normal')], default='Normal', max_length=14, verbose_name='Preference')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
            ],
            options={
                'verbose_name': 'Security',
                'verbose_name_plural': 'Security',
            },
        ),
        migrations.CreateModel(
            name='AnalyticsSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook_pixel', models.CharField(blank=True, max_length=70, verbose_name='Pixel ID')),
                ('facebook_account', models.CharField(blank=True, max_length=70, verbose_name='Account ID')),
                ('facebook_app', models.CharField(blank=True, max_length=70, verbose_name='App ID')),
                ('google_analytics_enabled', models.BooleanField(blank=True, default=False, verbose_name='Analytics enabled')),
                ('google_analytics_id', models.CharField(blank=True, max_length=255, verbose_name='Analytics ID')),
                ('google_adwords_enabled', models.BooleanField(blank=True, default=False, verbose_name='Adwords enabled')),
                ('google_adwords_id', models.CharField(blank=True, max_length=255, verbose_name='Adwords ID')),
                ('google_tagmanager_enabled', models.BooleanField(blank=True, default=False, verbose_name='Tagmanager enabled')),
                ('google_tagmanager_id', models.CharField(blank=True, max_length=255, verbose_name='TagManager ID')),
                ('google_site_verification', models.CharField(blank=True, max_length=255, verbose_name='Site Verification Key')),
                ('default_title', models.CharField(max_length=300, verbose_name='Title')),
                ('title_suffix', models.CharField(default='Wuafbox', help_text='For SEO the pages will appear in this manner: Title | Suffix', max_length=40, verbose_name='Title Suffix')),
                ('default_description', models.CharField(max_length=255, verbose_name='Description')),
                ('default_language', models.CharField(choices=[('es', 'Spanish'), ('en', 'English')], default='es', max_length=6, verbose_name='Language')),
                ('default_promote_image', models.ForeignKey(help_text='Image used by default for the SEO metas. 1200x630 preferably', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Share Image')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
            ],
            options={
                'verbose_name': 'SEO',
                'verbose_name_plural': 'SEO',
            },
        ),
    ]
