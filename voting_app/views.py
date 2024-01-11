from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from voting_app.forms import VotingForm
from .models import Voting, Option, Vote
from django.contrib.auth.decorators import login_required


@login_required
def voting_list(request):
    votings = Voting.objects.all()
    return render(request, 'index.html', {'votings': votings})


@login_required
def voting_detail(request, voting_id):
    voting = get_object_or_404(Voting, pk=voting_id)
    options = Option.objects.filter(voting_id=voting)
    existing_vote = Vote.objects.filter(user=request.user, option__voting_id=voting)
    if request.method == 'POST':
        selected_option_id = request.POST.get('option')
        selected_option = get_object_or_404(Option, pk=selected_option_id)
        vote_percents = []
        options_id = []
        votes_summ = 0
        for option in options:
            vote_summ = 0
            for vote in Vote.objects.filter(option_id=option.id):
                vote_summ += 1
            votes_summ += vote_summ
        for option in options:
            vote_summ = 0
            for vote in Vote.objects.filter(option_id=option.id):
                vote_summ += 1
            vote_percents.append(int(vote_summ / votes_summ * 100))
            options_id.append(option.id)
        vote_percents_rend = dict(zip(options_id, vote_percents))
        if not existing_vote.exists():
            Vote.objects.create(user=request.user, option=selected_option)
            return render(request, 'voting.html', {'voting': voting, 'options': options, 'already_voted': 1, 'vote_percents': vote_percents_rend})
        elif existing_vote.exists():
            return render(request, 'voting.html', {'voting': voting, 'options': options, 'already_voted': 1, 'vote_percents': vote_percents_rend})
    else:
        return render(request, 'voting.html', {'voting': voting, 'options': options, 'already_voted': 0})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('voting_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('voting_list')


def create_voting(request):
    if request.method == 'POST':
        form = VotingForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect('voting_list')
    else:
        form = VotingForm(request=request)
    return render(request, 'create_voting.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('voting_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def edit_voting(request, voting_id):
    voting = get_object_or_404(Voting, pk=voting_id)
    if request.user != voting.author:
        return redirect('voting_list')

    if request.method == 'POST':
        form = VotingForm(request.POST, instance=voting, request=request)
        if form.is_valid():
            form.save()
            return redirect('voting_list')
    else:
        form = VotingForm(instance=voting, request=request)

    return render(request, 'edit.html', {'form': form, 'voting': voting})