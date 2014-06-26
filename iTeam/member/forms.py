# coding: utf-8
#
# This file is part of Progdupeupl.
#
# Progdupeupl is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Progdupeupl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Progdupeupl. If not, see <http://www.gnu.org/licenses/>.

from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import (
    Layout, Div, Fieldset, Submit, Field, HTML
)

class LoginForm(forms.Form):

    """Form used for login in users."""

    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=76, widget=forms.PasswordInput)


class RegisterForm(forms.Form):

    """Form used for to register new users."""

    email = forms.EmailField(label=u'Adresse email')
    username = forms.CharField(label=u'Nom d’utilisateur', max_length=30)
    password = forms.CharField(
        label=u'Mot de passe', max_length=76, widget=forms.PasswordInput
    )
    password_confirm = forms.CharField(
        label=u'Confirmation', max_length=76, widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                u'Identifiants',
                Field('username'),
                Field('password'),
                Field('password_confirm'),
                Field('email'),
            ),
            Div(
                Submit('submit', u'Valider mon inscription'),
                HTML(u'<a href="/" class="button secondary">Annuler</a>'),
                css_class='button-group'
            )
        )
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        # Check that the password and it's confirmation match
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if not password_confirm == password:
            msg = u'Les mots de passe sont différents'
            self._errors['password'] = self.error_class([''])
            self._errors['password_confirm'] = self.error_class([msg])

            if 'password' in cleaned_data:
                del cleaned_data['password']

            if 'password_confirm' in cleaned_data:
                del cleaned_data['password_confirm']

        # Check that the user doesn't exist yet
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).count() > 0:
            msg = u'Ce nom d\'utilisateur est déjà utilisé'
            self._errors['username'] = self.error_class([msg])

        return cleaned_data


# update extra information about user

class SettingsForm(forms.Form):
    """Form used to change an user's personnal informations and options."""

    password_new = forms.CharField(
        label=u'Nouveau mot de passe ',
        max_length=76,
        widget=forms.PasswordInput
    )

    password_old = forms.CharField(
        label=u'Mot de passe actuel ',
        max_length=76,
        widget=forms.PasswordInput
    )

    password_confirm = forms.CharField(
        label=u'Confirmer le nouveau mot de passe ',
        max_length=76,
        widget=forms.PasswordInput
    )

    avatar_url = forms.CharField(
        label=u'Avatar',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': u'Lien vers un avatar externe '
                   u'(laisser vide pour utiliser Gravatar).'}
        )
    )


    def __init__(self, user, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.user = user

        # Get initial value form checkbox show email
        initial = kwargs.get('initial', {})
        value_checked = ''

        self.helper.layout = Layout(
            Fieldset(
                u'Changement de mot de passe',
                Field('password_old'),
                Field('password_new'),
                Field('password_confirm'),
                Div(
                    Submit('submit', u'Changer mon mot de passe'),
                    css_class='button-group'
                )
            ),
            Div(
                HTML(u'{% include "misc/editor.part.html" %}'),
                Field('avatar_url'),
                # Inline checkbox is not supported by crispy form
                HTML(
                    u'<div id="div_id_show_email" class="ctrlHolder checkbox"'
                    u'style="padding-top:10px"><label for="id_show_email"> '
                    u'<input id="id_show_email" type="checkbox"'
                    u'class="checkboxinput" name="show_email" {}/> Afficher '
                    u'mon adresse mail publiquement</label></div>'
                    .format(value_checked)),
            ),
            Div(
                Submit('submit', 'Editer mon profil'),
                css_class='button-group'
            )
        )
        super(SettingsForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()

        password_old = cleaned_data.get('password_old')
        password_new = cleaned_data.get('password_new')
        password_confirm = cleaned_data.get('password_confirm')

        # Check if the actual password is not empty
        if password_old:
            user_exist = authenticate(
                username=self.user.username, password=password_old
            )
            if not user_exist and password_old != "":
                self._errors['password_old'] = self.error_class(
                    [u'Mot de passe incorrect.'])
                if 'password_old' in cleaned_data:
                    del cleaned_data['password_old']

        # Check that the password and it's confirmation match
        if not password_confirm == password_new:
            msg = u'Les mots de passe sont différents.'
            self._errors['password_new'] = self.error_class([msg])
            self._errors['password_confirm'] = self.error_class([msg])

            if 'password_new' in cleaned_data:
                del cleaned_data['password_new']

            if 'password_confirm' in cleaned_data:
                del cleaned_data['password_confirm']

        return cleaned_data