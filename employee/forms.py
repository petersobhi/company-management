from django import forms

from .models import Employee


class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    job_title = forms.CharField(max_length=50)
    profile_picture = forms.ImageField()
    birthdate = forms.DateField(widget=forms.SelectDateWidget(years=range(1920, 2050)))
    biography = forms.Textarea()

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'birthdate', 'biography')

    def save_employee(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        user.employee.job_title = self.cleaned_data['job_title']
        user.employee.birthdate = self.cleaned_data['birthdate']
        user.employee.biography = self.cleaned_data['biography']
        user.employee.profile_picture = self.cleaned_data['profile_picture']
        user.employee.save()

    def signup(self, request, user):
        self.save_employee(user)

    def save(self, commit=True):
        user = super(EmployeeForm, self).save(commit=False)
        self.save_employee(user)
        return user
