import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  Sparkles, 
  Heart, 
  TrendingUp, 
  Users, 
  Crown,
  Calendar,
  Target,
  Award,
  Gift,
  Zap,
  Star
} from 'lucide-react'
import { useUser } from '../contexts/UserContext'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import SocialProofFeed from './SocialProofFeed'

const HomePage = () => {
  const { user, getDailyAffirmation, platformStats, fetchPlatformStats } = useUser()
  const [dailyAffirmation, setDailyAffirmation] = useState('')
  const [showDailyReward, setShowDailyReward] = useState(false)
  const [rewardClaimed, setRewardClaimed] = useState(false)

  const affirmations = [
    "You are capable of amazing things today! ✨",
    "Your inner strength guides you through every challenge 💪",
    "Today is full of possibilities for growth and joy 🌸",
    "You deserve all the love and success coming your way 💖",
    "Your unique perspective makes the world a better place 🌟"
  ]

  useEffect(() => {
    // Fetch real daily affirmation
    const loadDailyAffirmation = async () => {
      const today = new Date().toDateString()
      const savedDate = localStorage.getItem('affirmationDate')
      
      if (savedDate !== today) {
        try {
          const affirmationData = await getDailyAffirmation()
          if (affirmationData) {
            setDailyAffirmation(affirmationData.affirmation)
            localStorage.setItem('affirmationDate', today)
            localStorage.setItem('dailyAffirmation', affirmationData.affirmation)
          }
        } catch (error) {
          console.error('Error fetching affirmation:', error)
          // Fallback to saved or default affirmation
          setDailyAffirmation(localStorage.getItem('dailyAffirmation') || "You are capable of amazing things today! ✨")
        }
      } else {
        setDailyAffirmation(localStorage.getItem('dailyAffirmation') || "You are capable of amazing things today! ✨")
      }
    }

    loadDailyAffirmation()

    // Fetch platform stats
    if (fetchPlatformStats) {
      fetchPlatformStats()
    }

    // Check for daily reward
    const today = new Date().toDateString()
    const lastRewardDate = localStorage.getItem('lastRewardDate')
    if (lastRewardDate !== today) {
      setShowDailyReward(true)
    } else {
      setRewardClaimed(true)
    }
  }, [getDailyAffirmation, fetchPlatformStats])

  const claimDailyReward = () => {
    const rewards = [
      { type: 'points', amount: 50, icon: '⭐', message: 'Daily Points Bonus!' },
      { type: 'points', amount: 100, icon: '✨', message: 'Bonus Points!' },
      { type: 'points', amount: 250, icon: '💎', message: 'Rare Gem Bonus!' },
      { type: 'streak', amount: 1, icon: '🔥', message: 'Streak Bonus!' },
      { type: 'inspiration', amount: 0, icon: '💝', message: 'Inspiration Boost!' },
      { type: 'exclusive_content', icon: '👑', message: 'Exclusive Content Unlocked!' },
      { type: 'identity_boost', icon: '🌟', message: 'Identity Boost!' }
    ]
    
    // Introduce rarity: common (70%), uncommon (20%), rare (10%)
    const random = Math.random()
    let reward
    if (random < 0.7) { // Common
      reward = rewards[Math.floor(Math.random() * 3)] // Points or Streak
    } else if (random < 0.9) { // Uncommon
      reward = rewards[Math.floor(Math.random() * 2) + 3] // Inspiration or 100/250 points
    } else { // Rare
      reward = rewards[Math.floor(Math.random() * 2) + 5] // Exclusive content or Identity boost
    }

    if (reward.type === 'points') {
      updateUser({ points: (user?.points || 0) + reward.amount })
    } else if (reward.type === 'streak') {
      updateUser({ streak: (user?.streak || 0) + 1 })
    } else if (reward.type === 'exclusive_content') {
      // Logic to unlock exclusive content (e.g., update user state, show modal)
      console.log('Exclusive content unlocked!')
    } else if (reward.type === 'identity_boost') {
      // Logic to provide an identity boost (e.g., special badge, temporary title)
      console.log('Identity boost received!')
    }
    
    setShowDailyReward(false)
    setRewardClaimed(true)
    localStorage.setItem('lastRewardDate', new Date().toDateString())
  }

  const quickActions = [

    {
      title: 'Style Sanctuary',
      description: 'Discover your style',
      icon: Heart,
      href: '/style-sanctuary',
      color: 'from-pink-400 to-rose-400'
    },
    {
      title: 'She-EO Hub',
      description: 'Build your empire',
      icon: TrendingUp,
      href: '/she-eo-hub',
      color: 'from-amber-400 to-orange-400'
    },
    {
      title: 'Community',
      description: 'Connect with sisters',
      icon: Users,
      href: '/community',
      color: 'from-emerald-400 to-teal-400'
    }
  ]

  const achievements = [
    { name: 'First Steps', description: 'Joined Inner Bloom', earned: true, icon: '🌱' },
    { name: 'Daily Warrior', description: '7-day streak', earned: (user?.streak || 0) >= 7, icon: '⚔️' },
    { name: 'Point Collector', description: '100 points earned', earned: (user?.points || 0) >= 100, icon: '💎' },
    { name: 'Community Star', description: 'Made 5 posts', earned: false, icon: '⭐' }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-amber-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Daily Reward Modal */}
        {showDailyReward && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="bg-white rounded-2xl p-8 max-w-sm mx-4 text-center bloom-card"
            >
              <div className="text-6xl mb-4">🎁</div>
              <h3 className="text-2xl font-bold inner-bloom-text-gradient mb-4">
                Daily Reward!
              </h3>
              <p className="text-gray-600 mb-6">
                Claim your daily bonus for being amazing!
              </p>
              <Button
                onClick={claimDailyReward}
                className="w-full bg-primary hover:bg-primary/90 sparkle-effect"
              >
                Claim Reward ✨
              </Button>
            </motion.div>
          </motion.div>
        )}

        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-6xl font-bold inner-bloom-text-gradient mb-4">
            Welcome back, {user?.username || 'Beautiful'}! 🌸
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Ready to bloom into your best self today? Your journey of empowerment continues here.
          </p>
        </motion.div>

        {/* Daily Affirmation */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8"
        >
          <Card className="bloom-card border-0 shadow-lg">
            <CardContent className="p-8 text-center">
              <div className="text-3xl mb-4">💫</div>
              <h2 className="text-2xl font-bold inner-bloom-text-gradient mb-4">
                Today's Affirmation
              </h2>
              <p className="text-lg text-gray-700 italic">
                "{dailyAffirmation}"
              </p>
            </CardContent>
          </Card>
        </motion.div>

        {/* Stats Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"
        >
          <Card className="bloom-card border-0">
            <CardContent className="p-4 text-center">
              <Crown className="w-8 h-8 text-amber-500 mx-auto mb-2" />
              <div className="text-2xl font-bold">Level {user?.level || 1}</div>
              <div className="text-sm text-gray-600">Your Level</div>
            </CardContent>
          </Card>
          
          <Card className="bloom-card border-0">
            <CardContent className="p-4 text-center">
              <Star className="w-8 h-8 text-purple-500 mx-auto mb-2" />
              <div className="text-2xl font-bold">{user?.points || 0}</div>
              <div className="text-sm text-gray-600">Points</div>
            </CardContent>
          </Card>
          
          <Card className="bloom-card border-0">
            <CardContent className="p-4 text-center">
              <Zap className="w-8 h-8 text-orange-500 mx-auto mb-2" />
              <div className="text-2xl font-bold">{user?.streak || 0}</div>
              <div className="text-sm text-gray-600">Day Streak</div>
            </CardContent>
          </Card>
          
          <Card className="bloom-card border-0">
            <CardContent className="p-4 text-center">
              <Calendar className="w-8 h-8 text-green-500 mx-auto mb-2" />
              <div className="text-2xl font-bold">
                {user?.joinedAt ? Math.floor((new Date() - new Date(user.joinedAt)) / (1000 * 60 * 60 * 24)) : 0}
              </div>
              <div className="text-sm text-gray-600">Days Active</div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mb-8"
        >
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {quickActions.map((action, index) => {
              const Icon = action.icon
              return (
                <motion.div
                  key={action.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 * index }}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <Link to={action.href}>
                    <Card className="h-full bloom-card border-0 hover:shadow-xl transition-all duration-300 cursor-pointer">
                      <CardContent className="p-6 text-center">
                        <div className={`w-16 h-16 rounded-full bg-gradient-to-r ${action.color} flex items-center justify-center mx-auto mb-4`}>
                          <Icon className="w-8 h-8 text-white" />
                        </div>
                        <h3 className="text-lg font-bold text-gray-800 mb-2">{action.title}</h3>
                        <p className="text-gray-600 text-sm">{action.description}</p>
                      </CardContent>
                    </Card>
                  </Link>
                </motion.div>
              )
            })}
          </div>
        </motion.div>

        {/* Progress Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8"
        >
          {/* Level Progress */}
          <Card className="bloom-card border-0">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Target className="w-5 h-5 text-primary" />
                <span>Level Progress</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between text-sm">
                  <span>Level {user?.level || 1}</span>
                  <span>{user?.points || 0} / {((user?.level || 1) * 100)} points</span>
                </div>
                <Progress 
                  value={((user?.points || 0) % 100)} 
                  className="h-3"
                />
                <p className="text-sm text-gray-600">
                  {100 - ((user?.points || 0) % 100)} points to next level!
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Achievements */}
          <Card className="bloom-card border-0">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Award className="w-5 h-5 text-primary" />
                <span>Achievements</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {achievements.map((achievement, index) => (
                  <div 
                    key={achievement.name}
                    className={`flex items-center space-x-3 p-2 rounded-lg ${
                      achievement.earned ? 'bg-green-50 border border-green-200' : 'bg-gray-50'
                    }`}
                  >
                    <span className="text-2xl">{achievement.icon}</span>
                    <div className="flex-1">
                      <div className={`font-medium ${achievement.earned ? 'text-green-800' : 'text-gray-600'}`}>
                        {achievement.name}
                      </div>
                      <div className="text-sm text-gray-500">{achievement.description}</div>
                    </div>
                    {achievement.earned && (
                      <div className="text-green-600 font-medium text-sm">Earned!</div>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Addictive Rewards System */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mb-8"
        >
          <AddictiveRewards 
            user={user} 
            onRewardClaimed={(reward) => {
              // Handle reward claiming logic
              console.log('Reward claimed:', reward)
            }} 
          />
        </motion.div>

        {/* Social Proof & FOMO Feed */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="mb-8"
        >
          <SocialProofFeed />
        </motion.div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="text-center"
        >
          <Card className="bloom-card border-0 inner-bloom-gradient">
            <CardContent className="p-8">
              <h2 className="text-3xl font-bold text-white mb-4">
                Ready to Bloom Today? 🌸
              </h2>
              <p className="text-white/90 mb-6 text-lg">
                Choose your path to empowerment and let's grow together!
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link to="/bloom-ai">
                  <Button className="bg-white text-primary hover:bg-white/90 px-8 py-3 rounded-full font-medium">
                    Start with AI Guidance ✨
                  </Button>
                </Link>
                <Link to="/community">
                  <Button variant="outline" className="border-white text-white hover:bg-white/10 px-8 py-3 rounded-full font-medium">
                    Join the Community 💕
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}

export default HomePage

