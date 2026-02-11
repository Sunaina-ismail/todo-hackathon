import { ChartSkeleton } from '@/components/dashboard/chart-skeleton'

export default function DashboardLoading() {
  return (
    <div className="space-y-8">
      {/* Welcome Section Skeleton */}
      <div>
        <div className="h-9 w-64 bg-forest-charcoal/30 rounded animate-pulse" />
        <div className="h-5 w-96 bg-forest-charcoal/20 rounded mt-2 animate-pulse" />
      </div>

      {/* Stats Grid Skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[...Array(6)].map((_, i) => (
          <ChartSkeleton key={i} height="h-32" />
        ))}
      </div>

      {/* Charts Grid Skeleton */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {[...Array(4)].map((_, i) => (
          <div
            key={i}
            className="bg-forest-charcoal/30 border border-forest-charcoal/50 rounded-lg p-6"
          >
            <div className="h-6 w-48 bg-forest-charcoal/40 rounded mb-4 animate-pulse" />
            <ChartSkeleton height="h-64" />
          </div>
        ))}
      </div>
    </div>
  )
}
