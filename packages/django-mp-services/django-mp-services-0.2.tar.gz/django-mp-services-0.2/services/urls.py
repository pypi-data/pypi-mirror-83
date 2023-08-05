
from django.urls import path

from services import views

app_name = 'services'


urlpatterns = [

    path('print-services/<int:sale_id>/', views.print_services,
         name='print-services'),

    path('print-service-items/', views.print_service_items,
         name='print-service-items'),

    path('report/', views.get_report, name='report'),

    path('items/', views.get_service_items, name='items'),

    path('<int:sale_id>/add-service/', views.add_service, name='add-service'),

    path('<int:service_id>/remove/', views.remove_service,
         name='remove-service')

]
