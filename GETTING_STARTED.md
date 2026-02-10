# AWS Multi-Account Aggregation Tool - Getting Started

## What Has Been Built

This project is a **comprehensive AWS multi-account aggregation tool** that helps you collect and visualize AWS resources across multiple accounts and services.

### Current Implementation Status

✅ **Fully Working MVP** with the following features:

1. **Python Scraper** (boto3)
   - IAM users, roles, and policies scraper
   - Command-line interface
   - 17 tests passing with 65% code coverage
   - Extensible architecture for adding more services

2. **Backend API** (Node.js + Express + SQLite)
   - REST API with endpoints for accounts and IAM data
   - Dashboard aggregation
   - Scan history tracking

3. **Frontend Dashboard** (React + Tailwind CSS)
   - Beautiful, responsive UI
   - Dashboard with key metrics
   - Account selection
   - IAM users table with MFA status

4. **Database** (SQLite)
   - Complete schema for all planned AWS services
   - Optimized with indexes
   - Demo data included

5. **Documentation**
   - Comprehensive ROADMAP.md
   - Setup instructions
   - Security review
   - Configuration examples

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- AWS credentials configured

### 1. Clone and Setup

```bash
git clone https://github.com/benhunter/awsui.git
cd awsui
```

### 2. Initialize Database

```bash
cd database
sqlite3 awsui.db < schema.sql
cd ..
```

### 3. Setup Python Scraper

#### Using `uv` for Python Environment Management

