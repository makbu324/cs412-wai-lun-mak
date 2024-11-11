from django.shortcuts import render
from .models import Voter 
from django.views.generic import ListView, DetailView

import plotly
import plotly.graph_objects as go
from datetime import date

# Create your views here.
class VotersListView(ListView):
    '''View to display marathon results'''
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year_selection'] = list(range(1910, 2025))
        context['voter_score'] = list(range(0, 6))
        context['parties'] = ['U ', 'D ', 'R ', 'J ', 'A ', 'CC', 'X ', 'L ', 'Q ', 'S ', 'FF', 'G ', 'HH', 'T ', 'AA', 'GG', 'Z ', 'O ', 'P ', 'E ', 'V ', 'H ', 'Y ', 'W ', 'EE', 'K ']
        
        # input
        context['max_year'] = self.request.GET.get('max_year')
        context['min_year'] = self.request.GET.get('min_year')
        context['vs'] = self.request.GET.get('voter_score')
        context['p'] = self.request.GET.get('parties')
        context['v20state'] = self.request.GET.get('v20state')
        context['v21town'] = self.request.GET.get('v21town')
        context['v21primary'] = self.request.GET.get('v21primary')
        context['v22general'] = self.request.GET.get('v22general')
        context['v23town'] = self.request.GET.get('v23town')

        return context
    
    def get_queryset(self):
        
        # start with entire queryset
        qs = super().get_queryset().order_by('birth_date')
        # filter results by these field(s):
        if 'max_year' in self.request.GET:
            year = self.request.GET['max_year']
            qs=qs.filter(birth_date__year__lte=int(year))

        if 'min_year' in self.request.GET:
            year = self.request.GET['min_year']
            qs=qs.filter(birth_date__year__gte=int(year))

        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if not voter_score == "Any":
                qs=qs.filter(voter_count=int(voter_score))

        if 'parties' in self.request.GET:
            party = self.request.GET['parties']
            s = ""
            if (len(party)==1):
                s = " "
            if not party == "Any":
                qs=qs.filter(party_affiliation=party + s)



        # checkboxes
        if 'v20state' in self.request.GET:
            qs=qs.filter(v20state = True)
        
        if 'v21town' in self.request.GET:
            qs=qs.filter(v21town = True)
        
        if 'v21primary' in self.request.GET:
            qs=qs.filter(v21primary = True)
        
        if 'v22general' in self.request.GET:
            qs=qs.filter(v22general = True)
        
        if 'v23town' in self.request.GET:
            qs=qs.filter(v23town = True)
                
        return qs
        
class VoterView(DetailView):
    model = Voter 
    template_name = 'voter_analytics/show_voter.html'
    context_object_name = 'v'




# OHHHH #
class GraphListView(ListView):
    '''View to display marathon results'''
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year_selection'] = list(range(1910, 2025))
        context['voter_score'] = list(range(0, 6))
        context['parties'] = ['U ', 'D ', 'R ', 'J ', 'A ', 'CC', 'X ', 'L ', 'Q ', 'S ', 'FF', 'G ', 'HH', 'T ', 'AA', 'GG', 'Z ', 'O ', 'P ', 'E ', 'V ', 'H ', 'Y ', 'W ', 'EE', 'K ']
        
        # input
        context['max_year'] = self.request.GET.get('max_year')
        context['min_year'] = self.request.GET.get('min_year')
        context['vs'] = self.request.GET.get('voter_score')
        context['p'] = self.request.GET.get('parties')
        context['v20state'] = self.request.GET.get('v20state')
        context['v21town'] = self.request.GET.get('v21town')
        context['v21primary'] = self.request.GET.get('v21primary')
        context['v22general'] = self.request.GET.get('v22general')
        context['v23town'] = self.request.GET.get('v23town')

        voters = self.get_queryset()
        context['how_many_voters'] = len(voters)

        # Bar Year Distribution
        year_dict = dict()
        for v in voters:
            year = v.birth_date.year
            if not year in year_dict:
                year_dict[year] = 1
            else:
                year_dict[year] += 1
        x = []
        y = []
        for year in year_dict:
            x += [year]
            y += [year_dict[year]]
        
        fig = go.Bar(x=x, y=y)
        bar_div = plotly.offline.plot({'data': [fig]},
                                      auto_open=False,
                                      output_type='div',)
        context['bar_div'] = bar_div


        # Party Distribution
        party_dict = dict()
        for v in voters:
            party = v.party_affiliation
            if not party in party_dict:
                party_dict[party] = 1
            else:
                party_dict[party] += 1
        x_party = []
        y_party = []
        for party in party_dict:
            x_party += [party]
            y_party += [party_dict[party]]
        
        fig = go.Pie(labels=x_party, values=y_party)
        pie_div = plotly.offline.plot({'data': [fig]},
                                      auto_open=False,
                                      output_type='div',)
        context['pie_div'] = pie_div


        # Bar (Vote Count) Distribution
        count_dict = dict()
        count_dict["v20state"] = 0
        count_dict["v21town"] = 0
        count_dict["v21primary"] = 0
        count_dict["v22general"] = 0
        count_dict["v23town"] = 0
        for v in voters:
            if v.v20state:
                count_dict["v20state"] += 1
            if v.v21town:
                count_dict["v21town"] += 1
            if v.v21primary:
                count_dict["v21primary"] += 1
            if v.v22general:
                count_dict["v22general"] += 1
            if v.v23town:
                count_dict["v23town"] += 1
        
        x = []
        y = []
        for count in count_dict:
            x += [count]
            y += [count_dict[count]]
        
        fig = go.Bar(x=x, y=y)
        bar_div_2 = plotly.offline.plot({'data': [fig]},
                                      auto_open=False,
                                      output_type='div',)
        context['bar_div_2'] = bar_div_2



        return context
    
    def get_queryset(self):
        
        # start with entire queryset
        qs = super().get_queryset().order_by('birth_date')
        # filter results by these field(s):
        if 'max_year' in self.request.GET:
            year = self.request.GET['max_year']
            qs=qs.filter(birth_date__year__lte=int(year))

        if 'min_year' in self.request.GET:
            year = self.request.GET['min_year']
            qs=qs.filter(birth_date__year__gte=int(year))

        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if not voter_score == "Any":
                qs=qs.filter(voter_count=int(voter_score))

        if 'parties' in self.request.GET:
            party = self.request.GET['parties']
            s = ""
            if (len(party)==1):
                s = " "
            if not party == "Any":
                qs=qs.filter(party_affiliation=party + s)



        # checkboxes
        if 'v20state' in self.request.GET:
            qs=qs.filter(v20state = True)
        
        if 'v21town' in self.request.GET:
            qs=qs.filter(v21town = True)
        
        if 'v21primary' in self.request.GET:
            qs=qs.filter(v21primary = True)
        
        if 'v22general' in self.request.GET:
            qs=qs.filter(v22general = True)
        
        if 'v23town' in self.request.GET:
            qs=qs.filter(v23town = True)
                
        return qs
    
    