import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Crown, 
  Star, 
  Sparkles, 
  Check,
  X,
  Zap,
  Heart,
  Users,
  Palette,
  TrendingUp,
  Shield,
  Headphones,
  Gift,
  Infinity,
  CreditCard,
  Calendar,
  Award,
  Lock,
  Unlock
} from 'lucide-react'
import { useUser } from '../contexts/UserContext'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Badge } from './ui/badge'

const Subscription = () => {
  const { user, updateUser } = useUser()
  const [billingCycle, setBillingCycle] = useState('monthly')
  const [selectedPlan, setSelectedPlan] = useState(user?.subscription || 'free')

  const plans = [
    {
      id: 'free',
      name: 'Free',
      price: { monthly: 0, yearly: 0 },
      description: 'Perfect for getting started on your empowerment journey',
      icon: '🌸',
      color: 'from-gray-400 to-gray-500',
      features: [
        'Basic AI companion interactions',
        'Access to community feed',
        'Daily affirmations',
        'Basic wardrobe tracking',
        'Limited style recommendations',
        'Basic goal setting',
        '5 virtual hugs per day'
      ],
      limitations: [
        'Limited AI conversations (10/day)',
        'No premium content access',
        'Basic customer support',
        'Watermarked downloads'
      ]
    },
    {
      id: 'premium',
      name: 'Premium',
      price: { monthly: 29.99, yearly: 299.99 },
      description: 'Unlock your full potential with advanced features',
      icon: '✨',
      color: 'from-pink-400 to-purple-400',
      popular: true,
      features: [
        'Unlimited AI companion conversations',
        'Advanced personality insights',
        'Premium sisterhood circles',
        'AI-powered outfit generation',
        'Sustainable fashion marketplace',
        'Business launchpad access',
        'Priority customer support',
        'Unlimited virtual hugs',
        'Advanced analytics dashboard',
        'Custom goal templates',
        'Premium content library',
        'Early access to new features'
      ],
      limitations: []
    },
    {
      id: 'vip',
      name: 'VIP',
      price: { monthly: 59.99, yearly: 599.99 },
      description: 'The ultimate empowerment experience with exclusive perks',
      icon: '👑',
      color: 'from-yellow-400 to-orange-400',
      features: [
        'Everything in Premium',
        'Personal AI coach with voice calls',
        'Exclusive VIP community access',
        'One-on-one mentor matching',
        'Custom business plan creation',
        'Investor network access',
        'White-glove onboarding',
        'Monthly group coaching calls',
        'Exclusive VIP events',
        'Personal brand consultation',
        'Advanced market research tools',
        'Priority feature requests',
        'Dedicated success manager',
        'Custom integrations'
      ],
      limitations: []
    }
  ]

  const addOns = [
    {
      id: 'personal-stylist',
      name: 'Personal AI Stylist',
      price: 19.99,
      description: 'Get personalized styling advice and outfit curation',
      icon: '👗'
    },
    {
      id: 'business-accelerator',
      name: 'Business Accelerator',
      price: 39.99,
      description: 'Advanced entrepreneurship tools and mentorship',
      icon: '🚀'
    },
    {
      id: 'wellness-coach',
      name: 'Wellness Coach',
      price: 24.99,
      description: 'Personalized health and wellness guidance',
      icon: '🧘‍♀️'
    }
  ]

  const testimonials = [
    {
      name: 'Sarah M.',
      plan: 'VIP',
      text: 'Inner Bloom VIP transformed my life! The personal AI coach helped me launch my business and the investor network connected me with amazing opportunities.',
      rating: 5,
      avatar: '👩‍💼'
    },
    {
      name: 'Emma K.',
      plan: 'Premium',
      text: 'The Premium plan is worth every penny. The AI styling feature saved me hours and the sisterhood circles provide incredible support.',
      rating: 5,
      avatar: '👩‍🎨'
    },
    {
      name: 'Lisa R.',
      plan: 'Premium',
      text: 'I love the sustainable fashion marketplace! I\'ve saved money and helped the environment while looking amazing.',
      rating: 5,
      avatar: '👩‍🌾'
    }
  ]

  const benefits = [
    {
      title: 'Save with Annual Billing',
      description: 'Get 2 months free when you choose yearly billing',
      icon: Calendar,
      color: 'text-green-600'
    },
    {
      title: '30-Day Money Back Guarantee',
      description: 'Not satisfied? Get a full refund within 30 days',
      icon: Shield,
      color: 'text-blue-600'
    },
    {
      title: 'Cancel Anytime',
      description: 'No long-term commitments. Cancel or change plans anytime',
      icon: Unlock,
      color: 'text-purple-600'
    },
    {
      title: '24/7 Support',
      description: 'Premium and VIP members get priority customer support',
      icon: Headphones,
      color: 'text-orange-600'
    }
  ]

  const handleUpgrade = (planId) => {
    if (planId === 'free') return
    
    // Simulate payment process
    setSelectedPlan(planId)
    updateUser({ subscription: planId })
    
    // Show success message
    alert(`🎉 Welcome to Inner Bloom ${planId.charAt(0).toUpperCase() + planId.slice(1)}! Your journey to empowerment just got supercharged!`)
  }

  const getSavings = (plan) => {
    if (plan.price.yearly === 0) return 0
    const monthlyCost = plan.price.monthly * 12
    return monthlyCost - plan.price.yearly
  }

  const getCurrentPlanFeatures = () => {
    const currentPlan = plans.find(p => p.id === user?.subscription) || plans[0]
    return currentPlan.features
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-amber-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold inner-bloom-text-gradient mb-4">
            Choose Your Empowerment Plan 💎
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            Unlock your full potential with features designed to accelerate your personal and professional growth.
          </p>
          
          {/* Billing Toggle */}
          <div className="flex items-center justify-center space-x-4 mb-8">
            <span className={`font-medium ${billingCycle === 'monthly' ? 'text-primary' : 'text-gray-500'}`}>
              Monthly
            </span>
            <button
              onClick={() => setBillingCycle(billingCycle === 'monthly' ? 'yearly' : 'monthly')}
              className={`relative w-14 h-7 rounded-full transition-colors ${
                billingCycle === 'yearly' ? 'bg-primary' : 'bg-gray-300'
              }`}
            >
              <div className={`absolute w-5 h-5 bg-white rounded-full top-1 transition-transform ${
                billingCycle === 'yearly' ? 'translate-x-8' : 'translate-x-1'
              }`} />
            </button>
            <span className={`font-medium ${billingCycle === 'yearly' ? 'text-primary' : 'text-gray-500'}`}>
              Yearly
            </span>
            {billingCycle === 'yearly' && (
              <Badge className="bg-green-100 text-green-700 ml-2">
                Save up to 17%
              </Badge>
            )}
          </div>
        </motion.div>

        {/* Pricing Plans */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12"
        >
          {plans.map((plan, index) => (
            <motion.div
              key={plan.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * index }}
              className="relative"
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <Badge className="bg-primary text-white px-4 py-1">
                    Most Popular ⭐
                  </Badge>
                </div>
              )}
              
              <Card className={`bloom-card border-0 h-full ${
                plan.id === user?.subscription ? 'ring-2 ring-primary' : ''
              } ${plan.popular ? 'scale-105 shadow-xl' : ''}`}>
                <CardHeader className="text-center pb-4">
                  <div className={`w-16 h-16 rounded-full bg-gradient-to-r ${plan.color} flex items-center justify-center text-white text-2xl mx-auto mb-4`}>
                    {plan.icon}
                  </div>
                  <CardTitle className="text-2xl font-bold">{plan.name}</CardTitle>
                  <p className="text-gray-600 text-sm">{plan.description}</p>
                  
                  <div className="mt-4">
                    <div className="text-4xl font-bold text-gray-800">
                      ${billingCycle === 'monthly' ? plan.price.monthly : Math.round(plan.price.yearly / 12)}
                      <span className="text-lg font-normal text-gray-500">/month</span>
                    </div>
                    {billingCycle === 'yearly' && plan.price.yearly > 0 && (
                      <div className="text-sm text-green-600 font-medium">
                        Save ${getSavings(plan)} per year
                      </div>
                    )}
                  </div>
                </CardHeader>
                
                <CardContent className="pt-0">
                  <div className="space-y-3 mb-6">
                    {plan.features.map((feature, featureIndex) => (
                      <div key={featureIndex} className="flex items-start space-x-3">
                        <Check className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                        <span className="text-sm text-gray-700">{feature}</span>
                      </div>
                    ))}
                    
                    {plan.limitations.map((limitation, limitIndex) => (
                      <div key={limitIndex} className="flex items-start space-x-3">
                        <X className="w-5 h-5 text-red-400 mt-0.5 flex-shrink-0" />
                        <span className="text-sm text-gray-500">{limitation}</span>
                      </div>
                    ))}
                  </div>
                  
                  <Button
                    onClick={() => handleUpgrade(plan.id)}
                    disabled={plan.id === user?.subscription}
                    className={`w-full ${
                      plan.id === user?.subscription
                        ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                        : plan.popular
                        ? 'bg-primary hover:bg-primary/90'
                        : 'bg-gray-800 hover:bg-gray-700'
                    }`}
                  >
                    {plan.id === user?.subscription ? (
                      <>
                        <Crown className="w-4 h-4 mr-2" />
                        Current Plan
                      </>
                    ) : plan.id === 'free' ? (
                      'Get Started Free'
                    ) : (
                      <>
                        <Sparkles className="w-4 h-4 mr-2" />
                        Upgrade to {plan.name}
                      </>
                    )}
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </motion.div>

        {/* Add-ons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mb-12"
        >
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">
            Enhance Your Experience
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {addOns.map((addon) => (
              <Card key={addon.id} className="bloom-card border-0">
                <CardContent className="p-6 text-center">
                  <div className="text-4xl mb-4">{addon.icon}</div>
                  <h3 className="text-lg font-bold text-gray-800 mb-2">{addon.name}</h3>
                  <p className="text-gray-600 text-sm mb-4">{addon.description}</p>
                  <div className="text-2xl font-bold text-primary mb-4">
                    ${addon.price}/month
                  </div>
                  <Button variant="outline" className="w-full">
                    Add to Plan
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </motion.div>

        {/* Benefits */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-12"
        >
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">
            Why Choose Inner Bloom?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {benefits.map((benefit, index) => {
              const Icon = benefit.icon
              return (
                <Card key={index} className="bloom-card border-0 text-center">
                  <CardContent className="p-6">
                    <Icon className={`w-12 h-12 mx-auto mb-4 ${benefit.color}`} />
                    <h3 className="font-bold text-gray-800 mb-2">{benefit.title}</h3>
                    <p className="text-gray-600 text-sm">{benefit.description}</p>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </motion.div>

        {/* Testimonials */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mb-12"
        >
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">
            What Our Members Say
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {testimonials.map((testimonial, index) => (
              <Card key={index} className="bloom-card border-0">
                <CardContent className="p-6">
                  <div className="flex items-center mb-4">
                    <div className="text-3xl mr-3">{testimonial.avatar}</div>
                    <div>
                      <h4 className="font-bold text-gray-800">{testimonial.name}</h4>
                      <Badge className="bg-primary/10 text-primary text-xs">
                        {testimonial.plan} Member
                      </Badge>
                    </div>
                  </div>
                  <p className="text-gray-600 text-sm mb-4">"{testimonial.text}"</p>
                  <div className="flex space-x-1">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="w-4 h-4 text-yellow-400 fill-current" />
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </motion.div>

        {/* Current Plan Status */}
        {user?.subscription && user.subscription !== 'free' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="mb-8"
          >
            <Card className="bloom-card border-0 inner-bloom-gradient">
              <CardContent className="p-8 text-center">
                <Crown className="w-12 h-12 text-white mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-white mb-4">
                  You're a {user.subscription.charAt(0).toUpperCase() + user.subscription.slice(1)} Member! 🎉
                </h3>
                <p className="text-white/90 mb-6">
                  Thank you for being part of our empowered community. Your journey to greatness is accelerated!
                </p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                  <div>
                    <div className="text-2xl font-bold text-white">Unlimited</div>
                    <div className="text-sm text-white/80">AI Conversations</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-white">Premium</div>
                    <div className="text-sm text-white/80">Content Access</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-white">Priority</div>
                    <div className="text-sm text-white/80">Support</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* FAQ */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="text-center"
        >
          <h2 className="text-3xl font-bold text-gray-800 mb-8">
            Questions? We're Here to Help
          </h2>
          <div className="max-w-2xl mx-auto">
            <p className="text-gray-600 mb-6">
              Our customer success team is available 24/7 to help you choose the perfect plan and make the most of your Inner Bloom experience.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button className="bg-primary hover:bg-primary/90">
                <Headphones className="w-4 h-4 mr-2" />
                Contact Support
              </Button>
              <Button variant="outline">
                <Gift className="w-4 h-4 mr-2" />
                View FAQ
              </Button>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Subscription

