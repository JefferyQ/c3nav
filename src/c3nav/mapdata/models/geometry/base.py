import math
from contextlib import contextmanager

from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from shapely.geometry import Point, box
from shapely.ops import unary_union

from c3nav.mapdata.models.base import SerializableMixin
from c3nav.mapdata.utils.geometry import assert_multipolygon, good_representative_point, smart_mapping
from c3nav.mapdata.utils.json import format_geojson

geometry_affecting_fields = ('height', 'width', 'access_restriction')


class GeometryMixin(SerializableMixin):
    no_orig = False

    """
    A map feature with a geometry
    """
    geometry = None
    import_tag = models.CharField(_('import tag'), null=True, blank=True, max_length=32)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.no_orig:
            self.orig_geometry = None if 'geometry' in self.get_deferred_fields() else self.geometry
            self._orig = {field.attname: (None if field.attname in self.get_deferred_fields()
                                          else getattr(self, field.attname))
                          for field in self._meta.get_fields()
                          if field.name in geometry_affecting_fields}

    @classmethod
    @contextmanager
    def dont_keep_originals(cls):
        # to do: invert this and to no_orig being True by default
        cls.no_orig = True
        yield
        cls.no_orig = False

    def get_geojson_properties(self, *args, **kwargs) -> dict:
        result = {
            'type': self.__class__.__name__.lower(),
            'id': self.id
        }
        if getattr(self, 'bounds', False):
            result['bounds'] = True
        return result

    def to_geojson(self, instance=None) -> dict:
        result = {
            'type': 'Feature',
            'properties': self.get_geojson_properties(instance=instance),
            'geometry': format_geojson(smart_mapping(self.geometry), round=False),
        }
        original_geometry = getattr(self, 'original_geometry', None)
        if original_geometry:
            result['original_geometry'] = format_geojson(smart_mapping(original_geometry), round=False)
        return result

    @classmethod
    def serialize_type(cls, geomtype=True, **kwargs):
        result = super().serialize_type()
        if geomtype:
            result['geomtype'] = cls._meta.get_field('geometry').geomtype
        return result

    @cached_property
    def point(self):
        return good_representative_point(self.geometry)

    def _serialize(self, geometry=True, simple_geometry=False, **kwargs):
        result = super()._serialize(simple_geometry=simple_geometry, **kwargs)
        if geometry:
            result['geometry'] = format_geojson(smart_mapping(self.geometry), round=False)
        if simple_geometry:
            result['point'] = (self.level_id, ) + tuple(round(i, 2) for i in self.point.coords[0])
            if not isinstance(self.geometry, Point):
                minx, miny, maxx, maxy = self.geometry.bounds
                result['bounds'] = ((int(math.floor(minx)), int(math.floor(miny))),
                                    (int(math.ceil(maxx)), int(math.ceil(maxy))))
        return result

    def details_display(self, detailed_geometry=True, **kwargs):
        result = super().details_display(**kwargs)
        result['geometry'] = self.get_geometry(detailed_geometry=detailed_geometry)
        return result

    def get_geometry(self, detailed_geometry=True):
        if detailed_geometry:
            return format_geojson(smart_mapping(self.geometry), round=False)
        return format_geojson(smart_mapping(box(*self.geometry.bounds)), round=False)

    def get_shadow_geojson(self):
        pass

    def contains(self, x, y) -> bool:
        return self.geometry.contains(Point(x, y))

    @property
    def all_geometry_changed(self):
        return any(getattr(self, attname) != value for attname, value in self._orig.items())

    @property
    def geometry_changed(self):
        if self.orig_geometry is None:
            return True
        if self.geometry is self.orig_geometry:
            return False
        if not self.geometry.almost_equals(self.orig_geometry, 1):
            return True
        field = self._meta.get_field('geometry')
        rounded = field.to_python(field.get_prep_value(self.geometry))
        if not rounded.almost_equals(self.orig_geometry, 2):
            return True
        return False

    def get_changed_geometry(self):
        field = self._meta.get_field('geometry')
        new_geometry = field.get_final_value(self.geometry)
        if self.orig_geometry is None:
            return new_geometry
        difference = new_geometry.symmetric_difference(self.orig_geometry)
        if self._meta.get_field('geometry').geomtype in ('polygon', 'multipolygon'):
            difference = unary_union(assert_multipolygon(difference))
        return difference