This project now uses [`uv`](https://github.com/astral-sh/uv) for Python environment and dependency management instead of `python -m venv` and `pip`.

**Why `uv`?**

- Much faster dependency installation
- Modern, reliable, and compatible with `pip`/`venv` workflows
- No need to manually activate/deactivate virtual environments

#### Quick Start for Scraper

1. **Install `uv`**
   - [See official instructions](https://github.com/astral-sh/uv#installation)
   - Example (recommended):
     ```bash
     # On Windows, Mac, or Linux (requires Python 3.8+)
     pip install uv
     # Or use a prebuilt binary from the releases page
     ```

2. **Install dependencies and set up**

   ```bash
   cd scraper
   uv venv .venv
   uv pip install -r requirements.txt
   cp accounts.yaml.example accounts.yaml
   cp config.yaml.example config.yaml
   # Edit accounts.yaml with your AWS account details
   ```

3. **Activate the environment**

   ```bash
   # On Windows:
   .venv\Scripts\activate
   # On Mac/Linux:
   source .venv/bin/activate
   ```

4. **Run the scraper**
   ```bash
   uv pip install -r requirements.txt  # (if not already done)
   python -m src.cli
   ```

**Notes:**

- You can still use `deactivate` to exit the environment.
- `uv` is a drop-in replacement for most `pip`/`venv` commands.
- For more, see the [uv documentation](https://github.com/astral-sh/uv).

### 4. Run Scraper (Optional - Demo data already loaded)

```bash
# Run the scraper
python -m src.cli

# Or run tests
pytest -v
```

### 5. Start Backend API

```bash
cd ../backend
npm install
npm start
# Server runs on http://localhost:3000
```

### 6. Start Frontend

```bash
# In a new terminal
cd frontend
npm install
npm run dev
# App runs on http://localhost:5173
```

### 7. Access the Application

Open your browser to **http://localhost:5173**

You'll see:

- Dashboard with statistics (accounts, users, roles, findings)
- Account cards (click to view details)
- IAM users table with MFA status

## Demo Data

The application comes with demo data so you can explore it immediately:

- 2 AWS accounts (Production and Development)
- 5 IAM users with MFA status
- 3 IAM roles
- Scan history

## Next Steps

### To Use With Your AWS Accounts

1. Edit `scraper/accounts.yaml` with your AWS account details
2. Ensure AWS credentials are configured (via `~/.aws/credentials` or environment variables)
3. Run the scraper: `python -m src.cli`
4. Refresh the dashboard to see your actual AWS data

### To Add More AWS Services

The framework is ready for additional services. To add a new service:

1. Create a scraper in `scraper/src/scrapers/`
2. Add database insert methods in `scraper/src/database.py`
3. Add API endpoints in `backend/src/index.js`
4. Add UI components in `frontend/src/`

See `ROADMAP.md` for detailed implementation plans for:

- SecurityHub findings
- GuardDuty findings
- AWS Config resources
- Lambda functions
- S3 buckets
- EKS clusters
- ECR repositories

## Development Workflow

### Running Tests

```bash
cd scraper
pytest -v
pytest --cov=src --cov-report=html
```

### Code Review and Security

The code has been:

- ✅ Code reviewed with all feedback addressed
- ✅ Security scanned with CodeQL
- ✅ Tested (17 tests passing)
- ✅ Documented

See `docs/SECURITY.md` for security considerations.

## Architecture Overview

```
┌─────────────────┐
│   Frontend      │  React + Tailwind CSS
│   (Port 5173)   │  - Dashboard
└────────┬────────┘  - Account views
         │           - IAM tables
    HTTP API
         │
┌────────┴────────┐
│   Backend       │  Node.js + Express
│   (Port 3000)   │  - REST API
└────────┬────────┘  - SQLite queries
         │
      SQLite
         │
┌────────┴────────┐
│   Database      │  awsui.db
│                 │  - Accounts
└────────┬────────┘  - IAM data
         │           - Service data
         │
┌────────┴────────┐
│   Scraper       │  Python + boto3
│   (CLI)         │  - AWS API calls
└─────────────────┘  - Data collection
```

## Project Structure

```
awsui/
├── scraper/          # Python AWS scraper
│   ├── src/
│   │   ├── config.py         # Configuration loader
│   │   ├── database.py       # Database manager
│   │   ├── base_scraper.py   # Base scraper class
│   │   ├── cli.py            # Command-line interface
│   │   └── scrapers/
│   │       └── iam_scraper.py
│   ├── tests/                # 17 tests
│   ├── accounts.yaml.example
│   ├── config.yaml.example
│   └── requirements.txt
│
├── backend/          # Node.js API server
│   ├── src/
│   │   └── index.js          # Express server
│   └── package.json
│
├── frontend/         # React dashboard
│   ├── src/
│   │   ├── App.tsx           # Main app component
│   │   ├── main.tsx
│   │   └── index.css
│   └── package.json
│
├── database/         # SQLite database
│   ├── schema.sql            # Database schema
│   └── awsui.db             # Database file (with demo data)
│
├── docs/
│   └── SECURITY.md           # Security review
│
├── README.md                 # Setup instructions
├── ROADMAP.md               # Development plan
└── .gitignore
```

## Troubleshooting

### Database Errors

- Make sure the database is initialized: `sqlite3 database/awsui.db < database/schema.sql`
- Check database permissions

### Backend Won't Start

- Install dependencies: `npm install`
- Check port 3000 is available
- Verify database path in backend/.env

### Frontend Won't Start

- Install dependencies: `npm install`
- Check port 5173 is available
- Verify API URL in frontend/.env

### Scraper Errors

- Verify AWS credentials are configured
- Check AWS IAM permissions
- Review accounts.yaml configuration

## Production Deployment

Before deploying to production, implement:

1. **Rate Limiting** on API endpoints (see docs/SECURITY.md)
2. **Authentication** for API access
3. **HTTPS** enforcement
4. **Environment-based configuration**
5. **Monitoring and logging**

See ROADMAP.md Phase 7 for complete deployment guide.

## Contributing

This project follows test-driven development:

1. Write tests first
2. Implement features
3. Run tests
4. Document changes

## Support

- Check ROADMAP.md for development plans
- Review docs/SECURITY.md for security considerations
- See README.md for detailed setup instructions

## License

See LICENSE file for details.

---

**Status**: MVP Complete ✅  
**Tests**: 17 passing ✅  
**Security**: Reviewed ✅  
**Ready for**: Development & Demo ✅  
**Production**: Requires hardening (see ROADMAP.md Phase 7)
