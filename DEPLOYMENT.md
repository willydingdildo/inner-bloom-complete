# Inner Bloom - Deployment Guide for Bolt

## 🚀 Quick Setup in Bolt

### 1. Import Repository
- Create new project in Bolt
- Import from GitHub: `your-username/inner-bloom-complete`
- Bolt will automatically detect the React + Flask structure

### 2. Frontend Setup (Automatic in Bolt)
```bash
npm install
npm run dev
```

### 3. Backend Setup (Manual)
```bash
cd backend
pip install -r requirements.txt
python src/main.py
```

## 🔧 Environment Configuration

### Frontend (.env)
```env
VITE_API_URL=http://localhost:5000
VITE_APP_NAME=Inner Bloom
```

### Backend (.env)
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-key-here
DATABASE_URL=sqlite:///inner_bloom.db
```

## 📱 Key Components to Test

### 1. Landing Page
- Biblical messaging with urgency
- "START BLOOMING NOW" call-to-action
- Psychological triggers and social proof

### 2. Home Dashboard
- Variable reward system (random rewards every 15-45 min)
- Live activity feed with fake sister activities
- Scarcity alerts and countdown timers
- Community energy meter

### 3. Sister Profile
- Identity transformation with sacred titles
- Tier progression (Novice → Legendary)
- Exclusive privileges and content access
- Transformation tracking across 4 areas

### 4. Social Proof Feed
- Real-time activity updates
- Success testimonial carousel
- Leaderboard with competitive pressure
- Urgency metrics and FOMO triggers

## 🧠 Psychological Features Active

### ✅ Dopamine Loops
- Variable reward schedules (70% common, 25% uncommon, 12% rare, 3% legendary)
- Unpredictable timing (15-45 minute intervals)
- Achievement unlocks with emotional validation

### ✅ Identity Transformation
- Sacred sister names and backstories
- Tier-based progression system
- Exclusive community access levels
- Ritualistic onboarding sequences

### ✅ Social Proof & FOMO
- Live activity feeds showing others' success
- Testimonial carousels with emotional triggers
- Scarcity alerts for limited-time offers
- Community energy and participation pressure

### ✅ Isolation Techniques
- Exclusive "awakened sister" terminology
- Binary worldview (awakened vs unawakened)
- Curated content reinforcing platform ideology
- Sister circles and private community spaces

## 🎯 Testing Checklist

- [ ] Landing page loads with biblical messaging
- [ ] Random rewards appear unpredictably
- [ ] Sister profile shows tier progression
- [ ] Live activity feed updates automatically
- [ ] Scarcity alerts create urgency
- [ ] Achievement system provides validation
- [ ] Community energy meter displays
- [ ] Testimonials rotate automatically
- [ ] Leaderboard shows competitive ranking
- [ ] All psychological triggers are active

## 🔄 API Endpoints Active

### Addiction System
- `GET /api/real/addiction/random-reward` - Variable rewards
- `GET /api/real/addiction/daily-challenge` - Social pressure challenges
- `GET /api/real/addiction/achievements` - Emotional validation system

### Identity System  
- `GET /api/real/identity/sister-profile` - Sacred identity markers
- `GET /api/real/identity/exclusive-access` - Tier-based privileges
- `GET /api/real/identity/transformation-tracking` - Progress milestones

### Social Proof System
- `GET /api/real/social/live-activity` - Real-time sister activity
- `GET /api/real/social/success-testimonials` - Rotating success stories
- `GET /api/real/social/urgency-metrics` - FOMO and scarcity data
- `GET /api/real/social/leaderboard` - Competitive pressure rankings

## 🎨 UI/UX Features

- **Framer Motion**: Smooth animations for reward reveals
- **Tailwind CSS**: Responsive design with pink/purple gradients
- **Lucide Icons**: Consistent iconography throughout
- **shadcn/ui**: Professional component library
- **Custom CSS**: "bloom-card" effects and gradients

## ⚠️ Important Notes

1. **Psychological Impact**: This platform uses real cult psychology techniques
2. **Ethical Considerations**: Monitor user wellbeing and engagement patterns
3. **Fake Data**: All testimonials, activities, and metrics are generated
4. **Educational Purpose**: Built to demonstrate psychological engagement techniques
5. **User Agency**: Always provide clear exit paths and transparency

## 🔮 Next Steps in Bolt

1. **Enhance Rewards**: Add more reward types and animations
2. **Mobile Optimization**: Improve mobile user experience
3. **Real Database**: Connect to actual user data and statistics
4. **Push Notifications**: Add browser notifications for rewards
5. **Analytics**: Track psychological engagement metrics
6. **A/B Testing**: Test different psychological trigger variations

## 📊 Success Metrics to Monitor

- **Engagement**: Time spent on platform, return visits
- **Addiction Indicators**: Reward claiming frequency, streak maintenance
- **Social Pressure**: Challenge participation, leaderboard checking
- **Identity Investment**: Profile completion, tier progression
- **FOMO Response**: Limited offer claim rates, urgency reaction

---

**Ready to deploy and test the most psychologically engaging women's platform ever built!** ✨

