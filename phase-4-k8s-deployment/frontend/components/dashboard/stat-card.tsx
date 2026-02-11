'use client'

import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'
import { cardHoverVariants } from '@/lib/animations'
import {
  CheckSquare,
  Clock,
  AlertCircle,
  TrendingUp,
  ListTodo,
  Target,
  LucideIcon,
} from 'lucide-react'

// Icon map to avoid passing functions from Server to Client Components
const iconMap: Record<string, LucideIcon> = {
  ListTodo,
  CheckSquare,
  Clock,
  AlertCircle,
  TrendingUp,
  Target,
}

interface StatCardProps {
  title: string
  value: string | number
  description?: string
  iconName: keyof typeof iconMap
  trend?: {
    value: number
    isPositive: boolean
  }
  color?: 'default' | 'success' | 'warning' | 'error'
  className?: string
}

export function StatCard({
  title,
  value,
  description,
  iconName,
  trend,
  color = 'default',
  className,
}: StatCardProps) {
  const Icon = iconMap[iconName]
  const colorClasses = {
    default: 'border-forest-charcoal/50 bg-forest-charcoal/30',
    success: 'border-success/30 bg-success/10',
    warning: 'border-warning/30 bg-warning/10',
    error: 'border-error/30 bg-error/10',
  }

  const iconColorClasses = {
    default: 'bg-neon-lime/10 text-neon-lime',
    success: 'bg-success/20 text-success',
    warning: 'bg-warning/20 text-warning',
    error: 'bg-error/20 text-error',
  }

  return (
    <motion.div
      variants={cardHoverVariants}
      initial="initial"
      whileHover="hover"
      className={cn(
        'rounded-lg border p-6 backdrop-blur-sm transition-all',
        colorClasses[color],
        className
      )}
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-forest-gray">{title}</p>
          <p className="text-3xl font-bold mt-2 text-white">{value}</p>
          {description && (
            <p className="text-sm text-forest-gray mt-1">{description}</p>
          )}
          {trend && (
            <div className="flex items-center gap-1 mt-2">
              <span
                className={cn(
                  'text-sm font-medium',
                  trend.isPositive ? 'text-success' : 'text-error'
                )}
              >
                {trend.isPositive ? '+' : ''}
                {trend.value}%
              </span>
              <span className="text-sm text-forest-gray">from last week</span>
            </div>
          )}
        </div>
        <div className={cn(
          'h-12 w-12 rounded-lg flex items-center justify-center',
          iconColorClasses[color]
        )}>
          <Icon className="h-6 w-6" />
        </div>
      </div>
    </motion.div>
  )
}
