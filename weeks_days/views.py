from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic import ListView
from weeks_days.models import Week, Day
from django.shortcuts import redirect
from django.urls import reverse_lazy
from programs.models import Program
import pdb

# WEEK

# Read
class WeekListView(ListView):
  model = Week
  template_name = 'weeks_days/list_week.html'
  context_object_name = 'list_week'
  
  def get_queryset(self):
    queryset = super().get_queryset()
    program_id = self.kwargs['program_id']
    return queryset.filter(program_id=program_id)	

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['program'] = Program.objects.get( id=self.kwargs['program_id'])
      return context
  
def add_week(request, program_id):
   weeks = Week.objects.filter(program_id=program_id)
   if weeks.exists():
      new_week_num = weeks.latest('week').week + 1
   else:
      new_week_num = 1
   
   new_week = Week(program_id=program_id, week=new_week_num)
   new_week.save()

   return redirect('weeks_days:list_week', program_id=program_id)


# DAY

# Read
class DayListView(ListView):
  model = Day
  template_name = 'weeks_days/list_day.html'
  context_object_name = 'list_day'
  
  def get_queryset(self):
    queryset = super().get_queryset()
    week_id = self.kwargs['week_id']
    return queryset.filter(week_id=week_id)	

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['week'] = Week.objects.get( id=self.kwargs['week_id'])
      return context
  
def add_day(request, week_id):
   days = Day.objects.filter(week_id=week_id)
   if days.exists():
      new_day_num = days.latest('day').day + 1
   else:
      new_day_num = 1
   
   new_day = Day(week_id=week_id, day=new_day_num)
   new_day.save()

   return redirect('weeks_days:list_day', week_id=week_id)