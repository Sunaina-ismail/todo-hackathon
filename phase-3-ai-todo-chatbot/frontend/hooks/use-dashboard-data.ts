'use client'

import { useQuery } from '@tanstack/react-query'
import type { DashboardMetrics, ChartDataPoint } from '@/lib/types'

interface DashboardData {
  metrics: DashboardMetrics
  completionTrend: ChartDataPoint[]
  priorityDistribution: ChartDataPoint[]
  statusBreakdown: ChartDataPoint[]
  activityTimeline: Array<{
    date: string
    created: number
    completed: number
    updated: number
    label: string
  }>
}

/**
 * Fetch all dashboard data in a single API call
 * This replaces 5 separate hooks with one efficient hook
 */
async function fetchDashboardData(days: 7 | 30 | 90 = 7): Promise<DashboardData> {
  const response = await fetch(`/api/dashboard/all?days=${days}`)
  const data = await response.json()

  if (!data.success) {
    throw new Error(data.error?.message || 'Failed to fetch dashboard data')
  }

  return data.data
}

/**
 * Hook to fetch all dashboard data efficiently
 */
export function useDashboardData(days: 7 | 30 | 90 = 7) {
  return useQuery({
    queryKey: ['dashboard-all', days],
    queryFn: () => fetchDashboardData(days),
    staleTime: 30 * 1000, // 30 seconds
    refetchOnMount: true,
    refetchOnWindowFocus: true,
  })
}
