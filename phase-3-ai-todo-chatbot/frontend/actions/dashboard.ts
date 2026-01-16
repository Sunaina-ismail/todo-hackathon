/**
 * Server Actions for Dashboard Analytics
 *
 * Fetches task statistics for the dashboard overview
 */

'use server'

import { headers } from 'next/headers'
import { fetchTasks } from './tasks'

export interface TaskStats {
  total: number
  completed: number
  pending: number
  highPriority: number
  dueSoon: number // Due within 7 days
  overdue: number
}

/**
 * Fetch task statistics for the authenticated user
 */
export async function fetchTaskStats(): Promise<{ stats?: TaskStats; error?: string }> {
  try {
    // Fetch all tasks
    const allTasksResult = await fetchTasks({ limit: 100 })

    if (allTasksResult.error) {
      return { error: allTasksResult.error }
    }

    const tasks = allTasksResult.tasks || []
    const now = new Date()
    const sevenDaysFromNow = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000)

    // Calculate statistics
    const stats: TaskStats = {
      total: tasks.length,
      completed: tasks.filter(t => t.completed).length,
      pending: tasks.filter(t => !t.completed).length,
      highPriority: tasks.filter(t => t.priority === 'High' && !t.completed).length,
      dueSoon: tasks.filter(t => {
        if (!t.due_date || t.completed) return false
        const dueDate = new Date(t.due_date)
        return dueDate >= now && dueDate <= sevenDaysFromNow
      }).length,
      overdue: tasks.filter(t => {
        if (!t.due_date || t.completed) return false
        const dueDate = new Date(t.due_date)
        return dueDate < now
      }).length,
    }

    return { stats }
  } catch (error) {
    console.error('Failed to fetch task stats:', error)
    return { error: 'Failed to fetch task statistics' }
  }
}

/**
 * Fetch recent tasks for the dashboard
 */
export async function fetchRecentTasks(limit: number = 5) {
  return fetchTasks({
    sort_by: 'created_at',
    sort_direction: 'desc',
    limit,
  })
}
