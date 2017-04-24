import json
from django.contrib.gis.geos import GEOSGeometry


def geojson_serializer(geo_field, *args, **kwargs):

    def decorator(Serializer):
        class GeojsonSerializer(Serializer):
            def to_representation(self, instance):
                flat = super(GeojsonSerializer, self).to_representation(instance)
                result = {
                    'type': 'Feature',
                    'geometry': json.loads(GEOSGeometry(flat.pop(geo_field)).geojson),
                    'properties': flat
                }

                id_field = kwargs.get('id')
                if id_field:
                    result['id'] = flat.pop(id_field)

                bbox_field = kwargs.get('bbox')
                if bbox_field:
                    result['bbox'] = flat.pop(bbox_field)

                return result

            def to_internal_value(self, data):
                data.update(data.pop('properties'));
                data.update({geo_field: GEOSGeometry(json.dumps(data.pop('geometry')))})
                return super(GeojsonSerializer, self).to_internal_value(data)

        return GeojsonSerializer

    decorator.geo_field = geo_field
    decorator.args = args
    decorator.kwargs = kwargs

    return decorator
