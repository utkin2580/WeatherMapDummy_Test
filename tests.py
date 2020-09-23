import pytest
import requests
from database import Database

DB = Database()
host = "127.0.0.1"
port = "5000"
api_route = "http://"+host+":"+port+"/api/v1/current"


class TestPositive:
    def test_city_random_positive(self):
        # Checking that request with a city name will get valid data; location is randomly selected
        appid = DB.get_random_appid()
        db_entry = DB.get_random_locations(1)
        city = db_entry[0]['name']
        response = requests.get(api_route+"?city="+city+"&appid="+appid)
        response_body = response.json()
        assert type(response_body) is list
        assert db_entry[0] in response_body  # several cities with the same name might be returned
        assert all(
            DB.is_location_valid(k) for k in response_body)  # checking that all entries in the response are valid
        assert response.status_code == 200

    def test_city_plus_country_random_positive(self):
        # Checking that request with a city name and a country code will get valid data;
        # location is randomly selected
        appid = DB.get_random_appid()
        db_entry = DB.get_random_locations(1)
        city = db_entry[0]['name']
        country = db_entry[0]['country']
        response = requests.get(api_route+"?city="+city+","+country+"&appid="+appid)
        response_body = response.json()
        assert type(response_body) is list
        assert db_entry[0] in response_body  # several cities with the same name might be returned
        assert all(
            DB.is_location_valid(k) for k in response_body)  # checking that all entries in the response are valid
        assert response.status_code == 200

    def test_id_random_positive(self):
        # Checking that request with a city id will get valid data; location is randomly selected
        appid = DB.get_random_appid()
        db_entry = DB.get_random_locations(1)
        id = str(db_entry[0]['id'])
        response = requests.get(api_route+"?id="+id+"&appid="+appid)
        response_body = response.json()
        assert type(response_body) is list
        assert len(response_body) == 1  # id is unique, so only one city should be returned
        assert db_entry[0] == response_body[0]
        assert response.status_code == 200

    def test_lat_lon_random_positive(self):
        # Checking that request with geographic coordinates will get valid data; location is randomly selected
        appid = DB.get_random_appid()
        db_entry = DB.get_random_locations(1)
        lat = str(db_entry[0]['lat'])
        lon = str(db_entry[0]['lon'])
        response = requests.get(api_route+"?lat="+lat+"&lon="+lon+"&appid="+appid)
        response_body = response.json()
        assert type(response_body) is list
        assert len(response_body) == 1  # lat&lon combination is unique, so only one city should be returned
        assert db_entry[0] == response_body[0]
        assert response.status_code == 200

    def test_zip_random_positive(self):
        # Checking that request with a location zip and country code will get valid data;
        # location is randomly selected
        appid = DB.get_random_appid()
        db_entry = DB.get_random_locations(1)
        zip = db_entry[0]['zip']
        country = db_entry[0]['country']
        response = requests.get(api_route+"?zip="+zip+","+country+"&appid="+appid)
        response_body = response.json()
        assert type(response_body) is list
        assert len(response_body) == 1  # zip is unique, so only one city should be returned
        assert db_entry[0] == response_body[0]
        assert response.status_code == 200

    def test_mixed_order_positive(self):
        # Checking that request with mixed order of parameters  will get valid data
        appid = DB.get_random_appid()
        db_entry = DB.get_random_locations(1)
        lat = str(db_entry[0]['lat'])
        lon = str(db_entry[0]['lon'])
        response = requests.get(api_route+"?appid="+appid+"&lon="+lon+"&lat="+lat)
        response_body = response.json()
        assert type(response_body) is list
        assert len(response_body) == 1  # lat&lon combination is unique, so only one city should be returned
        assert db_entry[0] == response_body[0]
        assert response.status_code == 200


