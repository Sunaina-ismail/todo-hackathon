#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
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

# Step 1: Validate prerequisites
log_info "Step 1: Validating prerequisites..."
MISSING_TOOLS=()

if ! command -v minikube &> /dev/null; then
    MISSING_TOOLS+=("minikube")
fi

if ! command -v helm &> /dev/null; then
    MISSING_TOOLS+=("helm")
fi

if ! command -v docker &> /dev/null; then
    MISSING_TOOLS+=("docker")
fi

if ! command -v kubectl &> /dev/null; then
    MISSING_TOOLS+=("kubectl")
fi

if [ ${#MISSING_TOOLS[@]} -ne 0 ]; then
    log_error "Missing required tools: ${MISSING_TOOLS[*]}"
    log_error "Please install the missing tools and try again"
    exit 1
fi

log_success "All required tools are installed"

# Step 2: Check Minikube status
log_info "Step 2: Checking Minikube status..."
if minikube status &> /dev/null; then
    log_success "Minikube is already running"
else
    log_info "Starting Minikube..."
    minikube start
    log_success "Minikube started successfully"
fi

# Step 3: Configure Docker to use Minikube daemon
log_info "Step 3: Configuring Docker to use Minikube daemon..."
eval $(minikube docker-env)
log_success "Docker configured to use Minikube daemon"

# Step 4: Build Docker images
log_info "Step 4: Building Docker images..."
cd "$(dirname "$0")/.."

log_info "Building frontend image..."
docker build -t todo-frontend:latest ./frontend
log_success "Frontend image built successfully"

log_info "Building backend image..."
docker build -t todo-backend:latest ./backend
log_success "Backend image built successfully"

# Step 5: Load environment variables from .env
log_info "Step 5: Loading environment variables from .env..."
if [ ! -f .env ]; then
    log_error ".env file not found. Please create one from .env.example"
    exit 1
fi

# Source .env file
set -a
source .env
set +a

# Validate required environment variables
REQUIRED_VARS=("DATABASE_URL" "BETTER_AUTH_SECRET")
MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        MISSING_VARS+=("$var")
    fi
done

# Check if at least one LLM API key is set
if [ -z "$OPENAI_API_KEY" ] && [ -z "$OPENROUTER_API_KEY" ] && [ -z "$GROQ_API_KEY" ] && [ -z "$GEMINI_API_KEY" ]; then
    MISSING_VARS+=("At least one LLM API key (OPENAI_API_KEY, OPENROUTER_API_KEY, GROQ_API_KEY, or GEMINI_API_KEY)")
fi

if [ ${#MISSING_VARS[@]} -ne 0 ]; then
    log_error "Missing required environment variables: ${MISSING_VARS[*]}"
    exit 1
fi

log_success "All required environment variables are set"

# Step 6: Create Kubernetes namespace
log_info "Step 6: Creating Kubernetes namespace..."
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -
log_success "Namespace ready"

# Step 7: Deploy application with Helm
log_info "Step 7: Deploying application with Helm..."
helm upgrade --install todo-app ./helm/todo-app \
  -f ./helm/todo-app/values-dev.yaml \
  -n todo-app \
  --set secrets.DATABASE_URL="$DATABASE_URL" \
  --set secrets.BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET" \
  --set secrets.OPENAI_API_KEY="$OPENAI_API_KEY" \
  --set secrets.OPENROUTER_API_KEY="$OPENROUTER_API_KEY" \
  --set secrets.GROQ_API_KEY="$GROQ_API_KEY" \
  --set secrets.GEMINI_API_KEY="$GEMINI_API_KEY" \
  --set secrets.CLOUDFLARE_R2_ACCOUNT_ID="$CLOUDFLARE_R2_ACCOUNT_ID" \
  --set secrets.CLOUDFLARE_R2_ACCESS_KEY_ID="$CLOUDFLARE_R2_ACCESS_KEY_ID" \
  --set secrets.CLOUDFLARE_R2_SECRET_ACCESS_KEY="$CLOUDFLARE_R2_SECRET_ACCESS_KEY" \
  --set secrets.CLOUDFLARE_R2_BUCKET_NAME="$CLOUDFLARE_R2_BUCKET_NAME"

log_success "Helm deployment completed"

# Step 8: Wait for pods to be ready
log_info "Step 8: Waiting for pods to be ready (max 120 seconds)..."
if kubectl wait --for=condition=ready pod --all -n todo-app --timeout=120s; then
    log_success "All pods are ready"
else
    log_error "Pods failed to reach ready state within 120 seconds"
    log_info "Checking pod status..."
    kubectl get pods -n todo-app
    exit 1
fi

# Step 9: Display access information
log_success "Step 9: Deployment complete! Access information:"

echo ""
echo "=================================================="
echo "          TODO APPLICATION DEPLOYED"
echo "=================================================="
echo ""
echo "🌐 Access Application:"
echo ""
echo "   RECOMMENDED (WSL2/Windows):"
echo "   1. Forward Frontend Port (Keep running in a separate terminal):"
echo "      kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app --address 0.0.0.0"
echo ""
echo "   2. Forward Backend Port (Keep running in a separate terminal):"
echo "      kubectl port-forward svc/todo-app-backend 8001:8001 -n todo-app --address 0.0.0.0"
echo ""
echo "   Once forwarding is running:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend:  http://localhost:8001"
echo ""
echo "   Alternative (Linux/Mac):"
MINIKUBE_IP=$(minikube ip)
echo "   Frontend: http://$MINIKUBE_IP:30300"
echo ""
echo "📊 Useful Commands:"
echo "  - View pods:        kubectl get pods -n todo-app"
echo "  - View services:    kubectl get svc -n todo-app"
echo "  - Frontend logs:    kubectl logs -n todo-app -l app.kubernetes.io/component=frontend -f"
echo "  - Backend logs:     kubectl logs -n todo-app -l app.kubernetes.io/component=backend -f"
echo "  - Scale frontend:   kubectl scale deployment -n todo-app todo-app-frontend --replicas=3"
echo ""
echo "🗑️  Uninstall:"
echo "  - helm uninstall todo-app -n todo-app"
echo "  - kubectl delete namespace todo-app"
echo ""
echo "=================================================="
