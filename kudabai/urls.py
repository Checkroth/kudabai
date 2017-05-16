"""kudabai URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
import fruits.views
import sales.views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^top/', fruits.views.mgmt_top, name='top'),
    url(r'^$', fruits.views.mgmt_top),
    url(r'^master/', fruits.views.master, name='master'),
    url(r'^addfruit/', fruits.views.add_fruit, name='add_fruit'),
    url(r'^editfruit/(?P<fruit_id>[0-9]+)/$', fruits.views.edit_fruit, name='edit_fruit'),
    url(r'^deletefruit/(?P<fruit_id>[0-9]+)/$', fruits.views.del_fruit, name='delete_fruit'),
    url(r'^sales/', sales.views.show_sales, name='show_sales'),
    url(r'^addsale/', sales.views.add_sale, name='add_sale'),
    url(r'^editsales/(?P<sale_id>[0-9]+)/$', sales.views.edit_sale, name='edit_sale'),
    url(r'^deletesale/(?P<sale_id>[0-9]+)/$', sales.views.del_sale, name='delete_sale'),
    url(r'^bulkadd/', sales.views.bulk_add_sale, name='bulk_add_sale'),
    url(r'^salesstats/', sales.views.sales_stats, name='sales_stats'),
    url(r'^login/', auth_views.login, name='login'),
]
