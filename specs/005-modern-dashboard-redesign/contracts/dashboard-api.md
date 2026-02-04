# API Contract: Dashboard Metrics

**Endpoint**: `/api/dashboard/metrics`
**Method**: GET
**Authentication**: Required (JWT token)
**Feature**: 005-modern-dashboard-redesign

## Overview

This endpoint provides aggregated task statistics for the authenticated user's dashboard overview. It returns metrics including total tasks, completion rates, priority distribution, and trend data for visualization.

---

## Request

### Headers

```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| timeRange | string | No | "7d" | Time range for trend data: "7d", "30d", "90d" |

### Example Request

```bash
GET /api/dashboard/metrics?timeRange=7d
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Response

### Success Response (200 OK)

```typescript
{
  "success": true,
  "data": {
    "totalTasks": 42,
    "completedTasks": 28,
    "pendingTasks": 14,
    "completionRate": 66.67,
    "highPriorityCount": 5,
    "mediumPriorityCount": 8,
    "lowPriorityCount": 1,
    "trendData": [
      {
        "date": "2026-01-20",
        "completed": 3,
        "created": 2,
        "cumulative": 25
      },
      {
        "date": "2026-01-21",
        "completed": 5,
        "created": 1,
        "cumulative": 30
      }
      // ... more data points
    ],
    "lastUpdated": "2026-01-26T10:30:00Z"
  }
}
```

### Response Schema

```typescript
interface DashboardMetricsResponse {
  success: boolean
  data: {
    totalTasks: number           // Total number of tasks
    completedTasks: number       // Number of completed tasks
    pendingTasks: number         // Number of pending tasks
    completionRate: number       // Percentage (0-100)
    highPriorityCount: number    // High priority task count
    mediumPriorityCount: number  // Medium priority task count
    lowPriorityCount: number     // Low priority task count
    trendData: Array<{
      date: string               // ISO date (YYYY-MM-DD)
      completed: number          // Tasks completed on date
      created: number            // Tasks created on date
      cumulative: number         // Cumulative completed
    }>
    lastUpdated: string          // ISO timestamp
  }
}
```

### Error Responses

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
    "code": "INVALID_TIME_RANGE",
    "message": "timeRange must be one of: 7d, 30d, 90d"
  }
}
```

**500 Internal Server Error**
```json
{
  "success": false,
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "Failed to fetch dashboard metrics"
  }
}
```

---

## Business Rules

1. **User Isolation**: Only return metrics for authenticated user's tasks
2. **Time Range**: Trend data limited to requested time range (default 7 days)
3. **Completion Rate**: Calculated as `(completedTasks / totalTasks) * 100`
4. **Priority Counts**: Only count pending tasks (exclude completed)
5. **Trend Data**: Sorted chronologically (oldest to newest)
6. **Cumulative**: Cumulative count includes all completed tasks up to date

---

## Performance Considerations

- **Caching**: Response cached for 5 minutes per user
- **Query Optimization**: Use database indexes on `user_id`, `created_at`, `completed_at`
- **Data Limit**: Trend data limited to maximum 90 days
- **Response Time**: Target < 200ms for cached, < 500ms for fresh query

---

## Implementation Notes

### Backend (FastAPI)

```python
@router.get("/dashboard/metrics")
async def get_dashboard_metrics(
    time_range: str = Query("7d", regex="^(7d|30d|90d)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> DashboardMetricsResponse:
    """
    Get aggregated dashboard metrics for authenticated user.
    """
    # Query tasks filtered by user_id
    # Aggregate metrics
    # Calculate trend data
    # Return response
```

### Frontend (Next.js)

```typescript
// hooks/use-dashboard-metrics.ts
export function useDashboardMetrics(timeRange: '7d' | '30d' | '90d' = '7d') {
  return useQuery({
    queryKey: ['dashboard-metrics', timeRange],
    queryFn: () => fetchDashboardMetrics(timeRange),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}
```

---

## Testing

### Test Cases

1. **Valid Request**: Returns metrics for authenticated user
2. **Invalid Time Range**: Returns 400 error
3. **Unauthenticated**: Returns 401 error
4. **No Tasks**: Returns zero counts with empty trend data
5. **Large Dataset**: Handles 1000+ tasks efficiently

### Example Test

```typescript
describe('GET /api/dashboard/metrics', () => {
  it('returns metrics for authenticated user', async () => {
    const response = await request(app)
      .get('/api/dashboard/metrics?timeRange=7d')
      .set('Authorization', `Bearer ${validToken}`)
      .expect(200)

    expect(response.body.success).toBe(true)
    expect(response.body.data.totalTasks).toBeGreaterThanOrEqual(0)
    expect(response.body.data.completionRate).toBeGreaterThanOrEqual(0)
    expect(response.body.data.completionRate).toBeLessThanOrEqual(100)
  })
})
```

---

**Contract Status**: ✅ Complete
**Breaking Changes**: None (new endpoint)
**Backward Compatibility**: N/A
