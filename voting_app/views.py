from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from voting_app.forms import ClaimForm, VotingForm
from .models import Claim, Voting, Option, Vote
from django.contrib.auth.decorators import login_required


@login_required
def voting_list(request):
    votings = Voting.objects.all()
    return render(request, 'index.html', {'votings': votings})


@login_required
def voting_detail(request, voting_id):
    voting = get_object_or_404(Voting, pk=voting_id)
    options = Option.objects.filter(voting_id=voting)
    existing_votes = Vote.objects.filter(user=request.user, option__voting_id=voting)
    claims = Claim.objects.filter(voting_id=voting)
    voting_type = voting.voting_type
    if request.method == 'POST':
        selected_options_ids = request.POST.getlist('options')
        selected_options = Option.objects.filter(id__in=selected_options_ids)
        if not existing_votes.exists() and selected_options.exists():
            for option in selected_options:
                Vote.objects.create(user=request.user, option=option)
        vote_percents = {}
        votes_summ = 0
        users = []
        for option in options:
            for vote in Vote.objects.filter(option_id=option.id):
                if vote.user not in users:
                    users.append(vote.user)
        for option in options:
            vote_summ = Vote.objects.filter(option_id=option.id).count()
            if len(users) > 0:
                vote_percents[option.id] = int(vote_summ / max(1, len(users)) * 100)
            else:
                vote_percents[option.id] = 0
        return render(request, 'voting.html', {'voting': voting, 'options': options, 'already_voted': 1, 'vote_percents': vote_percents})
    else:
        return render(request, 'voting.html', {'voting': voting, 'options': options, 'already_voted': 0, 'voting_type': voting_type, 'claims': claims})






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
        form = VotingForm(request.POST, request.FILES, request=request)
        voting_type = request.POST['voting_type']
        if form.is_valid():
            form.save()
    else:
        form = VotingForm(request=request)

    context = {'form': form}
    return render(request, 'create_voting.html', context)


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

@login_required
def user_votes(request, user_id):
    user_votes = Vote.objects.filter(user=user_id)
    user_votes_data = list()
    for vote in user_votes:
        option = get_object_or_404(Option, id=vote.option_id)
        voting = get_object_or_404(Voting, id=option.voting_id_id)
        user_votes_data.append({
            'voting_title': voting.title,
            'voting_author': voting.author,
            'option_content': option.content,
        })
    context = {
        'user_votes_data': user_votes_data,
    }
    return render(request, 'user_options_list.html', context)


def create_claim(request, voting_id):
    voting = Voting.objects.get(pk=voting_id)

    if request.method == 'POST':
        form = ClaimForm(request.user, request.POST, initial={'voting': voting})
        if form.is_valid():
            form.user = request.user
            form.save()
            return redirect('voting_list')
    else:
        form = ClaimForm(request.user, initial={'voting': voting})

    return render(request, 'create_claim.html', {'form': form})


def handler404(request, exception):
    return render(request, '404.html', status=404)