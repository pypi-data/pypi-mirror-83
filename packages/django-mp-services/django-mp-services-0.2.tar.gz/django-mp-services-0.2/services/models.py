
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from services.managers import ServiceItemManager


class ServiceCategory(models.Model):

    name = models.CharField(_('Category name'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Service category')
        verbose_name_plural = _('Service categories')


class ServiceItem(models.Model):

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Category'))

    name = models.CharField(
        _('Service name'), max_length=255, blank=True, db_index=True)

    code = models.CharField(
        _('Code'), max_length=255, blank=True, db_index=True)

    price = models.FloatField(_('Price'))

    objects = ServiceItemManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('code', )
        verbose_name = _('Service item')
        verbose_name_plural = _('Service items')


class Service(models.Model):

    sale = models.ForeignKey(
        'invoices.Sale',
        on_delete=models.PROTECT,
        related_name='services',
        verbose_name=_('Sale'),
        blank=True,
        null=True
    )

    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.PROTECT,
        related_name='services',
        verbose_name=_('Customer'),
        blank=True,
        null=True
    )

    item = models.ForeignKey(
        ServiceItem,
        on_delete=models.PROTECT,
        verbose_name=_('Service item')
    )

    created = models.DateTimeField(_('Creation date'), auto_now_add=True)

    qty = models.IntegerField(_('Quantity'), default=1)

    price = models.FloatField(_('Price'))

    def __str__(self):
        if self.customer:
            return '{} - {}'.format(self.item.name, self.customer.name)

        return self.item.name

    def render(self):
        return render_to_string('services/item.html', {'object': self})

    @property
    def name(self):
        return self.item.name

    @property
    def code(self):
        return self.item.code

    @property
    def subtotal(self):
        return self.price * self.qty

    @property
    def remove_url(self):
        return reverse_lazy('services:remove-service', args=[self.pk])

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Service')
