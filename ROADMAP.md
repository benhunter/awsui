# AWS Multi-Account Aggregation Tool - Roadmap

## Overview
This roadmap outlines the development plan for an AWS multi-account aggregation tool that collects information from multiple AWS services across multiple accounts and displays it through a web interface.

## Architecture

### High-Level Components
1. **AWS Data Scraper** (Python + boto3)
   - Collects data from multiple AWS accounts
   - Supports: IAM, SecurityHub, GuardDuty, Config, Lambda, S3, EKS, ECR
   - Stores data in SQLite database

2. **Backend API** (Bun + TypeScript)
   - RESTful API to serve data from SQLite
   - Handles authentication and authorization
   - Provides endpoints for each AWS service

3. **Frontend Web App** (React + shadcn + Tailwind CSS)
   - Dashboard view showing all accounts and services
   - Service-specific detail views
   - Account-specific views
   - Data visualization and filtering

## Technology Stack

### Backend
- **Runtime**: Bun (JavaScript/TypeScript runtime)
- **Language**: TypeScript
- **Web Framework**: Hono (lightweight and fast)
- **Database**: SQLite with better-sqlite3
- **ORM**: Drizzle ORM (TypeScript-first)

### Frontend
- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **UI Components**: shadcn/ui
- **Styling**: Tailwind CSS
- **State Management**: TanStack Query (React Query)
- **Routing**: React Router

### Data Scraper
- **Language**: Python 3.10+
- **AWS SDK**: boto3
- **Database**: SQLite3
- **Testing**: pytest

## Development Phases

### Phase 1: Project Setup and Infrastructure (Days 1-2)
**Goal**: Establish project structure and basic infrastructure

#### Tasks:
1. **Project Structure**
   ```
   awsui/
   ├── scraper/          # Python AWS scraper
   │   ├── src/
   │   ├── tests/
   │   └── requirements.txt
   ├── backend/          # Bun/TypeScript API
   │   ├── src/
   │   ├── tests/
   │   └── package.json
   ├── frontend/         # React app
   │   ├── src/
   │   ├── tests/
   │   └── package.json
   ├── database/         # SQLite database schema
   │   └── schema.sql
   ├── docs/            # Documentation
   └── README.md
   ```

2. **Initialize Scraper Module**
   - Setup Python virtual environment
   - Install boto3, pytest, and dependencies
   - Create basic project structure
   - Setup pytest configuration

3. **Initialize Backend**
   - Initialize Bun project
   - Install Hono, Drizzle ORM, better-sqlite3
   - Setup TypeScript configuration
   - Create basic server structure

4. **Initialize Frontend**
   - Create Vite + React + TypeScript project
   - Install shadcn/ui components
   - Setup Tailwind CSS
   - Configure TanStack Query

5. **Database Schema Design**
   - Design tables for each AWS service
   - Create migration scripts
   - Setup Drizzle schema

**Deliverables**:
- ✅ Project structure created
- ✅ All package managers initialized
- ✅ Basic configuration files in place
- ✅ Development environment setup guide

### Phase 2: Database Design (Days 2-3)
**Goal**: Design and implement database schema

#### Tables Design:

1. **accounts**
   - id, account_id, account_name, account_alias, created_at, updated_at

2. **iam_users**
   - id, account_id, user_name, user_id, arn, create_date, password_last_used, mfa_enabled

3. **iam_roles**
   - id, account_id, role_name, role_id, arn, create_date, description

4. **iam_policies**
   - id, account_id, policy_name, policy_id, arn, default_version_id, attachment_count

5. **security_hub_findings**
   - id, account_id, finding_id, title, severity, resource_type, compliance_status, updated_at

6. **guardduty_findings**
   - id, account_id, finding_id, finding_type, severity, resource_type, service, updated_at

7. **config_resources**
   - id, account_id, resource_id, resource_type, resource_name, compliance_status, region

8. **lambda_functions**
   - id, account_id, function_name, function_arn, runtime, handler, memory_size, timeout, last_modified

9. **s3_buckets**
   - id, account_id, bucket_name, creation_date, region, versioning_enabled, encryption_enabled, public_access

10. **eks_clusters**
    - id, account_id, cluster_name, cluster_arn, version, status, endpoint, created_at

