# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Order'
        db.create_table(u'order_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='checkout', max_length=32)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('last_status_change', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('billing_first_name', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('billing_last_name', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('billing_company_name', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('billing_street_address_1', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('billing_street_address_2', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('billing_city', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('billing_postal_code', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('billing_country', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('billing_country_area', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('billing_tax_id', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('billing_phone', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('payment_type_name', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('payment_type_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('payment_price', self.gf('django_prices.models.PriceField')(default=0, currency='USD', max_digits=12, decimal_places=4)),
            ('token', self.gf('django.db.models.fields.CharField')(default='', max_length=36, blank=True)),
        ))
        db.send_create_signal(u'order', ['Order'])

        # Adding model 'DeliveryGroup'
        db.create_table(u'order_deliverygroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='groups', to=orm['order.Order'])),
            ('delivery_price', self.gf('django_prices.models.PriceField')(default=0, currency='USD', max_digits=12, decimal_places=4)),
            ('delivery_type', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('delivery_type_name', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('delivery_type_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('require_shipping_address', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('shipping_first_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('shipping_last_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('shipping_company_name', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('shipping_street_address_1', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('shipping_street_address_2', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('shipping_city', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('shipping_postal_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('shipping_country', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('shipping_country_area', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('shipping_phone', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal(u'order', ['DeliveryGroup'])

        # Adding model 'OrderedItem'
        db.create_table(u'order_ordereditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('delivery_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['order.DeliveryGroup'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, on_delete=models.SET_NULL, to=orm['product.Product'])),
            ('product_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('quantity', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('unit_price_net', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=4)),
            ('unit_price_gross', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=4)),
        ))
        db.send_create_signal(u'order', ['OrderedItem'])


    def backwards(self, orm):
        # Deleting model 'Order'
        db.delete_table(u'order_order')

        # Deleting model 'DeliveryGroup'
        db.delete_table(u'order_deliverygroup')

        # Deleting model 'OrderedItem'
        db.delete_table(u'order_ordereditem')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'order.deliverygroup': {
            'Meta': {'object_name': 'DeliveryGroup'},
            'delivery_price': ('django_prices.models.PriceField', [], {'default': '0', 'currency': "'USD'", 'max_digits': '12', 'decimal_places': '4'}),
            'delivery_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'delivery_type_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'delivery_type_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groups'", 'to': u"orm['order.Order']"}),
            'require_shipping_address': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shipping_city': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'shipping_company_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'shipping_country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'shipping_country_area': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'shipping_first_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'shipping_last_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'shipping_phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'shipping_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'shipping_street_address_1': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'shipping_street_address_2': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        u'order.order': {
            'Meta': {'ordering': "('-last_status_change',)", 'object_name': 'Order'},
            'billing_city': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'billing_company_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'billing_country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'billing_country_area': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'billing_first_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'billing_last_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'billing_phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'billing_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'billing_street_address_1': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'billing_street_address_2': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'billing_tax_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_status_change': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'payment_price': ('django_prices.models.PriceField', [], {'default': '0', 'currency': "'USD'", 'max_digits': '12', 'decimal_places': '4'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'payment_type_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'payment_type_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'checkout'", 'max_length': '32'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '36', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'order.ordereditem': {
            'Meta': {'object_name': 'OrderedItem'},
            'delivery_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['order.DeliveryGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['product.Product']"}),
            'product_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'unit_price_gross': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            'unit_price_net': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'})
        },
        u'product.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['product.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'product.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': u"orm['product.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'price': ('django_prices.models.PriceField', [], {'currency': "'USD'", 'max_digits': '12', 'decimal_places': '4'}),
            'stock': ('django.db.models.fields.DecimalField', [], {'default': "'1'", 'max_digits': '10', 'decimal_places': '4'}),
            'subtype_attr': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['order']