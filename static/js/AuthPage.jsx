import { initializeApp } from 'firebase/app';
import { createUserWithEmailAndPassword, getAuth, signInWithEmailAndPassword } from 'firebase/auth';
import { doc, getFirestore, setDoc } from 'firebase/firestore';
import { useEffect, useState } from 'react';

// Firebase configuration (replace with your actual config)
const firebaseConfig = {
  apiKey: "your-api-key",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "your-app-id"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// Main App Component
const App = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [isVisible, setIsVisible] = useState(false);

  // Login form state
  const [loginData, setLoginData] = useState({
    email: '',
    password: ''
  });

  // Signup form state
  const [signupData, setSignupData] = useState({
    fullName: '',
    username: '',
    email: '',
    phoneNumber: '',
    password: ''
  });

  // Animate card on mount
  useEffect(() => {
    setIsVisible(true);
  }, []);

  // Clear message when switching forms
  useEffect(() => {
    setMessage('');
  }, [isLogin]);

  // Handle login form submission
  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');

    try {
      const userCredential = await signInWithEmailAndPassword(auth, loginData.email, loginData.password);
      setMessage('Login successful! Welcome back.');
      console.log('User logged in:', userCredential.user);
    } catch (error) {
      setMessage(`Login failed: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle signup form submission
  const handleSignup = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');

    try {
      // Create user with Firebase Auth
      const userCredential = await createUserWithEmailAndPassword(auth, signupData.email, signupData.password);
      const user = userCredential.user;

      // Store additional user data in Firestore
      await setDoc(doc(db, 'users', user.uid), {
        fullName: signupData.fullName,
        username: signupData.username,
        email: signupData.email,
        phoneNumber: signupData.phoneNumber,
        createdAt: new Date(),
        uid: user.uid
      });

      setMessage('Account created successfully! Welcome to our platform.');
      console.log('User created and data stored:', user);
    } catch (error) {
      setMessage(`Signup failed: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle input changes for login form
  const handleLoginChange = (e) => {
    setLoginData({
      ...loginData,
      [e.target.name]: e.target.value
    });
  };

  // Handle input changes for signup form
  const handleSignupChange = (e) => {
    setSignupData({
      ...signupData,
      [e.target.name]: e.target.value
    });
  };

  // Switch between forms
  const toggleForm = () => {
    setIsLogin(!isLogin);
    setMessage('');
  };

  // Login Form Component
  const LoginForm = () => (
    <div className="w-full max-w-md">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-white mb-2">Welcome Back</h2>
        <p className="text-white/70">Sign in to your account</p>
      </div>

      <form onSubmit={handleLogin} className="space-y-6">
        {/* Email Input */}
        <div className="space-y-2">
          <label className="text-white/80 text-sm font-medium block">
            Email Address
          </label>
          <input
            type="email"
            name="email"
            value={loginData.email}
            onChange={handleLoginChange}
            required
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent transition-all duration-300 hover:bg-white/15"
            placeholder="Enter your email"
          />
        </div>

        {/* Password Input */}
        <div className="space-y-2">
          <label className="text-white/80 text-sm font-medium block">
            Password
          </label>
          <input
            type="password"
            name="password"
            value={loginData.password}
            onChange={handleLoginChange}
            required
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent transition-all duration-300 hover:bg-white/15"
            placeholder="Enter your password"
          />
        </div>

        {/* Forgot Password Link */}
        <div className="text-right">
          <a
            href="#"
            className="text-purple-300 hover:text-purple-200 text-sm transition-colors duration-300"
          >
            Forgot password?
          </a>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-purple-500/25 hover:from-purple-500 hover:to-pink-500 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:ring-offset-2 focus:ring-offset-transparent transition-all duration-300 transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        >
          {isLoading ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              Signing In...
            </div>
          ) : (
            'Sign In'
          )}
        </button>

        {/* Toggle to Signup */}
        <div className="text-center">
          <p className="text-white/70">
            Don't have an account?{' '}
            <button
              type="button"
              onClick={toggleForm}
              className="text-purple-300 hover:text-purple-200 font-medium transition-colors duration-300"
            >
              Sign Up
            </button>
          </p>
        </div>
      </form>
    </div>
  );

  // Signup Form Component
  const SignupForm = () => (
    <div className="w-full max-w-md">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-white mb-2">Create Account</h2>
        <p className="text-white/70">Join us today</p>
      </div>

      <form onSubmit={handleSignup} className="space-y-6">
        {/* Full Name Input */}
        <div className="space-y-2">
          <label className="text-white/80 text-sm font-medium block">
            Full Name
          </label>
          <input
            type="text"
            name="fullName"
            value={signupData.fullName}
            onChange={handleSignupChange}
            required
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent transition-all duration-300 hover:bg-white/15"
            placeholder="Enter your full name"
          />
        </div>

        {/* Username Input */}
        <div className="space-y-2">
          <label className="text-white/80 text-sm font-medium block">
            Username
          </label>
          <input
            type="text"
            name="username"
            value={signupData.username}
            onChange={handleSignupChange}
            required
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent transition-all duration-300 hover:bg-white/15"
            placeholder="Choose a username"
          />
        </div>

        {/* Email Input */}
        <div className="space-y-2">
          <label className="text-white/80 text-sm font-medium block">
            Email Address
          </label>
          <input
            type="email"
            name="email"
            value={signupData.email}
            onChange={handleSignupChange}
            required
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent transition-all duration-300 hover:bg-white/15"
            placeholder="Enter your email"
          />
        </div>

        {/* Phone Number Input */}
        <div className="space-y-2">
          <label className="text-white/80 text-sm font-medium block">
            Phone Number
          </label>
          <input
            type="tel"
            name="phoneNumber"
            value={signupData.phoneNumber}
            onChange={handleSignupChange}
            required
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent transition-all duration-300 hover:bg-white/15"
            placeholder="Enter your phone number"
          />
        </div>

        {/* Password Input */}
        <div className="space-y-2">
          <label className="text-white/80 text-sm font-medium block">
            Password
          </label>
          <input
            type="password"
            name="password"
            value={signupData.password}
            onChange={handleSignupChange}
            required
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent transition-all duration-300 hover:bg-white/15"
            placeholder="Create a password"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-purple-500/25 hover:from-purple-500 hover:to-pink-500 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:ring-offset-2 focus:ring-offset-transparent transition-all duration-300 transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        >
          {isLoading ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              Creating Account...
            </div>
          ) : (
            'Create Account'
          )}
        </button>

        {/* Toggle to Login */}
        <div className="text-center">
          <p className="text-white/70">
            Already have an account?{' '}
            <button
              type="button"
              onClick={toggleForm}
              className="text-purple-300 hover:text-purple-200 font-medium transition-colors duration-300"
            >
              Sign In
            </button>
          </p>
        </div>
      </form>
    </div>
  );

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated Gradient Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 animate-gradient-x"></div>

      {/* Animated Background Orbs */}
      <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
      <div className="absolute top-1/3 right-1/4 w-72 h-72 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
      <div className="absolute bottom-1/4 left-1/3 w-72 h-72 bg-indigo-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>

      {/* Main Card */}
      <div
        className={`relative z-10 w-full max-w-md p-8 bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 shadow-2xl transition-all duration-1000 ${
          isVisible
            ? 'opacity-100 scale-100 translate-y-0'
            : 'opacity-0 scale-95 translate-y-4'
        }`}
      >
        {/* Form Content with Animation */}
        <div
          className={`transition-all duration-500 ${
            isLogin ? 'opacity-100' : 'opacity-0'
          }`}
          style={{ display: isLogin ? 'block' : 'none' }}
        >
          <LoginForm />
        </div>

        <div
          className={`transition-all duration-500 ${
            !isLogin ? 'opacity-100' : 'opacity-0'
          }`}
          style={{ display: !isLogin ? 'block' : 'none' }}
        >
          <SignupForm />
        </div>

        {/* Message Display */}
        {message && (
          <div
            className={`mt-4 p-3 rounded-lg text-center text-sm transition-all duration-300 ${
              message.includes('successful') || message.includes('Welcome')
                ? 'bg-green-500/20 text-green-300 border border-green-500/30'
                : 'bg-red-500/20 text-red-300 border border-red-500/30'
            }`}
          >
            {message}
          </div>
        )}
      </div>

      {/* Custom CSS Animations */}
      <style jsx>{`
        @keyframes gradient-x {
          0%, 100% {
            transform: translate(0%, 0%);
          }
          50% {
            transform: translate(-50%, -50%);
          }
        }

        @keyframes blob {
          0% {
            transform: translate(0px, 0px) scale(1);
          }
          33% {
            transform: translate(30px, -50px) scale(1.1);
          }
          66% {
            transform: translate(-20px, 20px) scale(0.9);
          }
          100% {
            transform: translate(0px, 0px) scale(1);
          }
        }

        .animate-gradient-x {
          animation: gradient-x 15s ease infinite;
          background-size: 400% 400%;
        }

        .animate-blob {
          animation: blob 7s infinite;
        }

        .animation-delay-2000 {
          animation-delay: 2s;
        }

        .animation-delay-4000 {
          animation-delay: 4s;
        }
      `}</style>
    </div>
  );
};

export default App;
