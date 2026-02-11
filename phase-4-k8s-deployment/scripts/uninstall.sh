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

log_info "Uninstalling Todo Application"
log_info "=============================="

# Step 1: Remove Helm release
log_info "Step 1: Removing Helm release..."
if helm list -n todo-app | grep -q todo-app; then
    helm uninstall todo-app -n todo-app
    log_success "Helm release removed"
else
    log_info "No Helm release found"
fi

# Step 2: Delete namespace
log_info "Step 2: Deleting namespace..."
if kubectl get namespace todo-app > /dev/null 2>&1; then
    kubectl delete namespace todo-app
    log_success "Namespace deleted"
else
    log_info "Namespace already deleted"
fi

# Step 3: Verify cleanup
log_info "Step 3: Verifying cleanup..."
if kubectl get all -n todo-app > /dev/null 2>&1; then
    log_error "Some resources still exist in namespace"
    kubectl get all -n todo-app
else
    log_success "All resources removed"
fi

log_success "Uninstall complete"
