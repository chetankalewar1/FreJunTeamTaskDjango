from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Import slugify to generate slugs from strings
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given phone and password.
        """
        user = self.model(email=email, is_active=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):

        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["is_leader"] = True
        return self._create_user(email, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    AbstractBaseUser provides the following:
        * password
        * last_login
        * set_password()
        * check_password()
    PermissionsMixin provides:
        * is_superuser
        * groups
        * permissions
        * several methods() related to groups and permissions
    """

    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(max_length=64)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(
        _("staff status"), default=False, help_text=_("Can log into this admin site.")
    )

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("abstract_user")
        verbose_name_plural = _("abstract_users")
        abstract = True


class User(AbstractUser):
    is_leader = models.BooleanField(_('leader'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    def __str__(self):
        return self.email


class Team(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    team = models.ForeignKey(Team, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Task(models.Model):
    HIGH = "high"
    LOW = "low"
    MEDIUM = "medium"

    priority_choices = (
        (HIGH, "high"),
        (LOW, "low"),
        (MEDIUM, "medium"),
    )

    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    UNDER_REVIEW = "under_review"
    DONE = "done"

    status_choices = (
        (ASSIGNED, "assigned"),
        (IN_PROGRESS, "in_progress"),
        (DONE, "done"),
        (UNDER_REVIEW, "under_review"),
    )

    name = models.CharField(max_length=128)
    priority = models.CharField(max_length=16, default=LOW, choices=priority_choices)
    created_by = models.ForeignKey(User, models.CASCADE)
    start = models.DateField()
    end = models.DateField()
    status = models.CharField(max_length=16, default=ASSIGNED, choices=status_choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class AssignTask(models.Model):
    task = models.ForeignKey(Task, models.CASCADE)
    member = models.ForeignKey(User, models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.task} -> {self.member.email}"
