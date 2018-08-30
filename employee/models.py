from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from company.models import Company, Team

User = get_user_model()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/<username>/profile_pic.<ext>
    basename, file_extension = filename.split(".")
    new_filename = "profile_pic.%s" % (file_extension)
    return 'users/{0}/{1}'.format(instance.user.username, new_filename)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    job_title = models.CharField(max_length=50, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name='employees', null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='members', null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    biography = models.TextField(max_length=500, blank=True, null=True)

    @property
    def is_admin(self):
        if self.company:
            return self.user == self.company.admin

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)


class Invitation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='invitations')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='invitations')
    message = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        unique_together = ('company', 'employee',)
