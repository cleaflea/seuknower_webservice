from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'seuknower_webservice.views.home', name='home'),
    # url(r'^seuknower_webservice/', include('seuknower_webservice.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('curriculum_service.views',
    url(r'^seuknower_webservice/curriculum/([\w]+)/([\w-]+)/$', 'parserHtml'),
    url(r'^seuknower_webservice/curriculums/term/$', 'getCurriculumTerm'),
    url(r'^seuknower_webservice/curriculums/([\w]+)/([\w-]+)/$', 'curriculum'),
)

urlpatterns += patterns('tyx_service.views',
  url(r'^seuknower_webservice/tyx/([\w]+)/([\w]+)/$', 'tyxPc'),
  url(r'^seuknower_webservice/tyx/checkAccount/$', 'check_account'),
  url(r'^seuknower_webservice/tyx/test/$', 'test'),
  url(r'^seuknower_webservice/tyx/tyb_broadcast/$', 'get_ren_tyb__broadcast'),
)

urlpatterns += patterns('jwc_service.views',
  url(r'^seuknower_webservice/jwc/$', 'getJwcInfo'),
  url(r'^seuknower_webservice/jwc/more/(\d+)/$', 'getMoreInfo'),
  url(r'^seuknower_webservice/jwc/detaile/(\d+)/$', 'getDetaile'),
  url(r'^seuknower_webservice/jwc/info$', 'getJwcInfor'),
)

urlpatterns += patterns('library_webservice.views',
    # Examples:
    # url(r'^$', 'libsite.views.home', name='home'),
    # url(r'^libsite/', include('libsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^seuknower_webservice/library/instruction/$', 'instruction'),
    url(r'^seuknower_webservice/library/search_book/$', 'search_book'),
    url(r'^seuknower_webservice/library/book_detail/$', 'book_detail'),
    url(r'^seuknower_webservice/library/rendered_books/$', 'check_render_books'),
    url(r'^seuknower_webservice/library/renew/$', 'renew_book'),
    url(r'^seuknower_webservice/library/appointed_books/$', 'check_appointed_books'),
    url(r'^seuknower_webservice/library/appoint_book/$', 'appoint_book'),
    url(r'^seuknower_webservice/library/cancel_appoint/$', 'cancel_appoint'),
    url(r'^seuknower_webservice/library/appoint_info/$', 'appoint_info'),
    url(r'^seuknower_webservice/library/appoint_book/$', 'appoint_book'),
    url(r'^seuknower_webservice/library/check_account/$', 'check_account'),
)