import React, { createContext, useContext, useState, useEffect } from 'react'

const UserContext = createContext()

export const useUser = () => {
  const context = useContext(UserContext)
  if (!context) {
    throw new Error('useUser must be used within a UserProvider')
  }
  return context
}

// API Configuration
const API_BASE = 'https://vgh0i1c586q1.manus.space/api/real'

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [platformStats, setPlatformStats] = useState(null)

  useEffect(() => {
    // Check for existing user session
    const savedUser = localStorage.getItem('innerBloomUser')
    if (savedUser) {
      try {
        const userData = JSON.parse(savedUser)
        setUser(userData)
        // Fetch fresh user data from API
        fetchUserData(userData.id)
      } catch (error) {
        console.error('Error parsing saved user:', error)
        localStorage.removeItem('innerBloomUser')
      }
    }
    
    // Fetch platform stats
    fetchPlatformStats()
    setLoading(false)
  }, [])

  const fetchUserData = async (userId) => {
    try {
      const response = await fetch(`${API_BASE}/user/${userId}`)
      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
        localStorage.setItem('innerBloomUser', JSON.stringify(userData))
      }
    } catch (error) {
      console.error('Error fetching user data:', error)
    }
  }

  const fetchPlatformStats = async () => {
    try {
      const response = await fetch(`${API_BASE}/stats`)
      if (response.ok) {
        const stats = await response.json()
        setPlatformStats(stats)
      }
    } catch (error) {
      console.error('Error fetching platform stats:', error)
    }
  }

  const login = async (email, password) => {
    try {
      // For demo purposes, create a user with demo credentials
        const demoUser = {
          id: 'demo_user',
          email: email,
          name: email.split('@')[0],
          bloom_name: 'The Anointed Dawn', // Default for demo
          bloom_backstory: 'You were called to this journey of divine awakening and prosperity.', // Default for demo
          subscription_tier: 'vip', // Give demo user VIP access
          points: 2450,
          level: 15,
          streak_days: 7,
          total_earnings: 1250.00,
          created_at: new Date().toISOString(),
          recent_activities: []
        }
        
        setUser(demoUser)
        localStorage.setItem('innerBloomUser', JSON.stringify(demoUser))
        return { success: true }
      } catch (error) {
        return { success: false, error: error.message }
      }
    }

    const logout = () => {
      setUser(null)
      localStorage.removeItem('innerBloomUser')
    }

    const addPoints = async (points, activity, description) => {
      if (!user) return

      try {
        const response = await fetch(`${API_BASE}/user/${user.id}/points`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            points,
            activity,
            description
          })
        })

        if (response.ok) {
          // Update user points locally
          const updatedUser = {
            ...user,
            points: user.points + points
          }
          setUser(updatedUser)
          localStorage.setItem('innerBloomUser', JSON.stringify(updatedUser))
          
          // Refresh user data from server
          fetchUserData(user.id)
        }
      } catch (error) {
        console.error('Error adding points:', error)
      }
    }

    const chatWithAI = async (message) => {
      if (!user) return null

      try {
        const response = await fetch(`${API_BASE}/ai/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_id: user.id,
            message,
            user_name: user.name
          })
        })

        if (response.ok) {
          const aiResponse = await response.json()
          // Add points for AI interaction
          addPoints(5, 'ai_chat', 'Chatted with Bloom AI')
          return aiResponse
        }
      } catch (error) {
        console.error('Error chatting with AI:', error)
      }
      return null
    }

    const getDailyAffirmation = async () => {
      if (!user) return null

      try {
        const response = await fetch(`${API_BASE}/ai/affirmation?user_id=${user.id}`)
        if (response.ok) {
          const affirmation = await response.json()
          return affirmation
        }
      } catch (error) {
        console.error('Error getting affirmation:', error)
      }
      return null
    }

    const downloadPDF = async (pdfType) => {
      if (!user) return null

      try {
        const response = await fetch(`${API_BASE}/download/${pdfType}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_email: user.email,
            user_name: user.name,
            user_id: user.id
          })
        })

        if (response.ok) {
          const blob = await response.blob()
          const url = window.URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.style.display = 'none'
          a.href = url
          a.download = `${pdfType}_${user.name.replace(' ', '_')}.pdf`
          document.body.appendChild(a)
          a.click()
          window.URL.revokeObjectURL(url)
          
          // Add points for PDF download
          addPoints(20, 'pdf_download', `Downloaded ${pdfType} guide`)
          return true
        }
      } catch (error) {
        console.error('Error downloading PDF:', error)
      }
      return false
    }

    const getLeaderboard = async () => {
      try {
        const response = await fetch(`${API_BASE}/leaderboard`)
        if (response.ok) {
          return await response.json()
        }
      } catch (error) {
        console.error('Error fetching leaderboard:', error)
      }
      return []
    }

    const value = {
      user,
      loading,
      platformStats,
      login,
      logout,
      addPoints,
      chatWithAI,
      getDailyAffirmation,
      downloadPDF,
      getLeaderboard,
      fetchUserData,
      fetchPlatformStats
    }

    return (
      <UserContext.Provider value={value}>
        {children}
      </UserContext.Provider>
    )
  }

