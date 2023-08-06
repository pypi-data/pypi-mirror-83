from django.db.models import Model
from django.http import HttpResponseBadRequest, JsonResponse
from typing import Type

from employee_info.models import CostCenter, Function, WorkPlace


def relation_autocomplete(model: Type[Model], company_code, search_value):
    output = []
    query_set = model.objects.filter(company__companyCode=company_code, value__startswith=search_value)

    for value in query_set:
        output.append({'value': value.value, 'label': '%s %s' % (value.value, value.description)})

    return output


def autocomplete(request, model: Type[Model], limit=1):
    company_code = request.GET.get('company')
    if not company_code:
        return HttpResponseBadRequest('Company must be specified')
    search = request.GET.get('term')
    if search and len(search) >= limit:
        values = relation_autocomplete(model, company_code, search)
        return JsonResponse(values, safe=False)
    else:
        return HttpResponseBadRequest('At least %d characters must be provided' % limit)


def cost_center(request):
    return autocomplete(request, CostCenter, 2)


def function(request):
    return autocomplete(request, Function)


def work_place(request):
    return autocomplete(request, WorkPlace)
