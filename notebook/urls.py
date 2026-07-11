from django.urls import path
from .views import DashboardView, NoteDetailView, NoteCreateView, NoteUpdateView

app_name = 'notebook'

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("notes/create/", NoteCreateView.as_view(), name='create'),
    path("notes/<int:pk>/", NoteDetailView.as_view(), name="detail"),
    path("notes/<int:pk>/edit/", NoteUpdateView.as_view(), name="edit"),
]