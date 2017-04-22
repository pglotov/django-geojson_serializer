"""tests URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from models import City
from django.contrib.gis.geos import Polygon, GEOSGeometry
from geojson_serializer.serializers import geojson_serializer
import json

@geojson_serializer('location')
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields =['name', 'location']


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


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class CityViewSetBox(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializerBox


router = routers.DefaultRouter()
router.register(r'cities', CityViewSet)
router.register(r'cities_box', CityViewSetBox)

urlpatterns = [
    url(r'^', include(router.urls))
]
