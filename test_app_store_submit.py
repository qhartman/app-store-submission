import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import os

# mock values of env values for testing locally
os.environ['APP_STORE_KEY_ID'] = 'dummy_key_id'
os.environ['APP_STORE_ISSUER_ID'] = 'dummy_issuer_id'
os.environ['APP_STORE_APP_ID'] = 'dummy_app_id'
os.environ['GOOGLE_PLAY_JSON_KEY'] = json.dumps({"type": "service_account", "project_id": "dummy_project"})
os.environ['GOOGLE_PLAY_PACKAGE_NAME'] = 'com.example.app'

from app_store_submit import (
    generate_jwt,
    make_app_store_api_request,
    get_latest_app_store_build,
    create_app_store_version,
    update_app_store_version,
    submit_app_store_for_review,
    setup_google_play_api,
    promote_to_google_play_production,
    main
)

class TestAppStoreSubmit(unittest.TestCase):

    @patch('app_store_submit.jwt.encode')
    @patch('app_store_submit.serialization.load_pem_private_key')
    def test_generate_jwt(self, mock_load_key, mock_encode):
        mock_load_key.return_value = "mock_key"
        mock_encode.return_value = "mock_jwt_token"
        
        result = generate_jwt()
        
        self.assertEqual(result, "mock_jwt_token")
        mock_load_key.assert_called_once()
        mock_encode.assert_called_once()

    @patch('app_store_submit.requests.request')
    def test_make_app_store_api_request(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "mock_data"}
        mock_request.return_value = mock_response
        
        result = make_app_store_api_request("/test_endpoint")
        
        self.assertEqual(result, {"data": "mock_data"})
        mock_request.assert_called_once()

    @patch('app_store_submit.make_app_store_api_request')
    def test_get_latest_app_store_build(self, mock_api_request):
        mock_api_request.return_value = {
            "data": [{"id": "build_id", "attributes": {"version": "1.0"}}],
            "included": [{"type": "buildBundles", "attributes": {"cfBundleShortVersionString": "1.0.0"}}]
        }
        
        build_id, version_string, bundle_version = get_latest_app_store_build()
        
        self.assertEqual(build_id, "build_id")
        self.assertEqual(version_string, "1.0")
        self.assertEqual(bundle_version, "1.0.0")

    @patch('app_store_submit.make_app_store_api_request')
    def test_create_app_store_version(self, mock_api_request):
        mock_api_request.return_value = {"data": {"id": "version_id"}}
        
        result = create_app_store_version("build_id", "1.0")
        
        self.assertEqual(result, {"data": {"id": "version_id"}})
        mock_api_request.assert_called_once()

    @patch('app_store_submit.make_app_store_api_request')
    def test_update_app_store_version(self, mock_api_request):
        mock_api_request.return_value = {"data": {"id": "version_id", "attributes": {"releaseNotes": "New features"}}}
        
        result = update_app_store_version("version_id", "New features")
        
        self.assertEqual(result["data"]["attributes"]["releaseNotes"], "New features")
        mock_api_request.assert_called_once()

    @patch('app_store_submit.make_app_store_api_request')
    def test_submit_app_store_for_review(self, mock_api_request):
        mock_api_request.return_value = {"data": {"id": "submission_id"}}
        
        result = submit_app_store_for_review("version_id")
        
        self.assertEqual(result, {"data": {"id": "submission_id"}})
        mock_api_request.assert_called_once()

    @patch('app_store_submit.service_account.Credentials.from_service_account_info')
    @patch('app_store_submit.build')
    def test_setup_google_play_api(self, mock_build, mock_credentials):
        mock_credentials.return_value = "mock_credentials"
        mock_build.return_value = "mock_service"

        result = setup_google_play_api()

        self.assertEqual(result, "mock_service")
        mock_credentials.assert_called_once()
        mock_build.assert_called_once_with('androidpublisher', 'v3', credentials="mock_credentials")

    @patch('app_store_submit.setup_google_play_api')
    def test_promote_to_google_play_production(self, mock_setup_api):
        mock_service = MagicMock()
        mock_setup_api.return_value = mock_service

        mock_edit = MagicMock()
        mock_edit.insert().execute.return_value = {"id": "edit_id"}
        mock_service.edits.return_value = mock_edit

        mock_track = MagicMock()
        mock_track.get().execute.return_value = {
            "releases": [{"versionCodes": ["12345"]}]
        }
        mock_edit.tracks.return_value = mock_track

        promote_to_google_play_production(mock_service, "com.example.app", "New features")

        mock_setup_api.assert_called_once()
        mock_edit.insert.assert_called_once()
        mock_track.get.assert_called_once()
        mock_track.update.assert_called_once()
        mock_edit.commit.assert_called_once()

    @patch('app_store_submit.get_latest_app_store_build')
    @patch('app_store_submit.create_app_store_version')
    @patch('app_store_submit.update_app_store_version')
    @patch('app_store_submit.submit_app_store_for_review')
    @patch('app_store_submit.setup_google_play_api')
    @patch('app_store_submit.promote_to_google_play_production')
    @patch('builtins.open', new_callable=mock_open, read_data="New features")
    def test_main(self, mock_file, mock_promote, mock_setup_google, mock_submit, mock_update, mock_create, mock_get_build):
        mock_get_build.return_value = ("build_id", "1.0", "1.0.0")
        mock_create.return_value = {"data": {"id": "version_id"}}
        mock_setup_google.return_value = "mock_service"
        
        main()
        
        mock_file.assert_called_once_with('whats_new.txt', 'r')
        mock_get_build.assert_called_once()
        mock_create.assert_called_once()
        mock_update.assert_called_once()
        mock_submit.assert_called_once()
        mock_setup_google.assert_called_once()
        mock_promote.assert_called_once_with("mock_service", "com.example.app", "New features")

if __name__ == '__main__':
    unittest.main()