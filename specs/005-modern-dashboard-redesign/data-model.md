# Data Model: Modern Dashboard UI Redesign

**Feature**: 005-modern-dashboard-redesign
**Date**: 2026-01-26
**Status**: Complete

## Overview

This document defines the data structures and entities required for the modern dashboard UI redesign. All entities are derived from the feature specification requirements and support the Forest & Neon themed interface.

---

## Core Entities

### 1. DashboardMetrics

**Purpose**: Aggregated task statistics for dashboard overview display

**Fields**:
```typescript
interface DashboardMetrics {
  totalTasks: number           // Total number of tasks for user
  completedTasks: number       // Number of completed tasks
  pendingTasks: number         // Number of pending/active tasks
  completionRate: number       // Percentage (0-100) of completed tasks
  highPriorityCount: number    // Number of high priority tasks
  mediumPriorityCount: number  // Number of medium priority tasks
  lowPriorityCount: number     // Number of low priority tasks
  trendData: TrendDataPoint[]  // Time-series data for completion trend
  lastUpdated: string          // ISO timestamp of last calculation
}
```

**Source**: Aggregated from existing `Task` table in Neon PostgreSQL database

**Validation Rules**:
- All count fields must be non-negative integers
- `completionRate` must be between 0 and 100
- `totalTasks` must equal `completedTasks + pendingTasks`
- `lastUpdated` must be valid ISO 8601 timestamp

**Relationships**:
- Derived from multiple `Task` records filtered by `user_id`
- No direct database table (computed on-demand)

---

### 2. ChartDataPoint

**Purpose**: Individual data point for chart visualizations

**Fields**:
```typescript
interface ChartDataPoint {
  date: string        // ISO date string (YYYY-MM-DD)
  value: number       // Numeric value for the data point
  category?: string   // Optional category label (e.g., "high", "medium", "low")
  label?: string      // Optional display label
}
```

**Source**: Derived from `Task` completion timestamps and priority fields

**Validation Rules**:
- `date` must be valid ISO 8601 date string
- `value` must be numeric (can be negative for trends)
- `category` must match predefined categories if provided

**Usage**:
- Completion trend chart: `date` = day, `value` = tasks completed
- Priority distribution: `category` = priority level, `value` = count
- Activity timeline: `date` = day, `value` = total activity

---

### 3. TrendDataPoint

**Purpose**: Time-series data point for completion trends

**Fields**:
```typescript
interface TrendDataPoint {
  date: string           // ISO date string (YYYY-MM-DD)
  completed: number      // Tasks completed on this date
  created: number        // Tasks created on this date
  cumulative: number     // Cumulative completed tasks up to this date
}
```

**Source**: Aggregated from `Task` table `created_at` and `completed_at` timestamps

**Validation Rules**:
- `date` must be valid ISO 8601 date string
- All numeric fields must be non-negative integers
- `cumulative` must be monotonically increasing over time

---

### 4. PriorityDistribution

**Purpose**: Distribution of tasks by priority level

**Fields**:
```typescript
interface PriorityDistribution {
  high: number      // Count of high priority tasks
  medium: number    // Count of medium priority tasks
  low: number       // Count of low priority tasks
  total: number     // Total tasks (sum of all priorities)
}
```

**Source**: Aggregated from `Task` table `priority` field

**Validation Rules**:
- All fields must be non-negative integers
- `total` must equal `high + medium + low`

---

### 5. SidebarState

**Purpose**: User's sidebar UI preference state

**Fields**:
```typescript
interface SidebarState {
  isCollapsed: boolean    // Whether sidebar is collapsed
  activeRoute: string     // Current active route path
  lastToggled?: string    // ISO timestamp of last toggle action
}
```

**Source**:
- `isCollapsed`: localStorage (`sidebar-collapsed` key)
- `activeRoute`: Next.js router pathname
- `lastToggled`: localStorage (`sidebar-last-toggled` key)

**Validation Rules**:
- `isCollapsed` must be boolean
- `activeRoute` must match valid application routes
- `lastToggled` must be valid ISO 8601 timestamp if provided

**Storage**:
- Client-side only (localStorage)
- No server-side persistence required

---

### 6. LoadingState

**Purpose**: Component loading state management

**Fields**:
```typescript
interface LoadingState {
  isLoading: boolean                           // Whether component is loading
  loadingType: 'skeleton' | 'spinner' | 'progress'  // Type of loading indicator
  progress?: number                            // Optional progress percentage (0-100)
  error?: string                               // Optional error message
}
```

**Source**: Component state during async operations

**Validation Rules**:
- `isLoading` must be boolean
- `loadingType` must be one of the enum values
- `progress` must be between 0 and 100 if provided
- `error` should be present only when `isLoading` is false

**Usage**:
- Dashboard page: `loadingType: 'skeleton'`
- Button actions: `loadingType: 'spinner'`
- File uploads: `loadingType: 'progress'` with `progress` value

---

### 7. ChartConfiguration

**Purpose**: Chart display configuration and styling

