## This action is still a WIP. Please do not use it unless you are prepared to find and fix issues.

# App Store and Google Play Store Submission Action

This GitHub Action automates the process of submitting your latest TestFlight build to App Store Review and promoting your internal testing build to production on Google Play Store. It simplifies the app submission workflow, allowing you to integrate app submissions directly into your CI/CD pipeline for both iOS and Android platforms.

## Features

- Retrieves the latest build from TestFlight and submits it for App Store Review
- Updates the "What's New" text for the new App Store version
- Promotes the latest internal testing build to production on Google Play Store

## Prerequisites

Before you can use this action, you need to set up the following:

1. An App Store Connect API Key (Key ID, Issuer ID, and .p8 file)
2. Your iOS App's Apple ID
3. A file containing the "What's New" text for your app update
4. A Google Play Service Account JSON key with the necessary permissions
5. Your Android app's package name

### Obtaining an App Store Connect API Key

1. Log in to [App Store Connect](https://appstoreconnect.apple.com/).
2. Go to "Users and Access" and then click on the "Keys" tab.
3. Click the "+" button to create a new key.
4. Give your key a name and select the appropriate access permissions.
5. Click "Generate" and immediately download the generated .p8 file (you won't be able to download it again).
6. Note down the Key ID and the Issuer ID (visible at the top of the keys page).

### Obtaining a Google Play Service Account JSON Key

1. Go to the [Google Play Console](https://play.google.com/console/) as the account holder.
2. Navigate to Setup > API Access.
3. Click on "Create new service account".
4. Follow the link to the Google Cloud Platform.
5. In the GCP Console, go to IAM & Admin > Service Accounts.
6. Click "Create Service Account".
7. Give it a name and click "Create".
8. For the role, choose "Basic" > "Editor".
9. Click "Continue" and then "Done".
10. On the Service Accounts page, find the account you just created and click on the three dots menu > "Manage keys".
11. Click "Add Key" > "Create new key". Choose JSON as the key type.
12. A JSON file will be downloaded. Keep this file secure.
13. Back in the Play Console, click "Grant Access" for the newly created service account.
14. Choose the appropriate permissions for this service account.
## Usage

To use this action in your workflow, add the following step:

```yaml
- name: Submit to App Stores
  uses: yourusername/app-store-submit-action@v2.0.0
  with:
    app_store_key_id: ${{ secrets.APP_STORE_CONNECT_KEY_ID }}
    app_store_issuer_id: ${{ secrets.APP_STORE_CONNECT_ISSUER_ID }}
    app_store_private_key: ${{ secrets.APP_STORE_CONNECT_PRIVATE_KEY }}
    app_store_app_id: ${{ secrets.APP_STORE_APP_ID }}
    whats_new_file: 'path/to/whats_new.txt'
    google_play_json_key: ${{ secrets.GOOGLE_PLAY_JSON_KEY }}
    google_play_package_name: ${{ secrets.GOOGLE_PLAY_PACKAGE_NAME }}
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `app_store_key_id` | App Store Connect API Key ID | Yes | N/A |
| `app_store_issuer_id` | App Store Connect API Issuer ID | Yes | N/A |
| `app_store_private_key` | App Store Connect API Private Key (.p8 file contents) | Yes | N/A |
| `app_store_app_id` | Your app's Apple ID in App Store Connect | Yes | N/A |
| `whats_new_file` | Path to the file containing "What's New" text | No | `whats_new.txt` |
| `google_play_json_key` | Google Play Service Account JSON key | Yes | N/A |
| `google_play_package_name` | Your app's package name on Google Play | Yes | N/A |

## Setting Up Secrets

For security, it's crucial to store your API credentials as GitHub secrets. Here's how to set them up:

1. In your GitHub repository, go to Settings > Secrets > Actions.
2. Add the following secrets:
   - `APP_STORE_CONNECT_KEY_ID`: Your App Store Connect API Key ID
   - `APP_STORE_CONNECT_ISSUER_ID`: Your App Store Connect API Issuer ID
   - `APP_STORE_CONNECT_PRIVATE_KEY`: The contents of your .p8 private key file
   - `APP_STORE_APP_ID`: Your app's Apple ID in App Store Connect
   - `GOOGLE_PLAY_JSON_KEY`: Your Google Play Service Account JSON key (entire contents of the JSON file)
   - `GOOGLE_PLAY_PACKAGE_NAME`: Your app's package name on Google Play

## Example Workflow

Here's an example of a complete workflow file that uses this action:

```yaml
name: Submit to App Stores

on:
  workflow_dispatch:  # Allows manual triggering

jobs:
  submit_to_app_stores:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Submit to App Stores
      uses: yourusername/app-store-submit-action@v2.0.0
      with:
        app_store_key_id: ${{ secrets.APP_STORE_CONNECT_KEY_ID }}
        app_store_issuer_id: ${{ secrets.APP_STORE_CONNECT_ISSUER_ID }}
        app_store_private_key: ${{ secrets.APP_STORE_CONNECT_PRIVATE_KEY }}
        app_store_app_id: ${{ secrets.APP_STORE_APP_ID }}
        whats_new_file: 'path/to/whats_new.txt'
        google_play_json_key: ${{ secrets.GOOGLE_PLAY_JSON_KEY }}
        google_play_package_name: ${{ secrets.GOOGLE_PLAY_PACKAGE_NAME }}
```

## Important Notes

- Ensure that you have a build in TestFlight ready for submission before running this action for iOS.
- Make sure you have an internal testing build ready for promotion on Google Play for Android.
- The "What's New" text file should be committed to your repository or generated as part of your build process.
- This action assumes you're submitting an iOS app to the App Store and an Android app to Google Play. If you're only targeting one platform, you can omit the irrelevant inputs.

## Contributing

We welcome contributions to improve this action! Please see our [Contributing Guide](CONTRIBUTING.md) for more information on how to get started. Whether you're fixing bugs, improving documentation, or proposing new features, your efforts are appreciated.

## Troubleshooting

If you encounter any issues:

1. Check that all required secrets are correctly set in your repository.
2. Ensure your App Store Connect API Key and Google Play Service Account have the necessary permissions.
3. Verify that you have valid builds ready for submission/promotion on both platforms.
4. Check the action logs for any error messages or unexpected behavior.

If you're still having trouble, please open an issue in this repository with a detailed description of the problem, including any relevant logs or error messages.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
