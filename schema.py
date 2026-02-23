# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountsStudent(models.Model):
    id = models.UUIDField(primary_key=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField()
    current_grade = models.ForeignKey('EducationGrade', models.DO_NOTHING, blank=True, null=True)
    user = models.OneToOneField('AccountsUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_student'


class AccountsUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    id = models.UUIDField(primary_key=True)
    email = models.CharField(unique=True, max_length=254)
    created_at = models.DateTimeField()
    is_active = models.BooleanField()
    is_staff = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'accounts_user'


class AccountsUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_user_groups'
        unique_together = (('user', 'group'),)


class AccountsUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AiErroranalysis(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    ai_explanation = models.TextField()
    helpful_hint = models.TextField()
    generated_at = models.DateTimeField()
    user_answer = models.OneToOneField('ExercisesUseranswer', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ai_erroranalysis'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AccountsUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EducationChapter(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=255)
    order_index = models.IntegerField()
    subject = models.ForeignKey('EducationSubject', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'education_chapter'
        unique_together = (('subject', 'order_index'),)


class EducationGrade(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    level = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'education_grade'


class EducationLesson(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=255)
    order_index = models.IntegerField()
    is_completed = models.BooleanField()
    chapter = models.ForeignKey(EducationChapter, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'education_lesson'
        unique_together = (('chapter', 'order_index'),)


class EducationLessoncontent(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    rich_text_content = models.TextField()
    illustrations_url = models.CharField(max_length=200)
    audio_url = models.CharField(max_length=200)
    lesson = models.OneToOneField(EducationLesson, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'education_lessoncontent'


class EducationSubject(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=150)
    icon_url = models.CharField(max_length=200)
    grade = models.ForeignKey(EducationGrade, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'education_subject'
        unique_together = (('name', 'grade'),)


class ExercisesAnswer(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    choice_text = models.CharField(max_length=255)
    is_correct_option = models.BooleanField()
    question = models.ForeignKey('ExercisesQuestion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'exercises_answer'


class ExercisesDifficulty(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    level_name = models.CharField(unique=True, max_length=50)
    value = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'exercises_difficulty'


class ExercisesExercise(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    difficulty = models.ForeignKey(ExercisesDifficulty, models.DO_NOTHING)
    lesson = models.ForeignKey(EducationLesson, models.DO_NOTHING, blank=True, null=True)
    type = models.ForeignKey('ExercisesExercisetype', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'exercises_exercise'


class ExercisesExercisetype(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    name = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'exercises_exercisetype'


class ExercisesQuestion(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    question_text = models.TextField()
    points = models.FloatField()
    exercise = models.ForeignKey(ExercisesExercise, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'exercises_question'


class ExercisesUseranswer(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    response_text = models.TextField()
    is_correct_submission = models.BooleanField()
    submission_date = models.DateTimeField()
    answer = models.ForeignKey(ExercisesAnswer, models.DO_NOTHING, blank=True, null=True)
    question = models.ForeignKey(ExercisesQuestion, models.DO_NOTHING)
    student = models.ForeignKey(AccountsStudent, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'exercises_useranswer'


class NotificationsAchievement(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    badge_name = models.CharField(max_length=150)
    icon_url = models.CharField(max_length=200)
    date_earned = models.DateTimeField()
    student = models.ForeignKey(AccountsStudent, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'notifications_achievement'


class NotificationsNotification(models.Model):
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    message = models.TextField()
    is_read = models.BooleanField()
    created_at = models.DateTimeField()
    student = models.ForeignKey(AccountsStudent, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'notifications_notification'


class OfflineOfflinecontent(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    content_type = models.CharField(max_length=50)
    related_entity_id = models.UUIDField()
    local_file_path = models.CharField(max_length=255)
    last_synced = models.DateTimeField()
    student = models.ForeignKey(AccountsStudent, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'offline_offlinecontent'


class ProgressProgress(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    completion_percentage = models.FloatField()
    average_score = models.FloatField()
    last_activity = models.DateTimeField()
    lesson = models.ForeignKey(EducationLesson, models.DO_NOTHING)
    student = models.ForeignKey(AccountsStudent, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'progress_progress'
        unique_together = (('student', 'lesson'),)


class RevisionRevisionsession(models.Model):
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField()
    is_completed = models.BooleanField()
    student = models.ForeignKey(AccountsStudent, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'revision_revisionsession'