11. **ecr_repositories**
    - id, account_id, repository_name, repository_arn, repository_uri, created_at, image_count

12. **scan_history**
    - id, account_id, service_name, scan_start, scan_end, status, error_message, records_collected

**Deliverables**:
- ✅ Complete database schema
- ✅ Migration scripts
- ✅ Database documentation

### Phase 3: AWS Data Scraper Development (Days 3-7)
**Goal**: Build Python scraper to collect AWS data

#### Test-Driven Development Approach:
For each service, follow this pattern:
1. Write tests first (using mocks)
2. Implement scraper
3. Run tests and verify
4. Integration test with real AWS (optional)

#### Implementation Order:

1. **Base Scraper Infrastructure** (Day 3)
   - Account manager (handle multiple AWS accounts)
   - Configuration loader (AWS credentials, accounts to scan)
   - Database connection manager
   - Logging framework
   - Error handling and retry logic
   - **Tests**: Mock AWS credentials, test account switching

2. **IAM Scraper** (Day 4)
   - List users, roles, policies
   - Get user details (MFA status, access keys)
   - Store in database
   - **Tests**: Mock boto3 IAM responses

3. **SecurityHub Scraper** (Day 4)
   - Get findings by severity
   - Get compliance status
   - **Tests**: Mock SecurityHub findings

4. **GuardDuty Scraper** (Day 5)
   - List detectors
   - Get findings
   - **Tests**: Mock GuardDuty responses

5. **Config Scraper** (Day 5)
   - List discovered resources
   - Get compliance status
   - **Tests**: Mock Config responses

6. **Lambda Scraper** (Day 6)
   - List functions
   - Get function configurations
   - **Tests**: Mock Lambda responses

7. **S3 Scraper** (Day 6)
   - List buckets
   - Get bucket configurations (versioning, encryption, public access)
   - **Tests**: Mock S3 responses

8. **EKS Scraper** (Day 7)
   - List clusters
   - Get cluster details
   - **Tests**: Mock EKS responses

9. **ECR Scraper** (Day 7)
   - List repositories
   - Get image counts
   - **Tests**: Mock ECR responses

10. **Orchestrator** (Day 7)
    - Schedule and run all scrapers
    - Handle parallel execution
    - Record scan history
    - **Tests**: Integration tests

**Deliverables**:
- ✅ Complete scraper for all 8 AWS services
- ✅ Unit tests for each scraper (>80% coverage)
- ✅ Configuration documentation
- ✅ CLI tool to run scrapers

### Phase 4: Backend API Development (Days 8-11)
**Goal**: Build TypeScript backend API with Bun

#### Test-Driven Development Approach:
1. Write API endpoint tests
2. Implement endpoint
3. Test with real database
4. Add integration tests

#### Implementation:

1. **Core Setup** (Day 8)
   - Hono server setup
   - Database connection with Drizzle ORM
   - Middleware (CORS, logging, error handling)
   - **Tests**: Server startup, middleware

2. **Account Endpoints** (Day 8)
   ```
   GET /api/accounts - List all accounts
   GET /api/accounts/:id - Get account details
   ```
   - **Tests**: Test account listing and details

3. **IAM Endpoints** (Day 9)
   ```
   GET /api/accounts/:id/iam/users
   GET /api/accounts/:id/iam/roles
   GET /api/accounts/:id/iam/policies
   ```
   - **Tests**: Test IAM data retrieval

4. **Security Endpoints** (Day 9)
   ```
   GET /api/accounts/:id/security-hub/findings
   GET /api/accounts/:id/guardduty/findings
   GET /api/accounts/:id/config/resources
   ```
   - **Tests**: Test security data retrieval

5. **Service Endpoints** (Day 10)
   ```
   GET /api/accounts/:id/lambda/functions
   GET /api/accounts/:id/s3/buckets
   GET /api/accounts/:id/eks/clusters
   GET /api/accounts/:id/ecr/repositories
   ```
   - **Tests**: Test service data retrieval

6. **Dashboard/Aggregation Endpoints** (Day 10)
   ```
   GET /api/dashboard - Overview of all accounts
   GET /api/dashboard/security - Security overview
   GET /api/dashboard/compliance - Compliance overview
   ```
   - **Tests**: Test aggregation logic