**Fields**:
```typescript
interface ChartConfiguration {
  type: 'line' | 'area' | 'bar' | 'pie' | 'donut'  // Chart type
  title: string                                     // Chart title
  height: number                                    // Chart height in pixels
  showGrid: boolean                                 // Show grid lines
  showLegend: boolean                               // Show legend
  colors: {
    primary: string      // Primary color (Neon Lime #BEF264)
    secondary: string    // Secondary color
    background: string   // Background color (Forest Black #090E0C)
    text: string         // Text color (White #FFFFFF)
    grid: string         // Grid color (Emerald-Gray #64748B)
  }
  animation: {
    duration: number     // Animation duration in ms
    easing: string       // Easing function name
  }
}
```

**Source**: Static configuration in component props

**Validation Rules**:
- `type` must be one of the enum values
- `height` must be positive integer
- All color values must be valid hex codes
- `animation.duration` must be positive integer

**Default Configuration**:
```typescript
const defaultChartConfig: ChartConfiguration = {
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
```

---

## Derived Data Structures

### 8. StatCard

**Purpose**: Individual metric card on dashboard

**Fields**:
```typescript
interface StatCard {
  id: string              // Unique identifier
  title: string           // Card title (e.g., "Total Tasks")
  value: number | string  // Primary value to display
  change?: number         // Percentage change from previous period
  trend?: 'up' | 'down' | 'neutral'  // Trend direction
  icon?: string           // Icon name/component
  color?: string          // Accent color (defaults to Neon Lime)
}
```

**Source**: Derived from `DashboardMetrics`

**Example**:
```typescript
const totalTasksCard: StatCard = {
  id: 'total-tasks',
  title: 'Total Tasks',
  value: metrics.totalTasks,
  change: 12.5,
  trend: 'up',
  icon: 'CheckSquare',
  color: '#BEF264'
}
```

---

### 9. ActivityData

**Purpose**: User activity timeline data

**Fields**:
```typescript
interface ActivityData {
  date: string           // ISO date string
  tasksCreated: number   // Tasks created on this date
  tasksCompleted: number // Tasks completed on this date
  tasksUpdated: number   // Tasks updated on this date
  totalActivity: number  // Sum of all activities
}
```

**Source**: Aggregated from `Task` table timestamps

**Validation Rules**:
- All numeric fields must be non-negative integers
- `totalActivity` must equal sum of other activity counts

---

## Data Flow

### Dashboard Metrics Flow

```
User Request → API Route → Database Query → Aggregate Data → DashboardMetrics → UI Components
```

1. User navigates to dashboard
2. Dashboard page fetches metrics from `/api/dashboard/metrics`
3. API route queries Task table filtered by user_id
4. Data is aggregated into DashboardMetrics structure
5. Metrics are returned to client
6. UI components render charts and stat cards

### Chart Data Flow

```
DashboardMetrics → Chart Utilities → ChartDataPoint[] → Recharts Components → Rendered Charts
```

1. DashboardMetrics contains raw data
2. Chart utility functions transform data into ChartDataPoint arrays
3. ChartDataPoint arrays are passed to Recharts components
4. Recharts renders visualizations with Forest & Neon styling

### Sidebar State Flow

```
User Toggle → useSidebar Hook → localStorage → Component Re-render → Framer Motion Animation
```

1. User clicks sidebar toggle button
2. `useSidebar` hook updates state
3. State is persisted to localStorage
4. Component re-renders with new state
5. Framer Motion animates layout change

---

## Type Definitions Location

All TypeScript type definitions will be located in:
```
phase-3-ai-todo-chatbot/frontend/lib/types.ts
```

This centralizes type definitions for easy import across components:
```typescript
import type { DashboardMetrics, ChartDataPoint, SidebarState } from '@/lib/types'
```

---

## Database Schema (Existing)

**Note**: This redesign uses existing database schema from Phase 2. No schema changes required.

**Relevant Tables**:
- `tasks`: Contains all task data (id, user_id, title, description, priority, status, created_at, completed_at)
- `users`: Contains user authentication data
- `conversations`: Contains AI chatbot conversation history (Phase 3)
- `messages`: Contains individual chat messages (Phase 3)

**Key Indexes** (already exist):
- `tasks.user_id` - For filtering tasks by user
- `tasks.created_at` - For time-based queries
- `tasks.completed_at` - For completion trend analysis
- `tasks.priority` - For priority distribution

---

## Data Transformation Utilities

Location: `phase-3-ai-todo-chatbot/frontend/lib/chart-utils.ts`

**Key Functions**:

```typescript
// Transform tasks into completion trend data
export function getCompletionTrend(
  tasks: Task[],
  days: number = 7
): TrendDataPoint[]

// Transform tasks into priority distribution
export function getPriorityDistribution(
  tasks: Task[]
): PriorityDistribution

// Transform tasks into activity timeline
export function getActivityTimeline(
  tasks: Task[],
  days: number = 30
): ActivityData[]

// Calculate dashboard metrics from tasks
export function calculateMetrics(
  tasks: Task[]
): DashboardMetrics
```

---

**Data Model Status**: ✅ Complete
**All Entities Defined**: Yes
**Ready for Contract Definition**: Yes
