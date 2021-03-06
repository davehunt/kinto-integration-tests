import configparser
import hashlib
import pytest
import requests

from pytest_testrail.plugin import testrail


@pytest.fixture
def conf():
    config = configparser.ConfigParser()
    config.read('manifest.ini')
    return config


@testrail('C81661')
def test_fennec_dlc_exists(env, conf):
    r = requests.get(conf.get(env, 'font_collection'))
    response = r.json()

    for record in response['data']:
        # Make sure it's a type of record we're expecting
        assert 'kind' in record or 'hyphenation' in record

        # Make sure the file existsZ
        url = "%s/%s" % (conf.get(env, 'cdn'), record['attachment']['location'])
        response = requests.get(url)
        assert int(response.status_code) != 404
        assert len(response.content) > 0

        # Check the file hash matches
        m = hashlib.sha256()
        m.update(response.content)
        assert record['attachment']['hash'] == m.hexdigest()


@testrail('C81662')
def test_fonts_fingerprinting_defenses(env, conf):
    r = requests.get(conf.get(env, 'fingerprinting-defenses'))
    response = r.json()

    if 'error' in response:
        pytest.skip('fingerprinting-defenses/fonts not accessible')

    for record in response['data']:
        assert 'last_modified' in record
        assert 'platforms' in record
        assert 'schema' in record
        assert 'filename' in record['attachment']
        assert 'hash' in record['attachment']


@testrail('C81663')
def test_fonts_fingerprinting_defenses_preview(env, conf):
    r = requests.get(conf.get(env, 'fingerprinting-defenses-preview'))
    response = r.json()

    if 'error' in response:
        pytest.skip('fingerprinting-defenses-preview/fonts not accessible')

    for record in response['data']:
        assert 'last_modified' in record
        assert 'platforms' in record
        assert 'schema' in record
        assert 'filename' in record['attachment']
        assert 'hash' in record['attachment']
