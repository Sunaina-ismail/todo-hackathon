# kagent Guide for Todo Application

This document provides working examples of using kagent for automated diagnostics and monitoring of the Todo application Kubernetes deployment.

## Prerequisites

Install kagent:
```bash
# Installation instructions
# Visit: https://github.com/kubeshop/kagent
```

## Example 1: Automated Pod Restart Diagnostics

**Scenario**: A pod keeps restarting and you need to understand why.

**Command**:
```bash
kagent diagnose pod-restarts --namespace todo-app
```

**Expected Output**:
```
🔍 Analyzing pod restart patterns in namespace: todo-app

📊 Findings:
- todo-app-backend-xyz: 3 restarts in last hour
  Reason: Liveness probe failed
  Last error: Database connection timeout
  
🔧 Recommendations:
1. Check database connectivity from pod
2. Increase liveness probe initialDelaySeconds
3. Review database connection pool settings

📝 Detailed Events:
- 10:15:23 Liveness probe failed: Get "http://10.244.0.5:8001/api/health": context deadline exceeded
- 10:15:38 Container backend failed liveness probe, will be restarted
- 10:15:45 Container backend started
```

**Explanation**: kagent analyzes pod events, logs, and probe failures to identify the root cause of restarts and provides actionable recommendations.

---

## Example 2: Resource Usage Monitoring

**Scenario**: You want to monitor CPU and memory usage across all pods.

**Command**:
```bash
kagent monitor resources --namespace todo-app --duration 5m
```

**Expected Output**:
```
📈 Resource Usage Monitoring (5 minute window)

Frontend Pods:
┌─────────────────────────┬──────────┬──────────┬────────┬────────┐
│ Pod                     │ CPU Avg  │ CPU Peak │ Mem Avg│ Mem Peak│
├─────────────────────────┼──────────┼──────────┼────────┼────────┤
│ todo-app-frontend-abc   │ 45m      │ 120m     │ 180Mi  │ 245Mi  │
└─────────────────────────┴──────────┴──────────┴────────┴────────┘

Backend Pods:
┌─────────────────────────┬──────────┬──────────┬────────┬────────┐
│ Pod                     │ CPU Avg  │ CPU Peak │ Mem Avg│ Mem Peak│
├─────────────────────────┼──────────┼──────────┼────────┼────────┤
│ todo-app-backend-xyz    │ 85m      │ 180m     │ 320Mi  │ 410Mi  │
└─────────────────────────┴──────────┴──────────┴────────┴────────┘

⚠️  Alerts:
- Backend pod approaching memory limit (410Mi / 512Mi = 80%)

🔧 Recommendations:
- Consider increasing backend memory limit to 768Mi
- Monitor for memory leaks if usage continues to grow
```

**Explanation**: kagent continuously monitors resource usage and provides alerts when pods approach their resource limits.

---

## Example 3: Health Probe Failure Analysis

**Scenario**: Readiness probes are failing and pods aren't receiving traffic.

**Command**:
```bash
kagent analyze probes --namespace todo-app --component backend
```

**Expected Output**:
```
🏥 Health Probe Analysis: todo-app-backend

Liveness Probe:
✅ Status: Passing
   Endpoint: /api/health
   Success Rate: 100% (120/120 checks)
   
Readiness Probe:
❌ Status: Failing
   Endpoint: /api/ready
   Success Rate: 45% (54/120 checks)
   
🔍 Failure Analysis:
- Database connectivity check failing intermittently
- Error pattern: "connection refused" (60% of failures)
- Error pattern: "timeout" (40% of failures)

📊 Timeline:
10:00 - Probe started failing
10:05 - Pod removed from service endpoints
10:10 - Database connection restored
10:12 - Probe passing again
10:15 - Pod added back to service endpoints

🔧 Recommendations:
1. Investigate database connection stability
2. Add connection retry logic to readiness probe
3. Consider increasing probe timeout from 5s to 10s
4. Review database connection pool configuration

📝 Related Logs:
[10:05:23] ERROR: Database connection failed: connection refused
[10:05:38] WARNING: Readiness probe failed 3 consecutive times
[10:10:15] INFO: Database connection restored
```

**Explanation**: kagent analyzes probe success/failure patterns, correlates with logs and events, and provides specific recommendations for fixing probe issues.

---

## Additional kagent Commands

### Check Deployment Health
```bash
kagent health-check --namespace todo-app
```

### Analyze Network Issues
```bash
kagent diagnose network --namespace todo-app
```

### Generate Incident Report
```bash
kagent report --namespace todo-app --output incident-report.md
```

---

## Tips for Using kagent

1. **Run regularly**: Set up kagent monitoring as a cron job
2. **Export reports**: Use `--output` flag to save analysis results
3. **Combine with alerts**: Integrate kagent with your alerting system
4. **Historical analysis**: Use `--since` flag to analyze past incidents

---

## Troubleshooting

If kagent doesn't provide useful insights:
1. Ensure pods have been running long enough to generate data
2. Check that kagent has proper RBAC permissions
3. Increase analysis duration with `--duration` flag
4. Review kagent logs: `kagent logs`
