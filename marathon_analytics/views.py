from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Result 

import plotly
import plotly.graph_objects as go


# Create your views here.
class ResultsListView(ListView):
    '''View to display marathon results'''
    template_name = 'marathon_analytics/results.html'
    model = Result
    context_object_name = 'results'
    paginate_by = 50
    
    def get_queryset(self):
        
        # start with entire queryset
        qs = super().get_queryset().order_by('place_overall')
        # filter results by these field(s):
        if 'city' in self.request.GET:
            city = self.request.GET['city']
            qs=Result.objects.filter(city__icontains=city)
                
        return qs 
    

class ResultDetailView(DetailView):
    '''Display a single Result on its own page'''

    template_name = 'marathon_analytics/result_detail.html'
    model = Result
    context_object_name = "r"

    # implement some methods 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r = context['r'] # obtain the single Result instance

        # get data: half-marathon splits
        first_half_seconds = (r.time_half1.hour * 3600 +
                              r.time_half1.minute * 60 +
                              r.time_half1.second)
        
        second_half_seconds = (r.time_half2.hour * 3600 +
                              r.time_half2.minute * 60 +
                              r.time_half2.second)


        # build a pie chart 
        x = ['first half time', 'second half time']
        y = [first_half_seconds, second_half_seconds]
        fig = go.Pie(labels=x,values=y)

        pie_div = plotly.offline.plot({'data':[fig]}, auto_open=False,output_type='div')

        context['pie_div'] = pie_div

        x = [f'runner passed by {r.first_name}',
             f'runner who passed {r.first_name}']
        y = [r.get_runners_passed(),
             r.get_runners_passed_by()]
        
        fig = go.Bar(x=x,y=y)
        bar_div = plotly.offline.plot({'data': [fig]},
                                      auto_open=False,
                                      output_type='div')

        context['bar_div'] = bar_div

        return context


