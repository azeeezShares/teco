from django.shortcuts import render



def home(request):
    context = {
        "details": {
            "title": "Tecoshop - Electric Scooter Workshop"
        }
    }
    return render(request, 'index.html', context=context)