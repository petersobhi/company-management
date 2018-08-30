from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from . import forms
from .models import Company, Team

User = get_user_model()


def home(request):
    return redirect('accounts_login')


class ViewCompany(LoginRequiredMixin, TemplateView):
    model = Company
    template_name = 'company_details.html'

    def get_object(self, queryset=None):
        return self.request.user.employee.company

    def get(self, request, *args, **kwargs):
        if not self.get_object():
            return redirect('profile', username=self.request.user.username)
        add_employees_form = forms.AddEmployeesForm(self.request.GET or None, instance=self.get_object())
        remove_employees_form = forms.RemoveEmployeesForm(self.request.GET or None, instance=self.get_object())
        invite_employee_form = forms.InviteEmployeeForm(self.request.GET or None, company=self.get_object())
        add_team_members_form = forms.AddTeamMembersForm(self.request.GET or None, company=self.get_object())
        add_team_form = forms.TeamForm(self.request.GET or None)
        context = self.get_context_data(**kwargs)
        context['add_employees_form'] = add_employees_form
        context['remove_employees_form'] = remove_employees_form
        context['invite_employee_form'] = invite_employee_form
        context['add_team_members_form'] = add_team_members_form
        context['add_team_form'] = add_team_form
        context['company'] = self.get_object()
        return self.render_to_response(context)


class AddEmployees(LoginRequiredMixin, UpdateView):
    form_class = forms.AddEmployeesForm
    template_name = 'company_details.html'
    success_url = reverse_lazy('company')

    def get_object(self, queryset=None):
        company = self.request.user.employee.company
        if company.admin != self.request.user:
            raise PermissionDenied()
        return company


class RemoveEmployees(LoginRequiredMixin, UpdateView):
    form_class = forms.RemoveEmployeesForm
    template_name = 'company_details.html'
    success_url = reverse_lazy('company')

    def get_object(self, queryset=None):
        company = self.request.user.employee.company
        if company.admin != self.request.user:
            raise PermissionDenied()
        return company


class AddTeamMembers(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = forms.AddTeamMembersForm
    template_name = 'company_details.html'
    success_url = reverse_lazy('company')

    def get_object(self, queryset=None):
        team = super(AddTeamMembers, self).get_object(queryset=queryset)
        if team.company.admin != self.request.user:
            raise PermissionDenied()
        return team


class InviteEmployee(LoginRequiredMixin, CreateView):
    form_class = forms.InviteEmployeeForm
    template_name = 'company_details.html'
    success_url = reverse_lazy('company')

    def form_valid(self, form):
        company = self.request.user.admined_company
        obj = form.save(commit=False)
        if obj.employee.user == self.request.user:
            raise PermissionDenied()
        obj.company = self.request.user.admined_company
        return super(InviteEmployee, self).form_valid(form)


class TeamAdd(LoginRequiredMixin, CreateView):
    form_class = forms.TeamForm
    template_name = 'company_details.html'
    success_url = reverse_lazy('company')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.company = self.request.user.admined_company
        return super(TeamAdd, self).form_valid(form)


class TeamDelete(LoginRequiredMixin, DeleteView):
    model = Team
    success_url = reverse_lazy('company')

    def get(self, request, *args, **kwargs):
        # skip delete confirmation
        return self.post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        team = super(TeamDelete, self).get_object()
        if team.company.admin != self.request.user:
            raise PermissionDenied()
        return team