class TestEmptyParameters:
    def test_city_empty(self):
        # Checking that request with an empty city name will get "400 Bad Request" response
        appid = DB.get_random_appid()
        response = requests.get(api_route + "?city=&appid=" + appid)
        assert response.status_code == 400

    def test_city_country_code_empty(self):
        # Checking that request with an empty country code along with city name will get "400 Bad Request" response
        appid = DB.get_random_appid()
        db_entry = DB.get_random_locations(1)
        city = db_entry[0]['name']
        response = requests.get(api_route + "?city="+city+",&appid=" + appid)
        assert response.status_code == 400

    def test_id_empty(self):
        # Checking that request with an empty location id will get "400 Bad Request" response
        appid = DB.get_random_appid()
        response = requests.get(api_route + "?id=&appid=" + appid)
        assert response.status_code == 400

    def test_lat_empty(self):
        # Checking that request with an empty latitude will get "400 Bad Request" response
        appid = DB.get_random_appid()
        db_entry = DB.get_random_locations(1)
        lon = str(db_entry[0]['lon'])
        response = requests.get(api_route + "?lat=&lon=" + lon + "&appid=" + appid)
        assert response.status_code == 400

    def test_lon_empty(self):
        # Checking that request with an empty longitude will get "400 Bad Request" response
        appid = DB.get_random_appid()
        db_entry = DB.get_random_locations(1)
        lat = str(db_entry[0]['lat'])
        response = requests.get(api_route + "?lat=" + lat + "&lon=&appid=" + appid)
        assert response.status_code == 400

    def test_zip_n_country_code_empty(self):
        # Checking that request with an empty zip and country code will get "400 Bad Request" response
        appid = DB.get_random_appid()
        response = requests.get(api_route+"?zip=&appid="+appid)
        assert response.status_code == 400

    def test_zip__empty(self):
        # Checking that request with an empty zip but valid country code will get "400 Bad Request" response
        appid = DB.get_random_appid()
        db_entry = DB.get_random_locations(1)
        country = db_entry[0]['country']
        response = requests.get(api_route+"?zip=,"+country+"&appid="+appid)
        assert response.status_code == 400

    def test_country_code_empty(self):
        # Checking that request with a valid zip but empty country code will get "400 Bad Request" response
        appid = DB.get_random_appid()
        db_entry = DB.get_random_locations(1)
        zip = db_entry[0]['zip']
        response = requests.get(api_route+"?zip="+zip+",&appid="+appid)
        assert response.status_code == 400

    def test_appid_empty(self):
        # Checking that request with an empty appid along with city name will get "400 Bad Request" response
        db_entry = DB.get_random_locations(1)
        city = db_entry[0]['name']
        response = requests.get(api_route + "?city="+city+",&appid=")
        assert response.status_code == 400


class TestInvalidValues:
    @pytest.mark.parametrize('country', ('ZZ', 'a1b2c3', '11111', '-3.1415926'))
    def test_invalid_country_code_w_city(self, country):
        # Checking that request with valid city name and invalid country code will get "400 Bad Request" response
        appid = DB.get_random_appid()
        db_entry = DB.get_random_locations(1)
        city = db_entry[0]['name']
        response = requests.get(api_route+"?city="+city+","+country+"&appid="+appid)
        assert response.status_code == 400

    @pytest.mark.parametrize('id', ('-1', '1000000000', 'a1b2c3', '-3.1415926'))
    def test_invalid_id(self, id):
        # Checking that request invalid id will get "400 Bad Request" response
        appid = DB.get_random_appid()
        response = requests.get(api_route+"?id="+id+"&appid="+appid)
        assert response.status_code == 400

    @pytest.mark.parametrize('latlon', (('-90.01', '180.01'), ('90.01', '-180.01'), ('-90.01', '0'),
                                        ('0', '-180.01'), ('a', 'b')))
    def test_invalid_lat_lon(self, latlon):
        # Checking that request invalid lat and/or lon will get "400 Bad Request" response
        appid = DB.get_random_appid()
        lat, lon = latlon
        response = requests.get(api_route+"?lat="+lat+"&lon="+lon+"&appid="+appid)
        assert response.status_code == 400

    @pytest.mark.parametrize('country', ('ZZ', 'a1b2c3', '11', '-3.1415926'))
    def test_invalid_country_cod_w_zip(self, country):
        # Checking that request with valid zip and invalid country code will get "400 Bad Request" response
        appid = DB.get_random_appid()
        db_entry = DB.get_random_locations(1)
        zip = db_entry[0]['zip']
        response = requests.get(api_route+"?zip="+zip+","+country+"&appid="+appid)
        assert response.status_code == 400

    @pytest.mark.parametrize('appid', ('-1', 'A', 'ZZ', '-3.1415926',
                             '1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF'))
    def test_invalid_appid(self, appid):
        # Checking that request with valid zip and invalid appid will get "400 Bad Request" response
        db_entry = DB.get_random_locations(1)
        zip = db_entry[0]['zip']
        country = db_entry[0]['country']
        response = requests.get(api_route+"?zip="+zip+","+country+"&appid="+appid)
        assert response.status_code == 400


