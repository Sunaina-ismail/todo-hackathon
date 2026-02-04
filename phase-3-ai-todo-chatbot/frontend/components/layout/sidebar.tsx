/**
 * Dashboard Sidebar Component
 *
 * Features:
 * - Collapsible sidebar with smooth transitions (desktop)
 * - Compact mobile sidebar that slides in from left
 * - White/light theme matching website colors
 * - User profile and navigation
 */

'use client'

import * as React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
  LayoutDashboard,
  CheckSquare,
  Settings,
  LogOut,
} from 'lucide-react'
import { authClient } from '@/lib/auth-client'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { cn } from '@/lib/utils'
import { motion } from 'framer-motion'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Tasks', href: '/dashboard/tasks', icon: CheckSquare },
  { name: 'Settings', href: '/dashboard/settings', icon: Settings },
]

interface SidebarProps {
  className?: string
  forceCollapsed?: boolean
  onClose?: () => void
}

export function Sidebar({ className, forceCollapsed = false, onClose }: SidebarProps) {
  const pathname = usePathname()
  const [user, setUser] = React.useState<{ name: string; email: string } | null>(null)
  const [hoveredItem, setHoveredItem] = React.useState<string | null>(null)

  // Fetch user data on mount
  React.useEffect(() => {
    async function fetchUser() {
      const session = await authClient.getSession()
      if (session?.data?.user) {
        setUser({
          name: session.data.user.name || 'User',
          email: session.data.user.email || '',
        })
      }
    }
    fetchUser()
  }, [])

  const handleSignOut = async () => {
    try {
      await authClient.signOut({
        fetchOptions: {
          onSuccess: () => {
            window.location.href = '/sign-in'
          },
          onError: (ctx) => {
            console.error('Sign out error:', ctx.error)
            window.location.href = '/sign-in'
          }
        }
      })
    } catch (error) {
      console.error('Sign out error:', error)
      window.location.href = '/sign-in'
    }
  }

  return (
    <aside
      className={cn(
        'flex flex-col h-full',
        'bg-forest-charcoal border-r border-forest-charcoal/50',
        'transition-all duration-300',
        className
      )}
    >
      <div className={cn(
        "flex flex-col h-full py-6 transition-all duration-300",
        forceCollapsed ? "items-center px-3" : "items-start px-4"
      )}>
        {/* Logo */}
        <Link href="/dashboard" className={cn(
          "mb-8 flex-shrink-0 transition-all duration-300",
          forceCollapsed ? "" : "ml-2"
        )}>
          <div className={cn(
            "flex items-center justify-center rounded-lg",
            "bg-neon-lime/20 border border-neon-lime/30",
            "shadow-lg hover:shadow-neon-lime/20",
            "transition-all duration-300 hover:scale-105",
            forceCollapsed ? "h-10 w-10" : "h-10 w-10"
          )}>
            <CheckSquare className="h-6 w-6 text-neon-lime" />
          </div>
          {!forceCollapsed && (
            <span className="ml-3 text-lg font-semibold text-white inline-block">TaskFlow</span>
          )}
        </Link>

        {/* Navigation */}
        <nav className={cn(
          "flex-1 flex flex-col gap-2 w-full transition-all duration-300"
        )}>
          {navigation.map((item) => {
            const isActive = pathname === item.href
            const Icon = item.icon
            const isHovered = hoveredItem === item.name

            return (
              <div
                key={item.name}
                className="relative flex"
                onMouseEnter={() => setHoveredItem(item.name)}
                onMouseLeave={() => setHoveredItem(null)}
              >
                {/* Active indicator */}
                {isActive && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.5 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-neon-lime rounded-r-full"
                  />
                )}

                {/* Tooltip - only show when collapsed */}
                {isHovered && forceCollapsed && (
                  <motion.div
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -10 }}
                    className="absolute left-full top-1/2 -translate-y-1/2 ml-2 px-3 py-1.5 rounded-lg bg-forest-black border border-neon-lime/30 text-white text-sm font-medium whitespace-nowrap z-50 shadow-lg"
                  >
                    {item.name}
                  </motion.div>
                )}

                <Link
                  href={item.href}
                  onClick={onClose}
                  className={cn(
                    'flex items-center gap-3 transition-all duration-200 group',
                    forceCollapsed
                      ? 'h-11 w-11 rounded-lg justify-center mx-auto'
                      : 'h-11 px-3 rounded-lg w-full',
                    isActive
                      ? 'bg-neon-lime/20 text-neon-lime border border-neon-lime/30'
                      : 'text-forest-gray hover:bg-forest-black/50 hover:text-white'
                  )}
                >
                  <Icon className="h-5 w-5 flex-shrink-0" />
                  {!forceCollapsed && (
                    <span className="text-sm font-medium whitespace-nowrap">
                      {item.name}
                    </span>
                  )}
                </Link>
              </div>
            )
          })}
        </nav>

        {/* User section */}
        {user && (
          <div className={cn(
            "border-t border-forest-charcoal/50 pt-4 w-full",
            forceCollapsed ? "px-0" : "px-0"
          )}>
            {!forceCollapsed && (
              <div className="flex items-center gap-3 px-3 mb-3">
                <Avatar className="h-9 w-9">
                  <AvatarFallback className="bg-neon-lime/20 border border-neon-lime/30 text-neon-lime text-sm">
                    {user.name
                      .split(' ')
                      .map((n) => n[0])
                      .join('')
                      .toUpperCase()}
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-white truncate">{user.name}</p>
                  <p className="text-xs text-forest-gray truncate">{user.email}</p>
                </div>
              </div>
            )}

            {forceCollapsed && (
              <div className="flex justify-center mb-3">
                <Avatar className="h-9 w-9">
                  <AvatarFallback className="bg-neon-lime/20 border border-neon-lime/30 text-neon-lime text-sm">
                    {user.name
                      .split(' ')
                      .map((n) => n[0])
                      .join('')
                      .toUpperCase()}
                  </AvatarFallback>
                </Avatar>
              </div>
            )}

            {/* Logout Button */}
            <div
              className="relative flex"
              onMouseEnter={() => setHoveredItem('Sign Out')}
              onMouseLeave={() => setHoveredItem(null)}
            >
              {/* Tooltip - only show when collapsed */}
              {hoveredItem === 'Sign Out' && forceCollapsed && (
                <motion.div
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="absolute left-full top-1/2 -translate-y-1/2 ml-2 px-3 py-1.5 rounded-lg bg-forest-black border border-neon-lime/30 text-white text-sm font-medium whitespace-nowrap z-50 shadow-lg"
                >
                  Sign Out
                </motion.div>
              )}

              <Button
                onClick={handleSignOut}
                variant="ghost"
                size={forceCollapsed ? "icon" : "default"}
                className={cn(
                  "text-forest-gray hover:bg-forest-black/50 hover:text-white",
                  "transition-all duration-200",
                  forceCollapsed
                    ? "h-11 w-11 rounded-lg mx-auto"
                    : "h-11 w-full rounded-lg justify-start gap-3 px-3"
                )}
              >
                <LogOut className="h-5 w-5 flex-shrink-0" />
                {!forceCollapsed && (
                  <span className="text-sm font-medium whitespace-nowrap">
                    Sign Out
                  </span>
                )}
              </Button>
            </div>
          </div>
        )}
      </div>
    </aside>
  )
}
