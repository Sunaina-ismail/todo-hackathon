/**
 * Dashboard Layout Component
 *
 * Features:
 * - Collapsible sidebar with smooth transitions (desktop)
 * - Mobile sidebar that slides in from left
 * - White/light theme matching website colors
 * - Proper responsive behavior on all screen sizes
 * - Hamburger menu in top-left on mobile (not bottom-right)
 */

'use client'

import * as React from 'react'
import { usePathname } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { Sidebar } from '@/components/layout/sidebar'
import { Button } from '@/components/ui/button'
import { Menu, X, ChevronLeft, ChevronRight } from 'lucide-react'
import { cn } from '@/lib/utils'

interface DashboardLayoutProps {
  children: React.ReactNode
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const pathname = usePathname()
  const [sidebarCollapsed, setSidebarCollapsed] = React.useState(false)
  const [mobileSidebarOpen, setMobileSidebarOpen] = React.useState(false)

  // Close mobile sidebar when route changes
  React.useEffect(() => {
    setMobileSidebarOpen(false)
  }, [pathname])

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Desktop Sidebar - Collapsible */}
      <motion.aside
        initial={false}
        animate={{
          width: sidebarCollapsed ? 80 : 256,
        }}
        transition={{ duration: 0.3, ease: 'easeInOut' }}
        className="hidden lg:flex fixed left-0 top-0 h-full z-40 flex-col"
      >
        {/* Sidebar container with toggle */}
        <div className="relative h-full">
          <Sidebar
            className="h-full"
            forceCollapsed={sidebarCollapsed}
          />

          {/* Collapse Toggle Button - Floating on the right edge */}
          <button
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className={cn(
              "absolute right-0 top-20 translate-x-1/2 z-50",
              "flex h-8 w-8 items-center justify-center rounded-full",
              "bg-white border-2 border-gray-200",
              "text-gray-600 hover:text-gray-900",
              "shadow-lg hover:shadow-xl",
              "transition-all duration-200 hover:scale-110"
            )}
          >
            {sidebarCollapsed ? (
              <ChevronRight className="h-4 w-4" />
            ) : (
              <ChevronLeft className="h-4 w-4" />
            )}
          </button>
        </div>
      </motion.aside>

      {/* Mobile overlay */}
      <AnimatePresence>
        {mobileSidebarOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-40 bg-black/50 lg:hidden"
            onClick={() => setMobileSidebarOpen(false)}
          />
        )}
      </AnimatePresence>

      {/* Mobile sidebar - Slides in from left */}
      <AnimatePresence>
        {mobileSidebarOpen && (
          <motion.div
            initial={{ x: '-100%', opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: '-100%', opacity: 0 }}
            transition={{ duration: 0.3, ease: 'easeInOut' }}
            className="fixed inset-y-0 left-0 z-50 lg:hidden"
          >
            <div className={cn(
              "h-full w-64 flex flex-col",
              "bg-white border-r border-gray-200",
              "relative"
            )}>
              {/* Close button floating outside on the right */}
              <button
                onClick={() => setMobileSidebarOpen(false)}
                className={cn(
                  "absolute -right-12 top-4 z-50",
                  "flex h-10 w-10 items-center justify-center rounded-lg",
                  "bg-white border border-gray-200",
                  "text-gray-600 hover:text-gray-900",
                  "shadow-lg",
                  "transition-colors"
                )}
              >
                <X className="h-5 w-5" />
              </button>

              <Sidebar
                className="w-full h-full"
                forceCollapsed={false}
                onClose={() => setMobileSidebarOpen(false)}
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main content area */}
      <div
        className={cn(
          "transition-all duration-300",
          sidebarCollapsed ? "lg:pl-20" : "lg:pl-64"
        )}
      >
        {/* Mobile header with hamburger menu */}
        <header className={cn(
          "sticky top-0 z-30 flex h-16 items-center gap-4 px-4 lg:hidden",
          "bg-white border-b border-gray-200"
        )}>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setMobileSidebarOpen(true)}
            className="text-gray-600 hover:text-gray-900 hover:bg-gray-100"
          >
            <Menu className="h-6 w-6" />
          </Button>
          <div className="flex-1" />
        </header>

        {/* Page content - Full width, responsive padding */}
        <main className="w-full">
          <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