class TestNonExistingValues:
    @pytest.mark.parametrize('city', ('AAAAAAA', 'abcdefgh', '11111111'))
    def test_city_non_existing(self, city):
        # Checking that request with a non-existing city name will get empty array
        appid = DB.get_random_appid()
        response = requests.get(api_route+"?city="+city+"&appid="+appid)
        response_body = response.json()
        assert type(response_body) is list
        assert len(response_body) == 0
        assert response.status_code == 200

    @pytest.mark.parametrize('city', ('ZZZZZZZZZZ', 'klmnopqrs', '99999999'))
    def test_city_non_existing_w_country_code(self, city):
        # Checking that request with a non-existing city name and random country code will get empty array
        appid = DB.get_random_appid()
        country_code = DB.get_random_country_code()
        response = requests.get(api_route+"?city="+city+","+country_code+"&appid="+appid)
        response_body = response.json()
        assert type(response_body) is list
        assert len(response_body) == 0
        assert response.status_code == 200

    @pytest.mark.parametrize('id', ('0', '000000001', '99999999'))
    def test_id_non_existing(self, id):
        # Checking that request with a non-existing id will get empty array
        appid = DB.get_random_appid()
        response = requests.get(api_route+"?id="+id+"&appid="+appid)
        response_body = response.json()
        assert type(response_body) is list
        assert len(response_body) == 0
        assert response.status_code == 200

    @pytest.mark.parametrize('latlon', (('0', '0'), ('90.0', '180.0'), ('-90.0', '-180.0')))
    def test_lat_lon_non_existing(self, latlon):
        # Checking that request with a non-existing coordinates will get empty array
        appid = DB.get_random_appid()
        lat, lon = latlon
        response = requests.get(api_route+"?lat="+lat+"&lon="+lon+"&appid="+appid)
        response_body = response.json()
        assert type(response_body) is list
        assert len(response_body) == 0
        assert response.status_code == 200

    @pytest.mark.parametrize('zip', ('XYZ', '00000', 'merry had a little lamb'))
    def test_zip_non_existing(self, zip):
        # Checking that request with a non-existing zip will get empty array
        appid = DB.get_random_appid()
        country = DB.get_random_country_code()
        response = requests.get(api_route+"?zip="+zip+","+country+"&appid="+appid)
        response_body = response.json()
        assert type(response_body) is list
        assert len(response_body) == 0
        assert response.status_code == 200

    @pytest.mark.parametrize('appid', ('aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffff1234',
                                       '0000000000000000000000000000000000000000000000000000000000000000',
                                       'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'))
    def test_app_id(self, appid):
        # Checking that request with a non-existing appid will get 401 Unauthorized
        db_entry = DB.get_random_locations(1)
        lat = str(db_entry[0]['lat'])
        lon = str(db_entry[0]['lon'])
        response = requests.get(api_route+"?appid="+appid+"&lat="+lat+"&lon="+lon)
        assert response.status_code == 401


