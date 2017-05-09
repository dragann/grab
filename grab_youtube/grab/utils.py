import datetime
import json
import types
from decimal import *

from django.db.models.fields.files import FieldFile
from django.http import HttpResponse
from django.db import models

from django.db.models import Model
from django.db.models.query import QuerySet
from django.utils.functional import Promise
from django.utils.encoding import smart_unicode, force_unicode
from django.core.serializers.json import DjangoJSONEncoder

# from haystack.models import SearchResult


class ModelJSONEncoder(DjangoJSONEncoder):
    fields = None

    def __init__(self, fields=None, *args, **kwargs):
        self.fields = fields
        super(ModelJSONEncoder, self).__init__(*args, **kwargs)

    """
    (simplejson) DjangoJSONEncoder subclass that knows how to encode fields.

    (adated from django.serializers, which, strangely, didn't
     factor out this part of the algorithm)
    """
    def handle_field(self, obj, field):
        return smart_unicode(getattr(obj, field.name), strings_only=True)

    def handle_fk_field(self, obj, field):
        related = getattr(obj, field.name)
        if related is not None:
            if field.rel.field_name == related._meta.pk.name:
                # Related to remote object via primary key
                related = related._get_pk_val()
            else:
                # Related to remote object via other field
                related = getattr(related, field.rel.field_name)
        return smart_unicode(related, strings_only=True)

    def handle_m2m_field(self, obj, field):
        if field.creates_table:
            return [
                smart_unicode(related._get_pk_val(), strings_only=True)
                for related
                in getattr(obj, field.name).iterator()
                ]


    def handle_list(self, obj_list):
        ret = []
        for obj in obj_list:
            ret.append(self.default(obj))
        return ret

    def handle_dict(self, dict):
        ret = {}
        for k,v in dict.items():
            ret[k] = self.default(v)
        return ret

    def handle_model(self, obj):
        dic = {}
        for field in obj._meta.local_fields:
            if self.fields is not None:
                if field.name not in self.fields:
                    continue
            if field.serialize or field.name in self.fields:
                if field.rel is None:
                    dic[field.name] = self.handle_field(obj, field)
                else:
                    dic[field.name] = self.handle_fk_field(obj, field)
        for field in obj._meta.many_to_many:
            if field.serialize:
                dic[field.name] = self.handle_m2m_field(obj, field)
        return dic

    def default(self, obj):
        # if isinstance(obj, SearchResult):
        #     if obj.object is None:
        #         return None
        #
        #     return {
        #         'post_type': obj.model._meta.model_name,
        #         'title': obj.text,
        #         'slug': obj.slug,
        #         'thumbnail_url': obj.thumbnail_url or obj.avatar_url,
        #         "score": obj.score,
        #         'url': obj.object.get_absolute_url(),
        #     }
        if isinstance(obj, Model):
            return self.handle_model(obj)
        elif type(obj) is types.ListType or isinstance(obj, QuerySet):
            return self.handle_list(obj)
        elif type(obj) is types.DictType:
            self.handle_dict(obj)
        else:
            return super(ModelJSONEncoder, self).default(obj)

# ------------------------------------------------------------------------------
class LazyEncoder(ModelJSONEncoder):
    def default(self, o):
        if isinstance(o, Promise):
            return force_unicode(o)
        else:
            return super(LazyEncoder, self).default(o)




def render_to_json(context, status=None, content_type='application/json'):
    resp = []

    if type(context) is not dict:
        return HttpResponse(parse(context), content_type=content_type)

    for k in context.iterkeys():
        resp.append('%s: %s' % (parse(k), parse(context[k])))

    data = '{%s}' % ','.join(resp)
    return HttpResponse(data, content_type=content_type, status=status)

def parse(data):
    """
    The main issues with django's default json serializer is that properties that
    had been added to a object dynamically are being ignored (and it also has
    problems with some models).
    """

    def _any(data):
        ret = None
        if type(data) is types.ListType:
            ret = _list(data)
        elif type(data) is types.DictType:
            ret = _dict(data)
        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            #ret = str(data)
            ret = float(data)
        elif isinstance(data, models.query.QuerySet):
            # Actually its the same as a list ...
            ret = _list(data)
        elif isinstance(data, models.Model):
            ret = _model(data)
        elif isinstance(data, datetime.date):
            ret = data.isoformat()
#            ret = time.strftime("%Y/%m/%d",data.timetuple())
        elif isinstance(data, FieldFile):
            try:
                ret = data.url
            except ValueError:
                pass
        else:
            ret = data
        return ret

    def _model(data):
        ret = {}
        # If we only have a model, we only want to encode the fields.
        for f in data._meta.fields:
            ret[f.attname] = _any(getattr(data, f.attname))
        # And additionally encode arbitrary properties that had been added.
        fields = dir(data.__class__) + ret.keys()
#        add_ons = [k for k in dir(data) if k not in fields]
        add_ons = [k for k in dir(data) if k not in fields and k not in ('delete', '_state',)]
        for k in add_ons:
            ret[k] = _any(getattr(data, k))
        return ret

    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret

    def _dict(data):
        ret = {}
        for k,v in data.items():
            ret[k] = _any(v)
        return ret

    ret = _any(data)

    return json.dumps(ret, cls=ModelJSONEncoder)