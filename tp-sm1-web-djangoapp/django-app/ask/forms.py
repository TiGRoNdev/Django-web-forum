from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from ask.models import Question, Answer


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=20, initial='Your nickname')
    email = forms.EmailField(initial='example_email@example.com')
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def clean(self):
        cd = self.cleaned_data
        if cd['username'] == 'Your nickname' or cd['email'] == 'example_email@example.com':
            raise forms.ValidationError('In the fields can not contain a default values')
        elif len(cd['password']) < 4:
            raise forms.ValidationError('The "password" field must contain more than 3 characters')
        try:
            if User.objects.get(username=cd['username']) is not None:
                raise forms.ValidationError('Invalid "Username"(Does exist)')
        except User.DoesNotExist:
            return cd

    def save(self):
        cd = self.cleaned_data
        user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
        user = authenticate(username=cd['username'], password=cd['password'])
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, initial='Your nickname')
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def clean(self):
        cd = self.cleaned_data
        try:
            if cd['username'] == 'Your nickname' or cd['password'] == 'DefaultPasswordAboutThinkAbout':
                raise forms.ValidationError('Do not use the default value of "Username"')
        except KeyError:
            raise forms.ValidationError('All fields must be not empty')
        user = authenticate(username=cd['username'], password=cd['password'])
        if user is not None:
            if user.is_active:
                return cd
            else:
                raise forms.ValidationError('Your account is banned')
        else:
            raise forms.ValidationError('Incorrect username/password')

    def save(self):
        cd = self.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password'])
        return user


class AskForm(forms.Form):
    title = forms.CharField(max_length=100, initial='Your Question')
    text = forms.CharField(widget=forms.Textarea)
    author = forms.ModelChoiceField(required=False, queryset=User.objects.all(), widget=forms.HiddenInput)

    def clean(self):
        text = self.cleaned_data['text']
        author = self.cleaned_data['author']
        if author is None:
            raise forms.ValidationError('You must be an authenticated user, please SignIn or Register')
        if len(text) > 1000:
            raise forms.ValidationError('Symbols in text > 1000')
        return self.cleaned_data

    def save(self, user=None):
        question = Question.objects.create_question(self.cleaned_data)
        question.author = user
        question.save()
        return question


def all_choices():
    def get_tuple(obj):
        return (str(obj), str(obj))
    qs = Question.objects.all()
    return tuple(map(get_tuple, qs))


class AnswerForm(forms.Form):
    text = forms.CharField(max_length=600, widget=forms.Textarea, initial='Your answer')
    author = forms.ModelChoiceField(required=False, queryset=User.objects.all(), widget=forms.HiddenInput)

    def save(self, user=None, question_id=None):
        answer = Answer.objects.create_answer(self.cleaned_data)
        answer.author = user
        answer.question = Question.objects.get(id=question_id)
        answer.save()
        return answer
