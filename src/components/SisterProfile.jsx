import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Crown, 
  Star, 
  Heart, 
  Sparkles, 
  Lock, 
  Unlock,
  TrendingUp,
  Users,
  Calendar,
  Award,
  Flame,
  Moon
} from 'lucide-react'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Progress } from './ui/progress'
import { Badge } from './ui/badge'

const SisterProfile = ({ user }) => {
  const [profile, setProfile] = useState(null)
  const [transformation, setTransformation] = useState(null)
  const [exclusiveAccess, setExclusiveAccess] = useState(null)
  const [sisterActivities, setSisterActivities] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchSisterProfile()
    fetchTransformation()
    fetchExclusiveAccess()
    fetchSisterActivities()
  }, [user])

  const fetchSisterProfile = async () => {
    try {
      const response = await fetch(`/api/real/identity/sister-profile?user_id=${user?.id || 1}`)
      const data = await response.json()
      if (data.success) {
        setProfile(data.profile)
      }
    } catch (error) {
      console.error('Error fetching sister profile:', error)
    }
  }

  const fetchTransformation = async () => {
    try {
      const response = await fetch('/api/real/identity/transformation-tracking')
      const data = await response.json()
      if (data.success) {
        setTransformation(data.transformation)
      }
    } catch (error) {
      console.error('Error fetching transformation:', error)
    }
  }

  const fetchExclusiveAccess = async () => {
    try {
      const response = await fetch(`/api/real/identity/exclusive-access?tier=${profile?.tier || 'novice'}`)
      const data = await response.json()
      if (data.success) {
        setExclusiveAccess(data.access)
      }
    } catch (error) {
      console.error('Error fetching exclusive access:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchSisterActivities = async () => {
    try {
      const response = await fetch('/api/real/identity/sisterhood-bonding')
      const data = await response.json()
      if (data.success) {
        setSisterActivities(data.activities)
      }
    } catch (error) {
      console.error('Error fetching sister activities:', error)
    }
  }

  const getTierColor = (tier) => {
    const colors = {
      'novice': 'from-green-400 to-emerald-500',
      'intermediate': 'from-blue-400 to-indigo-500',
      'advanced': 'from-purple-400 to-pink-500',
      'legendary': 'from-amber-400 to-orange-500'
    }
    return colors[tier] || colors.novice
  }

  const getTierIcon = (tier) => {
    const icons = {
      'novice': Star,
      'intermediate': Sparkles,
      'advanced': Crown,
      'legendary': Flame
    }
    const IconComponent = icons[tier] || Star
    return <IconComponent className="w-6 h-6" />
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full"
        />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Sister Identity Card */}
      {profile && (
        <Card className="bloom-card border-0 shadow-lg overflow-hidden">
          <div className={`h-32 bg-gradient-to-r ${getTierColor(profile.tier)} relative`}>
            <div className="absolute inset-0 bg-black bg-opacity-20" />
            <div className="absolute bottom-4 left-6 text-white">
              <div className="flex items-center space-x-2 mb-2">
                {getTierIcon(profile.tier)}
                <span className="text-lg font-bold">{profile.tier_display} Sister</span>
              </div>
              <div className="text-sm opacity-90">Sacred ID: {profile.sister_id}</div>
            </div>
          </div>
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-2xl font-bold inner-bloom-text-gradient">{profile.bloom_name}</h2>
                <p className="text-lg text-gray-600 italic">"{profile.sacred_title}"</p>
              </div>
              <div className="text-right">
                <div className="text-3xl font-bold text-primary">{profile.points}</div>
                <div className="text-sm text-gray-500">Sacred Points</div>
              </div>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="text-center p-3 bg-purple-50 rounded-lg">
                <Moon className="w-6 h-6 text-purple-500 mx-auto mb-1" />
                <div className="text-sm font-medium">{profile.moon_phase_joined}</div>
                <div className="text-xs text-gray-500">Joined Phase</div>
              </div>
              <div className="text-center p-3 bg-pink-50 rounded-lg">
                <Flame className="w-6 h-6 text-pink-500 mx-auto mb-1" />
                <div className="text-sm font-medium">{profile.divine_element}</div>
                <div className="text-xs text-gray-500">Sacred Element</div>
              </div>
              <div className="text-center p-3 bg-amber-50 rounded-lg">
                <Star className="w-6 h-6 text-amber-500 mx-auto mb-1" />
                <div className="text-sm font-medium">{profile.sacred_number}</div>
                <div className="text-xs text-gray-500">Divine Number</div>
              </div>
              <div className="text-center p-3 bg-green-50 rounded-lg">
                <TrendingUp className="w-6 h-6 text-green-500 mx-auto mb-1" />
                <div className="text-sm font-medium">Level {profile.transformation_level}</div>
                <div className="text-xs text-gray-500">Transformation</div>
              </div>
            </div>

            {profile.next_tier_requirements.next_tier && (
              <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium">Next Tier: {profile.next_tier_requirements.next_tier}</span>
                  <span className="text-sm text-gray-600">
                    {profile.next_tier_requirements.points_needed - profile.points} points needed
                  </span>
                </div>
                <Progress 
                  value={(profile.points / profile.next_tier_requirements.points_needed) * 100} 
                  className="h-2"
                />
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Transformation Tracking */}
      {transformation && (
        <Card className="bloom-card border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Heart className="w-5 h-5 text-primary" />
              <span>Sacred Transformation Journey</span>
            </CardTitle>
            <div className="text-sm text-gray-600">
              Current Stage: <span className="font-bold text-primary">{transformation.transformation_stage}</span>
              {' • '}Overall Progress: <span className="font-bold">{transformation.overall_progress}%</span>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {transformation.areas.map((area, index) => (
                <div key={area.area} className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="font-bold text-gray-800">{area.area}</h3>
                    <div className="text-right">
                      <div className="text-lg font-bold text-primary">
                        {area.current_level}/{area.max_level}
                      </div>
                      <div className="text-xs text-green-600">{area.recent_growth}</div>
                    </div>
                  </div>
                  <Progress value={(area.current_level / area.max_level) * 100} className="h-3" />
                  <div className="text-sm text-gray-600">{area.description}</div>
                  <div className="bg-purple-50 p-3 rounded-lg">
                    <div className="text-sm font-medium text-purple-800 mb-1">
                      Next Milestone: {area.next_milestone}
                    </div>
                    <div className="text-sm text-purple-700 italic">
                      "{area.affirmation}"
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Exclusive Access */}
      {exclusiveAccess && (
        <Card className="bloom-card border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Crown className="w-5 h-5 text-primary" />
              <span>Your Sacred Privileges</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4 mb-6">
              <h3 className="font-bold text-gray-800">Current Access Level: {exclusiveAccess.current_tier}</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {exclusiveAccess.privileges.map((privilege, index) => (
                  <div key={index} className="flex items-center space-x-2 p-2 bg-green-50 rounded-lg">
                    <Unlock className="w-4 h-4 text-green-500" />
                    <span className="text-sm text-green-800">{privilege}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="font-bold text-gray-800">Exclusive Content</h3>
              {exclusiveAccess.exclusive_content.map((content, index) => (
                <div key={index} className={`p-4 rounded-lg border-2 ${
                  content.locked ? 'border-gray-200 bg-gray-50' : 'border-primary bg-primary/5'
                }`}>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-bold text-gray-800">{content.title}</h4>
                    {content.locked ? (
                      <Lock className="w-5 h-5 text-gray-400" />
                    ) : (
                      <Unlock className="w-5 h-5 text-primary" />
                    )}
                  </div>
                  <p className="text-sm text-gray-600 mb-2">{content.description}</p>
                  <Badge variant={content.locked ? "secondary" : "default"}>
                    {content.type.replace('_', ' ').toUpperCase()}
                  </Badge>
                </div>
              ))}
            </div>

            {exclusiveAccess.next_unlock.tier && (
              <div className="mt-6 p-4 bg-gradient-to-r from-amber-50 to-orange-50 rounded-lg">
                <h4 className="font-bold text-amber-800 mb-2">
                  Next Unlock: {exclusiveAccess.next_unlock.tier} Tier
                </h4>
                <p className="text-sm text-amber-700 mb-2">
                  {exclusiveAccess.next_unlock.requirements}
                </p>
                <p className="text-sm text-amber-600">
                  Benefits: {exclusiveAccess.next_unlock.benefits}
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Sister Activities */}
      <Card className="bloom-card border-0 shadow-lg">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Users className="w-5 h-5 text-primary" />
            <span>Sacred Sister Activities</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {sisterActivities.map((activity, index) => (
              <div key={activity.id} className="p-4 bg-gradient-to-r from-pink-50 to-purple-50 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-bold text-gray-800">{activity.name}</h3>
                  <Badge variant="outline">{activity.energy_level}</Badge>
                </div>
                <p className="text-sm text-gray-600 mb-3">{activity.description}</p>
                <div className="space-y-2 text-xs text-gray-500">
                  <div className="flex items-center space-x-2">
                    <Calendar className="w-3 h-3" />
                    <span>{activity.time}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Users className="w-3 h-3" />
                    <span>{activity.participants} sisters participating</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Heart className="w-3 h-3" />
                    <span>Bonding Power: {activity.bonding_power}%</span>
                  </div>
                </div>
                <Button className="w-full mt-3 bg-primary hover:bg-primary/90 text-sm">
                  Join Sacred Circle
                </Button>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default SisterProfile

