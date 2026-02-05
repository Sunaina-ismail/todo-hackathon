// Type definitions for Modern Dashboard UI Redesign (Forest & Neon Edition)

export interface DashboardMetrics {
  totalTasks: number
  completedTasks: number
  pendingTasks: number
  completionRate: number
  highPriorityCount: number
  mediumPriorityCount: number
  lowPriorityCount: number
  trendData: TrendDataPoint[]
  lastUpdated: string
}

export interface ChartDataPoint {
  date: string
  value: number
  category?: string
  label?: string
  color?: string
}

export interface TrendDataPoint {
  date: string
  completed: number
  created: number
  cumulative: number
}

export interface PriorityDistribution {
  high: number
  medium: number
  low: number
  total: number
}

export interface SidebarState {
  isCollapsed: boolean
  activeRoute: string
  lastToggled?: string
}

export interface LoadingState {
  isLoading: boolean
  loadingType: 'skeleton' | 'spinner' | 'progress'
  progress?: number
  error?: string
}

export interface ChartConfiguration {
  type: 'line' | 'area' | 'bar' | 'pie' | 'donut'
  title: string
  height: number
  showGrid: boolean
  showLegend: boolean
  colors: {
    primary: string
    secondary: string
    background: string
    text: string
    grid: string
  }
  animation: {
    duration: number
    easing: string
  }
}

export interface StatCard {
  id: string
  title: string
  value: number | string
  change?: number
  trend?: 'up' | 'down' | 'neutral'
  icon?: string
  color?: string
}

export interface ActivityData {
  date: string
  tasksCreated: number
  tasksCompleted: number
  tasksUpdated: number
  totalActivity: number
}

// Default chart configuration
export const defaultChartConfig: ChartConfiguration = {
  type: 'line',
  title: '',
  height: 300,
  showGrid: true,
  showLegend: true,
  colors: {
    primary: '#BEF264',
    secondary: '#10B981',
    background: '#090E0C',
    text: '#FFFFFF',
    grid: '#64748B'
  },
  animation: {
    duration: 800,
    easing: 'ease-out'
  }
}
