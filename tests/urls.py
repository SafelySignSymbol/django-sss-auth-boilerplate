# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.urls import path, include


urlpatterns = [
    path(r'^', include('web3auth.urls', namespace='web3auth')),
]
