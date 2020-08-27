from django.http import Http404
from django.shortcuts import render
from django.views import View
from tours.data import departures, tours


class MainView(View):
    def get(self, request):
        return render(request, 'index.html')


class DepartureView(View):
    def get(self, request, departure):
        if departure not in departures.keys():
            raise Http404
        return render(request, 'departure.html')


class TourView(View):
    def get(self, request, id):
        if id not in tours.keys():
            raise Http404
        return render(request, 'tour.html')
