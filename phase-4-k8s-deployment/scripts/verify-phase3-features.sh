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

log_info "Phase 3 Feature Parity Verification"
log_info "===================================="

# Get frontend and backend URLs
log_info "Setting up port forwarding..."
kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app --address 0.0.0.0 > /dev/null 2>&1 &
PF_PID=$!
sleep 5

FRONTEND_URL="http://localhost:3000"
BACKEND_URL="http://localhost:8001"

# Test 1: Authentication - Signup
log_info "Test 1: Testing authentication signup..."
SIGNUP_RESPONSE=$(curl -s -X POST "$FRONTEND_URL/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpassword123"}' || echo "FAILED")

if echo "$SIGNUP_RESPONSE" | grep -q "success\|token\|user"; then
    log_success "Signup endpoint working"
else
    log_error "Signup endpoint failed"
fi

# Test 2: Authentication - Signin
log_info "Test 2: Testing authentication signin..."
SIGNIN_RESPONSE=$(curl -s -X POST "$FRONTEND_URL/api/auth/signin" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpassword123"}' || echo "FAILED")

if echo "$SIGNIN_RESPONSE" | grep -q "success\|token\|user"; then
    log_success "Signin endpoint working"
    TOKEN=$(echo "$SIGNIN_RESPONSE" | grep -o '"token":"[^"]*"' | cut -d'"' -f4 || echo "")
else
    log_error "Signin endpoint failed"
    TOKEN=""
fi

# Test 3: Task Management - Create Task
log_info "Test 3: Testing task creation..."
if [ -n "$TOKEN" ]; then
    CREATE_TASK_RESPONSE=$(curl -s -X POST "$FRONTEND_URL/api/tasks" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $TOKEN" \
      -d '{"title":"Test Task","description":"Test Description"}' || echo "FAILED")
    
    if echo "$CREATE_TASK_RESPONSE" | grep -q "id\|task"; then
        log_success "Task creation working"
        TASK_ID=$(echo "$CREATE_TASK_RESPONSE" | grep -o '"id":[0-9]*' | cut -d':' -f2 || echo "")
    else
        log_error "Task creation failed"
        TASK_ID=""
    fi
else
    log_error "Skipping task tests - no authentication token"
    TASK_ID=""
fi

# Test 4: Task Management - List Tasks
log_info "Test 4: Testing task listing..."
if [ -n "$TOKEN" ]; then
    LIST_TASKS_RESPONSE=$(curl -s -X GET "$FRONTEND_URL/api/tasks" \
      -H "Authorization: Bearer $TOKEN" || echo "FAILED")
    
    if echo "$LIST_TASKS_RESPONSE" | grep -q "tasks\|\["; then
        log_success "Task listing working"
    else
        log_error "Task listing failed"
    fi
fi

# Test 5: AI Chatbot
log_info "Test 5: Testing AI chatbot endpoint..."
if [ -n "$TOKEN" ]; then
    CHAT_RESPONSE=$(curl -s -X POST "$FRONTEND_URL/api/chat" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $TOKEN" \
      -d '{"message":"Hello"}' || echo "FAILED")
    
    if echo "$CHAT_RESPONSE" | grep -q "response\|message"; then
        log_success "AI chatbot endpoint working"
    else
        log_error "AI chatbot endpoint failed"
    fi
fi

# Cleanup
kill $PF_PID 2>/dev/null || true

log_success "Phase 3 feature parity verification complete"
log_info "Review the output above to confirm all features are working"
