from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from tapiriik.web import views
from tapiriik.web.views import privacy

urlpatterns = patterns('',
    url(r'^$', views.dashboard, name='dashboard'),

    url(r'^auth/redirect/(?P<service>[^/]+)$', 'tapiriik.web.views.oauth.authredirect', name='oauth_redirect'),
    url(r'^auth/redirect/(?P<service>[^/]+)/(?P<level>.+)$', 'tapiriik.web.views.oauth.authredirect', name='oauth_redirect'),
    url(r'^auth/return/(?P<service>[^/]+)$', 'tapiriik.web.views.oauth.authreturn', name='oauth_return'),
    url(r'^auth/return/(?P<service>[^/]+)/(?P<level>.+)$', 'tapiriik.web.views.oauth.authreturn', name='oauth_return'),  # django's URL magic couldn't handle the equivalent regex
    url(r'^auth/login/(?P<service>.+)$', views.auth_login, name='auth_simple'),
    url(r'^auth/login-ajax/(?P<service>.+)$', views.auth_login_ajax, name='auth_simple_ajax'),
    url(r'^auth/persist-ajax/(?P<service>.+)$', views.auth_persist_extended_auth_ajax, name='auth_persist_extended_auth_ajax'),
    url(r'^auth/disconnect/(?P<service>.+)$', views.auth_disconnect, name='auth_disconnect'),
    url(r'^auth/disconnect-ajax/(?P<service>.+)$', views.auth_disconnect_ajax, name='auth_disconnect_ajax'),
    url(r'^auth/logout$', views.auth_logout, name='auth_logout'),

    url(r'^account/setemail$', views.account_setemail, name='account_set_email'),
    url(r'^account/settz$', views.account_settimezone, name='account_set_timezone'),
    url(r'^account/configure$', views.account_setconfig, name='account_set_config'),

    url(r'^account/rollback/?$', views.account_rollback_initiate, name='account_rollback_initiate'),
    url(r'^account/rollback/(?P<task_id>.+)$', views.account_rollback_status, name='account_rollback_status'),

    url(r'^rollback$', views.rollback_dashboard, name='rollback_dashboard'),

    url(r'^configure/save/(?P<service>.+)?$', 'tapiriik.web.views.config.config_save', name='config_save'),
    url(r'^configure/dropbox$', 'tapiriik.web.views.config.dropbox', name='dropbox_config'),
    url(r'^configure/flow/save/(?P<service>.+)?$', 'tapiriik.web.views.config.config_flow_save', name='config_flow_save'),
    url(r'^settings/?$', 'tapiriik.web.views.settings.settings', name='settings_panel'),

    url(r'^dropbox/browse-ajax/?$', 'tapiriik.web.views.dropbox.browse', name='dropbox_browse_ajax'),

    url(r'^sync/status$', views.sync_status, name='sync_status'),
    url(r'^sync/activity$', views.sync_recent_activity, name='sync_recent_activity'),
    url(r'^sync/schedule/now$', views.sync_schedule_immediate, name='sync_schedule_immediate'),
    url(r'^sync/errors/(?P<service>[^/]+)/clear/(?P<group>.+)$', views.sync_clear_errorgroup, name='sync_clear_errorgroup'),
    url(r'^sync/bad_activities_acknowledgement_clear$', views.sync_clear_badactivitiesacknowledgement, name='sync_clear_errorgroup'),

    url(r'^activities$', views.activities_dashboard, name='activities_dashboard'),
    url(r'^activities/fetch$', views.activities_fetch_json, name='activities_fetch_json'),

    url(r'^sync/remote_callback/trigger_partial_sync/(?P<service>.+)$', views.sync_trigger_partial_sync_callback, name='sync_trigger_partial_sync_callback'),

    url(r'^diagnostics/$', views.diag_dashboard, name='diagnostics_dashboard'),
    url(r'^diagnostics/queue$', views.diag_queue_dashboard, name='diagnostics_queue_dashboard'),
    url(r'^diagnostics/errors$', views.diag_errors, name='diagnostics_errors'),
    url(r'^diagnostics/error/(?P<error>.+)$', views.diag_error, name='diagnostics_error'),
    url(r'^diagnostics/graphs$', views.diag_graphs, name='diagnostics_graphs'),
    url(r'^diagnostics/user/unsu$', views.diag_unsu, name='diagnostics_unsu'),
    url(r'^diagnostics/user/(?P<user>.+)$', views.diag_user, name='diagnostics_user'),
    url(r'^diagnostics/payments/$', views.diag_payments, name='diagnostics_payments'),
    url(r'^diagnostics/ip$', views.diag_ip, name='diagnostics_ip'),
    url(r'^diagnostics/login$', views.diag_login, name='diagnostics_login'),

    url(r'^supported-activities$', views.supported_activities, name='supported_activities'),
    # url(r'^supported-services-poll$', 'tapiriik.web.views.supported_services_poll', name='supported_services_poll'),

    url(r'^payments/claim$', views.payments_claim, name='payments_claim'),
    url(r'^payments/claim-ajax$', views.payments_claim_ajax, name='payments_claim_ajax'),
    url(r'^payments/promo-claim-ajax$', views.payments_promo_claim_ajax, name='payments_promo_claim_ajax'),
    url(r'^payments/claim-wait-ajax$', views.payments_claim_wait_ajax, name='payments_claim_wait_ajax'),
    url(r'^payments/claim/(?P<code>[a-f0-9]+)$', views.payments_claim_return, name='payments_claim_return'),
    url(r'^payments/return$', views.payments_return, name='payments_return'),
    url(r'^payments/confirmed$', views.payments_confirmed, name='payments_confirmed'),
    url(r'^payments/ipn$', views.payments_ipn, name='payments_ipn'),
    url(r'^payments/external/(?P<provider>[^/]+)/refresh$', views.payments_external_refresh, name='payments_external_refresh'),

    url(r'^ab/begin/(?P<key>[^/]+)$', views.ab_web_experiment_begin, name='ab_web_experiment_begin'),

    url(r'^privacy$', privacy.privacy, name='privacy'),

    url(r'^garmin_connect_users$', TemplateView.as_view(template_name='static/garmin_connect_users.html'), name='garmin_connect_users'),
    url(r'^garmin_connect_bad_data$', TemplateView.as_view(template_name='static/garmin_connect_bad_data.html'), name='garmin_connect_users'),

    url(r'^faq$', TemplateView.as_view(template_name='static/faq.html'), name='faq'),
    url(r'^credits$', TemplateView.as_view(template_name='static/credits.html'), name='credits'),
    url(r'^contact$', TemplateView.as_view(template_name='static/contact.html'), name='contact'),
    # Examples:
    # url(r'^$', 'tapiriik.views.home', name='home'),
    # url(r'^tapiriik/', include('tapiriik.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
