import { Suspense } from 'react'
import { auth } from '@/lib/auth'
import { headers } from 'next/headers'
import { redirect } from 'next/navigation'
import { DashboardLayout } from '@/components/dashboard/dashboard-layout'
import { StatCard } from '@/components/dashboard/stat-card'
import { fetchTaskStats, fetchRecentTasks } from '@/actions/dashboard'
import {
  CheckSquare,
  Clock,
  AlertCircle,
  TrendingUp,
  Calendar,
  ListTodo,
} from 'lucide-react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'

// Force dynamic rendering
export const dynamic = 'force-dynamic'

export default async function DashboardPage() {
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
      {/* Welcome Section */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back, {user.name.split(' ')[0]}! 👋
        </h1>
        <p className="text-gray-600 mt-2">
          Here's what's happening with your tasks today.
        </p>
      </div>

      {/* Stats Grid */}
      <Suspense fallback={<StatsGridSkeleton />}>
        <StatsGrid />
      </Suspense>

      {/* Recent Tasks Section */}
      <div className="mt-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Recent Tasks</h2>
          <Link href="/dashboard/tasks">
            <Button variant="outline" size="sm">
              View All Tasks
            </Button>
          </Link>
        </div>
        <Suspense fallback={<RecentTasksSkeleton />}>
          <RecentTasks />
        </Suspense>
      </div>
    </DashboardLayout>
  )
}

async function StatsGrid() {
  const { stats, error } = await fetchTaskStats()

  if (error || !stats) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
        Failed to load statistics. Please try again.
      </div>
    )
  }

  const completionRate = stats.total > 0
    ? Math.round((stats.completed / stats.total) * 100)
    : 0

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <StatCard
        title="Total Tasks"
        value={stats.total}
        description={`${stats.completed} completed, ${stats.pending} pending`}
        icon={ListTodo}
      />
      <StatCard
        title="Completion Rate"
        value={`${completionRate}%`}
        description={`${stats.completed} of ${stats.total} tasks completed`}
        icon={TrendingUp}
      />
      <StatCard
        title="High Priority"
        value={stats.highPriority}
        description="Tasks requiring attention"
        icon={AlertCircle}
        className={stats.highPriority > 0 ? 'border-orange-200 bg-orange-50' : ''}
      />
      <StatCard
        title="Due Soon"
        value={stats.dueSoon}
        description="Due within 7 days"
        icon={Calendar}
        className={stats.dueSoon > 0 ? 'border-blue-200 bg-blue-50' : ''}
      />
      <StatCard
        title="Overdue"
        value={stats.overdue}
        description="Past due date"
        icon={Clock}
        className={stats.overdue > 0 ? 'border-red-200 bg-red-50' : ''}
      />
      <StatCard
        title="Completed"
        value={stats.completed}
        description="Tasks finished"
        icon={CheckSquare}
        className="border-green-200 bg-green-50"
      />
    </div>
  )
}

async function RecentTasks() {
  const { tasks, error } = await fetchRecentTasks(5)

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
        Failed to load recent tasks.
      </div>
    )
  }

  if (!tasks || tasks.length === 0) {
    return (
      <div className="bg-white rounded-lg border p-8 text-center">
        <ListTodo className="h-12 w-12 text-gray-400 mx-auto mb-3" />
        <h3 className="text-lg font-medium text-gray-900 mb-1">No tasks yet</h3>
        <p className="text-gray-600 mb-4">
          Get started by creating your first task
        </p>
        <Link href="/dashboard/tasks">
          <Button>Go to Tasks</Button>
        </Link>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg border divide-y">
      {tasks.map((task) => (
        <Link
          key={task.id}
          href="/dashboard/tasks"
          className="block p-4 hover:bg-gray-50 transition-colors"
        >
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <h3 className="font-medium text-gray-900 truncate">
                  {task.title}
                </h3>
                <span
                  className={`px-2 py-0.5 text-xs font-medium rounded-full ${
                    task.priority === 'High'
                      ? 'bg-red-100 text-red-700'
                      : task.priority === 'Medium'
                      ? 'bg-yellow-100 text-yellow-700'
                      : 'bg-green-100 text-green-700'
                  }`}
                >
                  {task.priority}
                </span>
              </div>
              {task.description && (
                <p className="text-sm text-gray-600 mt-1 line-clamp-1">
                  {task.description}
                </p>
              )}
              <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                {task.due_date && (
                  <span className="flex items-center gap-1">
                    <Calendar className="h-3 w-3" />
                    {new Date(task.due_date).toLocaleDateString()}
                  </span>
                )}
                {task.tags && task.tags.length > 0 && (
                  <span className="flex items-center gap-1">
                    {task.tags.slice(0, 2).map((tag) => (
                      <span
                        key={tag}
                        className="px-2 py-0.5 bg-gray-100 rounded-full"
                      >
                        {tag}
                      </span>
                    ))}
                    {task.tags.length > 2 && (
                      <span className="text-gray-400">
                        +{task.tags.length - 2}
                      </span>
                    )}
                  </span>
                )}
              </div>
            </div>
            <div className="flex-shrink-0">
              {task.completed ? (
                <CheckSquare className="h-5 w-5 text-green-600" />
              ) : (
                <div className="h-5 w-5 border-2 border-gray-300 rounded" />
              )}
            </div>
          </div>
        </Link>
      ))}
    </div>
  )
}

function StatsGridSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {[...Array(6)].map((_, i) => (
        <div key={i} className="bg-white rounded-lg border p-6">
          <Skeleton className="h-4 w-24 mb-4" />
          <Skeleton className="h-8 w-16 mb-2" />
          <Skeleton className="h-3 w-32" />
        </div>
      ))}
    </div>
  )
}

function RecentTasksSkeleton() {
  return (
    <div className="bg-white rounded-lg border divide-y">
      {[...Array(5)].map((_, i) => (
        <div key={i} className="p-4">
          <Skeleton className="h-5 w-3/4 mb-2" />
          <Skeleton className="h-4 w-full mb-2" />
          <Skeleton className="h-3 w-1/2" />
        </div>
      ))}
    </div>
  )
}
