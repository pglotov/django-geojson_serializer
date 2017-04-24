========================================
django rest framework geojson serializer
========================================

DRF geojson serializer is a decorator which allows to format data as geojson http://geojson.org


Quick start
-------------
Geojson serializer works with django rest framework as a decorator.

1. Add django-geojson_serializer to your INSTALLED_APPS setting like this:
   ::

      INSTALLED_APPS = [
      ....
      'django-geojson_serializer'
      ]

2. In your code you can use :code:`geojson_serializer(<name-of-geo-field>)` decorator with a regualar serializer, e.g.:
   ::

     from geojson_serializer.serializers import geojson_serializer


     class City(models.Model):
         name = models.CharField(max_length=128)
         location = models.PointField()


     @geojson_serializer('location')
     class CitySerializer(serializers.ModelSerializer):
         class Meta:
             model = City
             fields =['name', 'location']


     class CityViewSet(viewsets.ModelViewSet):
         queryset = City.objects.all()
         serializer_class = CitySerializer

   Then you can register CityViewSet with a router and the view will generate and accept geojsons in corresponding requests.

3. Also supported are :code:`id` and :code:`bbox` fields:
   ::
      
      @geojson_serializer('location', id='id', bbox='bounding_box')
      class MySerializer(serializers.ModelSerializer):
      ....

   In this case :code:`'id'` and :code:`'bounding_box'` fields should be defined by the underlying serializer :code:`MySerializer`.



