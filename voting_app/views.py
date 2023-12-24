from django.shortcuts import render, get_object_or_404
from .models import Voting, Option, Vote

def voting_list(request):
    votings = Voting.objects.all()
    return render(request, 'index.html', {'votings': votings})

def voting_detail(request, voting_id):
    voting = get_object_or_404(Voting, pk=voting_id)
    options = Option.objects.filter(voting_id=voting)

    if request.method == 'POST':
        selected_option_id = request.POST.get('option')
        selected_option = get_object_or_404(Option, pk=selected_option_id)
        existing_vote = Vote.objects.filter(user=request.user, option__voting_id=voting)
        if existing_vote.exists():
            return render(request, 'already.html')
        Vote.objects.create(user=request.user, option=selected_option)

    return render(request, 'voting.html', {'voting': voting, 'options': options})