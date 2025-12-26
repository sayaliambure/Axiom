# AXIOM - Hiring Decision Intelligence Tool

## Phase 1: Core Domain & Financial Logic ✅

This phase implements the core financial models and calculation logic for determining hiring impact on runway.

## Phase 2: Backend API (FastAPI) ✅

This phase implements the REST API with authentication, CRUD operations, and hiring impact calculation endpoints.

### Project Structure

```
axiom/
├── src/
│   ├── __init__.py
│   ├── models.py              # Core domain models (Phase 1)
│   ├── services.py            # Financial calculation services (Phase 1)
│   ├── database.py            # Database configuration
│   ├── db_models.py           # SQLAlchemy database models
│   ├── schemas.py             # Pydantic request/response schemas
│   ├── auth.py                # Authentication utilities
│   ├── main.py                # FastAPI application
│   └── routers/
│       ├── auth.py            # Authentication routes
│       ├── companies.py       # Company CRUD routes
│       ├── financial_snapshots.py  # Financial snapshot CRUD routes
│       ├── hire_scenarios.py      # Hire scenario CRUD routes
│       └── hiring_impact.py       # Hiring impact calculation route
├── examples/
│   └── usage_examples.py      # Example inputs/outputs (Phase 1)
├── requirements.txt
├── alembic.ini                 # Database migration config
└── README.md
```

### Core Assumptions

1. **Monthly Burn Rate**: Calculated as (Monthly Revenue - Monthly Expenses)
   - Negative burn = spending more than earning
   - Positive burn = earning more than spending (rare for early startups)

2. **Runway Calculation**: 
   - Runway (months) = Current Cash / Monthly Burn Rate
   - Assumes burn rate remains constant (no growth/revenue changes)

3. **Hiring Impact**:
   - New hire adds to monthly expenses (salary + benefits + overhead)
   - Burn rate increases by hire cost
   - Runway decreases proportionally

4. **Runway Delta**:
   - Difference between current runway and runway after hire
   - Negative delta = runway shortened
   - Positive delta = runway extended (only if hire generates revenue > cost)

### Phase 2: API Endpoints

#### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

#### Companies
- `POST /api/companies` - Create a company
- `GET /api/companies` - List user's companies
- `GET /api/companies/{id}` - Get company details

#### Financial Snapshots
- `POST /api/financial-snapshots?company_id={id}` - Create financial snapshot
- `GET /api/financial-snapshots?company_id={id}` - List snapshots
- `GET /api/financial-snapshots/{id}` - Get snapshot details
- `PATCH /api/financial-snapshots/{id}` - Update snapshot
- `DELETE /api/financial-snapshots/{id}` - Delete snapshot

#### Hire Scenarios
- `POST /api/hire-scenarios?company_id={id}` - Create hire scenario
- `GET /api/hire-scenarios?company_id={id}` - List scenarios
- `GET /api/hire-scenarios/{id}` - Get scenario details
- `PATCH /api/hire-scenarios/{id}` - Update scenario
- `DELETE /api/hire-scenarios/{id}` - Delete scenario

#### Hiring Impact
- `POST /api/hiring-impact/calculate` - Calculate hiring impact on runway

### Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL database:**
   ```bash
   createdb axiom
   ```

3. **Configure environment variables:**
   Create a `.env` file (optional, defaults are in `src/database.py`):
   ```
   DATABASE_URL=postgresql://postgres:pass123@localhost:5432/axiom
   SECRET_KEY=your-secret-key-change-in-production
   ```

4. **Initialize database tables:**
   ```bash
   python init_db.py
   ```
   Or the tables will be created automatically when you start the server.
   
   **If you get schema errors** (e.g., "column does not exist"), run:
   ```bash
   python fix_db.py
   ```
   This will drop and recreate all tables with the correct schema.
   ⚠️  WARNING: This deletes all existing data!

5. **Run the API server:**
   ```bash
   python run_server.py
   ```
   Or:
   ```bash
   uvicorn src.main:app --reload
   ```

5. **Access API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Usage

- **Phase 1**: See `examples/usage_examples.py` for detailed examples of the core financial logic.
- **Phase 2**: Use the API endpoints above to interact with the system programmatically.

