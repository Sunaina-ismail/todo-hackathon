#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_info "Health Monitoring Verification"
log_info "================================"

# Test 1: Verify liveness probe triggers restart
log_info "Test 1: Testing liveness probe (manual verification required)"
log_info "To test: kubectl exec -n todo-app deployment/todo-app-backend -- kill 1"
log_info "Expected: Pod should restart within 30 seconds"

# Test 2: Verify readiness probe removes pod from service
log_info "Test 2: Testing readiness probe (manual verification required)"
log_info "To test: Break database connection and check pod status"
log_info "Expected: Pod should be removed from service endpoints"

# Test 3: Check current pod status
log_info "Test 3: Checking current pod status..."
kubectl get pods -n todo-app

# Test 4: Check pod events for probe activity
log_info "Test 4: Checking pod events..."
kubectl get events -n todo-app --sort-by='.lastTimestamp' | tail -20

log_success "Health monitoring verification complete"
log_info "Review the output above to confirm probe behavior"
