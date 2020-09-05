from random import randint

from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views import View

from tours.data import departures, description, subtitle, title, tours


class MainView(View):

    def get(self, request):
        rand_tours = {}
        i = 6
        while i:
            key = randint(1, len(tours))
            if key not in rand_tours:
                rand_tours[key] = tours[key]
                i = i - 1
            # print(rand_tours[key])
        context = {'site_title': title,
                   'tour_title': "",
                   'subtitle': subtitle,
                   'description': description,
                   'departures': departures,
                   'active': 'msk',
                   'rand_tours': rand_tours,
                   }

        return render(request, 'index.html', context=context)


class DepartureView(View):

    def get(self, request, departure):
        if departure not in departures.keys():
            raise Http404
        departure_tours = {key: value for key, value in tours.items() if value['departure'] == departure}
        list_tour = departure_tours.values()
        max_cost = max(list_tour, key=lambda x: x['price'])
        min_cost = min(list_tour, key=lambda x: x['price'])
        max_nights = max(list_tour, key=lambda x: x['nights'])
        min_nights = min(list_tour, key=lambda x: x['nights'])
        context = {'site_title': title,
                   'tour_title': "",
                   'active': departure,
                   'departure': departures[departure],
                   'departure_tours': departure_tours,
                   'tour_count': len(departure_tours),
                   'max_cost': max_cost['price'],
                   'max_nights': max_nights['nights'],
                   'min_cost': min_cost['price'],
                   'min_nights': min_nights['nights'],
                   'departures': departures,
                   }
        print(context['departure'], context['max_cost'], context['min_cost'])
        return render(request, 'departure.html', context=context)


class TourView(View):

    def get(self, request, id):
        if id not in tours.keys():
            raise Http404
        context = {
            'site_title': title,
            'tour_title': tours[id]['title'] + ' ' + tours[id]['stars'] + ' ★',
            'country': tours[id]['country'],
            'departure': departures[tours[id]['departure']],
            'nights': tours[id]['nights'],
            'picture': tours[id]['picture'],
            'description': tours[id]['description'],
            'price': tours[id]['price'],
            'departures': departures,
            'active': 'msk',
        }

        return render(request, 'tour.html', context=context)


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Простите извините!')


def custom_handler500(request):
    return HttpResponseServerError('Ой, что то пошло не так... Простите извините!')
