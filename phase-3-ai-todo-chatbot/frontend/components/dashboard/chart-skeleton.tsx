'use client'

import { Skeleton } from '@/components/ui/skeleton'
import { motion } from 'framer-motion'
import { skeletonPulseVariants } from '@/lib/animations'
import { cn } from '@/lib/utils'

interface ChartSkeletonProps {
  height?: string
  className?: string
}

export function ChartSkeleton({ height = 'h-64', className }: ChartSkeletonProps) {
  return (
    <motion.div
      variants={skeletonPulseVariants}
      initial="initial"
      animate="animate"
      className={cn("w-full", height, className)}
    >
      <Skeleton className="w-full h-full bg-forest-charcoal" />
    </motion.div>
  )
}
