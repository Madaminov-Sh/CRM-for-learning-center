import random
from django.urls import reverse
from django.views import generic
from leads.views import Agent
from django.core.mail import send_mail
from agents.mixins import OrganisorAndLoginRequiredMixin
from agents.forms import AgentModelForm


class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/list.html'

    def get_queryset(self):
        profil = self.request.user.userprofil
        return Agent.objects.filter(profil=profil)


class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "cud/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_organisor = False
        user.is_agent = True
        user.set_password(f'{random.randint(0, 10000)}')
        user.save()
        Agent.objects.create(
            user=user,
            profil=self.request.user.userprofil
        )
        send_mail(
            subject="Bu agent mavjud",
            message="Yangi agent mavjud",
            from_email="test@mail.com",
            recipient_list=[user.email],
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        profil = self.request.user.userprofil
        return Agent.objects.filter(profil=profil)


class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'cud/agent_update.html'
    form_class = AgentModelForm

    def get_queryset(self):
        profil = self.request.user.userprofil
        return Agent.objects.filter(profil=profil)

    def get_success_url(self):
        return reverse("agents:agent-list")


class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'cud/agent_delete.html'
    context_object_name = 'agent'

    def get_queryset(self):
        profil = self.request.user.userprofil
        return Agent.objects.filter(profil=profil)

    def get_success_url(self):
        return reverse('agents:agent-list')