7. **Scan Management** (Day 11)
   ```
   GET /api/scans/history - Scan history
   POST /api/scans/trigger - Trigger new scan (calls Python scraper)
   ```
   - **Tests**: Test scan management

8. **Filtering and Pagination** (Day 11)
   - Add query parameters for filtering
   - Implement pagination
   - **Tests**: Test filtering and pagination

**Deliverables**:
- ✅ Complete RESTful API
- ✅ API tests (>80% coverage)
- ✅ API documentation (OpenAPI/Swagger)
- ✅ Postman collection

### Phase 5: Frontend Development (Days 12-18)
**Goal**: Build React frontend with shadcn/ui

#### Test-Driven Development Approach:
1. Write component tests (React Testing Library)
2. Implement component
3. Test in browser
4. Add E2E tests (optional)

#### Implementation:

1. **Base Setup** (Day 12)
   - Vite + React + TypeScript
   - Tailwind CSS configuration
   - shadcn/ui components
   - React Router setup
   - TanStack Query setup
   - **Tests**: App renders, routing works

2. **Layout and Navigation** (Day 12)
   ```
   - Header with navigation
   - Sidebar for accounts/services
   - Main content area
   - Footer
   ```
   - **Tests**: Navigation components

3. **Dashboard Page** (Day 13)
   ```
   - Overview cards (total accounts, findings, resources)
   - Recent scans widget
   - Security alerts widget
   - Compliance status widget
   ```
   - **Tests**: Dashboard components

4. **Accounts Page** (Day 13)
   ```
   - List of all accounts
   - Account cards with quick stats
   - Search and filter
   ```
   - **Tests**: Account list component

5. **Account Detail Page** (Day 14)
   ```
   - Account overview
   - Service tabs (IAM, SecurityHub, etc.)
   - Resource counts per service
   ```
   - **Tests**: Account detail component

6. **IAM Views** (Day 14)
   ```
   - Users table with sorting/filtering
   - Roles table
   - Policies table
   - Detail modals
   ```
   - **Tests**: IAM components

7. **Security Views** (Day 15)
   ```
   - SecurityHub findings table
   - GuardDuty findings table
   - Severity filters
   - Compliance status charts
   ```
   - **Tests**: Security components

8. **Config View** (Day 15)
   ```
   - Resources table
   - Compliance status filter
   - Resource type filter
   ```
   - **Tests**: Config components

9. **Service Views** (Days 16-17)
   ```
   - Lambda functions table
   - S3 buckets table with security info
   - EKS clusters table
   - ECR repositories table
   ```
   - **Tests**: Service components

10. **Data Visualization** (Day 17)
    ```
    - Charts for findings by severity
    - Compliance trends
    - Resource distribution
    ```
    - Use recharts or similar
    - **Tests**: Chart components

11. **Scan Management UI** (Day 18)
    ```
    - Scan history table
    - Trigger scan button
    - Scan progress indicator
    ```
    - **Tests**: Scan management components

12. **Polish and Responsive Design** (Day 18)
    ```
    - Mobile responsiveness
    - Loading states
    - Error handling
    - Empty states
    ```
    - **Tests**: Responsive tests

**Deliverables**:
- ✅ Complete React application
- ✅ Component tests (>70% coverage)
- ✅ Responsive design
- ✅ User documentation

### Phase 6: Integration and Testing (Days 19-20)
**Goal**: End-to-end testing and integration

#### Tasks:
1. **Integration Testing**
   - Test scraper → database → API → frontend flow
   - Test with real AWS accounts (if available)
   - Performance testing

2. **Bug Fixes**
   - Address issues found during testing
   - Optimize slow queries
   - Fix UI/UX issues

3. **Documentation**
   - Complete README with setup instructions
   - Configuration guide
   - API documentation
   - User guide

4. **Deployment Preparation**
   - Docker configuration (optional)
   - Environment variable documentation
   - Security best practices

**Deliverables**:
- ✅ Fully integrated system
- ✅ All tests passing
- ✅ Complete documentation
- ✅ Deployment guide

### Phase 7: Deployment and Documentation (Days 21-22)
**Goal**: Deploy and finalize documentation

