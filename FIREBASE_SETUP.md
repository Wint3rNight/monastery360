# Firebase Authentication Setup Guide

## 🚀 Quick Start

Your authentication system is now ready! Here's what I've set up for you:

### ✅ What's Already Done

1. **Beautiful Login/Signup Page**: Located at `http://localhost:8000/login/`
2. **Django Integration**: Views and URLs configured
3. **Environment Variables**: Firebase config in `.env` file
4. **Navigation Integration**: Login button added to all pages
5. **Glass-morphism Design**: Stunning animated UI with React + Tailwind

### 🔥 Firebase Setup (Required)

To make authentication work, you need to:

#### Step 1: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or use existing project
3. Enable Analytics (optional)

#### Step 2: Enable Authentication

1. In Firebase Console, go to **Authentication** → **Sign-in method**
2. Enable **Email/Password** authentication
3. Optionally enable other providers (Google, Facebook, etc.)

#### Step 3: Create Web App

1. Go to **Project Settings** → **General**
2. Click **Add app** → **Web app** (`</>`)
3. Register your app with a name (e.g., "Monastery360")
4. Copy the Firebase configuration object

#### Step 4: Enable Firestore

1. Go to **Firestore Database**
2. Click **Create database**
3. Choose **Start in test mode** (for development)
4. Select your region

#### Step 5: Update Environment Variables

Update your `.env` file with real Firebase credentials:

```env
# Firebase Configuration (Replace with your actual values)
FIREBASE_API_KEY=AIzaSyC...your-api-key
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=123456789
FIREBASE_APP_ID=1:123456789:web:abcdef...
```

### 🎨 Features Included

#### Visual Design

-   **Animated Gradient Background**: Deep indigo → Purple → Pink
-   **Glass-morphism Card**: Blurred background with subtle borders
-   **Floating Orbs**: Dynamic background animations
-   **Smooth Transitions**: Form switching and hover effects

#### Functionality

-   **Login Form**: Email + Password
-   **Signup Form**: Full Name, Username, Email, Phone, Password
-   **State Management**: React hooks for form handling
-   **Error Handling**: Success/error messages
-   **Loading States**: Spinner during authentication
-   **Auto-redirect**: Redirects to home page after successful auth

#### Firebase Integration

-   **Authentication**: Email/password signup and login
-   **Firestore Storage**: User data stored in `users` collection
-   **Environment Config**: Secure credential management

### 🌐 Testing Your Setup

1. **Visit the login page**: `http://localhost:8000/login/`
2. **Test signup**: Create a new account
3. **Test login**: Sign in with created account
4. **Check Firebase**: Verify users appear in Firebase console
5. **Check Firestore**: Confirm user data is stored in `users` collection

### 📱 Navigation Integration

The login button is now available on all pages:

-   **Desktop**: Orange button in top navigation
-   **Mobile**: In the hamburger menu
-   **All Pages**: Home, Tours, Map, Archives, Events

### 🔧 Customization Options

#### Colors & Branding

-   Update gradient colors in the template
-   Modify button colors to match your brand
-   Change logo and text in navigation

#### Form Fields

-   Add/remove fields in signup form
-   Modify validation rules
-   Customize error messages

#### Redirect Behavior

-   Change redirect URL after login/signup
-   Add role-based redirects
-   Implement protected routes

### 🛡️ Security Notes

#### Development

-   Current setup is perfect for development
-   Test mode Firestore allows all reads/writes

#### Production

-   Enable Firestore security rules
-   Set up proper authentication domains
-   Use environment-specific Firebase projects

### 📁 File Structure

```
monastery360/
├── templates/auth/login.html          # Authentication page
├── monastery360/auth_views.py         # Django views
├── monastery360/urls.py               # URL routing
├── .env                               # Environment variables
├── firebase_config.py                 # Firebase config template
└── FIREBASE_SETUP.md                  # This guide
```

### 🎯 Next Steps

1. **Set up Firebase** following steps above
2. **Test authentication** with real credentials
3. **Customize styling** to match your brand
4. **Add protected routes** for authenticated users
5. **Implement user dashboard** for logged-in users

### 🆘 Troubleshooting

#### Firebase Errors

-   Check API key and project ID are correct
-   Ensure authentication is enabled in Firebase console
-   Verify domain is added to authorized domains

#### Template Errors

-   Check Django template syntax
-   Ensure all static files are loading
-   Verify React and Babel are included

#### Network Issues

-   Check Firebase SDK versions
-   Ensure CDN resources are accessible
-   Test internet connectivity

---

**Your authentication system is ready to go! 🎉**

Just add your Firebase credentials and start testing the beautiful login/signup experience.
