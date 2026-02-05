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

log_info "Network Access Verification"
log_info "============================"

# Test 1: Get Minikube IP
log_info "Test 1: Getting Minikube IP..."
MINIKUBE_IP=$(minikube ip 2>/dev/null || echo "")

if [ -n "$MINIKUBE_IP" ]; then
    log_success "Minikube IP: $MINIKUBE_IP"
else
    log_error "Failed to get Minikube IP"
    exit 1
fi

# Test 2: Test frontend NodePort access
log_info "Test 2: Testing frontend NodePort access..."
if curl -f -s "http://$MINIKUBE_IP:30300/api/health" > /dev/null 2>&1; then
    log_success "Frontend accessible via NodePort (http://$MINIKUBE_IP:30300)"
else
    log_error "Frontend NOT accessible via NodePort"
fi

# Test 3: Test internal backend access from frontend pod
log_info "Test 3: Testing internal backend access from frontend pod..."
FRONTEND_POD=$(kubectl get pods -n todo-app -l app.kubernetes.io/component=frontend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")

if [ -n "$FRONTEND_POD" ]; then
    if kubectl exec -n todo-app "$FRONTEND_POD" -- curl -f -s http://todo-app-backend:8001/api/health > /dev/null 2>&1; then
        log_success "Backend accessible from frontend pod via internal DNS"
    else
        log_error "Backend NOT accessible from frontend pod"
    fi
else
    log_error "No frontend pod found for testing"
fi

# Test 4: Verify backend is NOT externally accessible
log_info "Test 4: Verifying backend is NOT externally accessible..."
if curl -f -s "http://$MINIKUBE_IP:8001/api/health" > /dev/null 2>&1; then
    log_error "Backend IS externally accessible (security issue!)"
    exit 1
else
    log_success "Backend is NOT externally accessible (correct)"
fi

log_success "Network access verification complete"
log_info "Frontend: http://$MINIKUBE_IP:30300 (or use port-forward)"
log_info "Backend: Internal only (http://todo-app-backend:8001)"
