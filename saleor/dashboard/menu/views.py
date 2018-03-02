from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.translation import pgettext_lazy

from ...core.utils import get_paginator_items
from ...menu.models import Menu
from ..views import staff_member_required
from .filters import MenuFilter
from .forms import MenuForm


@staff_member_required
@permission_required('menu.view_menu')
def menu_list(request):
    menus = Menu.objects.all()
    menu_filter = MenuFilter(request.GET, queryset=menus)
    menus = get_paginator_items(
        menu_filter.qs, settings.DASHBOARD_PAGINATE_BY,
        request.GET.get('page'))
    ctx = {'menus': menus, 'filter_set': menu_filter,
           'is_empty': not menu_filter.queryset.exists()}
    return TemplateResponse(request, 'dashboard/menu/list.html', ctx)


@staff_member_required
@permission_required('menu.edit_menu')
def menu_create(request):
    menu = Menu()
    form = MenuForm(request.POST or None, instance=menu)
    if form.is_valid():
        menu = form.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Add menu %s') % (menu,)
        messages.success(request, msg)
        return redirect('dashboard:menu-list')
    ctx = {'form': form, 'menu': menu}
    return TemplateResponse(request, 'dashboard/menu/form.html', ctx)