class TestAbsentParameters:
    def test_city_only(self):
        # Checking that request with a city name only will get "400 Bad Request" response
        db_entry = DB.get_random_locations(1)
        city = db_entry[0]['name']
        response = requests.get(api_route+"?city="+city)
        assert response.status_code == 400

    def test_city_country_code_only(self):
        # Checking that request with a city name and country code only will get "400 Bad Request" response
        db_entry = DB.get_random_locations(1)
        city = db_entry[0]['name']
        country = db_entry[0]['country']
        response = requests.get(api_route+"?city="+city+","+country)
        assert response.status_code == 400

    def test_id_only(self):
        # Checking that request with an id only will get "400 Bad Request" response
        db_entry = DB.get_random_locations(1)
        id = str(db_entry[0]['id'])
        response = requests.get(api_route+"?id="+id)
        assert response.status_code == 400

    def test_lat_only(self):
        # Checking that request with lat only will get "400 Bad Request" response
        db_entry = DB.get_random_locations(1)
        lat = str(db_entry[0]['lat'])
        response = requests.get(api_route+"?lat="+lat)
        assert response.status_code == 400

    def test_lon_only(self):
        # Checking that request with lon only will get "400 Bad Request" response
        db_entry = DB.get_random_locations(1)
        lon = str(db_entry[0]['lon'])
        response = requests.get(api_route+"?lon="+lon)
        assert response.status_code == 400

    def test_lat_lon_only(self):
        # Checking that request with lat and lon only will get "400 Bad Request" response
        db_entry = DB.get_random_locations(1)
        lat = str(db_entry[0]['lat'])
        lon = str(db_entry[0]['lon'])
        response = requests.get(api_route+"?lon="+lon+"&lat="+lat)
        assert response.status_code == 400

    def test_zip_country_code_only(self):
        # Checking that request with lat and lon only will get "400 Bad Request" response
        db_entry = DB.get_random_locations(1)
        zip = db_entry[0]['zip']
        country = db_entry[0]['country']
        response = requests.get(api_route+"?zip="+zip+","+country)
        assert response.status_code == 400

    def test_appid_only(self):
        # Checking that request with appid only will get "400 Bad Request" response
        appid = DB.get_random_appid()
        response = requests.get(api_route+"?appid="+appid)
        assert response.status_code == 400


class TestOtherNegative:
    def test_post_http_method(self):
        # Checking that request using POST HTTP method will get "405 Method Not Allowed"
        appid = DB.get_random_appid()
        db_entry = DB.get_random_locations(1)
        city = db_entry[0]['name']
        response = requests.post(api_route+"?city="+city+"&appid="+appid)
        assert response.status_code == 405

    @pytest.mark.parametrize('api_route_invalid',
                             ("http://"+host+":"+port, "http://"+host+":"+port+"/api/v12345/current"))
    def test_invalid_api_route(self, api_route_invalid):
        # Checking that request with invalid api route will get "404 Not Found"
        appid = DB.get_random_appid()
        db_entry = DB.get_random_locations(1)
        city = db_entry[0]['name']
        response = requests.get(api_route_invalid+"?city="+city+"&appid="+appid)
        assert response.status_code == 404

    def test_unknown_parameter(self):
        # Checking that request with unknown parameter will get "400 Bad Request" response
        appid = DB.get_random_appid()
        db_entry = DB.get_random_locations(1)
        city = db_entry[0]['name']
        response = requests.get(api_route+"?city="+city+"&appid="+appid+"&state=Virginia")
        assert response.status_code == 400

    def test_garbage_instead_of_parameters(self):
        # Checking that request with some garbage instead of parameters will get "400 Bad Request" response
        response = requests.get(api_route+"?a11bs22def")
        assert response.status_code == 400
