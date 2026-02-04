/**
 * Dashboard Page - Server Component
 *
 * Fetches tasks once and passes to child components
 * Following reference-code-uneeza pattern for efficiency
 */

import { Suspense } from 'react'
import { auth } from '@/lib/auth'
import { headers } from 'next/headers'
import { fetchTasks } from '@/actions/tasks'
import { StatCard } from '@/components/dashboard/stat-card'
import { CompletionChart } from '@/components/dashboard/completion-chart'
import { StatusDonut } from '@/components/dashboard/status-donut'
import { PriorityChart } from '@/components/dashboard/priority-chart'
import { ActivityChart } from '@/components/dashboard/activity-chart'
import { ChartSkeleton } from '@/components/dashboard/chart-skeleton'
import { getCompletionTrend, getActivityTimeline } from '@/lib/chart-utils'

export default async function DashboardPage() {
  // Get session for welcome message
  const session = await auth.api.getSession({
    headers: await headers()
  })

  // Fetch all tasks once for dashboard analytics (limit to 100 for performance)
  const tasksResult = await fetchTasks({
    limit: 100,
    sort_by: 'created',
    sort_direction: 'desc'
  })

  const tasks = tasksResult.tasks || []

  // Calculate statistics from tasks
  const total = tasks.length
  const completed = tasks.filter(task => task.completed).length
  const pending = tasks.filter(task => !task.completed).length

  // Calculate completion rate
  const completionRate = total > 0
    ? Math.round((completed / total) * 100)
    : 0

  // Count by priority (only pending tasks)
  const pendingTasks = tasks.filter(t => !t.completed)
  const highPriorityCount = pendingTasks.filter(t => t.priority === 'High').length
  const mediumPriorityCount = pendingTasks.filter(t => t.priority === 'Medium').length

  // Calculate chart data from tasks
  const completionTrend = getCompletionTrend(tasks, 7)
  const activityTimeline = getActivityTimeline(tasks, 7)

  // Status breakdown
  const completedCount = tasks.filter(t => t.completed).length
  const pendingCount = tasks.filter(t => !t.completed).length
  const statusBreakdown: Array<{ name: string; value: number; color: string }> = [
    { name: 'Completed', value: completedCount, color: '#10b981' },
    { name: 'Pending', value: pendingCount, color: '#f59e0b' },
  ]

  // Priority distribution (only pending tasks)
  const highCount = pendingTasks.filter(t => t.priority === 'High').length
  const mediumCount = pendingTasks.filter(t => t.priority === 'Medium').length
  const lowCount = pendingTasks.filter(t => t.priority === 'Low').length
  const priorityDistribution: Array<{ name: string; value: number; color: string }> = [
    { name: 'High', value: highCount, color: '#ef4444' },
    { name: 'Medium', value: mediumCount, color: '#f59e0b' },
    { name: 'Low', value: lowCount, color: '#10b981' },
  ]

  // Format completion trend for chart
  const completionData = completionTrend.map(point => ({
    date: point.date,
    value: point.completed,
    cumulative: point.cumulative,
    label: new Date(point.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }))

  // Format activity timeline for chart
  const activityData = activityTimeline.map(point => ({
    date: point.date,
    created: point.tasksCreated,
    completed: point.tasksCompleted,
    updated: point.tasksUpdated,
    label: new Date(point.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }))

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div>
        <h1 className="text-3xl font-bold text-white">
          Welcome back, {session?.user?.name?.split(' ')[0] || 'User'}! 👋
        </h1>
        <p className="text-forest-gray mt-2">
          Track your productivity and task completion metrics
        </p>
      </div>

      {/* Stats Grid - Keep your beautiful design */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <StatCard
          title="Total Tasks"
          value={total}
          description={`${completed} completed`}
          iconName="ListTodo"
          color="default"
        />
        <StatCard
          title="Completion Rate"
          value={`${completionRate}%`}
          description="Overall progress"
          iconName="TrendingUp"
          color="success"
          trend={{
            value: 12,
            isPositive: true,
          }}
        />
        <StatCard
          title="High Priority"
          value={highPriorityCount}
          description="Urgent tasks"
          iconName="AlertCircle"
          color={highPriorityCount > 0 ? 'error' : 'default'}
        />
        <StatCard
          title="Medium Priority"
          value={mediumPriorityCount}
          description="Important tasks"
          iconName="Target"
          color={mediumPriorityCount > 0 ? 'warning' : 'default'}
        />
        <StatCard
          title="Pending Tasks"
          value={pending}
          description="To be completed"
          iconName="Clock"
          color="default"
        />
        <StatCard
          title="Completed"
          value={completed}
          description="Tasks finished"
          iconName="CheckSquare"
          color="success"
        />
      </div>

      {/* Charts Grid - Keep your beautiful design */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Completion Trend Chart */}
        <div className="bg-forest-charcoal/30 border border-forest-charcoal/50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-white mb-4">
            Completion Trend
          </h3>
          <CompletionChart data={completionData} />
        </div>

        {/* Status Breakdown Donut */}
        <div className="bg-forest-charcoal/30 border border-forest-charcoal/50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-white mb-4">
            Status Breakdown
          </h3>
          <StatusDonut data={statusBreakdown} />
        </div>

        {/* Priority Distribution Chart */}
        <div className="bg-forest-charcoal/30 border border-forest-charcoal/50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-white mb-4">
            Priority Distribution
          </h3>
          <PriorityChart data={priorityDistribution} />
        </div>

        {/* Activity Timeline Chart */}
        <div className="bg-forest-charcoal/30 border border-forest-charcoal/50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-white mb-4">
            Activity Timeline
          </h3>
          <ActivityChart data={activityData} />
        </div>
      </div>
    </div>
  )
}
