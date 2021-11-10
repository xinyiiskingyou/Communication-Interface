import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, create_channel
from tests.fixture import VALID, ACCESSERROR, INPUTERROR, DEFAULT_IMG_URL

##########################################
##### user_profile_upload_photo tests ####
##########################################

# Input Error: Inavalid token
def test_user_profile_uploadphoto_invalid_token(global_owner):
    invalid_token = global_owner['token']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': invalid_token
    })

    url_test = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"

    upload_photo = requests.post(config.url + 'user/profile/uploadphoto/v1', json = {
        'token': invalid_token,
        'img_url': url_test,
        'x_start': 2,
        'y_start': 2,
        'x_end': 20,
        'y_end': 20,
    })
    assert upload_photo.status_code == ACCESSERROR

# Input Error: img_url returns an HTTP status other then 200
def test_user_profile_uploadphoto_invalid_status(global_owner):
    token = global_owner['token']

    invalid_url = "http://invalid"
    upload_photo = requests.post(config.url + 'user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': invalid_url,
        'x_start': 0,
        'y_start': 0,
        'x_end': 10,
        'y_end': 10,
    })

    assert upload_photo.status_code == INPUTERROR

# Input Error: values outside of call boundary
def test_user_profile_uploadphoto_outside_boundary_big(global_owner):
    token = global_owner['token']

    url_test = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    upload_photo1 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': url_test,
        'x_start': 0,
        'y_start': 0,
        'x_end': 1000,
        'y_end': 1000,
    })
    assert upload_photo1.status_code == INPUTERROR

    upload_photo2 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': url_test,
        'x_start': 1000,
        'y_start': 1000,
        'x_end': 0,
        'y_end': 0,
    })
    assert upload_photo2.status_code == INPUTERROR

# Input Error: values outside of call boundary
def test_user_profile_uploadphoto_outside_boundary_small(global_owner):
    token = global_owner['token']

    url_test = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"

    upload_photo1 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': url_test,
        'x_start': 1,
        'y_start': 1,
        'x_end': -50,
        'y_end': -50,
    })
    assert upload_photo1.status_code == INPUTERROR

    upload_photo2 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': url_test,
        'x_start': -50,
        'y_start': -50,
        'x_end': 1,
        'y_end': 1,
    })
    assert upload_photo2.status_code == INPUTERROR

# Input Error: x_end is smaller then x_start
def test_user_profile_uploadphoto_x_end_smaller(global_owner):
    token = global_owner['token']

    url_test = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"

    upload_photo1 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': url_test,
        'x_start': 10,
        'y_start': 10,
        'x_end': 5,
        'y_end': 20,
    })
    assert upload_photo1.status_code == INPUTERROR

    upload_photo2 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': url_test,
        'x_start': 30,
        'y_start': 20,
        'x_end': 20,
        'y_end': 30,
    })
    assert upload_photo2.status_code == INPUTERROR

# Input Error: y_end is smaller then y_start
def test_user_profile_uploadphoto_y_end_smaller(global_owner):
    token = global_owner['token']

    url_test = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"

    upload_photo1 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': url_test,
        'x_start': 20,
        'y_start': 10,
        'x_end': 30,
        'y_end': 5,
    })
    assert upload_photo1.status_code == INPUTERROR

    upload_photo2 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': url_test,
        'x_start': 30,
        'y_start': 20,
        'x_end': 50,
        'y_end': 3,
    })
    assert upload_photo2.status_code == INPUTERROR

# Input Error: both x and y end are smaller then x and y start
def test_user_profile_uploadphoto_x_and_y_end_smaller(global_owner):
    token = global_owner['token']

    url_test = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"

    upload_photo1 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': url_test,
        'x_start': 20,
        'y_start': 10,
        'x_end': 10,
        'y_end': 5,
    })
    assert upload_photo1.status_code == INPUTERROR

# Input Error: incorrect image type -> not a JPG type of photo
def test_user_profile_uploadphoto_not_jpg(global_owner):
    token = global_owner['token']

    url_test = "http://www.cse.unsw.edu.au/~richardb/index_files/RichardBuckland-VALID.png"

    upload_photo1 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': url_test,
        'x_start': 20,
        'y_start': 10,
        'x_end': 30,
        'y_end': 20,
    })
    assert upload_photo1.status_code == INPUTERROR


###### Implementation ######
def test_user_profile_uploadphoto_valid(global_owner, create_channel):
    token = global_owner['token']

    url_test = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"

    upload_photo1 = requests.post(config.url + 'user/profile/uploadphoto/v1', json = {
        'token': token,
        'img_url': url_test,
        'x_start': 10,
        'y_start': 10,
        'x_end': 20,
        'y_end': 20,
    })
    assert upload_photo1.status_code == VALID

    resp1 = requests.get(config.url + "channel/details/v2", params ={
        'token': token,
        'channel_id': create_channel['channel_id'],
    })
    assert resp1.status_code == VALID

    # the image has successfully updated
    assert json.loads(resp1.text)['owner_members'][0]['profile_img_url'] != DEFAULT_IMG_URL
    assert json.loads(resp1.text)['all_members'][0]['profile_img_url'] != DEFAULT_IMG_URL