#### Tasks:
1. **Deployment Options**
   - Local deployment instructions
   - Docker Compose setup
   - Cloud deployment guide (AWS EC2, ECS, etc.)

2. **Security Hardening**
   - Review AWS credentials management
   - Add rate limiting
   - Input validation
   - SQL injection prevention

3. **Monitoring and Logging**
   - Setup application logging
   - Error tracking
   - Performance monitoring

4. **Final Documentation**
   - Architecture diagrams
   - API reference
   - User guide
   - Troubleshooting guide

**Deliverables**:
- ✅ Deployed application
- ✅ Complete documentation
- ✅ Security review completed

## Testing Strategy

### Test-Driven Development (TDD)
Each component will be developed following TDD:
1. **Red**: Write a failing test
2. **Green**: Write minimal code to pass the test
3. **Refactor**: Improve code while keeping tests green

### Test Coverage Goals
- **Scraper**: >80% code coverage
- **Backend API**: >80% code coverage
- **Frontend**: >70% code coverage

### Test Types
1. **Unit Tests**
   - Test individual functions and classes
   - Mock external dependencies (AWS API, database)

2. **Integration Tests**
   - Test component interactions
   - Test database operations
   - Test API endpoints

3. **End-to-End Tests** (Optional)
   - Test complete user workflows
   - Use Playwright or Cypress

## Configuration Management

### AWS Credentials
```yaml
# config/accounts.yaml
accounts:
  - name: "Production"
    account_id: "123456789012"
    profile: "prod-profile"
    regions: ["us-east-1", "us-west-2"]
  - name: "Development"
    account_id: "210987654321"
    profile: "dev-profile"
    regions: ["us-east-1"]
```

### Scraper Configuration
```yaml
# config/scraper.yaml
scraper:
  parallel_accounts: 3
  services:
    - iam
    - securityhub
    - guardduty
    - config
    - lambda
    - s3
    - eks
    - ecr
  schedule: "0 */6 * * *"  # Every 6 hours
```

### API Configuration
```env
# backend/.env
DATABASE_PATH=./data/awsui.db
PORT=3000
LOG_LEVEL=info
CORS_ORIGIN=http://localhost:5173
```

### Frontend Configuration
```env
# frontend/.env
VITE_API_URL=http://localhost:3000
```

## Future Enhancements

### Phase 8: Advanced Features (Future)
1. **Real-time Updates**
   - WebSocket support for live data
   - Automatic refresh on new scans

2. **Advanced Analytics**
   - Trend analysis over time
   - Cost analysis (integrate with Cost Explorer)
   - Resource utilization metrics

3. **Alerting and Notifications**
   - Email/Slack notifications for critical findings
   - Custom alert rules
   - Webhook support

4. **Multi-user Support**
   - User authentication
   - Role-based access control
   - Audit logging

5. **Export and Reporting**
   - PDF/Excel exports
   - Custom reports
   - Scheduled reports

6. **Additional AWS Services**
   - CloudTrail
   - CloudWatch
   - VPC
   - RDS
   - DynamoDB

7. **Cloud Provider Extension**
   - Azure support
   - GCP support

## Success Criteria

### Minimum Viable Product (MVP)
- ✅ Scraper collects data from all 8 AWS services
- ✅ Data stored in SQLite database
- ✅ Backend API serves data via REST endpoints
- ✅ Frontend displays data in organized, filterable views
- ✅ Can view data by account or by service
- ✅ Basic security (no hardcoded credentials)
- ✅ >70% test coverage overall

### Quality Metrics
- All core features working
- No critical bugs
- Tests passing
- Documentation complete
- Code follows TypeScript/Python best practices

## Timeline Summary
- **Phase 1-2**: Setup and Database (Days 1-3)
- **Phase 3**: Scraper Development (Days 3-7)
- **Phase 4**: Backend API (Days 8-11)
- **Phase 5**: Frontend (Days 12-18)
- **Phase 6**: Integration (Days 19-20)
- **Phase 7**: Deployment (Days 21-22)

**Total Estimated Time**: 22 development days (4-5 weeks)

## Getting Started
1. Review this roadmap
2. Setup development environment
3. Clone repository
4. Follow Phase 1 setup instructions
5. Begin implementing with TDD approach

---

**Last Updated**: February 2026
**Version**: 1.0
