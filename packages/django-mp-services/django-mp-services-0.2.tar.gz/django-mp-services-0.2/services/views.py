
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from pagination import paginate
from basement.admin import render
from invoices.models import Sale

from services.forms import ReportForm, SearchServiceForm
from services.models import ServiceCategory, ServiceItem, Service


@staff_member_required
def print_service_items(request):
    return render(request, 'services/print-service-items.html', {
        'categories': (
            ServiceCategory
                .objects
                .all()
                .prefetch_related('items')
            )
    })


@staff_member_required
def print_services(request, sale_id):

    sale = get_object_or_404(Sale, id=sale_id)

    return render(request, 'services/print-services.html', {
        'sale': sale,
        'services': sale.services.all()
    })


@staff_member_required
def get_report(request):

    form = ReportForm(request)

    services = Service.objects.filter(
        created__date__range=[
            form.cleaned_data['date_from'],
            form.cleaned_data['date_to']
        ]
    ).order_by('created')

    context = {
        'services': services,
        'form': form,
        'totals': {
            'qty': sum([s.qty for s in services]),
            'grand_total': sum([s.subtotal for s in services])
        }
    }

    context.update(form.cleaned_data)

    return render(request, 'services/report.html', context)


@staff_member_required
def get_service_items(request):

    form = SearchServiceForm(data=request.GET)

    if not form.is_valid():
        return HttpResponseBadRequest('Invalid form')

    queryset = ServiceItem.objects.search(**form.cleaned_data)

    page = paginate(request, queryset, per_page=50)

    return JsonResponse({
        'items': render_to_string('services/service-items.html', {
            'page_obj': page
        }),
        'has_next': page.has_next(),
        'next_page_url': '{}?{}'.format(
            request.path, page.next_page_number().querystring)
    })


@csrf_exempt
@require_POST
@staff_member_required
def add_service(request, sale_id):

    sale = get_object_or_404(Sale, id=sale_id)

    service_item = get_object_or_404(
        ServiceItem, id=request.POST.get('service_id'))

    try:
        service = Service.objects.get(
            sale=sale,
            item=service_item
        )
        service.qty += 1
    except Service.DoesNotExist:
        service = Service(
            customer=sale.customer,
            sale=sale,
            item=service_item,
            price=service_item.price
        )

    service.save()

    return JsonResponse({
        'status': 'OK',
        'html': service.render(),
        'item_id': service.id,
        'total': sale.serialize_totals()
    })


@csrf_exempt
@require_POST
@staff_member_required
def remove_service(request, service_id):

    service = get_object_or_404(Service, id=service_id)

    sale = service.sale

    service.delete()

    return JsonResponse({
        'message': _('Service removed'),
        'total': sale.serialize_totals()
    })
