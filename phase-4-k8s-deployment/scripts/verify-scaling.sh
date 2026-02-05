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

log_info "Horizontal Pod Scaling Verification"
log_info "===================================="

# Test 1: Scale frontend to 3 replicas
log_info "Test 1: Scaling frontend to 3 replicas..."
kubectl scale deployment -n todo-app todo-app-frontend --replicas=3

log_info "Waiting for rollout to complete..."
kubectl rollout status deployment -n todo-app todo-app-frontend --timeout=120s

# Test 2: Verify all 3 pods are ready
log_info "Test 2: Verifying all 3 frontend pods are ready..."
READY_PODS=$(kubectl get pods -n todo-app -l app.kubernetes.io/component=frontend -o jsonpath='{.items[?(@.status.phase=="Running")].metadata.name}' | wc -w)

if [ "$READY_PODS" -eq 3 ]; then
    log_success "All 3 frontend pods are ready"
else
    log_error "Expected 3 ready pods, found $READY_PODS"
    exit 1
fi

# Test 3: Scale backend to 2 replicas
log_info "Test 3: Scaling backend to 2 replicas..."
kubectl scale deployment -n todo-app todo-app-backend --replicas=2

log_info "Waiting for rollout to complete..."
kubectl rollout status deployment -n todo-app todo-app-backend --timeout=120s

# Test 4: Verify all 2 backend pods are ready
log_info "Test 4: Verifying all 2 backend pods are ready..."
READY_PODS=$(kubectl get pods -n todo-app -l app.kubernetes.io/component=backend -o jsonpath='{.items[?(@.status.phase=="Running")].metadata.name}' | wc -w)

if [ "$READY_PODS" -eq 2 ]; then
    log_success "All 2 backend pods are ready"
else
    log_error "Expected 2 ready pods, found $READY_PODS"
    exit 1
fi

# Test 5: Scale back to 1 replica each
log_info "Test 5: Scaling back to 1 replica each..."
kubectl scale deployment -n todo-app todo-app-frontend --replicas=1
kubectl scale deployment -n todo-app todo-app-backend --replicas=1

log_info "Waiting for scale-down to complete..."
sleep 10

log_success "Horizontal pod scaling verification complete"
log_info "Final pod status:"
kubectl get pods -n todo-app
