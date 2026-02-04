# API Contract: Chart Data Endpoints

**Feature**: 005-modern-dashboard-redesign
**Authentication**: Required (JWT token)

## Overview

These endpoints provide formatted data for various chart visualizations on the dashboard. All endpoints return data optimized for Recharts components with Forest & Neon color scheme.

---

## 1. Completion Trend Chart

**Endpoint**: `/api/dashboard/completion-trend`
**Method**: GET

### Request

**Query Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| days | number | No | 7 | Number of days to include (7, 30, or 90) |

### Response (200 OK)

```typescript
{
  "success": true,
  "data": [
    {
      "date": "2026-01-20",
      "value": 3,
      "label": "Jan 20"
    },
    {
      "date": "2026-01-21",
      "value": 5,
      "label": "Jan 21"
    }
    // ... more data points
  ]
}
```

### Response Schema

```typescript
interface CompletionTrendResponse {
  success: boolean
  data: Array<{
    date: string      // ISO date (YYYY-MM-DD)
    value: number     // Tasks completed on this date
    label: string     // Formatted date for display
  }>
}
```

---

## 2. Priority Distribution Chart

**Endpoint**: `/api/dashboard/priority-distribution`
**Method**: GET

### Request

**Query Parameters**: None (uses all pending tasks)

### Response (200 OK)

```typescript
{
  "success": true,
  "data": [
    {
      "category": "high",
      "value": 5,
      "label": "High Priority",
      "color": "#EF4444"
    },
    {
      "category": "medium",
      "value": 8,
      "label": "Medium Priority",
      "color": "#F59E0B"
    },
    {
      "category": "low",
      "value": 1,
      "label": "Low Priority",
      "color": "#10B981"
    }
  ]
}
```

### Response Schema

```typescript
interface PriorityDistributionResponse {
  success: boolean
  data: Array<{
    category: 'high' | 'medium' | 'low'
    value: number       // Count of tasks
    label: string       // Display label
    color: string       // Hex color code
  }>
}
```

---

## 3. Activity Timeline Chart

**Endpoint**: `/api/dashboard/activity-timeline`
**Method**: GET

### Request

**Query Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| days | number | No | 30 | Number of days to include (7, 30, or 90) |

### Response (200 OK)

```typescript
{
  "success": true,
  "data": [
    {
      "date": "2026-01-20",
      "created": 2,
      "completed": 3,
      "updated": 5,
      "label": "Jan 20"
    },
    {
      "date": "2026-01-21",
      "created": 1,
      "completed": 5,
      "updated": 3,
      "label": "Jan 21"
    }
    // ... more data points
  ]
}
```

### Response Schema

```typescript
interface ActivityTimelineResponse {
  success: boolean
  data: Array<{
    date: string        // ISO date (YYYY-MM-DD)
    created: number     // Tasks created
    completed: number   // Tasks completed
    updated: number     // Tasks updated
    label: string       // Formatted date
  }>
}
```

---

## 4. Task Status Breakdown

**Endpoint**: `/api/dashboard/status-breakdown`
**Method**: GET

### Request

**Query Parameters**: None

### Response (200 OK)

```typescript
{
  "success": true,
  "data": [
    {
      "category": "completed",
      "value": 28,
      "label": "Completed",
      "percentage": 66.67,
      "color": "#BEF264"
    },
    {
      "category": "pending",
      "value": 14,
      "label": "Pending",
      "percentage": 33.33,
      "color": "#1A221E"
    }
  ]
}
```

### Response Schema

```typescript
interface StatusBreakdownResponse {
  success: boolean
  data: Array<{
    category: 'completed' | 'pending'
    value: number         // Count of tasks
    label: string         // Display label
    percentage: number    // Percentage of total
    color: string         // Hex color code
  }>
}
```

---

## Common Error Responses

**401 Unauthorized**
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

**400 Bad Request**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "days must be 7, 30, or 90"
  }
}
```

**500 Internal Server Error**
```json
{
  "success": false,
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "Failed to fetch chart data"
  }
}
```

---

## Business Rules

1. **User Isolation**: All endpoints filter by authenticated user's ID
2. **Date Range**: Limited to 7, 30, or 90 days
3. **Empty Data**: Return empty arrays for users with no tasks
4. **Sorting**: All time-series data sorted chronologically
5. **Colors**: Use Forest & Neon palette consistently

---

## Performance Considerations

- **Caching**: Cache responses for 5 minutes per user
- **Aggregation**: Perform aggregation in database query
- **Data Points**: Limit to maximum 90 data points per chart
- **Response Time**: Target < 300ms per endpoint

---

## Frontend Integration

```typescript
// hooks/use-chart-data.ts
export function useCompletionTrend(days: 7 | 30 | 90 = 7) {
  return useQuery({
    queryKey: ['completion-trend', days],
    queryFn: () => fetchCompletionTrend(days),
    staleTime: 5 * 60 * 1000,
  })
}

export function usePriorityDistribution() {
  return useQuery({
    queryKey: ['priority-distribution'],
    queryFn: () => fetchPriorityDistribution(),
    staleTime: 5 * 60 * 1000,
  })
}

export function useActivityTimeline(days: 7 | 30 | 90 = 30) {
  return useQuery({
    queryKey: ['activity-timeline', days],
    queryFn: () => fetchActivityTimeline(days),
    staleTime: 5 * 60 * 1000,
  })
}

export function useStatusBreakdown() {
  return useQuery({
    queryKey: ['status-breakdown'],
    queryFn: () => fetchStatusBreakdown(),
    staleTime: 5 * 60 * 1000,
  })
}
```

---

**Contract Status**: ✅ Complete
**Breaking Changes**: None (new endpoints)
**Backward Compatibility**: N/A
