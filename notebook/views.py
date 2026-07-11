from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import calendar

from .models import Note
from .forms import NoteForm

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'notebook/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today_note'] = self._get_today_note()
        review_notes = self._get_review_notes()
        context['review_notes'] = review_notes
        context['review_count'] = sum(1 for item in review_notes if item['note'])
        context.update(self._get_calendar_context())
        context['total_notes'] = Note.objects.filter(user=self.request.user).count()
        context['streak_days'] = self._get_streak_days()
        return context

    def _get_today_note(self):
        today_note = Note.objects.filter(
            user=self.request.user,
            date=date.today(),
        ).first()
        return today_note

    def _get_review_notes(self):
        note_days = [
            ('昨日', 1),
            ('1週間前', 7),
            ('2週間前', 14),
            ('1ヶ月前', 30),
        ]
        notes = []
        for label, days in note_days:
            note = Note.objects.filter(
                user=self.request.user,
                date=date.today() - timedelta(days=days),
            ).first()
            notes.append({'label': label, 'note': note})
        return notes

    def _get_calendar_context(self):
        today = date.today()
        year = int(self.request.GET.get('year', today.year))
        month = int(self.request.GET.get('month', today.month))
        base_date = date(year, month, 1)

        cal = calendar.Calendar(firstweekday=6)
        month_weeks = cal.monthdatescalendar(base_date.year, base_date.month)

        notes_in_month = Note.objects.filter(
            user=self.request.user,
            date__year=base_date.year,
            date__month=base_date.month,
        )
        note_map = {note.date: note for note in notes_in_month}

        calendar_weeks = []
        for week in month_weeks:
            week_data = []
            for day in week:
                week_data.append({
                    'date': day,
                    'note': note_map.get(day),
                    'in_month': day.month == base_date.month,
                })
            calendar_weeks.append(week_data)
        
        prev_month = base_date - relativedelta(months=1)
        next_month = base_date + relativedelta(months=1)
        is_current_month = (base_date.year == today.year and base_date.month == today.month)
        current_month = base_date
        return {
            'prev_month': prev_month,
            'next_month': next_month,
            'is_current_month': is_current_month,
            'calendar_weeks': calendar_weeks,
            'current_month': current_month,
        }
    
    def _get_streak_days(self):
        note_dates = set(
            Note.objects.filter(user=self.request.user)
            .values_list('date', flat=True)
        )
        today = date.today()

        if today in note_dates:
            check_date = today
        else:
            check_date = today - timedelta(days=1)
        
        streak = 0
        while check_date in note_dates:
            streak += 1
            check_date -= timedelta(days=1)
        return streak

class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notebook/note_detail.html'
    context_object_name = 'note'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notebook/note_form.html'

    def get_success_url(self):
        return reverse_lazy('notebook:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'ノートを作成する',
            'cancel_url': reverse_lazy('notebook:dashboard'),
            'cancel_text': 'キャンセル',
            'submit_text': '作成する',
        })
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notebook/note_form.html'
    context_object_name = 'note'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'ノートを編集する',
            'cancel_url': reverse_lazy('notebook:detail', kwargs={'pk': self.object.pk}),
            'cancel_text': 'キャンセル',
            'submit_text': '更新する',
        })
        return context
    
    def get_success_url(self):
        return reverse_lazy('notebook:detail', kwargs={'pk': self.object.pk})