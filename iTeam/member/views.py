#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-20 18:26:44
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-10-30 22:14:22

# This file is part of iTeam.org.
# Copyright (C) 2014 Adrien Chardon (Nodraak).
#
# iTeam.org is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# iTeam.org is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with iTeam.org. If not, see <http://www.gnu.org/licenses/>.


from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.views.decorators.debug import sensitive_post_parameters
from django.shortcuts import redirect, render, get_object_or_404

from iTeam.member.models import Profile
from iTeam.member.forms import LoginForm, RegisterForm, SettingsForm
from iTeam.publications.models import Publication
from iTeam.events.models import Event


def index(request):
    members = User.objects.all().order_by('-date_joined')

    paginator = Paginator(members, settings.NB_MEMBERS_PER_PAGE)
    page = request.GET.get('page')

    try:
        shown_members = paginator.page(page)
    except PageNotAnInteger:
        shown_members = paginator.page(1)
    except EmptyPage:
        shown_members = paginator.page(paginator.num_pages)

    return render(request, 'member/index.html', {
        'data': shown_members,
        'members_count': members.count(),
    })


def detail(request, user_name):
    user = get_object_or_404(User, username=user_name)
    profile = get_object_or_404(Profile, user=user)
    profileRequest = None

    # admin actions
    if request.user.is_authenticated():
        profileRequest = get_object_or_404(Profile, user=request.user)

        if profileRequest.is_admin and request.method == 'POST':
            need_redirect = False

            if 'toggle_is_publisher' in request.POST:
                profile.is_publisher = not profile.is_publisher
                profile.save()
                need_redirect = True
            if 'toggle_is_admin' in request.POST:
                profile.is_admin = not profile.is_admin
                profile.is_publisher = profile.is_admin
                profile.save()
                need_redirect = True

            if need_redirect:
                redirect(reverse('member:detail', args=[user_name]))

    c = {
        'profile_detail': profile,
        'profile_request': profileRequest,
    }

    return render(request, 'member/detail.html', c)


@sensitive_post_parameters('password')
def login_view(request):
    csrf_tk = {}
    csrf_tk.update(csrf(request))

    if 'next' in request.GET:
        csrf_tk['next'] = request.GET['next']

    error = False

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                # Yeah auth successful
                if user.is_active:
                    login(request, user)
                    if 'auto_login' not in request.POST:
                        request.session.set_expiry(0)

                    if 'next' in request.GET:
                        return redirect(request.GET['next'])
                    else:
                        return redirect(reverse('iTeam.pages.views.home'))
                else:
                    error = (u'Le compte a été désactivé. Pour toute '
                             u'réclamation, merci de contacter '
                             u'l\'administrateur.')
            else:
                # auth failed
                error = u'Les identifiants fournis ne sont pas valides.'
        else:
            error = (u'Veuillez spécifier votre identifiant '
                     u'et votre mot de passe.')
    else:
        form = LoginForm()

    csrf_tk['error'] = error
    csrf_tk['form'] = form

    return render(request, 'member/login.html', csrf_tk)


@login_required
def logout_view(request):
    # If we got a secure POST, we disconnect
    if request.method == 'POST':
        logout(request)
        request.session.clear()  # clean explicitly stored data about the user
        return redirect(reverse('iTeam.pages.views.home'))
    # Elsewise we ask the user to submit a form with correct csrf token
    else:
        return render(request, 'member/logout.html')


@sensitive_post_parameters('password', 'password_confirm')
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password']
            )

            profile = Profile(user=user)
            profile.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, user)

            return render(request, 'member/register_success.html')
    else:  # method == GET
        form = RegisterForm()
    return render(request, 'member/register.html', {'form': form})


@login_required
@sensitive_post_parameters('password_old', 'password_new', 'password_confirm')
def settings_view(request):
    if request.method == 'POST':
        form = SettingsForm(request.user, request.POST)

        if form.is_valid():
            request.user.set_password(form.cleaned_data['password_new'])
            request.user.save()

            data = {'form': form, 'msg': u'Le mot de passe a bien été modifié.'}
            return render(request, 'member/settings_account.html', data)
    else:
        form = SettingsForm(request.user)

    return render(request, 'member/settings_account.html', {'form': form})


@login_required
def publications(request):
    profile = request.user.profile  # login_required

    if not profile.is_publisher:
        raise PermissionDenied

    publications_all = Publication.objects.all().filter(author=request.user).order_by('-pub_date')
    publications_list = publications_all.filter(is_draft=False)
    drafts_list = publications_all.filter(is_draft=True)

    c = {
        'publications_list': publications_list,
        'drafts_list': drafts_list,
    }

    return render(request, 'member/publications.html', c)


@login_required
def events(request):
    profile = request.user.profile  # login_required

    if not profile.is_publisher:
        raise PermissionDenied

    events_all = Event.objects.all().filter(author=request.user).order_by('-date_start')
    events_list = events_all.filter(is_draft=False)
    drafts_list = events_all.filter(is_draft=True)

    c = {
        'events_list': events_list,
        'drafts_list': drafts_list,
    }

    return render(request, 'member/events.html', c)
