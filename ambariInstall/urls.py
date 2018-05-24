"""ambariInstall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from . import view


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^mystart/', view.mystart),
    url(r'^input/', view.input),
    url(r'^ambari_install_submit/', view.ambari_install_submit),
    url(r'^ambari_status_query/', view.ambari_status_query),
    url(r'^ambari_install_progress/', view.ambari_install_progress),
    url(r'^install_hdp/', view.ambari_install_progress),
    url(r'^install_agent/', view.ambari_install_progress),
    url(r'^install_server/', view.ambari_install_progress),
    url(r'^query_hdp_log/', view.query_hdp_log),
    url(r'^query_server_log/', view.query_server_log),
    url(r'^query_agents_log/', view.query_agents_log),
    url(r'^query_agent_log/', view.query_agent_log),
    url(r'^$', view.hello),

]
