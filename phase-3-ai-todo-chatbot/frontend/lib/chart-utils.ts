// Chart data transformation utilities for Modern Dashboard UI Redesign

import type {
  DashboardMetrics,
  ChartDataPoint,
  TrendDataPoint,
  PriorityDistribution,
  ActivityData
} from './types'
import type { Task } from '@/types/task'

/**
 * Calculate dashboard metrics from tasks
 */
export function calculateMetrics(tasks: Task[]): DashboardMetrics {
  const totalTasks = tasks.length
  const completedTasks = tasks.filter(t => t.completed).length
  const pendingTasks = totalTasks - completedTasks
  const completionRate = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0

  const pendingByPriority = tasks.filter(t => !t.completed)
  const highPriorityCount = pendingByPriority.filter(t => t.priority === 'High').length
  const mediumPriorityCount = pendingByPriority.filter(t => t.priority === 'Medium').length
  const lowPriorityCount = pendingByPriority.filter(t => t.priority === 'Low').length

  const trendData = getCompletionTrend(tasks, 7)

  return {
    totalTasks,
    completedTasks,
    pendingTasks,
    completionRate: Math.round(completionRate * 100) / 100,
    highPriorityCount,
    mediumPriorityCount,
    lowPriorityCount,
    trendData,
    lastUpdated: new Date().toISOString()
  }
}

/**
 * Transform tasks into completion trend data
 */
export function getCompletionTrend(tasks: Task[], days: number = 7): TrendDataPoint[] {
  const now = new Date()
  const trendData: TrendDataPoint[] = []

  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(now)
    date.setDate(date.getDate() - i)
    date.setHours(0, 0, 0, 0)

    const nextDate = new Date(date)
    nextDate.setDate(nextDate.getDate() + 1)

    const dateStr = date.toISOString().split('T')[0]

    const completed = tasks.filter(t => {
      if (!t.completed) return false
      const completedDate = new Date(t.updated_at) // Use updated_at as completion date
      return completedDate >= date && completedDate < nextDate
    }).length

    const created = tasks.filter(t => {
      const createdDate = new Date(t.created_at)
      return createdDate >= date && createdDate < nextDate
    }).length

    const cumulativeCompleted = tasks.filter(t => {
      if (!t.completed) return false
      return new Date(t.updated_at) < nextDate
    }).length

    trendData.push({
      date: dateStr,
      completed,
      created,
      cumulative: cumulativeCompleted
    })
  }

  return trendData
}

/**
 * Transform tasks into priority distribution
 */
export function getPriorityDistribution(tasks: Task[]): PriorityDistribution {
  const pendingTasks = tasks.filter(t => !t.completed)

  const high = pendingTasks.filter(t => t.priority === 'High').length
  const medium = pendingTasks.filter(t => t.priority === 'Medium').length
  const low = pendingTasks.filter(t => t.priority === 'Low').length

  return {
    high,
    medium,
    low,
    total: high + medium + low
  }
}

/**
 * Transform tasks into activity timeline
 */
export function getActivityTimeline(tasks: Task[], days: number = 30): ActivityData[] {
  const now = new Date()
  const activityData: ActivityData[] = []

  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(now)
    date.setDate(date.getDate() - i)
    date.setHours(0, 0, 0, 0)

    const nextDate = new Date(date)
    nextDate.setDate(nextDate.getDate() + 1)

    const dateStr = date.toISOString().split('T')[0]

    const tasksCreated = tasks.filter(t => {
      const createdDate = new Date(t.created_at)
      return createdDate >= date && createdDate < nextDate
    }).length

    const tasksCompleted = tasks.filter(t => {
      if (!t.completed) return false
      const completedDate = new Date(t.updated_at)
      return completedDate >= date && completedDate < nextDate
    }).length

    const tasksUpdated = tasks.filter(t => {
      const updatedDate = new Date(t.updated_at)
      return updatedDate >= date && updatedDate < nextDate
    }).length

    activityData.push({
      date: dateStr,
      tasksCreated,
      tasksCompleted,
      tasksUpdated,
      totalActivity: tasksCreated + tasksCompleted + tasksUpdated
    })
  }

  return activityData
}

/**
 * Format chart data for Recharts
 */
export function formatChartData(
  trendData: TrendDataPoint[]
): ChartDataPoint[] {
  return trendData.map(point => ({
    date: point.date,
    value: point.completed,
    label: formatDateLabel(point.date)
  }))
}

/**
 * Format date for chart labels
 */
function formatDateLabel(dateStr: string): string {
  const date = new Date(dateStr)
  const month = date.toLocaleDateString('en-US', { month: 'short' })
  const day = date.getDate()
  return `${month} ${day}`
}
