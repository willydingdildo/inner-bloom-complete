import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import './App.css'

// Components
import Header from './components/Header'
import HomePage from './components/HomePage'

import StyleSanctuary from './components/StyleSanctuary'
import SheEOHub from './components/SheEOHub'
import Community from './components/Community'
import Profile from './components/Profile'
import Subscription from './components/Subscription'
import Login from './components/Login'
import BiblicalLanding from './components/BiblicalLanding'


// Context
import { UserProvider, useUser } from './contexts/UserContext'

function AppContent() {
  const { user, loading } = useUser()
  const [showWelcome, setShowWelcome] = useState(false)
  const [showLanding, setShowLanding] = useState(true)
  const [hasDoneInitiation, setHasDoneInitiation] = useState(false)

  useEffect(() => {
    // Check if user has seen the landing page before
    const hasSeenLanding = localStorage.getItem('hasSeenLanding')
    if (hasSeenLanding) {
      setShowLanding(false)
    }
    // Check if user has completed initiation
    const initiationStatus = localStorage.getItem('hasDoneInitiation')
    if (initiationStatus === 'true') {
      setHasDoneInitiation(true)
    }
  }, [])

  useEffect(() => {
    if (user && !localStorage.getItem('welcomeShown')) {
      setShowWelcome(true)
      localStorage.setItem('welcomeShown', 'true')
    }
  }, [user])

  const handleStartBlooming = () => {
    setShowLanding(false)
    localStorage.setItem('hasSeenLanding', 'true')
  }

  const handleInitiationComplete = (data) => {
    setHasDoneInitiation(true)
    localStorage.setItem('hasDoneInitiation', 'true')
    // Optionally update user context with bloom name/backstory if needed
    // user.bloom_name = data.name; user.bloom_backstory = data.backstory;
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center inner-bloom-gradient">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          className="w-16 h-16 border-4 border-white border-t-transparent rounded-full"
        />
      </div>
    )
  }

  // Show landing page first
  if (showLanding) {
    return <BiblicalLanding onStartBlooming={handleStartBlooming} />
  }

  // Show initiation sequence if not done and user is logged in (or attempting to log in)


  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-amber-50">
        <AnimatePresence>
          {showWelcome && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
              onClick={() => setShowWelcome(false)}
            >
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.8, opacity: 0 }}
                className="bg-white rounded-2xl p-8 max-w-md mx-4 text-center bloom-card"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="text-6xl mb-4">🌸</div>
                <h2 className="text-2xl font-bold inner-bloom-text-gradient mb-4">
                  Welcome to Inner Bloom!
                </h2>
                <p className="text-gray-600 mb-6">
                  Your journey of empowerment and growth starts here. Let's bloom together!
                </p>
                <button
                  onClick={() => setShowWelcome(false)}
                  className="bg-primary text-white px-6 py-3 rounded-full hover:bg-primary/90 transition-colors sparkle-effect"
                >
                  Let's Begin! ✨
                </button>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {user ? (
          <>
            <Header />
            <main className="pt-16">
              <Routes>
                <Route path="/" element={<HomePage />} />
              
                <Route path="/style-sanctuary" element={<StyleSanctuary />} />
                <Route path="/she-eo-hub" element={<SheEOHub />} />
                <Route path="/community" element={<Community />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/subscription" element={<Subscription />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </main>
          </>
        ) : (
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        )}
      </div>
    </Router>
  )
}

function App() {
  return (
    <UserProvider>
      <AppContent />
    </UserProvider>
  )
}

export default App
