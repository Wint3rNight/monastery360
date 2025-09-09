# Firebase Configuration
# Replace these values with your actual Firebase project configuration
# You can find these values in your Firebase Console:
# 1. Go to Project Settings
# 2. Under "Your apps" section, click on the web app
# 3. Copy the config object

FIREBASE_CONFIG = {
    "apiKey": "your-api-key-here",
    "authDomain": "your-project.firebaseapp.com",
    "projectId": "your-project-id",
    "storageBucket": "your-project.appspot.com",
    "messagingSenderId": "123456789",
    "appId": "your-app-id"
}

# Optional: Firebase Admin SDK configuration for server-side operations
FIREBASE_ADMIN_CONFIG = {
    "type": "service_account",
    "project_id": "your-project-id",
    "private_key_id": "your-private-key-id",
    "private_key": "-----BEGIN PRIVATE KEY-----\nyour-private-key\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com",
    "client_id": "your-client-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40your-project.iam.gserviceaccount.com"
}
