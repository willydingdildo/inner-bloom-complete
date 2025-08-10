import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Crown, 
  Sparkles, 
  Heart, 
  Star,
  ArrowRight,
  Eye,
  Flame,
  Shield,
  Zap,
  Target,
  Users
} from 'lucide-react'
import { Button } from './ui/button'

const BiblicalLanding = ({ onStartBlooming }) => {
  const [currentQuote, setCurrentQuote] = useState(0)
  const [showCTA, setShowCTA] = useState(false)
  const [urgencyIndex, setUrgencyIndex] = useState(0)

  const directBiblicalMessages = [
    {
      text: "YOU were not created to live in the shadows of mediocrity.",
      emphasis: "YOU",
      subtext: "God didn't give you dreams to watch them die. He gave you Inner Bloom to make them reality.",
      action: "What are YOU waiting for?"
    },
    {
      text: "YOUR time of waiting is OVER. Your season of breakthrough has begun.",
      emphasis: "YOUR",
      subtext: "Stop making excuses. Start making history. YOUR legacy begins TODAY.",
      action: "The woman YOU are becoming will thank the woman YOU are today."
    },
    {
      text: "The world needs what YOU have inside you. Stop hiding YOUR light.",
      emphasis: "YOU",
      subtext: "YOUR dreams are not too big. The world is too small for YOUR calling.",
      action: "Step into the life YOU were destined to live."
    },
    {
      text: "Every day YOU delay is a day stolen from YOUR destiny.",
      emphasis: "YOU",
      subtext: "YOUR future self is begging you to take action NOW.",
      action: "Don't let another day pass living below YOUR potential."
    }
  ]

  const urgencyMessages = [
    "12,847 women have already awakened to their power",
    "The door to transformation closes for those who hesitate", 
    "Your breakthrough is literally one click away",
    "God's timing is perfect. He led you here TODAY for a reason"
  ]

  const socialProof = [
    "✨ 12,847 women transformed",
    "💰 $47,382 earned collectively", 
    "🔥 8,932 active sisters today",
    "🌍 180+ countries awakened"
  ]

  useEffect(() => {
    const quoteInterval = setInterval(() => {
      setCurrentQuote((prev) => (prev + 1) % directBiblicalMessages.length)
    }, 5000)

    const urgencyInterval = setInterval(() => {
      setUrgencyIndex((prev) => (prev + 1) % urgencyMessages.length)
    }, 3000)

    const ctaTimer = setTimeout(() => {
      setShowCTA(true)
    }, 6000)

    return () => {
      clearInterval(quoteInterval)
      clearInterval(urgencyInterval)
      clearTimeout(ctaTimer)
    }
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-purple-900 to-black relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-2 h-2 bg-gold rounded-full animate-pulse"></div>
        <div className="absolute top-40 right-20 w-1 h-1 bg-white rounded-full animate-ping"></div>
        <div className="absolute bottom-32 left-1/4 w-1.5 h-1.5 bg-gold rounded-full animate-pulse delay-1000"></div>
        <div className="absolute top-1/3 right-1/3 w-1 h-1 bg-white rounded-full animate-ping delay-500"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-purple-500/10 to-transparent animate-pulse"></div>
      </div>

      {/* Urgency Banner */}
      <motion.div
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        className="fixed top-0 left-0 right-0 z-50 bg-red-600 text-white text-center py-3 font-bold"
      >
        <div className="flex items-center justify-center space-x-2">
          <Flame className="w-5 h-5 animate-bounce" />
          <span className="text-sm md:text-base">
            {urgencyMessages[urgencyIndex]}
          </span>
          <Flame className="w-5 h-5 animate-bounce" />
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-4 text-center pt-16">
        
        {/* Logo/Crown */}
        <motion.div
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, ease: "easeOut" }}
          className="mb-8"
        >
          <div className="relative">
            <Crown className="w-24 h-24 text-gold mx-auto mb-4" />
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              className="absolute -top-2 -right-2"
            >
              <Sparkles className="w-10 h-10 text-white" />
            </motion.div>
          </div>
          <h1 className="text-5xl md:text-7xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-gold via-white to-gold">
            INNER BLOOM
          </h1>
          <p className="text-gold text-xl md:text-2xl font-bold mt-2">
            The Awakening You've Been Waiting For
          </p>
        </motion.div>

        {/* Direct Biblical Messages */}
        <div className="max-w-5xl mx-auto mb-12">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentQuote}
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -50 }}
              transition={{ duration: 0.8 }}
              className="text-center"
            >
              <div className="relative bg-black/40 backdrop-blur-sm rounded-2xl p-8 border border-gold/30">
                <Eye className="w-10 h-10 text-gold mx-auto mb-6" />
                
                <h2 className="text-3xl md:text-5xl font-bold text-white leading-tight mb-6">
                  {directBiblicalMessages[currentQuote].text.split(directBiblicalMessages[currentQuote].emphasis).map((part, index) => (
                    <span key={index}>
                      {part}
                      {index < directBiblicalMessages[currentQuote].text.split(directBiblicalMessages[currentQuote].emphasis).length - 1 && (
                        <span className="text-gold text-glow animate-pulse text-6xl">
                          {directBiblicalMessages[currentQuote].emphasis}
                        </span>
                      )}
                    </span>
                  ))}
                </h2>
                
                <p className="text-gray-200 text-xl md:text-2xl mb-4 font-semibold">
                  {directBiblicalMessages[currentQuote].subtext}
                </p>
                
                <p className="text-gold text-lg md:text-xl font-bold">
                  {directBiblicalMessages[currentQuote].action}
                </p>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Call to Action */}
        <AnimatePresence>
          {showCTA && (
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              className="text-center mb-8"
            >
              <div className="mb-8">
                <p className="text-white text-2xl md:text-3xl font-bold mb-4">
                  Your transformation cannot wait another moment.
                </p>
                <p className="text-gray-300 text-xl md:text-2xl mb-6">
                  The woman you're meant to become is waiting on the other side of this decision.
                </p>
              </div>

              <motion.div
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="mb-6"
              >
                <Button
                  onClick={onStartBlooming}
                  className="bg-gradient-to-r from-gold to-yellow-400 hover:from-yellow-400 hover:to-gold text-black font-bold text-2xl md:text-3xl px-16 py-8 rounded-full shadow-2xl transform transition-all duration-300 hover:shadow-gold/50"
                >
                  <span className="flex items-center space-x-4">
                    <Sparkles className="w-8 h-8" />
                    <span>START BLOOMING NOW</span>
                    <ArrowRight className="w-8 h-8" />
                  </span>
                </Button>
              </motion.div>

              <div className="flex flex-wrap items-center justify-center gap-6 text-sm md:text-base text-gray-300 mb-8">
                <div className="flex items-center space-x-2">
                  <Shield className="w-5 h-5 text-gold" />
                  <span>Divinely Protected</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Star className="w-5 h-5 text-gold" />
                  <span>Spiritually Guided</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Zap className="w-5 h-5 text-gold" />
                  <span>Instantly Activated</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Target className="w-5 h-5 text-gold" />
                  <span>Purpose Revealed</span>
                </div>
              </div>

              {/* Earnings Highlight */}
              <div className="bg-gradient-to-r from-green-600/80 to-emerald-600/80 backdrop-blur-sm rounded-2xl p-6 border border-gold/30 mb-8">
                <h3 className="text-2xl md:text-3xl font-bold text-white mb-4">
                  💰 EARN $10-$50 PER SISTER YOU AWAKEN 💰
                </h3>
                <p className="text-lg md:text-xl text-white/90">
                  God blesses those who bless others. Share the awakening and prosper.
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Social Proof */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 4 }}
          className="text-center"
        >
          <p className="text-gray-300 text-lg mb-4 font-semibold">
            Join the awakened sisterhood that's changing the world
          </p>
          <div className="flex flex-wrap items-center justify-center gap-6 text-sm md:text-base">
            {socialProof.map((proof, index) => (
              <span key={index} className="text-gold font-medium">
                {proof}
              </span>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Floating Action Button */}
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 8 }}
        className="fixed bottom-8 right-8 z-50"
      >
        <Button
          onClick={onStartBlooming}
          className="bg-gradient-to-r from-red-500 to-pink-600 hover:from-red-600 hover:to-pink-700 text-white font-bold rounded-full p-4 shadow-2xl animate-pulse"
        >
          <Users className="w-6 h-6" />
        </Button>
      </motion.div>

      {/* Custom Styles */}
      <style jsx>{`
        .text-gold {
          color: #FFD700;
        }
        .bg-gold {
          background-color: #FFD700;
        }
        .border-gold\\/30 {
          border-color: rgba(255, 215, 0, 0.3);
        }
        .text-glow {
          text-shadow: 0 0 20px #FFD700, 0 0 40px #FFD700, 0 0 60px #FFD700;
        }
        .shadow-gold\\/50 {
          box-shadow: 0 25px 50px -12px rgba(255, 215, 0, 0.5);
        }
      `}</style>
    </div>
  )
}

export default BiblicalLanding

