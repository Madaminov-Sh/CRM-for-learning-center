from django.urls import reverse
from .forms import *
from agents.mixins import OrganisorAndLoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.views.generic import (TemplateView, ListView, DetailView,
 CreateView, UpdateView, DeleteView, FormView)


class SignupView(CreateView):
    template_name = "registration/signup.html"  
    form_class = NewUserForm

    def get_success_url (self):
        return reverse('leads:home')


class HomeView(TemplateView):
    template_name = 'home.html'


class LeadListView(LoginRequiredMixin,ListView):
    template_name = "leads_lists.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:              
            queryset = Lead.objects.filter(profil = user.userprofil)
        else:                              
            queryset = Lead.objects.filter(profil = user.agent.profil)
            queryset = queryset.filter(agent__user = self.request.user)
        return queryset                      

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                profil = user.userprofil,
                agent__isnull = True
            )
            context.update(
                {'unassigned_leads': queryset}
            )
        return context                     


class LeadDetailView(OrganisorAndLoginRequiredMixin, DetailView):
    template_name = 'details.html'
    queryset = Lead.objects.all()
    context_object_name = "lead"


class LeadCreateView(OrganisorAndLoginRequiredMixin, CreateView):
    template_name = "cud/create.html"
    form_class = LeadModelForm

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.profil = self.request.user.userprofil
        lead.save()
        return super(LeadCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('leads:lead-list')


class LeadUpdateView(OrganisorAndLoginRequiredMixin, UpdateView):
    template_name = 'cud/update.html'
    form_class = LeadModelForm
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('leads:lead-list')


class LeadDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = "cud/delete.html"
    form_class = LeadModelForm
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('leads:lead-list')


class AgentAssignToLeadView(LoginRequiredMixin, FormView):
    template_name = 'agentassigntolead.html'
    context_object_name = "leads"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AgentAssignToLeadView, self).get_form_kwargs(**kwargs)
        kwargs.update(
            {'request': self.request}
        )
        return kwargs

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id = self.kwargs['pk'])
        lead.agent = agent  
        lead.save()
        return super(AgentAssignToLeadView, self).form_valid(form)


class CategoryListView(OrganisorAndLoginRequiredMixin, ListView):
    template_name = "category/category_list.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                profil = user.userprofil
            )
        else:
            queryset = Category.objects.filter(profil = user.agent.profil)
        context.update(
            {'unassigned_categories_count': queryset.filter(kategoriya__isnull=True).count()}
        )
        return context            

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:              
            queryset = Category.objects.filter(profil = user.userprofil)
        else:                              
            queryset = Category.objects.filter(profil = user.agent.profil)
        return queryset    


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = 'category/category_detail.html'
    context_object_name = 'category'

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:              
            queryset = Category.objects.filter(profil = user.userprofil)
        else:                              
            queryset = Category.objects.filter(profil = user.agent.profil)
        return queryset    


class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'category/lead_category_update.html'
    form_class = LeadCategoryUpdateFrom

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:              
            queryset = Lead.objects.filter(profil = user.userprofil)
        else:                              
            queryset = Lead.objects.filter(profil = user.agent.profil)
        return queryset    

    def get_success_url(self): 
        return reverse('leads:lead-list')


class LeadCategoryUncertainView(LoginRequiredMixin, ListView):
    template_name = 'category/category_uncertain.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:              
            queryset = Lead.objects.filter(profil = user.userprofil)
        else:                              
            queryset = Lead.objects.filter(profil = user.agent.profil)
            queryset = queryset.filter(agent__user = self.request.user)
        return queryset           

    def get_context_data(self, **kwargs):
        context = super(LeadCategoryUncertainView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                profil = user.userprofil,
                kategoriya__isnull = True
            )
            context.update(
                {'unassigned_leads': queryset}
            )
        return context       
