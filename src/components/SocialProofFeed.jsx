import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Activity, 
  Users, 
  TrendingUp, 
  Clock, 
  Star, 
  Crown, 
  Zap,
  AlertTriangle,
  Flame,
  Heart,
  Trophy,
  Target,
  Timer
} from 'lucide-react'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Badge } from './ui/badge'
import { Progress } from './ui/progress'

const SocialProofFeed = () => {
  const [liveActivity, setLiveActivity] = useState([])
  const [testimonials, setTestimonials] = useState([])
  const [urgencyMetrics, setUrgencyMetrics] = useState({})
  const [scarcityAlerts, setScarcityAlerts] = useState([])
  const [communityEnergy, setCommunityEnergy] = useState({})
  const [leaderboard, setLeaderboard] = useState([])
  const [currentTestimonial, setCurrentTestimonial] = useState(0)

  useEffect(() => {
    fetchLiveActivity()
    fetchTestimonials()
    fetchUrgencyMetrics()
    fetchScarcityAlerts()
    fetchCommunityEnergy()
    fetchLeaderboard()

    // Set up real-time updates
    const activityInterval = setInterval(fetchLiveActivity, 30000) // Every 30 seconds
    const metricsInterval = setInterval(fetchUrgencyMetrics, 60000) // Every minute
    const testimonialRotation = setInterval(() => {
      setCurrentTestimonial(prev => (prev + 1) % testimonials.length)
    }, 8000) // Every 8 seconds

    return () => {
      clearInterval(activityInterval)
      clearInterval(metricsInterval)
      clearInterval(testimonialRotation)
    }
  }, [testimonials.length])

  const fetchLiveActivity = async () => {
    try {
      const response = await fetch('/api/real/social/live-activity')
      const data = await response.json()
      if (data.success) {
        setLiveActivity(data.activities.slice(0, 8)) // Show only recent 8
      }
    } catch (error) {
      console.error('Error fetching live activity:', error)
    }
  }

  const fetchTestimonials = async () => {
    try {
      const response = await fetch('/api/real/social/success-testimonials')
      const data = await response.json()
      if (data.success) {
        setTestimonials(data.testimonials)
      }
    } catch (error) {
      console.error('Error fetching testimonials:', error)
    }
  }

  const fetchUrgencyMetrics = async () => {
    try {
      const response = await fetch('/api/real/social/urgency-metrics')
      const data = await response.json()
      if (data.success) {
        setUrgencyMetrics(data.metrics)
      }
    } catch (error) {
      console.error('Error fetching urgency metrics:', error)
    }
  }

  const fetchScarcityAlerts = async () => {
    try {
      const response = await fetch('/api/real/social/scarcity-alerts')
      const data = await response.json()
      if (data.success) {
        setScarcityAlerts(data.alerts)
      }
    } catch (error) {
      console.error('Error fetching scarcity alerts:', error)
    }
  }

  const fetchCommunityEnergy = async () => {
    try {
      const response = await fetch('/api/real/social/community-energy')
      const data = await response.json()
      if (data.success) {
        setCommunityEnergy(data.energy)
      }
    } catch (error) {
      console.error('Error fetching community energy:', error)
    }
  }

  const fetchLeaderboard = async () => {
    try {
      const response = await fetch('/api/real/social/leaderboard')
      const data = await response.json()
      if (data.success) {
        setLeaderboard(data.leaderboard.slice(0, 5)) // Top 5
      }
    } catch (error) {
      console.error('Error fetching leaderboard:', error)
    }
  }

  const formatTimeAgo = (timestamp) => {
    const now = new Date()
    const time = new Date(timestamp)
    const diffInMinutes = Math.floor((now - time) / (1000 * 60))
    
    if (diffInMinutes < 1) return 'just now'
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`
    const diffInHours = Math.floor(diffInMinutes / 60)
    if (diffInHours < 24) return `${diffInHours}h ago`
    return `${Math.floor(diffInHours / 24)}d ago`
  }

  const getUrgencyColor = (level) => {
    switch (level) {
      case 'critical': return 'bg-red-100 text-red-800 border-red-300'
      case 'high': return 'bg-orange-100 text-orange-800 border-orange-300'
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-300'
      default: return 'bg-blue-100 text-blue-800 border-blue-300'
    }
  }

  return (
    <div className="space-y-6">
      {/* Community Energy Bar */}
      {communityEnergy.current_energy && (
        <Card className="bloom-card border-0 shadow-lg bg-gradient-to-r from-purple-50 to-pink-50">
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center space-x-2">
                <Flame className="w-5 h-5 text-orange-500" />
                <span className="font-bold text-gray-800">Community Energy</span>
              </div>
              <div className="text-2xl font-bold text-primary">{communityEnergy.current_energy}%</div>
            </div>
            <Progress value={communityEnergy.current_energy} className="h-3 mb-2" />
            <div className="flex items-center justify-between text-sm text-gray-600">
              <span>{communityEnergy.sisters_meditating_now} sisters meditating now</span>
              <span className="text-purple-600 font-medium">{communityEnergy.energy_trend}</span>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Scarcity Alerts */}
      <AnimatePresence>
        {scarcityAlerts.map((alert, index) => (
          <motion.div
            key={alert.type}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className={`p-4 rounded-lg border-2 ${getUrgencyColor(alert.urgency_level)}`}
          >
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center space-x-2">
                <AlertTriangle className="w-5 h-5" />
                <h3 className="font-bold">{alert.title}</h3>
              </div>
              <Badge variant="outline" className="text-xs">
                {alert.expires_in_hours}h left
              </Badge>
            </div>
            <p className="text-sm mb-3">{alert.message}</p>
            <div className="flex items-center justify-between">
              <div className="text-xs">
                {alert.claimed_count}/{alert.total_spots} claimed
              </div>
              <Button size="sm" className="bg-primary hover:bg-primary/90">
                Claim Now
              </Button>
            </div>
            <Progress 
              value={(alert.claimed_count / alert.total_spots) * 100} 
              className="h-2 mt-2"
            />
          </motion.div>
        ))}
      </AnimatePresence>

      {/* Live Activity Feed */}
      <Card className="bloom-card border-0 shadow-lg">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Activity className="w-5 h-5 text-primary" />
            <span>Live Sister Activity</span>
            <Badge variant="outline" className="ml-auto">
              {urgencyMetrics.sisters_online_now} online now
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3 max-h-64 overflow-y-auto">
            <AnimatePresence>
              {liveActivity.map((activity, index) => (
                <motion.div
                  key={activity.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-center space-x-3 p-2 bg-gradient-to-r from-pink-50 to-purple-50 rounded-lg"
                >
                  <div className="w-8 h-8 rounded-full bg-gradient-to-r from-pink-400 to-purple-400 flex items-center justify-center text-white text-sm font-bold">
                    {activity.sister_name[0]}
                  </div>
                  <div className="flex-1">
                    <div className="text-sm">
                      <span className="font-medium text-primary">{activity.sister_name}</span>
                      {' '}{activity.action}
                      {activity.points_earned && (
                        <span className="text-green-600 font-medium"> (+{activity.points_earned} points)</span>
                      )}
                    </div>
                    <div className="text-xs text-gray-500 flex items-center space-x-2">
                      <span>{formatTimeAgo(activity.timestamp)}</span>
                      <span>•</span>
                      <span>{activity.location}</span>
                    </div>
                  </div>
                  {activity.achievement_unlocked && (
                    <Badge variant="outline" className="text-xs">
                      {activity.achievement_unlocked}
                    </Badge>
                  )}
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </CardContent>
      </Card>

      {/* Success Testimonials Carousel */}
      {testimonials.length > 0 && (
        <Card className="bloom-card border-0 shadow-lg bg-gradient-to-r from-green-50 to-emerald-50">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Star className="w-5 h-5 text-green-600" />
              <span>Sister Success Stories</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <AnimatePresence mode="wait">
              <motion.div
                key={currentTestimonial}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.5 }}
                className="text-center"
              >
                <div className="mb-4">
                  <div className="text-lg font-medium text-gray-800 mb-2">
                    {testimonials[currentTestimonial]?.sister_name}
                  </div>
                  <p className="text-gray-600 italic">
                    "{testimonials[currentTestimonial]?.story}"
                  </p>
                </div>
                <div className="flex items-center justify-center space-x-4 text-sm text-gray-500">
                  <span>Transformation: {testimonials[currentTestimonial]?.transformation_area}</span>
                  <span>•</span>
                  <span>Time: {testimonials[currentTestimonial]?.time_to_result}</span>
                  {testimonials[currentTestimonial]?.verified && (
                    <>
                      <span>•</span>
                      <span className="text-green-600 font-medium">✓ Verified</span>
                    </>
                  )}
                </div>
              </motion.div>
            </AnimatePresence>
            <div className="flex justify-center mt-4 space-x-1">
              {testimonials.map((_, index) => (
                <div
                  key={index}
                  className={`w-2 h-2 rounded-full transition-colors ${
                    index === currentTestimonial ? 'bg-primary' : 'bg-gray-300'
                  }`}
                />
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Top Sisters Leaderboard */}
      <Card className="bloom-card border-0 shadow-lg">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Trophy className="w-5 h-5 text-amber-500" />
            <span>Top Sisters This Week</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {leaderboard.map((sister, index) => (
              <div
                key={sister.rank}
                className={`flex items-center space-x-3 p-3 rounded-lg ${
                  sister.is_current_user 
                    ? 'bg-primary/10 border-2 border-primary' 
                    : 'bg-gray-50'
                }`}
              >
                <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${
                  index === 0 ? 'bg-yellow-400 text-yellow-900' :
                  index === 1 ? 'bg-gray-300 text-gray-700' :
                  index === 2 ? 'bg-amber-600 text-white' :
                  'bg-gray-200 text-gray-600'
                }`}>
                  {sister.rank}
                </div>
                <div className="flex-1">
                  <div className="font-medium text-gray-800">
                    {sister.sister_name}
                    {sister.is_current_user && <span className="text-primary ml-2">(You)</span>}
                  </div>
                  <div className="text-sm text-gray-500">
                    Level {sister.level} • {sister.streak} day streak
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-bold text-primary">{sister.points}</div>
                  <div className="text-xs text-gray-500">points</div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Urgency Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="bloom-card border-0 text-center">
          <CardContent className="p-4">
            <Users className="w-6 h-6 text-blue-500 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-800">{urgencyMetrics.sisters_joined_today}</div>
            <div className="text-xs text-gray-600">Joined Today</div>
          </CardContent>
        </Card>
        
        <Card className="bloom-card border-0 text-center">
          <CardContent className="p-4">
            <TrendingUp className="w-6 h-6 text-green-500 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-800">{urgencyMetrics.transformations_in_progress}</div>
            <div className="text-xs text-gray-600">Transforming</div>
          </CardContent>
        </Card>
        
        <Card className="bloom-card border-0 text-center">
          <CardContent className="p-4">
            <Heart className="w-6 h-6 text-red-500 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-800">{urgencyMetrics.manifestations_today}</div>
            <div className="text-xs text-gray-600">Manifested Today</div>
          </CardContent>
        </Card>
        
        <Card className="bloom-card border-0 text-center">
          <CardContent className="p-4">
            <Zap className="w-6 h-6 text-purple-500 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-800">{urgencyMetrics.success_rate}</div>
            <div className="text-xs text-gray-600">Success Rate</div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default SocialProofFeed