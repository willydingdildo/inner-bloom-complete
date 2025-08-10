import React, { useState } from 'react';

const ThemeSelector = () => {
  const [currentTheme, setCurrentTheme] = useState('inner_bloom_classic');
  const [isOpen, setIsOpen] = useState(false);

  const themes = [
    {
      id: 'inner_bloom_classic',
      name: 'Inner Bloom Classic',
      description: 'Clean & Elegant (Free)',
      preview: '#E91E63'
    },
    {
      id: 'inner_bloom_premium',
      name: 'Inner Bloom Premium',
      description: 'Enhanced with Gradients ($29.99)',
      preview: 'linear-gradient(135deg, #6366F1, #EC4899)'
    },
    {
      id: 'inner_bloom_vip',
      name: 'Inner Bloom VIP - Royal Vintage',
      description: 'Gold & Black Luxury ($59.99)',
      preview: 'linear-gradient(135deg, #000000, #FFD700)'
    },
    {
      id: 'dark_mode',
      name: 'Dark Mode',
      description: 'Night-Friendly (All Tiers)',
      preview: 'linear-gradient(135deg, #121212, #BB86FC)'
    }
  ];

  const applyTheme = (themeId) => {
    const theme = themes.find(t => t.id === themeId);
    if (!theme) return;

    // Apply theme to document root
    const root = document.documentElement;
    
    switch(themeId) {
      case 'inner_bloom_classic':
        root.style.setProperty('--primary-color', '#E91E63');
        root.style.setProperty('--secondary-color', '#F8BBD9');
        root.style.setProperty('--background-color', '#FFFFFF');
        root.style.setProperty('--surface-color', '#F9F9F9');
        root.style.setProperty('--text-color', '#000000');
        root.style.setProperty('--font-family', 'Inter, sans-serif');
        break;
        
      case 'inner_bloom_premium':
        root.style.setProperty('--primary-color', '#6366F1');
        root.style.setProperty('--secondary-color', '#EC4899');
        root.style.setProperty('--background-color', 'linear-gradient(135deg, #6366F1, #EC4899)');
        root.style.setProperty('--surface-color', 'rgba(255, 255, 255, 0.1)');
        root.style.setProperty('--text-color', '#FFFFFF');
        root.style.setProperty('--font-family', 'Montserrat, sans-serif');
        break;
        
      case 'inner_bloom_vip':
        root.style.setProperty('--primary-color', '#FFD700');
        root.style.setProperty('--secondary-color', '#C9B037');
        root.style.setProperty('--background-color', '#0A0A0A');
        root.style.setProperty('--surface-color', '#1A1A1A');
        root.style.setProperty('--text-color', '#FFD700');
        root.style.setProperty('--font-family', 'Playfair Display, serif');
        root.style.setProperty('--border-style', '2px solid #FFD700');
        root.style.setProperty('--box-shadow', '0 4px 20px rgba(255, 215, 0, 0.3)');
        break;
        
      case 'dark_mode':
        root.style.setProperty('--primary-color', '#BB86FC');
        root.style.setProperty('--secondary-color', '#03DAC6');
        root.style.setProperty('--background-color', '#121212');
        root.style.setProperty('--surface-color', '#1E1E1E');
        root.style.setProperty('--text-color', '#FFFFFF');
        root.style.setProperty('--font-family', 'Inter, sans-serif');
        break;
    }
    
    setCurrentTheme(themeId);
    setIsOpen(false);
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 px-4 py-2 bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 hover:bg-white/20 transition-all duration-200"
      >
        <div 
          className="w-4 h-4 rounded-full"
          style={{ background: themes.find(t => t.id === currentTheme)?.preview }}
        ></div>
        <span className="text-sm font-medium">Themes</span>
        <svg className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute top-full right-0 mt-2 w-80 bg-white/95 backdrop-blur-sm rounded-xl shadow-2xl border border-white/20 z-50">
          <div className="p-4">
            <h3 className="text-lg font-semibold text-gray-800 mb-3">Choose Your Theme</h3>
            <div className="space-y-3">
              {themes.map((theme) => (
                <button
                  key={theme.id}
                  onClick={() => applyTheme(theme.id)}
                  className={`w-full p-3 rounded-lg border-2 transition-all duration-200 text-left ${
                    currentTheme === theme.id 
                      ? 'border-pink-500 bg-pink-50' 
                      : 'border-gray-200 hover:border-pink-300 hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <div 
                      className="w-8 h-8 rounded-full border-2 border-white shadow-md"
                      style={{ background: theme.preview }}
                    ></div>
                    <div className="flex-1">
                      <div className="font-medium text-gray-800">{theme.name}</div>
                      <div className="text-sm text-gray-600">{theme.description}</div>
                    </div>
                    {currentTheme === theme.id && (
                      <div className="text-pink-500">
                        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      </div>
                    )}
                  </div>
                </button>
              ))}
            </div>
            <div className="mt-4 p-3 bg-yellow-50 rounded-lg border border-yellow-200">
              <div className="text-sm text-yellow-800">
                <strong>Demo Mode:</strong> All themes are unlocked for testing! In production, Premium and VIP themes require subscriptions.
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ThemeSelector;

