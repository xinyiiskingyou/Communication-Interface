import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
##### user_profile_upload_photo tests ####
##########################################

# Input Error: Inavalid token
def test_user_profile_uploadphoto_invalid_token():
    invalid_token = global_owner['token']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': invalid_token
    })

    url_test = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    assert user_profile_uploadphoto(invalid_token, url_test, 0, 0, 1000, 1000) == INPUTERROR

# Input Error: img_url returns an HTTP status other then 200
def test_user_profile_uploadphoto_invalid_status(global_owner):
    requests.delete(config.url + "clear/v1")
    token = global_owner['token']

    invalid_url = "http://notvalidurl"
    invalid_case1 = user_profile_uploadphoto(token, invalid_url, 0, 0, 800, 800)

    assert invalid_case1 == INPUTERROR

# Input Error: values outside of call boundary
def test_user_profile_uploadphoto_outside_boundary_big(global_owner):
    requests.delete(config.url + "clear/v1")
    token = global_owner['token']

    # test InputError when index is out of picture
    url_test = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    assert user_profile_uploadphoto(token, url_test, 0, 0, 1000, 1000) == INPUTERROR
    assert user_profile_uploadphoto(token, url_test, 1000, 1000, 0, 0) == INPUTERROR

# Input Error: values outside of call boundary
def test_user_profile_uploadphoto_outside_boundary_small(global_owner):
    requests.delete(config.url + "clear/v1")
    token = global_owner['token']

    # test InputError when index is out of picture
    url_test = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    assert user_profile_uploadphoto(token, url_test, 1, 1, -50, -50) == INPUTERROR
    assert user_profile_uploadphoto(token, url_test, -50, -50, 1, 1) == INPUTERROR

# Input Error: x_end is smaller then x_start
def test_user_profile_uploadphoto_x_end_smaller(global_owner):
    requests.delete(config.url + "clear/v1")
    token = global_owner['token']

    # test InputError when index is out of picture
    url_test = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    assert user_profile_uploadphoto(token, url_test, 10, 10, 5, 20) == INPUTERROR
    assert user_profile_uploadphoto(token, url_test, 30, 20, 20, 30) == INPUTERROR
    assert user_profile_uploadphoto(token, url_test, 50, 10, 1, 20) == INPUTERROR

# Input Error: y_end is smaller then y_start
def test_user_profile_uploadphoto_y_end_smaller(global_owner):
    requests.delete(config.url + "clear/v1")
    token = global_owner['token']

    # test InputError when index is out of picture
    url_test = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    assert user_profile_uploadphoto(token, url_test, 20, 10, 30, 5) == INPUTERROR
    assert user_profile_uploadphoto(token, url_test, 30, 20, 50, 10) == INPUTERROR
    assert user_profile_uploadphoto(token, url_test, 50, 10, 60, 3) == INPUTERROR

# Input Error: both x and y end are smaller then x and y start
def test_user_profile_uploadphoto_y_end_smaller(global_owner):
    requests.delete(config.url + "clear/v1")
    token = global_owner['token']

    # test InputError when index is out of picture
    url_test = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    assert user_profile_uploadphoto(token, url_test, 20, 10, 10, 5) == INPUTERROR

# Input Error: incorrect image type -> not a JPG type of photo
def test_user_profile_uploadphoto_not_jpg(global_owner):
    requests.delete(config.url + "clear/v1")
    token = global_owner['token']

    # test InputError when index is out of picture
    url_test = "http://www.cse.unsw.edu.au/~richardb/index_files/RichardBuckland-200.png"
    assert user_profile_uploadphoto(token, url_test, 20, 10, 30, 20) == INPUTERROR
  