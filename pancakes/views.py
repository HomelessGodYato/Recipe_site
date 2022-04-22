from django.shortcuts import render


def home_page(request):
    context = {"recipes": ['pancakes', 'donuts']}
    return render(request, 'home.html', context)
