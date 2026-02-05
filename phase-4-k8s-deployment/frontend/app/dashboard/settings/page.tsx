import { auth } from '@/lib/auth'
import { headers } from 'next/headers'
import { redirect } from 'next/navigation'
import { User, Bell, Shield } from 'lucide-react'

// Force dynamic rendering
export const dynamic = 'force-dynamic'

export default async function SettingsPage() {
  // Get authenticated user
  const session = await auth.api.getSession({
    headers: await headers(),
  })

  if (!session?.user) {
    redirect('/sign-in')
  }

  const user = {
    name: session.user.name || 'User',
    email: session.user.email || '',
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">
          Settings
        </h1>
        <p className="text-forest-gray mt-1">
          Manage your account settings and preferences
        </p>
      </div>

      {/* Settings Sections */}
      <div className="grid gap-6">
        {/* Profile Section */}
        <div className="bg-forest-charcoal/30 border border-forest-charcoal/50 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="h-10 w-10 rounded-lg bg-neon-lime/20 border border-neon-lime/30 flex items-center justify-center">
              <User className="h-5 w-5 text-neon-lime" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-white">Profile</h2>
              <p className="text-sm text-forest-gray">
                Manage your personal information
              </p>
            </div>
          </div>
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-forest-gray">Name</label>
              <p className="mt-1 text-white">{user.name}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-forest-gray">Email</label>
              <p className="mt-1 text-white">{user.email}</p>
            </div>
          </div>
        </div>

        {/* Notifications Section */}
        <div className="bg-forest-charcoal/30 border border-forest-charcoal/50 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="h-10 w-10 rounded-lg bg-warning/20 border border-warning/30 flex items-center justify-center">
              <Bell className="h-5 w-5 text-warning" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-white">
                Notifications
              </h2>
              <p className="text-sm text-forest-gray">
                Configure how you receive notifications
              </p>
            </div>
          </div>
          <p className="text-sm text-forest-gray">
            Notification settings coming soon...
          </p>
        </div>

        {/* Security Section */}
        <div className="bg-forest-charcoal/30 border border-forest-charcoal/50 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="h-10 w-10 rounded-lg bg-success/20 border border-success/30 flex items-center justify-center">
              <Shield className="h-5 w-5 text-success" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-white">Security</h2>
              <p className="text-sm text-forest-gray">
                Manage your account security
              </p>
            </div>
          </div>
          <p className="text-sm text-forest-gray">
            Security settings coming soon...
          </p>
        </div>
      </div>
    </div>
  )
}
