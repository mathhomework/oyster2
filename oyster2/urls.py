from django.conf.urls import patterns, include, url

from django.contrib import admin
from main.forms import AnswerForm, ReviewForm, AnswerForm2, AnswerForm1, AnswerForm3, QuestionForm
from main.views import ReviewWizard

admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', 'main.views.register', name='register'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^profile/(?P<author_id>\w+)/$', 'main.views.profile', name='profile'),

    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

    url(r'^review/$', 'main.views.review', name='review'),
    url(r'^review_form/$', ReviewWizard.as_view([AnswerForm1, AnswerForm2, AnswerForm3, QuestionForm, ReviewForm]), name='review_form'),
    url(r'^archives/$', 'main.views.archives', name='archives'),
    url(r'^subject/(?P<subject_id>\w+)/$', 'main.views.subject', name='subject'),
)
