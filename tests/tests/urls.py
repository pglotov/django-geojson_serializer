from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from models import City
from django.contrib.gis.geos import Polygon, GEOSGeometry
from geojson_serializer.serializers import geojson_serializer
import json

@geojson_serializer('location', id='id')
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields =['name', 'location', 'id']


@geojson_serializer('box')
class CitySerializerBox(serializers.ModelSerializer):
    box = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields =['name', 'location', 'box']

    def get_box(self, obj):
        x = obj.location.x
        y = obj.location.y
        return GEOSGeometry(Polygon(((x - 1, y - 1), (x - 1, y + 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y - 1))))


@geojson_serializer('location', id='id', bbox='bbox')
class CitySerializerLocationBox(serializers.ModelSerializer):
    bbox = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields =['name', 'location', 'bbox', 'id']

    def get_bbox(self, obj):
        x = obj.location.x
        y = obj.location.y
        return [x - 1, y - 1, x + 1, y + 1]


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityViewSetBox(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializerBox


class CityViewSetLocationBox(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializerLocationBox


router = routers.DefaultRouter()
router.register(r'cities', CityViewSet)
router.register(r'cities_box', CityViewSetBox)
router.register(r'cities_bbox', CityViewSetLocationBox)


urlpatterns = [
    url(r'^', include(router.urls))
]
