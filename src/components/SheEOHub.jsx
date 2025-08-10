import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  TrendingUp, 
  DollarSign, 
  Users, 
  Lightbulb,
  Target,
  BarChart3,
  Rocket,
  Crown,
  Star,
  Calendar,
  MessageCircle,
  Award,
  Briefcase,
  Network,
  BookOpen,
  Video,
  Coffee,
  Handshake
} from 'lucide-react'
import { useUser } from '../contexts/UserContext'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Input } from './ui/input'
import { Badge } from './ui/badge'
import { Progress } from './ui/progress'

const SheEOHub = () => {
  const { user } = useUser()
  const [activeTab, setActiveTab] = useState('dashboard')

  const tabs = [
    { id: 'dashboard', name: 'Dashboard', icon: BarChart3 },
    { id: 'launchpad', name: 'Launchpad', icon: Rocket },
    { id: 'network', name: 'Network', icon: Network },
    { id: 'resources', name: 'Resources', icon: BookOpen },
    { id: 'funding', name: 'Funding', icon: DollarSign }
  ]

  const businessMetrics = [
    { label: 'Revenue Goal', value: '$50,000', progress: 65, color: 'text-green-600' },
    { label: 'Customer Acquisition', value: '127', progress: 42, color: 'text-blue-600' },
    { label: 'Product Development', value: '78%', progress: 78, color: 'text-purple-600' },
    { label: 'Market Validation', value: '91%', progress: 91, color: 'text-orange-600' }
  ]

  const launchpadSteps = [
    {
      id: 1,
      title: 'Business Idea Validation',
      description: 'Test and refine your business concept',
      status: 'completed',
      progress: 100,
      modules: ['Market Research', 'Customer Interviews', 'Competitor Analysis']
    },
    {
      id: 2,
      title: 'Business Plan Creation',
      description: 'Build a comprehensive business strategy',
      status: 'in-progress',
      progress: 60,
      modules: ['Executive Summary', 'Financial Projections', 'Marketing Strategy']
    },
    {
      id: 3,
      title: 'MVP Development',
      description: 'Create your minimum viable product',
      status: 'pending',
      progress: 0,
      modules: ['Product Design', 'Development', 'Testing']
    },
    {
      id: 4,
      title: 'Launch Strategy',
      description: 'Plan and execute your market entry',
      status: 'pending',
      progress: 0,
      modules: ['Go-to-Market', 'PR Strategy', 'Launch Campaign']
    }
  ]

  const networkConnections = [
    {
      id: 1,
      name: 'Sarah Chen',
      title: 'Tech Entrepreneur',
      company: 'AI Innovations Inc.',
      expertise: ['AI/ML', 'SaaS', 'Fundraising'],
      avatar: '👩‍💼',
      status: 'mentor',
      rating: 4.9
    },
    {
      id: 2,
      name: 'Maria Rodriguez',
      title: 'Marketing Director',
      company: 'Growth Partners',
      expertise: ['Digital Marketing', 'Brand Strategy', 'Growth Hacking'],
      avatar: '👩‍🎨',
      status: 'peer',
      rating: 4.8
    },
    {
      id: 3,
      name: 'Jennifer Kim',
      title: 'Angel Investor',
      company: 'Women Fund',
      expertise: ['Investment', 'Strategy', 'Scaling'],
      avatar: '👩‍💼',
      status: 'investor',
      rating: 5.0
    }
  ]

  const resources = [
    {
      category: 'Courses',
      items: [
        { title: 'Business Model Canvas Masterclass', duration: '2h 30m', rating: 4.9, type: 'video' },
        { title: 'Financial Planning for Startups', duration: '3h 15m', rating: 4.8, type: 'video' },
        { title: 'Digital Marketing Fundamentals', duration: '4h 20m', rating: 4.7, type: 'video' }
      ]
    },
    {
      category: 'Templates',
      items: [
        { title: 'Pitch Deck Template', downloads: '2.1K', rating: 4.9, type: 'document' },
        { title: 'Business Plan Template', downloads: '1.8K', rating: 4.8, type: 'document' },
        { title: 'Financial Model Template', downloads: '1.5K', rating: 4.7, type: 'document' }
      ]
    },
    {
      category: 'Tools',
      items: [
        { title: 'Market Research Toolkit', users: '5.2K', rating: 4.9, type: 'tool' },
        { title: 'Customer Validation Framework', users: '3.8K', rating: 4.8, type: 'tool' },
        { title: 'Competitive Analysis Tool', users: '2.9K', rating: 4.6, type: 'tool' }
      ]
    }
  ]

  const fundingOpportunities = [
    {
      id: 1,
      name: 'Women Founders Grant',
      amount: '$25,000',
      type: 'Grant',
      deadline: '2024-03-15',
      requirements: ['Women-led startup', 'Pre-seed stage', 'Tech focus'],
      status: 'open'
    },
    {
      id: 2,
      name: 'Angel Investor Network',
      amount: '$50K - $250K',
      type: 'Investment',
      deadline: 'Rolling',
      requirements: ['MVP ready', 'Traction metrics', 'Scalable model'],
      status: 'open'
    },
    {
      id: 3,
      name: 'Innovation Challenge',
      amount: '$100,000',
      type: 'Competition',
      deadline: '2024-04-30',
      requirements: ['Innovative solution', 'Social impact', 'Prototype'],
      status: 'open'
    }
  ]

  const upcomingEvents = [
    {
      id: 1,
      title: 'Women in Tech Networking',
      date: 'Mar 15, 2024',
      time: '6:00 PM',
      type: 'Networking',
      attendees: 47
    },
    {
      id: 2,
      title: 'Pitch Practice Session',
      date: 'Mar 18, 2024',
      time: '2:00 PM',
      type: 'Workshop',
      attendees: 23
    },
    {
      id: 3,
      title: 'Investor Panel Discussion',
      date: 'Mar 22, 2024',
      time: '7:00 PM',
      type: 'Panel',
      attendees: 156
    }
  ]

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-700'
      case 'in-progress': return 'bg-blue-100 text-blue-700'
      case 'pending': return 'bg-gray-100 text-gray-700'
      default: return 'bg-gray-100 text-gray-700'
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'mentor': return '🎓'
      case 'peer': return '🤝'
      case 'investor': return '💰'
      default: return '👤'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-red-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl md:text-5xl font-bold inner-bloom-text-gradient mb-4">
            She-EO Hub 👑
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Your entrepreneurial command center. Build, launch, and scale your business with AI-powered guidance and a supportive community.
          </p>
        </motion.div>

        {/* Quick Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"
        >
          <Card className="bloom-card border-0">
            <CardContent className="p-4 text-center">
              <Rocket className="w-8 h-8 text-orange-500 mx-auto mb-2" />
              <div className="text-2xl font-bold">3</div>
              <div className="text-sm text-gray-600">Active Projects</div>
            </CardContent>
          </Card>
          
          <Card className="bloom-card border-0">
            <CardContent className="p-4 text-center">
              <Network className="w-8 h-8 text-purple-500 mx-auto mb-2" />
              <div className="text-2xl font-bold">47</div>
              <div className="text-sm text-gray-600">Network Connections</div>
            </CardContent>
          </Card>
          
          <Card className="bloom-card border-0">
            <CardContent className="p-4 text-center">
              <DollarSign className="w-8 h-8 text-green-500 mx-auto mb-2" />
              <div className="text-2xl font-bold">$12K</div>
              <div className="text-sm text-gray-600">Revenue Generated</div>
            </CardContent>
          </Card>
          
          <Card className="bloom-card border-0">
            <CardContent className="p-4 text-center">
              <Award className="w-8 h-8 text-blue-500 mx-auto mb-2" />
              <div className="text-2xl font-bold">2</div>
              <div className="text-sm text-gray-600">Milestones Achieved</div>
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
            
            {/* Dashboard Tab */}
            {activeTab === 'dashboard' && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 space-y-6">
                  {/* Business Metrics */}
                  <Card className="bloom-card border-0">
                    <CardHeader>
                      <CardTitle className="flex items-center space-x-2">
                        <BarChart3 className="w-5 h-5" />
                        <span>Business Metrics</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {businessMetrics.map((metric, index) => (
                          <div key={index} className="space-y-3">
                            <div className="flex justify-between items-center">
                              <span className="font-medium text-gray-700">{metric.label}</span>
                              <span className={`font-bold ${metric.color}`}>{metric.value}</span>
                            </div>
                            <Progress value={metric.progress} className="h-2" />
                            <div className="text-sm text-gray-500">{metric.progress}% of target</div>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>

                  {/* Recent Activity */}
                  <Card className="bloom-card border-0">
                    <CardHeader>
                      <CardTitle>Recent Activity</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div className="flex items-start space-x-3">
                          <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center">
                            <Target className="w-4 h-4 text-green-600" />
                          </div>
                          <div className="flex-1">
                            <p className="text-gray-800">Completed market research milestone</p>
                            <p className="text-sm text-gray-500">2 hours ago</p>
                          </div>
                        </div>
                        
                        <div className="flex items-start space-x-3">
                          <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
                            <MessageCircle className="w-4 h-4 text-blue-600" />
                          </div>
                          <div className="flex-1">
                            <p className="text-gray-800">Connected with mentor Sarah Chen</p>
                            <p className="text-sm text-gray-500">1 day ago</p>
                          </div>
                        </div>
                        
                        <div className="flex items-start space-x-3">
                          <div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center">
                            <Lightbulb className="w-4 h-4 text-purple-600" />
                          </div>
                          <div className="flex-1">
                            <p className="text-gray-800">Updated business plan with AI suggestions</p>
                            <p className="text-sm text-gray-500">3 days ago</p>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
                
                {/* Sidebar */}
                <div className="space-y-6">
                  {/* Upcoming Events */}
                  <Card className="bloom-card border-0">
                    <CardHeader>
                      <CardTitle className="flex items-center space-x-2">
                        <Calendar className="w-5 h-5" />
                        <span>Upcoming Events</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      {upcomingEvents.slice(0, 3).map((event) => (
                        <div key={event.id} className="border-l-4 border-primary pl-4">
                          <h4 className="font-medium text-gray-800">{event.title}</h4>
                          <p className="text-sm text-gray-600">{event.date} • {event.time}</p>
                          <p className="text-xs text-gray-500">{event.attendees} attending</p>
                        </div>
                      ))}
                      <Button variant="outline" className="w-full">
                        View All Events
                      </Button>
                    </CardContent>
                  </Card>
                  
                  {/* AI Insights */}
                  <Card className="bloom-card border-0">
                    <CardHeader>
                      <CardTitle className="flex items-center space-x-2">
                        <Star className="w-5 h-5" />
                        <span>AI Insights</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                          <h4 className="font-bold text-blue-800 mb-2">💡 Opportunity</h4>
                          <p className="text-blue-700 text-sm">
                            Based on your market research, consider expanding to the B2B segment. 73% growth potential identified.
                          </p>
                        </div>
                        
                        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                          <h4 className="font-bold text-green-800 mb-2">📈 Trend Alert</h4>
                          <p className="text-green-700 text-sm">
                            Your industry is experiencing 15% growth. Perfect timing for your launch strategy.
                          </p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </div>
            )}

            {/* Launchpad Tab */}
            {activeTab === 'launchpad' && (
              <div className="space-y-6">
                <Card className="bloom-card border-0">
                  <CardContent className="p-8 text-center">
                    <Rocket className="w-16 h-16 text-orange-500 mx-auto mb-4" />
                    <h2 className="text-2xl font-bold inner-bloom-text-gradient mb-4">
                      Business Launchpad 🚀
                    </h2>
                    <p className="text-gray-600 mb-6">
                      Follow our proven framework to take your business from idea to launch
                    </p>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-primary">60%</div>
                      <div className="text-sm text-gray-600">Overall Progress</div>
                    </div>
                  </CardContent>
                </Card>

                <div className="space-y-6">
                  {launchpadSteps.map((step) => (
                    <Card key={step.id} className="bloom-card border-0">
                      <CardContent className="p-6">
                        <div className="flex items-start space-x-4">
                          <div className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-white ${
                            step.status === 'completed' ? 'bg-green-500' :
                            step.status === 'in-progress' ? 'bg-blue-500' :
                            'bg-gray-400'
                          }`}>
                            {step.id}
                          </div>
                          
                          <div className="flex-1">
                            <div className="flex justify-between items-start mb-3">
                              <div>
                                <h3 className="text-lg font-bold text-gray-800">{step.title}</h3>
                                <p className="text-gray-600">{step.description}</p>
                              </div>
                              <Badge className={getStatusColor(step.status)}>
                                {step.status.replace('-', ' ')}
                              </Badge>
                            </div>
                            
                            <div className="mb-4">
                              <div className="flex justify-between text-sm mb-2">
                                <span>Progress</span>
                                <span>{step.progress}%</span>
                              </div>
                              <Progress value={step.progress} className="h-2" />
                            </div>
                            
                            <div className="flex flex-wrap gap-2 mb-4">
                              {step.modules.map((module, index) => (
                                <Badge key={index} variant="outline" className="text-xs">
                                  {module}
                                </Badge>
                              ))}
                            </div>
                            
                            <Button 
                              className={`${
                                step.status === 'completed' ? 'bg-green-500 hover:bg-green-600' :
                                step.status === 'in-progress' ? 'bg-blue-500 hover:bg-blue-600' :
                                'bg-gray-400 hover:bg-gray-500'
                              }`}
                              disabled={step.status === 'pending'}
                            >
                              {step.status === 'completed' ? 'Review' :
                               step.status === 'in-progress' ? 'Continue' :
                               'Start'}
                            </Button>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}

            {/* Network Tab */}
            {activeTab === 'network' && (
              <div className="space-y-6">
                <div className="flex justify-between items-center">
                  <div>
                    <h2 className="text-2xl font-bold text-gray-800">Your Professional Network</h2>
                    <p className="text-gray-600">Connect with mentors, peers, and investors</p>
                  </div>
                  <Button className="bg-primary hover:bg-primary/90">
                    <Users className="w-4 h-4 mr-2" />
                    Find Connections
                  </Button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {networkConnections.map((connection) => (
                    <Card key={connection.id} className="bloom-card border-0 hover:shadow-lg transition-all">
                      <CardContent className="p-6">
                        <div className="text-center mb-4">
                          <div className="text-4xl mb-2">{connection.avatar}</div>
                          <h3 className="font-bold text-gray-800">{connection.name}</h3>
                          <p className="text-gray-600 text-sm">{connection.title}</p>
                          <p className="text-gray-500 text-xs">{connection.company}</p>
                        </div>
                        
                        <div className="flex justify-between items-center mb-4">
                          <Badge className={`${
                            connection.status === 'mentor' ? 'bg-purple-100 text-purple-700' :
                            connection.status === 'peer' ? 'bg-blue-100 text-blue-700' :
                            'bg-green-100 text-green-700'
                          }`}>
                            {getStatusIcon(connection.status)} {connection.status}
                          </Badge>
                          <div className="flex items-center space-x-1">
                            <Star className="w-4 h-4 text-yellow-500 fill-current" />
                            <span className="text-sm font-medium">{connection.rating}</span>
                          </div>
                        </div>
                        
                        <div className="flex flex-wrap gap-1 mb-4">
                          {connection.expertise.map((skill, index) => (
                            <Badge key={index} variant="outline" className="text-xs">
                              {skill}
                            </Badge>
                          ))}
                        </div>
                        
                        <div className="flex space-x-2">
                          <Button size="sm" className="flex-1 bg-primary hover:bg-primary/90">
                            <MessageCircle className="w-4 h-4 mr-1" />
                            Message
                          </Button>
                          <Button size="sm" variant="outline" className="flex-1">
                            <Coffee className="w-4 h-4 mr-1" />
                            Meet
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}

            {/* Resources Tab */}
            {activeTab === 'resources' && (
              <div className="space-y-8">
                {resources.map((category) => (
                  <div key={category.category}>
                    <h2 className="text-2xl font-bold text-gray-800 mb-6">{category.category}</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {category.items.map((item, index) => (
                        <Card key={index} className="bloom-card border-0 hover:shadow-lg transition-all">
                          <CardContent className="p-6">
                            <div className="flex items-start space-x-3 mb-4">
                              <div className="w-12 h-12 rounded-lg bg-gradient-to-r from-orange-400 to-red-400 flex items-center justify-center">
                                {item.type === 'video' ? <Video className="w-6 h-6 text-white" /> :
                                 item.type === 'document' ? <BookOpen className="w-6 h-6 text-white" /> :
                                 <Briefcase className="w-6 h-6 text-white" />}
                              </div>
                              <div className="flex-1">
                                <h3 className="font-bold text-gray-800 mb-2">{item.title}</h3>
                                <div className="flex items-center space-x-4 text-sm text-gray-600">
                                  {item.duration && <span>⏱️ {item.duration}</span>}
                                  {item.downloads && <span>📥 {item.downloads}</span>}
                                  {item.users && <span>👥 {item.users}</span>}
                                  <div className="flex items-center space-x-1">
                                    <Star className="w-4 h-4 text-yellow-500 fill-current" />
                                    <span>{item.rating}</span>
                                  </div>
                                </div>
                              </div>
                            </div>
                            <Button className="w-full bg-primary hover:bg-primary/90">
                              {item.type === 'video' ? 'Watch Now' :
                               item.type === 'document' ? 'Download' :
                               'Use Tool'}
                            </Button>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Funding Tab */}
            {activeTab === 'funding' && (
              <div className="space-y-6">
                <Card className="bloom-card border-0">
                  <CardContent className="p-8 text-center">
                    <DollarSign className="w-16 h-16 text-green-500 mx-auto mb-4" />
                    <h2 className="text-2xl font-bold inner-bloom-text-gradient mb-4">
                      Funding Opportunities 💰
                    </h2>
                    <p className="text-gray-600 mb-6">
                      Discover grants, investments, and competitions tailored for women entrepreneurs
                    </p>
                    <div className="grid grid-cols-3 gap-6 text-center">
                      <div>
                        <div className="text-2xl font-bold text-green-600">$2.3M</div>
                        <div className="text-sm text-gray-600">Available Funding</div>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-blue-600">47</div>
                        <div className="text-sm text-gray-600">Active Opportunities</div>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-purple-600">89%</div>
                        <div className="text-sm text-gray-600">Success Rate</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <div className="space-y-6">
                  {fundingOpportunities.map((opportunity) => (
                    <Card key={opportunity.id} className="bloom-card border-0 hover:shadow-lg transition-all">
                      <CardContent className="p-6">
                        <div className="flex justify-between items-start mb-4">
                          <div>
                            <h3 className="text-xl font-bold text-gray-800">{opportunity.name}</h3>
                            <div className="flex items-center space-x-4 mt-2">
                              <span className="text-2xl font-bold text-green-600">{opportunity.amount}</span>
                              <Badge className={`${
                                opportunity.type === 'Grant' ? 'bg-green-100 text-green-700' :
                                opportunity.type === 'Investment' ? 'bg-blue-100 text-blue-700' :
                                'bg-purple-100 text-purple-700'
                              }`}>
                                {opportunity.type}
                              </Badge>
                            </div>
                          </div>
                          <Badge className="bg-green-100 text-green-700">
                            {opportunity.status}
                          </Badge>
                        </div>
                        
                        <div className="mb-4">
                          <p className="text-sm text-gray-600 mb-2">
                            <strong>Deadline:</strong> {opportunity.deadline}
                          </p>
                          <div>
                            <p className="text-sm font-medium text-gray-700 mb-2">Requirements:</p>
                            <div className="flex flex-wrap gap-2">
                              {opportunity.requirements.map((req, index) => (
                                <Badge key={index} variant="outline" className="text-xs">
                                  {req}
                                </Badge>
                              ))}
                            </div>
                          </div>
                        </div>
                        
                        <div className="flex space-x-3">
                          <Button className="flex-1 bg-primary hover:bg-primary/90">
                            <Handshake className="w-4 h-4 mr-2" />
                            Apply Now
                          </Button>
                          <Button variant="outline" className="flex-1">
                            Learn More
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  )
}

export default SheEOHub

