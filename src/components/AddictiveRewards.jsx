import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Gift, 
  Clock, 
  Star, 
  Crown, 
  Zap, 
  Heart,
  Target,
  Trophy,
  Sparkles
} from 'lucide-react'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Progress } from './ui/progress'

const AddictiveRewards = ({ user, onRewardClaimed }) => {
  const [showRandomReward, setShowRandomReward] = useState(false)
  const [currentReward, setCurrentReward] = useState(null)
  const [dailyChallenge, setDailyChallenge] = useState(null)
  const [limitedOffer, setLimitedOffer] = useState(null)
  const [milestones, setMilestones] = useState([])
  const [achievements, setAchievements] = useState([])
  const [countdown, setCountdown] = useState(0)

  useEffect(() => {
    // Load daily challenge
    fetchDailyChallenge()
    // Load limited offer
    fetchLimitedOffer()
    // Load milestones
    fetchMilestones()
    // Load achievements
    fetchAchievements()
    
    // Set up random reward trigger (every 15-45 minutes)
    const randomInterval = Math.random() * (45 - 15) + 15 // 15-45 minutes
    const rewardTimer = setTimeout(() => {
      triggerRandomReward()
    }, randomInterval * 60 * 1000)

    return () => clearTimeout(rewardTimer)
  }, [])

  const fetchDailyChallenge = async () => {
    try {
      const response = await fetch('/api/real/addiction/daily-challenge')
      const data = await response.json()
      if (data.success) {
        setDailyChallenge(data.challenge)
      }
    } catch (error) {
      console.error('Error fetching daily challenge:', error)
    }
  }

  const fetchLimitedOffer = async () => {
    try {
      const response = await fetch('/api/real/addiction/limited-offer')
      const data = await response.json()
      if (data.success) {
        setLimitedOffer(data.offer)
        setCountdown(data.offer.expires_in_minutes * 60) // Convert to seconds
      }
    } catch (error) {
      console.error('Error fetching limited offer:', error)
    }
  }

  const fetchMilestones = async () => {
    try {
      const response = await fetch('/api/real/addiction/milestone-progress')
      const data = await response.json()
      if (data.success) {
        setMilestones(data.milestones)
      }
    } catch (error) {
      console.error('Error fetching milestones:', error)
    }
  }

  const fetchAchievements = async () => {
    try {
      const response = await fetch('/api/real/addiction/achievements')
      const data = await response.json()
      if (data.success) {
        setAchievements(data.achievements)
      }
    } catch (error) {
      console.error('Error fetching achievements:', error)
    }
  }

  const triggerRandomReward = async () => {
    try {
      const response = await fetch('/api/real/addiction/random-reward', {
        method: 'POST'
      })
      const data = await response.json()
      if (data.success) {
        setCurrentReward(data.reward)
        setShowRandomReward(true)
      }
    } catch (error) {
      console.error('Error triggering random reward:', error)
    }
  }

  const claimRandomReward = () => {
    if (currentReward && onRewardClaimed) {
      onRewardClaimed(currentReward)
    }
    setShowRandomReward(false)
    setCurrentReward(null)
    
    // Schedule next random reward
    const randomInterval = Math.random() * (45 - 15) + 15
    setTimeout(() => {
      triggerRandomReward()
    }, randomInterval * 60 * 1000)
  }

  // Countdown timer effect
  useEffect(() => {
    if (countdown > 0) {
      const timer = setInterval(() => {
        setCountdown(prev => prev - 1)
      }, 1000)
      return () => clearInterval(timer)
    }
  }, [countdown])

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const secs = seconds % 60
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div className="space-y-6">
      {/* Random Reward Modal */}
      <AnimatePresence>
        {showRandomReward && currentReward && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0, y: 50 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.8, opacity: 0, y: 50 }}
              className="bg-white rounded-2xl p-8 max-w-md mx-4 text-center bloom-card"
            >
              <motion.div
                animate={{ 
                  scale: [1, 1.2, 1],
                  rotate: [0, 10, -10, 0]
                }}
                transition={{ 
                  duration: 0.6,
                  repeat: Infinity,
                  repeatDelay: 2
                }}
                className="text-6xl mb-4"
              >
                {currentReward.icon}
              </motion.div>
              <h3 className="text-2xl font-bold inner-bloom-text-gradient mb-2">
                {currentReward.message}
              </h3>
              <div className="text-sm text-gray-500 mb-4 uppercase tracking-wide">
                {currentReward.rarity} Blessing
              </div>
              {currentReward.content && (
                <p className="text-gray-600 mb-4 italic">
                  "{currentReward.content}"
                </p>
              )}
              {currentReward.amount && (
                <div className="text-3xl font-bold text-primary mb-4">
                  +{currentReward.amount} Points
                </div>
              )}
              <Button
                onClick={claimRandomReward}
                className="w-full bg-primary hover:bg-primary/90 sparkle-effect"
              >
                Claim Your Blessing ✨
              </Button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Daily Challenge */}
      {dailyChallenge && (
        <Card className="bloom-card border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Target className="w-5 h-5 text-primary" />
              <span>Today's Sacred Challenge</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-4 mb-4">
              <div className="text-4xl">{dailyChallenge.icon}</div>
              <div className="flex-1">
                <h3 className="text-lg font-bold text-gray-800">{dailyChallenge.title}</h3>
                <p className="text-gray-600">{dailyChallenge.description}</p>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-primary">+{dailyChallenge.points}</div>
                <div className="text-sm text-gray-500">Points</div>
              </div>
            </div>
            <div className="bg-pink-50 p-3 rounded-lg mb-4">
              <p className="text-sm text-pink-800 font-medium">
                {dailyChallenge.social_message}
              </p>
            </div>
            <div className="bg-amber-50 p-3 rounded-lg mb-4">
              <p className="text-sm text-amber-800 font-medium flex items-center">
                <Clock className="w-4 h-4 mr-2" />
                {dailyChallenge.urgency}
              </p>
            </div>
            <Button className="w-full bg-primary hover:bg-primary/90">
              Accept Challenge
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Limited Time Offer */}
      {limitedOffer && (
        <Card className="bloom-card border-0 shadow-lg border-2 border-amber-300 bg-gradient-to-r from-amber-50 to-orange-50">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2 text-amber-800">
              <Zap className="w-5 h-5" />
              <span>Limited Divine Blessing</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-4 mb-4">
              <div className="text-4xl">{limitedOffer.icon}</div>
              <div className="flex-1">
                <h3 className="text-lg font-bold text-amber-800">{limitedOffer.title}</h3>
                <p className="text-amber-700">{limitedOffer.description}</p>
              </div>
            </div>
            <div className="bg-red-100 p-3 rounded-lg mb-4">
              <p className="text-sm text-red-800 font-bold">
                ⏰ Time Remaining: {formatTime(countdown)}
              </p>
            </div>
            <div className="bg-amber-100 p-3 rounded-lg mb-4">
              <p className="text-sm text-amber-800 font-medium">
                {limitedOffer.scarcity_message}
              </p>
              <p className="text-xs text-amber-700 mt-1">
                {limitedOffer.spots_remaining} spots remaining • {limitedOffer.claimed_by} sisters already blessed
              </p>
            </div>
            <Button className="w-full bg-amber-600 hover:bg-amber-700 text-white">
              Claim Limited Blessing
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Milestone Progress */}
      <Card className="bloom-card border-0 shadow-lg">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Trophy className="w-5 h-5 text-primary" />
            <span>Your Sacred Journey</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {milestones.map((milestone, index) => (
              <div key={milestone.id} className="space-y-3">
                <div className="flex items-center space-x-3">
                  <div className="text-3xl">{milestone.icon}</div>
                  <div className="flex-1">
                    <h3 className="font-bold text-gray-800">{milestone.name}</h3>
                    <p className="text-sm text-gray-600">{milestone.description}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-primary">{milestone.progress_percent}%</div>
                  </div>
                </div>
                <Progress value={milestone.progress_percent} className="h-3" />
                <div className="bg-purple-50 p-3 rounded-lg">
                  <p className="text-sm text-purple-800 italic">
                    {milestone.emotional_trigger}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Achievement Showcase */}
      <Card className="bloom-card border-0 shadow-lg">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Star className="w-5 h-5 text-primary" />
            <span>Sacred Achievements</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {achievements.slice(0, 4).map((achievement, index) => (
              <div key={achievement.id} className="p-4 bg-gradient-to-r from-pink-50 to-purple-50 rounded-lg">
                <div className="flex items-center space-x-3 mb-2">
                  <div className="text-2xl">{achievement.icon}</div>
                  <div className="flex-1">
                    <h4 className="font-bold text-gray-800">{achievement.name}</h4>
                    <p className="text-xs text-gray-600">{achievement.description}</p>
                  </div>
                  <div className="text-primary font-bold">+{achievement.points}</div>
                </div>
                <div className="bg-white p-2 rounded text-xs text-gray-700 italic">
                  {achievement.emotional_message}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default AddictiveRewards

