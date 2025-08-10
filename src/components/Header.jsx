import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  Heart, 
  Sparkles, 
  Palette, 
  TrendingUp, 
  Users, 
  User, 
  Crown,
  Menu,
  X,
  LogOut
} from 'lucide-react'
import { useUser } from '../contexts/UserContext'
import innerBloomLogo from '../assets/inner_bloom_logo.png'
import ThemeSelector from './ThemeSelector'

const Header = () => {
  const { user, logout } = useUser()
  const location = useLocation()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const navigation = [
    { name: 'Home', href: '/', icon: Heart },
    { name: 'Bloom AI', href: '/bloom-ai', icon: Sparkles },
    { name: 'Style Sanctuary', href: '/style-sanctuary', icon: Palette },
    { name: 'She-EO Hub', href: '/she-eo-hub', icon: TrendingUp },
    { name: 'Community', href: '/community', icon: Users },
  ]

  const isActive = (path) => location.pathname === path

  return (
    <header className="fixed top-0 left-0 right-0 z-40 bg-white/80 backdrop-blur-md border-b border-pink-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3">
            <img 
              src={innerBloomLogo} 
              alt="Inner Bloom" 
              className="h-10 w-auto floating-animation"
            />
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            {navigation.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-full transition-all duration-200 ${
                    isActive(item.href)
                      ? 'bg-primary text-white shadow-lg'
                      : 'text-gray-600 hover:text-primary hover:bg-pink-50'
                  }`}
                >
                  <Icon size={18} />
                  <span className="font-medium">{item.name}</span>
                </Link>
              )
            })}
          </nav>

          {/* User Menu */}
          <div className="hidden md:flex items-center space-x-4">
            {/* Theme Selector */}
            <ThemeSelector />
            
            {/* User Level & Points */}
            <div className="flex items-center space-x-2 bg-gradient-to-r from-pink-100 to-amber-100 px-3 py-1 rounded-full">
              <Crown size={16} className="text-amber-600" />
              <span className="text-sm font-medium">Level {user?.level || 1}</span>
              <span className="text-xs text-gray-500">•</span>
              <span className="text-sm font-medium">{user?.points || 0} pts</span>
            </div>

            {/* Profile & Subscription */}
            <div className="flex items-center space-x-2">
              <Link
                to="/subscription"
                className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                  user?.subscription === 'vip' 
                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                    : user?.subscription === 'premium'
                    ? 'bg-primary text-white'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {user?.subscription === 'vip' ? '👑 VIP' : 
                 user?.subscription === 'premium' ? '✨ Premium' : 'Free'}
              </Link>
              
              <Link
                to="/profile"
                className="flex items-center space-x-2 text-gray-600 hover:text-primary transition-colors"
              >
                <User size={20} />
              </Link>
              
              <button
                onClick={logout}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <LogOut size={20} />
              </button>
            </div>
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-md text-gray-600 hover:text-primary"
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Navigation */}
      {mobileMenuOpen && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="md:hidden bg-white border-t border-pink-100"
        >
          <div className="px-4 py-4 space-y-2">
            {navigation.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${
                    isActive(item.href)
                      ? 'bg-primary text-white'
                      : 'text-gray-600 hover:bg-pink-50'
                  }`}
                >
                  <Icon size={20} />
                  <span className="font-medium">{item.name}</span>
                </Link>
              )
            })}
            
            <div className="border-t border-pink-100 pt-4 mt-4">
              <Link
                to="/profile"
                onClick={() => setMobileMenuOpen(false)}
                className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-600 hover:bg-pink-50"
              >
                <User size={20} />
                <span className="font-medium">Profile</span>
              </Link>
              
              <Link
                to="/subscription"
                onClick={() => setMobileMenuOpen(false)}
                className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-600 hover:bg-pink-50"
              >
                <Crown size={20} />
                <span className="font-medium">Subscription</span>
              </Link>
              
              <button
                onClick={() => {
                  logout()
                  setMobileMenuOpen(false)
                }}
                className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-600 hover:bg-pink-50 w-full text-left"
              >
                <LogOut size={20} />
                <span className="font-medium">Logout</span>
              </button>
            </div>
          </div>
        </motion.div>
      )}
    </header>
  )
}

export default Header

