from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, DeleteView

from .forms import EmployeeForm
from .models import Invitation

User = get_user_model()


class ViewProfile(DetailView):
    model = User
    template_name = 'user_details.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        # Add edit profile form to context
        context = super(ViewProfile, self).get_context_data()
        user = self.request.user
        biography = user.employee.biography
        birthdate = user.employee.birthdate
        profile_picture = user.employee.profile_picture
        job_title = user.employee.job_title
        initial = {'biography': biography, 'birthdate': birthdate, 'profile_picture': profile_picture,
                   'job_title': job_title}
        context['form'] = EmployeeForm(self.request.GET or None, instance=self.get_object(), initial=initial)
        return context


class UpdateProfile(LoginRequiredMixin, UpdateView):
    form_class = EmployeeForm
    template_name = 'user_details.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

    def get_object(self, queryset=None):
        return self.request.user

    def get_initial(self):
        user = self.get_object()
        biography = user.employee.biography
        birthdate = user.employee.birthdate
        profile_picture = user.employee.profile_picture
        return {'biography': biography, 'birthdate': birthdate, 'profile_picture': profile_picture}


class ListInvitation(LoginRequiredMixin, ListView):
    model = Invitation
    template_name = 'invitation_list.html'
    context_object_name = 'invitations'

    def get_queryset(self):
        return Invitation.objects.filter(employee=self.request.user.employee)


class AcceptInvitation(LoginRequiredMixin, DeleteView):
    model = Invitation

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

    def get(self, request, *args, **kwargs):
        # skip delete confirmation
        return self.post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        invitation = super(AcceptInvitation, self).get_object()
        if invitation.employee.user != self.request.user:
            raise PermissionDenied()
        # Change company to the new one
        self.request.user.employee.company = invitation.company
        self.request.user.employee.save()
        return invitation


class DeleteInvitation(LoginRequiredMixin, DeleteView):
    model = Invitation

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

    def get(self, request, *args, **kwargs):
        # skip delete confirmation
        return self.post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        invitation = super(DeleteInvitation, self).get_object()
        if invitation.employee.user != self.request.user:
            raise PermissionDenied()
        return invitation
