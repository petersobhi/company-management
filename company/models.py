from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Company(TimeStampedModel):
    name = models.CharField(max_length=50)
    industry = models.CharField(max_length=120)
    description = models.TextField(max_length=500)
    admin = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='admined_company', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Company, self).save()

        # Add company's admin to its employees
        if self.admin:
            self.admin.employee.company = self
            self.admin.employee.save()


class Team(TimeStampedModel):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='teams')

    def __str__(self):
        return self.name
