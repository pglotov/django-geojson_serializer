from django.test import TestCase
from models import City
from rest_framework.test import APIClient


class TestGeojsonSerializer(TestCase):
    """
    unit tests for geojson_serializer decorator
    """

    def setUp(self):
        self.sf_geojson = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [13.0078125000020002, 42.4234565179379999]
            }, 'properties': {
                'name': 'San Francisco'
            }
        }
        self.client = APIClient()
        self.client.post('/cities/', self.sf_geojson, format='json')

    def test_to_representation(self):
        response = self.client.get('/cities/')
        assert len(response.data) == 1
        data = response.data[0]
        assert data.get('type') == 'Feature'
        assert data.has_key('properties')
        assert data['properties'].has_key('name')
        assert data['properties']['name'] == 'San Francisco'
        assert data.has_key('geometry')
        assert data['geometry'].has_key('type')
        assert data['geometry']['type'] == 'Point'
        assert data['geometry'].has_key('coordinates')
        assert data.has_key('id')

    def test_to_representation_box(self):
        response = self.client.get('/cities_box/')
        assert len(response.data) == 1
        data = response.data[0]
        assert data.get('type') == 'Feature'
        assert data.has_key('properties')
        assert data['properties'].has_key('name')
        assert data['properties']['name'] == 'San Francisco'
        assert data.has_key('geometry')
        assert data['geometry'].has_key('type')
        assert data['geometry']['type'] == 'Polygon'
        assert data['geometry'].has_key('coordinates')

    def test_to_representation_bbox(self):
        response = self.client.get('/cities_bbox/')
        assert len(response.data) == 1
