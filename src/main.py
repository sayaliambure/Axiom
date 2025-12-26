"""
Main FastAPI application for AXIOM.

This is the entry point for the API server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, companies, financial_snapshots, hire_scenarios, hiring_impact
from .database import Base, engine

# Import all models so SQLAlchemy registers them
from .db_models import User, Company, FinancialSnapshot, HireScenario

# Create database tables
# In production, use Alembic migrations instead
# This ensures tables exist when the app starts
def init_database():
    """Initialize database tables."""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables initialized")
    except Exception as e:
        print(f"⚠️  Warning: Could not create database tables: {e}")
        print("   Make sure PostgreSQL is running and database 'axiom' exists")
        raise

# Initialize database on startup
init_database()

# Create FastAPI app
app = FastAPI(
    title="AXIOM API",
    description="Hiring Decision Intelligence Tool for Startup Founders",
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure OpenAPI schema for better Swagger UI experience
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="AXIOM API",
        version="0.2.0",
        description="Hiring Decision Intelligence Tool for Startup Founders",
        routes=app.routes,
    )
    # Replace OAuth2 with simple Bearer token scheme
    # Remove any OAuth2 schemes that FastAPI might have added automatically
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    
    # Set only Bearer token scheme (remove OAuth2)
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token. Get it by calling POST /api/auth/login"
        }
    }
    
    # Add security requirements to all protected endpoints
    # Protected endpoints are those that use get_current_user dependency
    # Map paths to their HTTP methods that need protection
    protected_endpoints = {
        "/api/auth/me": ["get"],
        "/api/companies": ["get", "post"],
        "/api/companies/{company_id}": ["get"],
        "/api/financial-snapshots": ["get", "post"],
        "/api/financial-snapshots/{snapshot_id}": ["get", "patch", "delete"],
        "/api/hire-scenarios": ["get", "post"],
        "/api/hire-scenarios/{scenario_id}": ["get", "patch", "delete"],
        "/api/hiring-impact/calculate": ["post"]
    }
    
    # Apply Bearer security to protected endpoints
    for path, path_item in openapi_schema.get("paths", {}).items():
        # Check if this exact path needs protection
        if path in protected_endpoints:
            methods = protected_endpoints[path]
            for method in methods:
                if method in path_item:
                    operation = path_item[method]
                    # Add security requirement
                    operation["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Configure CORS
# In production, restrict origins to your frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(companies.router, prefix="/api")
app.include_router(financial_snapshots.router, prefix="/api")
app.include_router(hire_scenarios.router, prefix="/api")
app.include_router(hiring_impact.router, prefix="/api")


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "AXIOM API",
        "version": "0.2.0",
        "description": "Hiring Decision Intelligence Tool for Startup Founders",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

