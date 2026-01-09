import { auth } from '@/lib/auth'
import { headers } from 'next/headers'
import { redirect } from 'next/navigation'
import { DashboardLayout } from '@/components/dashboard/dashboard-layout'
import { Settings as SettingsIcon, User, Bell, Shield } from 'lucide-react'

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
    <DashboardLayout user={user}>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900">
            Settings
          </h1>
          <p className="text-gray-600 mt-1">
            Manage your account settings and preferences
          </p>
        </div>

        {/* Settings Sections */}
        <div className="grid gap-6">
          {/* Profile Section */}
          <div className="bg-white rounded-lg border p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="h-10 w-10 rounded-lg bg-blue-50 flex items-center justify-center">
                <User className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-900">Profile</h2>
                <p className="text-sm text-gray-600">
                  Manage your personal information
                </p>
              </div>
            </div>
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-700">Name</label>
                <p className="mt-1 text-gray-900">{user.name}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700">Email</label>
                <p className="mt-1 text-gray-900">{user.email}</p>
              </div>
            </div>
          </div>

          {/* Notifications Section */}
          <div className="bg-white rounded-lg border p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="h-10 w-10 rounded-lg bg-purple-50 flex items-center justify-center">
                <Bell className="h-5 w-5 text-purple-600" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-900">
                  Notifications
                </h2>
                <p className="text-sm text-gray-600">
                  Configure how you receive notifications
                </p>
              </div>
            </div>
            <p className="text-sm text-gray-500">
              Notification settings coming soon...
            </p>
          </div>

          {/* Security Section */}
          <div className="bg-white rounded-lg border p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="h-10 w-10 rounded-lg bg-green-50 flex items-center justify-center">
                <Shield className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-900">Security</h2>
                <p className="text-sm text-gray-600">
                  Manage your account security
                </p>
              </div>
            </div>
            <p className="text-sm text-gray-500">
              Security settings coming soon...
            </p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
