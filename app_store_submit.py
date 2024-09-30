import jwt
import requests
import os
import json
from datetime import datetime, timedelta
from time import time, mktime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

# App Store Connect API Key information
app_store_key_id = os.environ['APP_STORE_KEY_ID']
app_store_issuer_id = os.environ['APP_STORE_ISSUER_ID']
app_store_private_key = os.environ['APP_STORE_PRIVATE_KEY']
app_store_app_id = os.environ['APP_STORE_APP_ID']
whats_new_file = os.environ.get('WHATS_NEW_FILE', 'whats_new.txt')

# Google Play Store information
google_play_json_key = os.environ['GOOGLE_PLAY_JSON_KEY']
google_play_package_name = os.environ['GOOGLE_PLAY_PACKAGE_NAME']

def generate_jwt():
    private_key = serialization.load_pem_private_key(
        app_store_private_key.encode(),
        password=None,
        backend=None
    )

    dt = datetime.now() + timedelta(minutes=20)

    header = {
        'alg': 'ES256',
        'kid': app_store_key_id,
        'typ': 'JWT',
    }

    payload = {
        'iss': app_store_issuer_id,
        "iat": int(time()),
        "exp": int(mktime(dt.timetuple())),
        'aud': 'appstoreconnect-v1'
    }

    return jwt.encode(payload, private_key, algorithm='ES256', headers=header)

def make_app_store_api_request(endpoint, method="GET", json_data=None):
    base_url = "https://api.appstoreconnect.apple.com/v1"
    url = f"{base_url}{endpoint}"
    headers = {
        "Authorization": f"Bearer {generate_jwt()}",
        "Content-Type": "application/json"
    }
    response = requests.request(method, url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

def get_latest_app_store_build():
    # Get all builds
    builds_response = make_app_store_api_request(f"/apps/{app_store_app_id}/builds")
    
    if not builds_response['data']:
        raise Exception("No builds found for the app")
    
    # Sort builds by version and uploadedDate
    sorted_builds = sorted(
        builds_response['data'],
        key=lambda x: (x['attributes']['version'], x['attributes']['uploadedDate']),
        reverse=True
    )
    
    # Get the latest build
    latest_build = sorted_builds[0]
    build_id = latest_build['id']
    build_number = latest_build['attributes']['buildNumber']
    version_string = latest_build['attributes']['version']
    

    return build_id, build_number, version_string

def create_app_store_version(build_id, version_string):
    json_data = {
        "data": {
            "type": "appStoreVersions",
            "attributes": {
                "platform": "IOS",
                "versionString": version_string
            },
            "relationships": {
                "app": {"data": {"type": "apps", "id": app_store_app_id}},
                "build": {"data": {"type": "builds", "id": build_id}}
            }
        }
    }
    
    return make_app_store_api_request("/appStoreVersions", method="POST", json_data=json_data)

def update_app_store_version(version_id, whats_new_text):
    json_data = {
        "data": {
            "type": "appStoreVersions",
            "id": version_id,
            "attributes": {
                "releaseNotes": whats_new_text,
                "releaseType": "AFTER_APPROVAL"
            }
        }
    }

    return make_app_store_api_request(f"/appStoreVersions/{version_id}", method="PATCH", json_data=json_data)

def submit_app_store_for_review(version_id):
    json_data = {
        "data": {
            "type": "appStoreVersionSubmissions",
            "relationships": {
                "appStoreVersion": {
                    "data": {
                        "type": "appStoreVersions",
                        "id": version_id
                    }
                }
            }
        }
    }

    return make_app_store_api_request("/appStoreVersionSubmissions", method="POST", json_data=json_data)

def setup_google_play_api():
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(google_play_json_key),
        scopes=['https://www.googleapis.com/auth/androidpublisher']
    )
    return build('androidpublisher', 'v3', credentials=credentials)

def promote_to_google_play_production(service, package_name, whats_new_text):
    edit_request = service.edits().insert(body={}, packageName=package_name)
    result = edit_request.execute()
    edit_id = result['id']

    try:
        track_response = service.edits().tracks().get(
            editId=edit_id,
            track='internal',
            packageName=package_name
        ).execute()
        
        latest_release = track_response['releases'][-1]
        version_code = latest_release['versionCodes'][-1]

        service.edits().tracks().update(
            editId=edit_id,
            track='production',
            packageName=package_name,
            body={
                'releases': [
                    {
                        'versionCodes': [version_code],
                        'status': 'completed',
                        'releaseNotes': [
                            {
                                'language': 'en-US',
                                'text': whats_new_text
                            }
                        ]
                    }
                ]
            }
        ).execute()

        commit_request = service.edits().commit(
            editId=edit_id, packageName=package_name).execute()
        
        print(f"App {package_name} has been promoted to production. Edit ID: {commit_request['id']}")
    except Exception as e:
        print(f"Failed to promote app to production: {str(e)}")
        raise

def main():
    try:
        # Read "What's New" text
        with open(whats_new_file, 'r') as f:
            whats_new_text = f.read().strip()

        # App Store submission
        print("Starting App Store submission process...")
        build_id, build_number, version_string = get_latest_app_store_build()
        print(f"Latest App Store build ID: {build_id}")
        print(f"App Store build number: {build_number}")
        print(f"App Store version string: {version_string}")

        #new_version = create_app_store_version(build_id, version_string)
        #version_id = new_version['data']['id']
        #print(f"Created new App Store version with ID: {version_id}")

        #update_app_store_version(version_id, whats_new_text)
        #print("Updated App Store version with 'What's New' text")

        #submit_app_store_for_review(version_id)
        #print("Submitted to App Store for review successfully")

        # Google Play Store submission
        #print("\nStarting Google Play Store promotion process...")
        #service = setup_google_play_api()
        #promote_to_google_play_production(service, google_play_package_name, whats_new_text)
        #print("Promoted Google Play app to production successfully")

    except Exception as e:
        print(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()