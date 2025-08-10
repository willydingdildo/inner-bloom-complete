import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Users, 
  Heart, 
  MessageCircle, 
  Share2, 
  Plus,
  Crown,
  Star,
  Sparkles,
  Send,
  ThumbsUp,
  Gift,
  Zap,
  Award,
  Globe,
  Lock,
  TrendingUp
} from 'lucide-react'
import { useUser } from '../contexts/UserContext'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Input } from './ui/input'
import { Textarea } from './ui/textarea'
import { Badge } from './ui/badge'

const Community = () => {
  const { user, updateUser } = useUser()
  const [activeTab, setActiveTab] = useState('feed')
  const [newPost, setNewPost] = useState('')
  const [showHugModal, setShowHugModal] = useState(false)
  const [hugMessage, setHugMessage] = useState('')

  const tabs = [
    { id: 'feed', name: 'Community Feed', icon: Globe },
    { id: 'circles', name: 'My Circles', icon: Users },
    { id: 'hugs', name: 'Virtual Hugs', icon: Heart },
    { id: 'leaderboard', name: 'Leaderboard', icon: Crown }
  ]

  const communityPosts = [
    {
      id: 1,
      author: 'Sarah M.',
      avatar: '👩‍💼',
      time: '2 hours ago',
      content: 'Just landed my dream job! 🎉 The confidence-building exercises from Inner Bloom really helped me nail the interview. Feeling so grateful for this amazing community! 💕',
      likes: 47,
      comments: 12,
      shares: 8,
      type: 'celebration',
      tags: ['career', 'confidence', 'success']
    },
    {
      id: 2,
      author: 'Emma K.',
      avatar: '👩‍🎨',
      time: '4 hours ago',
      content: 'Having one of those days where everything feels overwhelming. Could really use some encouragement from my Inner Bloom sisters 🌸',
      likes: 23,
      comments: 18,
      shares: 3,
      type: 'support',
      tags: ['support', 'mental-health']
    },
    {
      id: 3,
      author: 'Lisa R.',
      avatar: '👩‍🚀',
      time: '6 hours ago',
      content: 'Started my sustainable fashion journey today! Swapped 5 items in the Style Sanctuary marketplace. Every small step counts! 🌱♻️',
      likes: 31,
      comments: 9,
      shares: 15,
      type: 'story',
      tags: ['sustainability', 'fashion', 'environment']
    }
  ]

  const sisterhoodCircles = [
    {
      id: 1,
      name: 'Entrepreneur Queens',
      description: 'Supporting women building their business empires',
      members: 127,
      isPrivate: true,
      lastActivity: '2 hours ago',
      category: 'Business',
      color: 'from-purple-400 to-pink-400'
    },
    {
      id: 2,
      name: 'Mindful Mamas',
      description: 'Balancing motherhood with personal growth',
      members: 89,
      isPrivate: true,
      lastActivity: '1 hour ago',
      category: 'Parenting',
      color: 'from-green-400 to-teal-400'
    },
    {
      id: 3,
      name: 'Creative Souls',
      description: 'Unleashing our artistic potential together',
      members: 156,
      isPrivate: false,
      lastActivity: '30 minutes ago',
      category: 'Creativity',
      color: 'from-orange-400 to-red-400'
    }
  ]

  const leaderboard = [
    { rank: 1, name: 'Alexandra P.', points: 2847, badge: '👑', streak: 45 },
    { rank: 2, name: 'Maria S.', points: 2634, badge: '⭐', streak: 38 },
    { rank: 3, name: 'Jennifer L.', points: 2521, badge: '💎', streak: 42 },
    { rank: 4, name: 'You', points: user?.points || 0, badge: '🌟', streak: user?.streak || 0 },
    { rank: 5, name: 'Rachel M.', points: 2156, badge: '✨', streak: 28 }
  ]

  const virtualHugs = [
    {
      id: 1,
      from: 'Anonymous Sister',
      message: 'You are stronger than you know! 💪✨',
      time: '1 hour ago',
      type: 'encouragement'
    },
    {
      id: 2,
      from: 'Sarah M.',
      message: 'Celebrating your wins with you! 🎉',
      time: '3 hours ago',
      type: 'celebration'
    },
    {
      id: 3,
      from: 'Global Community',
      message: 'Sending love and positive energy your way! 🌸💕',
      time: '5 hours ago',
      type: 'support'
    }
  ]

  const sendVirtualHug = () => {
    // Simulate sending a hug
    updateUser({ 
      points: (user?.points || 0) + 5,
      totalHugsSent: (user?.totalHugsSent || 0) + 1
    })
    setShowHugModal(false)
    setHugMessage('')
  }

  const sharePost = (postId) => {
    // Simulate sharing functionality
    alert('Post shared! Your friends can now discover Inner Bloom through your inspiring content! 🌟')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-amber-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Virtual Hug Modal */}
        {showHugModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="bg-white rounded-2xl p-8 max-w-md mx-4 bloom-card"
            >
              <div className="text-center mb-6">
                <div className="text-6xl mb-4 virtual-hug-animation">🤗</div>
                <h3 className="text-2xl font-bold inner-bloom-text-gradient mb-2">
                  Send a Virtual Hug
                </h3>
                <p className="text-gray-600">
                  Spread love and encouragement to the community
                </p>
              </div>
              
              <Textarea
                value={hugMessage}
                onChange={(e) => setHugMessage(e.target.value)}
                placeholder="Write an encouraging message..."
                className="mb-4"
              />
              
              <div className="flex space-x-3">
                <Button
                  onClick={() => setShowHugModal(false)}
                  variant="outline"
                  className="flex-1"
                >
                  Cancel
                </Button>
                <Button
                  onClick={sendVirtualHug}
                  className="flex-1 bg-primary hover:bg-primary/90"
                >
                  Send Hug 💕
                </Button>
              </div>
            </motion.div>
          </motion.div>
        )}

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl md:text-5xl font-bold inner-bloom-text-gradient mb-4">
            Inner Bloom Community 💕
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Connect with amazing women, share your journey, and grow together in our supportive sisterhood.
          </p>
        </motion.div>

        {/* Community Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"
        >
          <Card className="bloom-card border-0">
            <CardContent className="p-4 text-center">
              <Users className="w-8 h-8 text-purple-500 mx-auto mb-2" />
              <div className="text-2xl font-bold">12.5K</div>
              <div className="text-sm text-gray-600">Active Members</div>
            </CardContent>
          </Card>
          
          <Card className="bloom-card border-0">
            <CardContent className="p-4 text-center">
              <Heart className="w-8 h-8 text-red-500 mx-auto mb-2" />
              <div className="text-2xl font-bold">47.2K</div>
              <div className="text-sm text-gray-600">Virtual Hugs</div>
            </CardContent>
          </Card>
          
          <Card className="bloom-card border-0">
            <CardContent className="p-4 text-center">
              <MessageCircle className="w-8 h-8 text-blue-500 mx-auto mb-2" />
              <div className="text-2xl font-bold">156</div>
              <div className="text-sm text-gray-600">Active Circles</div>
            </CardContent>
          </Card>
          
          <Card className="bloom-card border-0">
            <CardContent className="p-4 text-center">
              <Share2 className="w-8 h-8 text-green-500 mx-auto mb-2" />
              <div className="text-2xl font-bold">8.9K</div>
              <div className="text-sm text-gray-600">Stories Shared</div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Tab Navigation */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <div className="flex flex-wrap gap-2 bg-white/50 p-2 rounded-2xl backdrop-blur-sm">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 px-4 py-3 rounded-xl transition-all ${
                    activeTab === tab.id
                      ? 'bg-primary text-white shadow-lg'
                      : 'text-gray-600 hover:bg-white/70'
                  }`}
                >
                  <Icon size={18} />
                  <span className="font-medium">{tab.name}</span>
                </button>
              )
            })}
          </div>
        </motion.div>

        {/* Tab Content */}
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            
            {/* Community Feed Tab */}
            {activeTab === 'feed' && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 space-y-6">
                  {/* Create Post */}
                  <Card className="bloom-card border-0">
                    <CardContent className="p-6">
                      <div className="flex items-start space-x-4">
                        <div className="w-12 h-12 rounded-full bg-gradient-to-r from-pink-400 to-purple-400 flex items-center justify-center text-white text-xl">
                          {user?.username?.[0]?.toUpperCase() || '👤'}
                        </div>
                        <div className="flex-1">
                          <Textarea
                            value={newPost}
                            onChange={(e) => setNewPost(e.target.value)}
                            placeholder="Share your journey, celebrate wins, or ask for support..."
                            className="mb-4 border-pink-200"
                          />
                          <div className="flex justify-between items-center">
                            <div className="flex space-x-2">
                              <Badge variant="outline" className="text-xs">💪 Support</Badge>
                              <Badge variant="outline" className="text-xs">🎉 Celebration</Badge>
                              <Badge variant="outline" className="text-xs">📖 Story</Badge>
                            </div>
                            <Button 
                              className="bg-primary hover:bg-primary/90"
                              disabled={!newPost.trim()}
                            >
                              <Send size={16} className="mr-2" />
                              Share
                            </Button>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  {/* Posts Feed */}
                  {communityPosts.map((post) => (
                    <Card key={post.id} className="bloom-card border-0 hover:shadow-lg transition-all">
                      <CardContent className="p-6">
                        <div className="flex items-start space-x-4 mb-4">
                          <div className="text-3xl">{post.avatar}</div>
                          <div className="flex-1">
                            <div className="flex justify-between items-start">
                              <div>
                                <h3 className="font-bold text-gray-800">{post.author}</h3>
                                <p className="text-gray-500 text-sm">{post.time}</p>
                              </div>
                              <Badge className={`${
                                post.type === 'celebration' ? 'bg-yellow-100 text-yellow-700' :
                                post.type === 'support' ? 'bg-blue-100 text-blue-700' :
                                'bg-green-100 text-green-700'
                              }`}>
                                {post.type === 'celebration' ? '🎉 Celebration' :
                                 post.type === 'support' ? '💙 Support' : '📖 Story'}
                              </Badge>
                            </div>
                          </div>
                        </div>
                        
                        <p className="text-gray-700 mb-4">{post.content}</p>
                        
                        <div className="flex flex-wrap gap-2 mb-4">
                          {post.tags.map((tag) => (
                            <Badge key={tag} variant="outline" className="text-xs">
                              #{tag}
                            </Badge>
                          ))}
                        </div>
                        
                        <div className="flex justify-between items-center pt-4 border-t border-pink-100">
                          <div className="flex space-x-6">
                            <button className="flex items-center space-x-2 text-gray-600 hover:text-red-500 transition-colors">
                              <Heart size={18} />
                              <span className="text-sm">{post.likes}</span>
                            </button>
                            <button className="flex items-center space-x-2 text-gray-600 hover:text-blue-500 transition-colors">
                              <MessageCircle size={18} />
                              <span className="text-sm">{post.comments}</span>
                            </button>
                            <button 
                              onClick={() => sharePost(post.id)}
                              className="flex items-center space-x-2 text-gray-600 hover:text-green-500 transition-colors"
                            >
                              <Share2 size={18} />
                              <span className="text-sm">{post.shares}</span>
                            </button>
                          </div>
                          <Button size="sm" variant="outline">
                            Comment
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
                
                {/* Sidebar */}
                <div className="space-y-6">
                  {/* Quick Actions */}
                  <Card className="bloom-card border-0">
                    <CardHeader>
                      <CardTitle className="flex items-center space-x-2">
                        <Zap className="w-5 h-5" />
                        <span>Quick Actions</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <Button 
                        onClick={() => setShowHugModal(true)}
                        className="w-full justify-start bg-red-50 text-red-700 hover:bg-red-100"
                      >
                        <Heart className="w-4 h-4 mr-2" />
                        Send Virtual Hug
                      </Button>
                      <Button variant="outline" className="w-full justify-start">
                        <Plus className="w-4 h-4 mr-2" />
                        Create Circle
                      </Button>
                      <Button variant="outline" className="w-full justify-start">
                        <Users className="w-4 h-4 mr-2" />
                        Find Sisters
                      </Button>
                    </CardContent>
                  </Card>
                  
                  {/* Trending Topics */}
                  <Card className="bloom-card border-0">
                    <CardHeader>
                      <CardTitle className="flex items-center space-x-2">
                        <TrendingUp className="w-5 h-5" />
                        <span>Trending</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm">#SelfLove</span>
                        <Badge variant="outline" className="text-xs">2.1K posts</Badge>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm">#EntrepreneurLife</span>
                        <Badge variant="outline" className="text-xs">1.8K posts</Badge>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm">#SustainableFashion</span>
                        <Badge variant="outline" className="text-xs">1.5K posts</Badge>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm">#MindfulMoments</span>
                        <Badge variant="outline" className="text-xs">1.2K posts</Badge>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </div>
            )}

            {/* Sisterhood Circles Tab */}
            {activeTab === 'circles' && (
              <div className="space-y-6">
                <div className="flex justify-between items-center">
                  <div>
                    <h2 className="text-2xl font-bold text-gray-800">Your Sisterhood Circles</h2>
                    <p className="text-gray-600">Private groups for deeper connections and support</p>
                  </div>
                  <Button className="bg-primary hover:bg-primary/90">
                    <Plus size={18} className="mr-2" />
                    Create Circle
                  </Button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {sisterhoodCircles.map((circle) => (
                    <Card key={circle.id} className="bloom-card border-0 hover:shadow-lg transition-all">
                      <CardContent className="p-6">
                        <div className={`w-full h-32 rounded-lg bg-gradient-to-r ${circle.color} mb-4 flex items-center justify-center`}>
                          <div className="text-white text-center">
                            <Users className="w-8 h-8 mx-auto mb-2" />
                            <div className="font-bold">{circle.members} members</div>
                          </div>
                        </div>
                        
                        <div className="flex justify-between items-start mb-3">
                          <h3 className="font-bold text-gray-800">{circle.name}</h3>
                          <div className="flex items-center space-x-1">
                            {circle.isPrivate ? (
                              <Lock size={16} className="text-gray-500" />
                            ) : (
                              <Globe size={16} className="text-gray-500" />
                            )}
                          </div>
                        </div>
                        
                        <p className="text-gray-600 text-sm mb-4">{circle.description}</p>
                        
                        <div className="flex justify-between items-center">
                          <div>
                            <Badge variant="outline" className="text-xs mb-2">
                              {circle.category}
                            </Badge>
                            <p className="text-xs text-gray-500">Active {circle.lastActivity}</p>
                          </div>
                          <Button size="sm" className="bg-primary hover:bg-primary/90">
                            Join
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}

            {/* Virtual Hugs Tab */}
            {activeTab === 'hugs' && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div>
                  <Card className="bloom-card border-0 mb-6">
                    <CardContent className="p-8 text-center">
                      <div className="text-6xl mb-4 virtual-hug-animation">🤗</div>
                      <h2 className="text-2xl font-bold inner-bloom-text-gradient mb-4">
                        Virtual Hugs Received
                      </h2>
                      <div className="text-4xl font-bold text-primary mb-2">
                        {user?.totalHugsReceived || 23}
                      </div>
                      <p className="text-gray-600">
                        You've received so much love from the community!
                      </p>
                    </CardContent>
                  </Card>
                  
                  <div className="space-y-4">
                    {virtualHugs.map((hug) => (
                      <Card key={hug.id} className="bloom-card border-0">
                        <CardContent className="p-4">
                          <div className="flex items-start space-x-3">
                            <div className="text-2xl">
                              {hug.type === 'encouragement' ? '💪' :
                               hug.type === 'celebration' ? '🎉' : '💕'}
                            </div>
                            <div className="flex-1">
                              <div className="flex justify-between items-start mb-2">
                                <span className="font-medium text-gray-800">{hug.from}</span>
                                <span className="text-xs text-gray-500">{hug.time}</span>
                              </div>
                              <p className="text-gray-600">{hug.message}</p>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
                
                <div>
                  <Card className="bloom-card border-0 mb-6">
                    <CardContent className="p-8 text-center">
                      <div className="text-6xl mb-4">💝</div>
                      <h2 className="text-2xl font-bold inner-bloom-text-gradient mb-4">
                        Spread the Love
                      </h2>
                      <p className="text-gray-600 mb-6">
                        Send virtual hugs to brighten someone's day and earn community points!
                      </p>
                      <Button 
                        onClick={() => setShowHugModal(true)}
                        className="bg-primary hover:bg-primary/90 px-8 py-3"
                      >
                        Send a Hug 🤗
                      </Button>
                    </CardContent>
                  </Card>
                  
                  <Card className="bloom-card border-0">
                    <CardHeader>
                      <CardTitle>Hug Impact</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div className="flex justify-between">
                          <span>Hugs Sent</span>
                          <span className="font-bold">{user?.totalHugsSent || 15}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Points Earned</span>
                          <span className="font-bold text-primary">+{(user?.totalHugsSent || 15) * 5}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Lives Brightened</span>
                          <span className="font-bold text-green-600">{user?.totalHugsSent || 15}</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </div>
            )}

            {/* Leaderboard Tab */}
            {activeTab === 'leaderboard' && (
              <div className="space-y-6">
                <Card className="bloom-card border-0">
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Crown className="w-5 h-5 text-amber-500" />
                      <span>Community Champions</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {leaderboard.map((member) => (
                        <div 
                          key={member.rank}
                          className={`flex items-center justify-between p-4 rounded-lg ${
                            member.name === 'You' ? 'bg-primary/10 border-2 border-primary' : 'bg-gray-50'
                          }`}
                        >
                          <div className="flex items-center space-x-4">
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${
                              member.rank === 1 ? 'bg-yellow-400 text-yellow-900' :
                              member.rank === 2 ? 'bg-gray-300 text-gray-700' :
                              member.rank === 3 ? 'bg-amber-600 text-white' :
                              'bg-gray-200 text-gray-600'
                            }`}>
                              {member.rank}
                            </div>
                            <div>
                              <div className="flex items-center space-x-2">
                                <span className="font-bold text-gray-800">{member.name}</span>
                                <span className="text-xl">{member.badge}</span>
                              </div>
                              <div className="text-sm text-gray-500">
                                {member.streak} day streak
                              </div>
                            </div>
                          </div>
                          <div className="text-right">
                            <div className="text-xl font-bold text-primary">{member.points}</div>
                            <div className="text-sm text-gray-500">points</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
                
                <Card className="bloom-card border-0 inner-bloom-gradient">
                  <CardContent className="p-8 text-center">
                    <Award className="w-12 h-12 text-white mx-auto mb-4" />
                    <h3 className="text-2xl font-bold text-white mb-4">
                      Climb the Leaderboard!
                    </h3>
                    <p className="text-white/90 mb-6">
                      Earn points by engaging with the community, sharing your journey, and supporting others
                    </p>
                    <div className="grid grid-cols-3 gap-4 text-center">
                      <div>
                        <div className="text-2xl font-bold text-white">+10</div>
                        <div className="text-sm text-white/80">Daily Check-in</div>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-white">+25</div>
                        <div className="text-sm text-white/80">Share Story</div>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-white">+5</div>
                        <div className="text-sm text-white/80">Send Hug</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  )
}

export default Community

