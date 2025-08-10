import React from 'react'
import SisterProfile from './SisterProfile'
import { useUser } from '../contexts/UserContext'

const Profile = () => {
  const { user } = useUser()

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-amber-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold inner-bloom-text-gradient mb-4">
            Your Sacred Profile
          </h1>
          <p className="text-xl text-gray-600">
            Embrace your divine transformation, beautiful sister
          </p>
        </div>
        
        <SisterProfile user={user} />
      </div>
    </div>
  )
}

export default Profile

