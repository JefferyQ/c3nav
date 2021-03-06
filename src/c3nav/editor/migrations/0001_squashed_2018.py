# Generated by Django 2.1.1 on 2018-12-07 18:42

import c3nav.mapdata.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('editor', '0001_initial'), ('editor', '0002_auto_20170612_1615'), ('editor', '0003_auto_20170618_1942'), ('editor', '0004_auto_20170620_0934'), ('editor', '0005_auto_20170627_0027'), ('editor', '0006_auto_20170629_1222'), ('editor', '0007_auto_20170629_1327'), ('editor', '0008_auto_20170629_1450'), ('editor', '0009_auto_20170701_1218'), ('editor', '0010_auto_20170704_1431'), ('editor', '0011_auto_20170704_1640'), ('editor', '0012_remove_changeset_session_id'), ('editor', '0013_remove_changesetupdate_session_user'), ('editor', '0014_last_update_foreign_key'), ('editor', '0015_changeset_last_state_update'), ('editor', '0016_auto_20170705_1938'), ('editor', '0017_changeset_map_update'), ('editor', '0018_changeset_last_cleaned_with'), ('editor', '0019_permissions'), ('editor', '0020_remove_permissions'), ('editor', '0021_auto_20180918_1736')]

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mapdata', '0001_squashed_2018'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangedObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('existing_object_pk', models.PositiveIntegerField(null=True, verbose_name='id of existing object')),
                ('updated_fields', c3nav.mapdata.fields.JSONField(default={}, verbose_name='updated fields')),
                ('m2m_added', c3nav.mapdata.fields.JSONField(default={}, verbose_name='added m2m values')),
                ('m2m_removed', c3nav.mapdata.fields.JSONField(default={}, verbose_name='removed m2m values')),
                ('deleted', models.BooleanField(default=False, verbose_name='object was deleted')),
            ],
            options={
                'verbose_name': 'Changed object',
                'verbose_name_plural': 'Changed objects',
                'ordering': ['created', 'pk'],
                'default_related_name': 'changed_objects_set',
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='ChangeSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('state', models.CharField(choices=[('unproposed', 'unproposed'), ('proposed', 'proposed'), ('review', 'in review'), ('rejected', 'rejected'), ('reproposed', 'proposed again'), ('finallyrejected', 'finally rejected'), ('applied', 'accepted and applied')], db_index=True, default='unproposed', max_length=20)),
                ('title', models.CharField(default='', max_length=100, verbose_name='Title')),
                ('description', models.TextField(default='', max_length=1000, verbose_name='Description')),
                ('assigned_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assigned_changesets', to=settings.AUTH_USER_MODEL, verbose_name='assigned to')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='changesets', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Change Set',
                'verbose_name_plural': 'Change Sets',
                'default_related_name': 'changesets',
            },
        ),
        migrations.CreateModel(
            name='ChangeSetUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='datetime')),
                ('comment', models.TextField(max_length=1000, null=True)),
                ('state', models.CharField(choices=[('unproposed', 'unproposed'), ('proposed', 'proposed'), ('review', 'in review'), ('rejected', 'rejected'), ('reproposed', 'proposed again'), ('finallyrejected', 'finally rejected'), ('applied', 'accepted and applied')], db_index=True, max_length=20, null=None)),
                ('title', models.CharField(max_length=100, null=True)),
                ('description', models.TextField(max_length=1000, null=True)),
                ('objects_changed', models.BooleanField(default=False)),
                ('assigned_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('changeset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='editor.ChangeSet')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Change set update',
                'verbose_name_plural': 'Change set updates',
                'ordering': ['datetime', 'pk'],
                'get_latest_by': 'datetime',
            },
        ),
        migrations.AddField(
            model_name='changeset',
            name='last_change',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='editor.ChangeSetUpdate', verbose_name='last object change'),
        ),
        migrations.AddField(
            model_name='changeset',
            name='last_cleaned_with',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='checked_changesets', to='mapdata.MapUpdate'),
        ),
        migrations.AddField(
            model_name='changeset',
            name='last_state_update',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='editor.ChangeSetUpdate', verbose_name='last state update'),
        ),
        migrations.AddField(
            model_name='changeset',
            name='last_update',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='editor.ChangeSetUpdate', verbose_name='last update'),
        ),
        migrations.AddField(
            model_name='changeset',
            name='map_update',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='changeset', to='mapdata.MapUpdate', verbose_name='map update'),
        ),
        migrations.AddField(
            model_name='changedobject',
            name='changeset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='changed_objects_set', to='editor.ChangeSet', verbose_name='Change Set'),
        ),
        migrations.AddField(
            model_name='changedobject',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='changed_objects_set', to='contenttypes.ContentType'),
        ),
        migrations.AlterUniqueTogether(
            name='changedobject',
            unique_together={('changeset', 'content_type', 'existing_object_pk')},
        ),
    ]
