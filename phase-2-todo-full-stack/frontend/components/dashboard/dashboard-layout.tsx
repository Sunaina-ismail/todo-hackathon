'use client'

import { Sidebar } from '@/components/dashboard/sidebar'
import { cn } from '@/lib/utils'

interface DashboardLayoutProps {
  children: React.ReactNode
  user: {
    name: string
    email: string
  }
}

export function DashboardLayout({ children, user }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar user={user} />

      {/* Main content */}
      <div className={cn(
        'transition-all duration-300',
        'lg:ml-64' // Default sidebar width
      )}>
        <main className="p-4 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  )
}
