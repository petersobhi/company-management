from django import forms

from employee.models import Employee, Invitation
from .models import Company, Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'description')


class AddEmployeesForm(forms.ModelForm):
    employees = forms.ModelMultipleChoiceField(queryset=Employee.objects.filter(company__isnull=True))

    class Meta:
        model = Company
        fields = ('employees',)

    def save(self, commit=True):
        company = super(AddEmployeesForm, self).save(commit=False)
        employees = self.cleaned_data['employees']
        company.employees.add(*list(employees))
        return company


class RemoveEmployeesForm(forms.ModelForm):
    employees = forms.ModelMultipleChoiceField(queryset=None)

    class Meta:
        model = Company
        fields = ('employees',)

    def __init__(self, *args, **kwargs):
        super(RemoveEmployeesForm, self).__init__(*args, **kwargs)
        employees = Employee.objects.filter(company=self.instance)
        if self.instance.admin:
            employees = employees.exclude(pk=self.instance.admin.pk)
        self.fields['employees'].queryset = employees

    def save(self, commit=True):
        company = super(RemoveEmployeesForm, self).save(commit=False)
        employees = self.cleaned_data['employees']
        company.employees.remove(*list(employees))
        return company


class AddTeamMembersForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(queryset=None)

    class Meta:
        model = Team
        fields = ('members',)

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(AddTeamMembersForm, self).__init__(*args, **kwargs)
        employees = Employee.objects.all()
        if company:
            employees = employees.filter(company=company)
            if company.admin:
                employees = employees.exclude(pk=company.admin.pk)
        self.fields['members'].queryset = employees

    def save(self, commit=True):
        team = super(AddTeamMembersForm, self).save(commit=False)
        members = self.cleaned_data['members']
        team.members.add(*list(members))
        return team


class InviteEmployeeForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ('employee', 'message')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(InviteEmployeeForm, self).__init__(*args, **kwargs)
        if company:
            invited_employees = Invitation.objects.filter(company=company).values('employee')
            employees = Employee.objects.exclude(company=company).exclude(id__in=invited_employees)
            if company.admin:
                employees = employees.exclude(pk=company.admin.pk)
            self.fields['employee'].queryset = employees
