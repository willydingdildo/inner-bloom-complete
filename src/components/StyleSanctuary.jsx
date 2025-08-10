import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Palette, 
  Camera, 
  Recycle, 
  Heart, 
  ShoppingBag,
  Sparkles,
  Leaf,
  Users,
  Star,
  Plus,
  Search,
  Filter,
  ArrowRight,
  Shirt,
  Crown
} from 'lucide-react'
import { useUser } from '../contexts/UserContext'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Input } from './ui/input'
import { Badge } from './ui/badge'

const StyleSanctuary = () => {
  const { user } = useUser()
  const [activeTab, setActiveTab] = useState('wardrobe')
  const [selectedCategory, setSelectedCategory] = useState('all')

  const tabs = [
    { id: 'wardrobe', name: 'My Wardrobe', icon: Shirt },
    { id: 'outfits', name: 'AI Styling', icon: Sparkles },
    { id: 'marketplace', name: 'Marketplace', icon: ShoppingBag },
    { id: 'sustainable', name: 'Eco Guide', icon: Leaf }
  ]

  const categories = [
    { id: 'all', name: 'All Items', count: 47 },
    { id: 'tops', name: 'Tops', count: 15 },
    { id: 'bottoms', name: 'Bottoms', count: 12 },
    { id: 'dresses', name: 'Dresses', count: 8 },
    { id: 'accessories', name: 'Accessories', count: 12 }
  ]

  const wardrobeItems = [
    {
      id: 1,
      name: 'Sustainable Cotton Blouse',
      category: 'tops',
      color: 'White',
      brand: 'Everlane',
      sustainabilityScore: 9,
      image: '👕',
      lastWorn: '3 days ago',
      wearCount: 12
    },
    {
      id: 2,
      name: 'Vintage Denim Jacket',
      category: 'tops',
      color: 'Blue',
      brand: 'Vintage',
      sustainabilityScore: 10,
      image: '🧥',
      lastWorn: '1 week ago',
      wearCount: 8
    },
    {
      id: 3,
      name: 'Organic Cotton Dress',
      category: 'dresses',
      color: 'Pink',
      brand: 'Reformation',
      sustainabilityScore: 8,
      image: '👗',
      lastWorn: '2 days ago',
      wearCount: 5
    },
    {
      id: 4,
      name: 'Recycled Polyester Pants',
      category: 'bottoms',
      color: 'Black',
      brand: 'Patagonia',
      sustainabilityScore: 7,
      image: '👖',
      lastWorn: '5 days ago',
      wearCount: 15
    }
  ]

  const aiOutfits = [
    {
      id: 1,
      name: 'Confident Professional',
      occasion: 'Work Meeting',
      items: ['Sustainable Cotton Blouse', 'Recycled Polyester Pants', 'Statement Necklace'],
      sustainabilityScore: 8.5,
      likes: 24,
      aiGenerated: true
    },
    {
      id: 2,
      name: 'Weekend Warrior',
      occasion: 'Casual Outing',
      items: ['Vintage Denim Jacket', 'Organic Cotton Dress', 'Eco-friendly Sneakers'],
      sustainabilityScore: 9.2,
      likes: 31,
      aiGenerated: true
    },
    {
      id: 3,
      name: 'Date Night Elegance',
      occasion: 'Dinner Date',
      items: ['Silk Blouse', 'High-waisted Jeans', 'Vintage Accessories'],
      sustainabilityScore: 7.8,
      likes: 18,
      aiGenerated: false
    }
  ]

  const marketplaceItems = [
    {
      id: 1,
      name: 'Designer Silk Scarf',
      seller: 'Sarah M.',
      price: 45,
      originalPrice: 120,
      condition: 'Like New',
      sustainabilityScore: 9,
      image: '🧣',
      location: 'New York',
      type: 'sale'
    },
    {
      id: 2,
      name: 'Vintage Leather Boots',
      seller: 'Emma K.',
      price: 0,
      swapFor: 'Designer Handbag',
      condition: 'Good',
      sustainabilityScore: 10,
      image: '👢',
      location: 'California',
      type: 'swap'
    },
    {
      id: 3,
      name: 'Sustainable Wool Coat',
      seller: 'Lisa R.',
      price: 89,
      originalPrice: 250,
      condition: 'Excellent',
      sustainabilityScore: 8,
      image: '🧥',
      location: 'Texas',
      type: 'sale'
    }
  ]

  const sustainabilityTips = [
    {
      title: 'Quality Over Quantity',
      description: 'Invest in well-made pieces that will last for years',
      icon: '💎',
      impact: 'High'
    },
    {
      title: 'Care for Your Clothes',
      description: 'Proper washing and storage extends garment life',
      icon: '🧼',
      impact: 'Medium'
    },
    {
      title: 'Swap & Share',
      description: 'Exchange clothes with friends and community',
      icon: '🔄',
      impact: 'High'
    },
    {
      title: 'Repair & Upcycle',
      description: 'Give new life to damaged or outdated pieces',
      icon: '✂️',
      impact: 'Medium'
    }
  ]

  const getSustainabilityColor = (score) => {
    if (score >= 8) return 'text-green-600 bg-green-100'
    if (score >= 6) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const filteredItems = selectedCategory === 'all' 
    ? wardrobeItems 
    : wardrobeItems.filter(item => item.category === selectedCategory)

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-purple-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl md:text-5xl font-bold inner-bloom-text-gradient mb-4">
            Style Sanctuary 🌿
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Your conscious closet companion. Discover sustainable style, create amazing outfits, and join the circular fashion movement.
          </p>
        </motion.div>

        {/* Stats Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"
        >
          <Card className="bloom-card border-0">
            <CardContent className="p-4 text-center">
              <Shirt className="w-8 h-8 text-pink-500 mx-auto mb-2" />
              <div className="text-2xl font-bold">47</div>
              <div className="text-sm text-gray-600">Wardrobe Items</div>
            </CardContent>
          </Card>
          
          <Card className="bloom-card border-0">
            <CardContent className="p-4 text-center">
              <Leaf className="w-8 h-8 text-green-500 mx-auto mb-2" />
              <div className="text-2xl font-bold">8.2</div>
              <div className="text-sm text-gray-600">Eco Score</div>
            </CardContent>
          </Card>
          
          <Card className="bloom-card border-0">
            <CardContent className="p-4 text-center">
              <Recycle className="w-8 h-8 text-blue-500 mx-auto mb-2" />
              <div className="text-2xl font-bold">12</div>
              <div className="text-sm text-gray-600">Items Swapped</div>
            </CardContent>
          </Card>
          
          <Card className="bloom-card border-0">
            <CardContent className="p-4 text-center">
              <Heart className="w-8 h-8 text-red-500 mx-auto mb-2" />
              <div className="text-2xl font-bold">156</div>
              <div className="text-sm text-gray-600">Outfit Likes</div>
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
            
            {/* My Wardrobe Tab */}
            {activeTab === 'wardrobe' && (
              <div className="space-y-6">
                {/* Add Item & Search */}
                <div className="flex flex-col sm:flex-row gap-4 justify-between">
                  <div className="flex gap-2">
                    <Input 
                      placeholder="Search your wardrobe..." 
                      className="w-64"
                    />
                    <Button variant="outline" size="icon">
                      <Search size={18} />
                    </Button>
                    <Button variant="outline" size="icon">
                      <Filter size={18} />
                    </Button>
                  </div>
                  <Button className="bg-primary hover:bg-primary/90">
                    <Plus size={18} className="mr-2" />
                    Add Item
                  </Button>
                </div>

                {/* Categories */}
                <div className="flex flex-wrap gap-2">
                  {categories.map((category) => (
                    <button
                      key={category.id}
                      onClick={() => setSelectedCategory(category.id)}
                      className={`px-4 py-2 rounded-full transition-all ${
                        selectedCategory === category.id
                          ? 'bg-primary text-white'
                          : 'bg-white text-gray-600 hover:bg-gray-50'
                      }`}
                    >
                      {category.name} ({category.count})
                    </button>
                  ))}
                </div>

                {/* Wardrobe Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                  {filteredItems.map((item) => (
                    <motion.div
                      key={item.id}
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      whileHover={{ scale: 1.02 }}
                      className="bg-white rounded-xl shadow-sm border border-pink-100 overflow-hidden hover:shadow-lg transition-all"
                    >
                      <div className="aspect-square bg-gradient-to-br from-pink-50 to-purple-50 flex items-center justify-center text-6xl">
                        {item.image}
                      </div>
                      <div className="p-4">
                        <div className="flex justify-between items-start mb-2">
                          <h3 className="font-bold text-gray-800 text-sm">{item.name}</h3>
                          <Badge className={`text-xs ${getSustainabilityColor(item.sustainabilityScore)}`}>
                            {item.sustainabilityScore}/10
                          </Badge>
                        </div>
                        <p className="text-gray-600 text-sm mb-2">{item.brand} • {item.color}</p>
                        <div className="flex justify-between text-xs text-gray-500">
                          <span>Worn {item.wearCount} times</span>
                          <span>{item.lastWorn}</span>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            )}

            {/* AI Styling Tab */}
            {activeTab === 'outfits' && (
              <div className="space-y-6">
                <Card className="bloom-card border-0">
                  <CardContent className="p-8 text-center">
                    <Sparkles className="w-16 h-16 text-primary mx-auto mb-4" />
                    <h2 className="text-2xl font-bold inner-bloom-text-gradient mb-4">
                      AI Styling Magic ✨
                    </h2>
                    <p className="text-gray-600 mb-6">
                      Let our AI create stunning outfits from your existing wardrobe
                    </p>
                    <Button className="bg-primary hover:bg-primary/90 px-8 py-3">
                      Generate New Outfit
                    </Button>
                  </CardContent>
                </Card>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {aiOutfits.map((outfit) => (
                    <Card key={outfit.id} className="bloom-card border-0 hover:shadow-lg transition-all">
                      <CardContent className="p-6">
                        <div className="flex justify-between items-start mb-4">
                          <div>
                            <h3 className="font-bold text-gray-800">{outfit.name}</h3>
                            <p className="text-gray-600 text-sm">{outfit.occasion}</p>
                          </div>
                          <div className="flex items-center space-x-2">
                            {outfit.aiGenerated && (
                              <Badge className="bg-purple-100 text-purple-700">AI</Badge>
                            )}
                            <Badge className={`${getSustainabilityColor(outfit.sustainabilityScore)}`}>
                              {outfit.sustainabilityScore}/10
                            </Badge>
                          </div>
                        </div>
                        
                        <div className="space-y-2 mb-4">
                          {outfit.items.map((item, index) => (
                            <div key={index} className="text-sm text-gray-600 flex items-center">
                              <ArrowRight size={14} className="mr-2 text-gray-400" />
                              {item}
                            </div>
                          ))}
                        </div>
                        
                        <div className="flex justify-between items-center">
                          <div className="flex items-center space-x-2">
                            <Heart size={16} className="text-red-500" />
                            <span className="text-sm text-gray-600">{outfit.likes} likes</span>
                          </div>
                          <Button size="sm" variant="outline">
                            Try On
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}

            {/* Marketplace Tab */}
            {activeTab === 'marketplace' && (
              <div className="space-y-6">
                <div className="flex justify-between items-center">
                  <div>
                    <h2 className="text-2xl font-bold text-gray-800">Sustainable Marketplace</h2>
                    <p className="text-gray-600">Buy, sell, and swap pre-loved fashion</p>
                  </div>
                  <Button className="bg-primary hover:bg-primary/90">
                    <Plus size={18} className="mr-2" />
                    List Item
                  </Button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {marketplaceItems.map((item) => (
                    <Card key={item.id} className="bloom-card border-0 hover:shadow-lg transition-all">
                      <CardContent className="p-0">
                        <div className="aspect-square bg-gradient-to-br from-pink-50 to-purple-50 flex items-center justify-center text-6xl">
                          {item.image}
                        </div>
                        <div className="p-4">
                          <div className="flex justify-between items-start mb-2">
                            <h3 className="font-bold text-gray-800">{item.name}</h3>
                            <Badge className={`${getSustainabilityColor(item.sustainabilityScore)}`}>
                              {item.sustainabilityScore}/10
                            </Badge>
                          </div>
                          
                          <p className="text-gray-600 text-sm mb-2">by {item.seller} • {item.location}</p>
                          <p className="text-gray-500 text-sm mb-3">Condition: {item.condition}</p>
                          
                          <div className="flex justify-between items-center">
                            {item.type === 'sale' ? (
                              <div>
                                <span className="text-2xl font-bold text-primary">${item.price}</span>
                                {item.originalPrice && (
                                  <span className="text-sm text-gray-500 line-through ml-2">
                                    ${item.originalPrice}
                                  </span>
                                )}
                              </div>
                            ) : (
                              <div>
                                <span className="text-sm text-gray-600">Swap for:</span>
                                <p className="font-medium text-primary">{item.swapFor}</p>
                              </div>
                            )}
                            <Button size="sm" className="bg-primary hover:bg-primary/90">
                              {item.type === 'sale' ? 'Buy' : 'Swap'}
                            </Button>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}

            {/* Sustainable Guide Tab */}
            {activeTab === 'sustainable' && (
              <div className="space-y-8">
                <Card className="bloom-card border-0">
                  <CardContent className="p-8 text-center">
                    <Leaf className="w-16 h-16 text-green-500 mx-auto mb-4" />
                    <h2 className="text-2xl font-bold inner-bloom-text-gradient mb-4">
                      Your Sustainability Journey 🌱
                    </h2>
                    <p className="text-gray-600 mb-6">
                      Every conscious choice you make creates a positive impact on our planet
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
                      <div>
                        <div className="text-3xl font-bold text-green-600">47kg</div>
                        <div className="text-sm text-gray-600">CO2 Saved</div>
                      </div>
                      <div>
                        <div className="text-3xl font-bold text-blue-600">1,200L</div>
                        <div className="text-sm text-gray-600">Water Saved</div>
                      </div>
                      <div>
                        <div className="text-3xl font-bold text-purple-600">23</div>
                        <div className="text-sm text-gray-600">Items Rescued</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <div>
                  <h3 className="text-xl font-bold text-gray-800 mb-6">Sustainability Tips</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {sustainabilityTips.map((tip, index) => (
                      <Card key={index} className="bloom-card border-0">
                        <CardContent className="p-6">
                          <div className="flex items-start space-x-4">
                            <div className="text-3xl">{tip.icon}</div>
                            <div className="flex-1">
                              <div className="flex justify-between items-start mb-2">
                                <h4 className="font-bold text-gray-800">{tip.title}</h4>
                                <Badge className={`${
                                  tip.impact === 'High' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                                }`}>
                                  {tip.impact} Impact
                                </Badge>
                              </div>
                              <p className="text-gray-600">{tip.description}</p>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>

                <Card className="bloom-card border-0 inner-bloom-gradient">
                  <CardContent className="p-8 text-center">
                    <Crown className="w-12 h-12 text-white mx-auto mb-4" />
                    <h3 className="text-2xl font-bold text-white mb-4">
                      Become a Sustainability Champion
                    </h3>
                    <p className="text-white/90 mb-6">
                      Unlock exclusive eco-friendly brands and earn rewards for sustainable choices
                    </p>
                    <Button className="bg-white text-primary hover:bg-white/90">
                      Upgrade to Premium
                    </Button>
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

export default StyleSanctuary

