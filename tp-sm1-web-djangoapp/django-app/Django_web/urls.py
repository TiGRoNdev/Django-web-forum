"""Django_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from ask.views import home, popular, question, ask, login, signup, signout

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^login/', login, name='login'),
    url(r'^signup/', signup, name='signup'),
    url(r'^question/([^/]+)/', question, name='question'),
    url(r'^ask/', ask, name='ask'),
    url(r'^popular/', popular, name='popular'),
    url(r'^new/', home, name='new'),
    url(r'^signout/', signout, name='signout')
]
