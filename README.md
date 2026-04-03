# Trip Planner — 2-Tier k8s App

```
Frontend (Node.js/Express)  :3000  ──►  Backend (Python/Flask)  :5000
     NodePort Service                        ClusterIP Service
```

## API Endpoints

| Friendly URL (frontend)      | Backend API             | Description                        |
|------------------------------|-------------------------|------------------------------------|
| `GET /`                      | —                       | Serves the HTML UI                 |
| `GET /locations`             | `/api/locations`        | All trip destinations              |
| `GET /locations?location=Goa`| `/api/locations/1`      | Single location detail             |
| `GET /mustvisit`             | `/api/mustvisit`        | All must-visit places              |
| `GET /mustvisit?location=Goa`| `/api/mustvisit/Goa`    | Must-visit for one location        |
| `GET /weather?location=Manali`| `/api/weather/Manali`  | Current weather                    |
| `GET /itinerary?location=Goa`| `/api/itinerary/Goa`   | Day-by-day itinerary               |
| `GET /health`                | `/health`               | Health check (proxied to backend)  |

## Quick Start

### 1. Build images

```bash
# Backend
docker build -t trip-backend:latest ./backend

# Frontend
docker build -t trip-frontend:latest ./frontend
```

### 2. (minikube) Load images into cluster

```bash
minikube image load trip-backend:latest
minikube image load trip-frontend:latest
```

### 3. Deploy to k8s

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/backend-deployment.yaml  -n trip-planner
kubectl apply -f k8s/frontend-deployment.yaml -n trip-planner
```

### 4. Verify pods are running

```bash
kubectl get pods -n trip-planner
kubectl get svc  -n trip-planner
```

### 5. Open the app

```bash
# minikube
minikube service trip-frontend-service -n trip-planner

# or NodePort
kubectl get nodes -o wide   # grab <node-ip>
open http://<node-ip>:30080
```

### 6. Hit the API directly

```bash
# via kubectl port-forward (no NodePort needed)
kubectl port-forward svc/trip-frontend-service 3000:3000 -n trip-planner

curl http://localhost:3000/locations
curl http://localhost:3000/mustvisit?location=Goa
curl http://localhost:3000/weather?location=Manali
curl http://localhost:3000/itinerary?location=Goa
curl http://localhost:3000/health
```

## File Structure

```
trip-planner/
├── backend/
│   ├── app.py              # Flask API
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/server.js       # Express proxy + route aliases
│   ├── public/index.html   # HTML UI
│   ├── package.json
│   └── Dockerfile
├── k8s/
│   ├── namespace.yaml
│   ├── backend-deployment.yaml   # Deployment + ClusterIP Service
│   └── frontend-deployment.yaml  # Deployment + NodePort Service
└── README.md
```

## Key k8s Concepts Demonstrated

- **2-tier separation**: Frontend pod talks to backend pod via ClusterIP DNS
- **ClusterIP**: Backend is internal-only — no direct external access
- **NodePort**: Frontend is exposed to the outside world on port 30080
- **Environment variable injection**: `BACKEND_URL` is set via `env:` in the pod spec
- **Health/readiness probes**: Both tiers have liveness + readiness checks
- **Resource limits**: CPU and memory limits set on both containers
- **Labels & selectors**: Services use `selector: app: trip-*` to find the right pods
