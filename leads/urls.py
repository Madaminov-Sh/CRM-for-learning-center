from django.urls import path
from .views import *

app_name = 'leads'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('leads/', LeadListView.as_view(), name ="lead-list"),
    path('category/', CategoryListView.as_view(), name ="category-list"),
    path('<int:pk>/category-detail', CategoryDetailView.as_view(), name ="category-detail"),
    path('<int:pk>/lead-category-update', LeadCategoryUpdateView.as_view(), name ="lead-category-update"),
    path('<int:pk>/detail', LeadDetailView.as_view(), name='detail'),
    path('<int:pk>/update', LeadUpdateView.as_view(), name='update'),
    path('<int:pk>/agent-to-lead', AgentAssignToLeadView.as_view(), name='agent-to-lead'),
    path('lead-category-uncertain/', LeadCategoryUncertainView.as_view(), name='aniqlash'),
    path('<int:pk>/delete', LeadDeleteView.as_view(), name='delete'),
    path('create-lead/', LeadCreateView.as_view(), name='lead-create'),
]
