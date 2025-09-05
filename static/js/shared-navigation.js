// Shared Navigation Component for Sikkim Monasteries
// This component should be included in all pages to maintain consistency

const SharedNavigation = ({ currentPage = "", theme = "dark" }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Navigation items with their routes and icons
  const navItems = [
    {
      name: "Home",
      href: "/",
      icon: (
        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M3 9L12 2L21 9V20A2 2 0 0 1 19 22H5A2 2 0 0 1 3 20V9Z"/>
        </svg>
      )
    },
    {
      name: "Virtual Tours",
      href: "/tours/",
      icon: (
        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="10"/>
          <path d="M2 12H22"/>
          <path d="M12 2A15.3 15.3 0 0 1 16 12A15.3 15.3 0 0 1 12 22A15.3 15.3 0 0 1 8 12A15.3 15.3 0 0 1 12 2Z"/>
        </svg>
      )
    },
    {
      name: "Interactive Map",
      href: "/monasteries/map/",
      icon: (
        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M21 10C21 17 12 23 12 23S3 17 3 10A9 9 0 0 1 21 10Z"/>
          <circle cx="12" cy="10" r="3"/>
        </svg>
      )
    },
    {
      name: "Digital Archives",
      href: "/archives/portal/",
      icon: (
        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M14 2H6A2 2 0 0 0 4 4V20A2 2 0 0 0 6 22H18A2 2 0 0 0 20 20V8L14 2Z"/>
          <polyline points="14,2 14,8 20,8"/>
        </svg>
      )
    },
    {
      name: "Cultural Calendar",
      href: "/events/",
      icon: (
        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
          <line x1="16" y1="2" x2="16" y2="6"/>
          <line x1="8" y1="2" x2="8" y2="6"/>
          <line x1="3" y1="10" x2="21" y2="10"/>
        </svg>
      )
    }
  ];

  // Theme-based styles
  const getThemeStyles = () => {
    if (theme === "light") {
      return {
        header: "bg-white shadow-sm",
        logo: "text-gray-900",
        subtitle: "text-gray-600",
        navLink: "text-gray-700 hover:text-orange-500",
        activeLink: "text-orange-500 font-semibold border-b-2 border-orange-500 pb-1",
        mobileButton: "text-gray-700",
        mobileBorder: "border-gray-200"
      };
    } else if (theme === "transparent") {
      return {
        header: "bg-white/10 backdrop-blur-sm",
        logo: "text-white",
        subtitle: "text-white/70",
        navLink: "text-white hover:text-orange-400",
        activeLink: "text-orange-400 font-semibold border-b-2 border-orange-400 pb-1",
        mobileButton: "text-white",
        mobileBorder: "border-white/20"
      };
    } else { // dark theme
      return {
        header: "bg-gray-900 shadow-lg",
        logo: "text-white",
        subtitle: "text-gray-400",
        navLink: "text-gray-300 hover:text-orange-500",
        activeLink: "text-orange-500 font-semibold border-b-2 border-orange-500 pb-1",
        mobileButton: "text-gray-300",
        mobileBorder: "border-gray-700"
      };
    }
  };

  const styles = getThemeStyles();

  return (
    <header className={`sticky top-0 z-50 ${styles.header}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 text-orange-500">
              <svg viewBox="0 0 24 24" fill="currentColor" className="w-full h-full">
                <path d="M12 2L3 7V10.5L12 15.5L21 10.5V7L12 2ZM12 4.2L18.4 7.5L12 10.8L5.6 7.5L12 4.2ZM5 9.1L11 12.1V19.9L5 16.9V9.1ZM13 19.9V12.1L19 9.1V16.9L13 19.9Z"/>
                <path d="M12 1L2 6V11L12 16L22 11V6L12 1ZM4 8.5V9.5L12 14L20 9.5V8.5L12 13L4 8.5Z"/>
              </svg>
            </div>
            <div>
              <h1 className={`text-xl font-bold ${styles.logo}`}>Sikkim Monasteries</h1>
              <p className={`text-sm ${styles.subtitle}`}>Heritage & Culture</p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => {
              const isActive = currentPage === item.name.toLowerCase().replace(" ", "-");
              return (
                <a
                  key={item.name}
                  href={item.href}
                  className={`flex items-center space-x-2 transition-colors ${
                    isActive ? styles.activeLink : styles.navLink
                  }`}
                >
                  {item.icon}
                  <span>{item.name}</span>
                </a>
              );
            })}
          </nav>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className={`md:hidden ${styles.mobileButton}`}
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
          <nav className={`md:hidden py-4 border-t ${styles.mobileBorder}`}>
            <div className="flex flex-col space-y-4">
              {navItems.map((item) => {
                const isActive = currentPage === item.name.toLowerCase().replace(" ", "-");
                return (
                  <a
                    key={item.name}
                    href={item.href}
                    className={`flex items-center space-x-2 transition-colors ${
                      isActive ? styles.activeLink : styles.navLink
                    }`}
                  >
                    {item.icon}
                    <span>{item.name}</span>
                  </a>
                );
              })}
            </div>
          </nav>
        )}
      </div>
    </header>
  );
};
