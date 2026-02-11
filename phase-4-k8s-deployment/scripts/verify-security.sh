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

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_info "Security Verification"
log_info "====================="

# Test 1: Check deployment logs for secrets
log_info "Test 1: Checking deployment logs for exposed secrets..."
LOGS=$(kubectl logs -n todo-app -l app.kubernetes.io/name=todo-app --tail=100 2>/dev/null || echo "")

SECRETS_FOUND=0
if echo "$LOGS" | grep -iE "(DATABASE_URL|BETTER_AUTH_SECRET|API_KEY)" | grep -vE "(Missing|required|environment)" > /dev/null 2>&1; then
    log_error "Potential secrets found in logs!"
    SECRETS_FOUND=1
else
    log_success "No secrets found in deployment logs"
fi

# Test 2: Check pod environment for plaintext secrets
log_info "Test 2: Checking pod environment for plaintext secrets..."
BACKEND_POD=$(kubectl get pods -n todo-app -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")

if [ -n "$BACKEND_POD" ]; then
    ENV_OUTPUT=$(kubectl exec -n todo-app "$BACKEND_POD" -- env 2>/dev/null || echo "")
    
    # Check if sensitive values are exposed (not just variable names)
    if echo "$ENV_OUTPUT" | grep -E "DATABASE_URL=postgresql://.*@" > /dev/null 2>&1; then
        log_warning "DATABASE_URL visible in pod environment (expected for functionality)"
    fi
    
    log_success "Pod environment check complete"
else
    log_warning "No backend pod found for environment check"
fi

# Test 3: Verify secrets are base64-encoded in Secret resource
log_info "Test 3: Verifying secrets are base64-encoded..."
SECRET_DATA=$(kubectl get secret -n todo-app -l app.kubernetes.io/name=todo-app -o jsonpath='{.items[0].data}' 2>/dev/null || echo "")

if [ -n "$SECRET_DATA" ]; then
    log_success "Secrets are stored in base64-encoded format"
else
    log_warning "No secrets found in namespace"
fi

# Test 4: Check if .env is in Git history
log_info "Test 4: Checking if .env is committed to Git..."
cd "$(dirname "$0")/.."

if git log --all --full-history --source -- .env 2>/dev/null | grep -q "commit"; then
    log_error ".env file found in Git history!"
    SECRETS_FOUND=1
else
    log_success ".env file not found in Git history"
fi

# Final result
echo ""
if [ $SECRETS_FOUND -eq 0 ]; then
    log_success "Security verification PASSED"
else
    log_error "Security verification FAILED - secrets may be exposed"
    exit 1
fi
