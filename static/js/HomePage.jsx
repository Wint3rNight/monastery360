import { useState } from 'react';

const HomePage = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 py-4 px-8 bg-white/10 backdrop-blur-sm">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 text-orange-500">
              <svg viewBox="0 0 24 24" fill="currentColor" className="w-full h-full">
                <path d="M12 2L3 7V10.5L12 15.5L21 10.5V7L12 2ZM12 4.2L18.4 7.5L12 10.8L5.6 7.5L12 4.2ZM5 9.1L11 12.1V19.9L5 16.9V9.1ZM13 19.9V12.1L19 9.1V16.9L13 19.9Z"/>
                <path d="M12 1L2 6V11L12 16L22 11V6L12 1ZM4 8.5V9.5L12 14L20 9.5V8.5L12 13L4 8.5Z"/>
              </svg>
            </div>
            <div>
              <h1 className="text-white text-xl font-bold">Sikkim Monasteries</h1>
              <p className="text-white/70 text-sm">Heritage & Culture</p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center space-x-8">
            <a href="#" className="flex items-center space-x-2 text-white hover:text-orange-400 transition-colors">
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 9L12 2L21 9V20A2 2 0 0 1 19 22H5A2 2 0 0 1 3 20V9Z"/>
              </svg>
              <span>Home</span>
            </a>
            <a href="#" className="flex items-center space-x-2 text-white hover:text-orange-400 transition-colors">
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M2 12H22"/>
                <path d="M12 2A15.3 15.3 0 0 1 16 12A15.3 15.3 0 0 1 12 22A15.3 15.3 0 0 1 8 12A15.3 15.3 0 0 1 12 2Z"/>
              </svg>
              <span>Virtual Tours</span>
            </a>
            <a href="#" className="flex items-center space-x-2 text-white hover:text-orange-400 transition-colors">
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 10C21 17 12 23 12 23S3 17 3 10A9 9 0 0 1 21 10Z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
              <span>Interactive Map</span>
            </a>
            <a href="#" className="flex items-center space-x-2 text-white hover:text-orange-400 transition-colors">
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M14 2H6A2 2 0 0 0 4 4V20A2 2 0 0 0 6 22H18A2 2 0 0 0 20 20V8L14 2Z"/>
                <polyline points="14,2 14,8 20,8"/>
              </svg>
              <span>Digital Archives</span>
            </a>
            <a href="#" className="flex items-center space-x-2 text-white hover:text-orange-400 transition-colors">
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
              <span>Cultural Calendar</span>
            </a>
          </nav>

          {/* Mobile Menu Button */}
          <button
            onClick={toggleMobileMenu}
            className="lg:hidden text-white"
          >
            <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="3" y1="6" x2="21" y2="6"/>
              <line x1="3" y1="12" x2="21" y2="12"/>
              <line x1="3" y1="18" x2="21" y2="18"/>
            </svg>
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <nav className="lg:hidden mt-4 pt-4 border-t border-white/20">
            <div className="flex flex-col space-y-4">
              <a href="#" className="flex items-center space-x-2 text-white hover:text-orange-400 transition-colors">
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M3 9L12 2L21 9V20A2 2 0 0 1 19 22H5A2 2 0 0 1 3 20V9Z"/>
                </svg>
                <span>Home</span>
              </a>
              <a href="#" className="flex items-center space-x-2 text-white hover:text-orange-400 transition-colors">
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M2 12H22"/>
                  <path d="M12 2A15.3 15.3 0 0 1 16 12A15.3 15.3 0 0 1 12 22A15.3 15.3 0 0 1 8 12A15.3 15.3 0 0 1 12 2Z"/>
                </svg>
                <span>Virtual Tours</span>
              </a>
              <a href="#" className="flex items-center space-x-2 text-white hover:text-orange-400 transition-colors">
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 10C21 17 12 23 12 23S3 17 3 10A9 9 0 0 1 21 10Z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
                <span>Interactive Map</span>
              </a>
              <a href="#" className="flex items-center space-x-2 text-white hover:text-orange-400 transition-colors">
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6A2 2 0 0 0 4 4V20A2 2 0 0 0 6 22H18A2 2 0 0 0 20 20V8L14 2Z"/>
                  <polyline points="14,2 14,8 20,8"/>
                </svg>
                <span>Digital Archives</span>
              </a>
              <a href="#" className="flex items-center space-x-2 text-white hover:text-orange-400 transition-colors">
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
                <span>Cultural Calendar</span>
              </a>
            </div>
          </nav>
        )}
      </header>

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center">
        {/* Background Image */}
        <div className="absolute inset-0">
          <img
            src="https://images.unsplash.com/photo-1594368952328-78a746b5a376?q=80&w=2070&auto=format&fit=crop"
            alt="Monastery in misty mountains"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-black/30"></div>
        </div>

        {/* Content */}
        <div className="relative z-10 text-center px-4 max-w-6xl mx-auto">
          <h1 className="text-4xl md:text-6xl font-extrabold text-white mb-6 leading-tight">
            Discover the Sacred{' '}
            <span className="text-red-400">Monasteries</span>{' '}
            of <span className="text-yellow-400">Sikkim</span>
          </h1>

          <p className="text-lg md:text-xl text-white/90 max-w-2xl mx-auto mb-12 leading-relaxed">
            Immerse yourself in the spiritual heritage of the Himalayas through virtual tours,
            interactive maps, and centuries-old digital archives.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <button className="bg-gradient-to-r from-red-500 to-orange-500 text-white px-8 py-4 rounded-full font-semibold shadow-lg hover:shadow-xl transition-all duration-300 flex items-center space-x-2 group">
              <span>Begin Your Journey</span>
              <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="5" y1="12" x2="19" y2="12"/>
                <polyline points="12,5 19,12 12,19"/>
              </svg>
            </button>

            <button className="bg-white/20 border border-white/30 text-white px-8 py-4 rounded-full font-semibold backdrop-blur-sm hover:bg-white/30 transition-all duration-300 flex items-center space-x-2">
              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="5,3 19,12 5,21"/>
              </svg>
              <span>Watch Introduction</span>
            </button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="absolute bottom-0 left-0 right-0 bg-white/70 backdrop-blur-md p-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Virtual Tours */}
            <div className="text-center">
              <div className="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-12 h-12 text-blue-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M2 12H22"/>
                  <path d="M12 2A15.3 15.3 0 0 1 16 12A15.3 15.3 0 0 1 12 22A15.3 15.3 0 0 1 8 12A15.3 15.3 0 0 1 12 2Z"/>
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Virtual Tours</h3>
              <p className="text-gray-600">360° immersive experiences of sacred spaces</p>
            </div>

            {/* Interactive Maps */}
            <div className="text-center">
              <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-12 h-12 text-green-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 10C21 17 12 23 12 23S3 17 3 10A9 9 0 0 1 21 10Z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Interactive Maps</h3>
              <p className="text-gray-600">Explore locations with detailed information</p>
            </div>

            {/* Digital Archives */}
            <div className="text-center">
              <div className="w-24 h-24 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-12 h-12 text-orange-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6A2 2 0 0 0 4 4V20A2 2 0 0 0 6 22H18A2 2 0 0 0 20 20V8L14 2Z"/>
                  <polyline points="14,2 14,8 20,8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                  <polyline points="10,9 9,9 8,9"/>
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Digital Archives</h3>
              <p className="text-gray-600">Centuries-old manuscripts and artifacts</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
