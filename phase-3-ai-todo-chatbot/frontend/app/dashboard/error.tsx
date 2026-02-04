'use client'

import { useEffect } from 'react'
import { motion } from 'framer-motion'
import { AlertCircle, RefreshCw } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { fadeInVariants } from '@/lib/animations'

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error('Dashboard error:', error)
  }, [error])

  return (
    <motion.div
      variants={fadeInVariants}
      initial="initial"
      animate="animate"
      className="flex items-center justify-center min-h-[60vh]"
    >
      <div className="text-center max-w-md">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-error/20 mb-6">
          <AlertCircle className="w-8 h-8 text-error" />
        </div>

        <h2 className="text-2xl font-bold text-white mb-2">
          Something went wrong
        </h2>

        <p className="text-forest-gray mb-6">
          We encountered an error while loading your dashboard. Please try again.
        </p>

        {error.message && (
          <div className="bg-forest-charcoal/30 border border-error/30 rounded-lg p-4 mb-6 text-left">
            <p className="text-sm text-forest-gray font-mono">
              {error.message}
            </p>
          </div>
        )}

        <Button
          onClick={reset}
          className="bg-neon-lime text-forest-black hover:bg-neon-lime/90"
        >
          <RefreshCw className="w-4 h-4 mr-2" />
          Try Again
        </Button>
      </div>
    </motion.div>
  )
}
