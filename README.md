# AWS Multi-Account Aggregation Tool

A comprehensive tool for aggregating and visualizing AWS resources across multiple accounts and services.

## Features

- 🔍 **Multi-Account Support**: Scrape data from multiple AWS accounts
- 🛡️ **Security Insights**: Aggregate SecurityHub and GuardDuty findings
- 📊 **Service Coverage**: IAM, SecurityHub, GuardDuty, Config, Lambda, S3, EKS, ECR
- 💾 **Local Storage**: SQLite database for offline access
- 🎨 **Modern UI**: React with shadcn/ui and Tailwind CSS
- ⚡ **Fast Backend**: Built with Bun and TypeScript

## Architecture

```
┌─────────────────┐
│   Frontend      │  React + shadcn/ui + Tailwind
│   (Vite)        │
└────────┬────────┘
         │
    HTTP API
         │
┌────────┴────────┐
│   Backend       │  Bun + TypeScript + Hono
│   (REST API)    │
└────────┬────────┘
         │
      SQLite
         │
┌────────┴────────┐
│   Scraper       │  Python + boto3
│   (AWS Data)    │
└─────────────────┘
```

## Prerequisites

- **Python** 3.10 or higher
- **Bun** 1.0 or higher ([Install Bun](https://bun.sh/))
- **Node.js** 18 or higher (for some tooling)
- **AWS Credentials** configured in `~/.aws/credentials` or environment variables

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/benhunter/awsui.git
cd awsui
```

### 2. Setup Python Scraper

```bash
cd scraper
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp accounts.yaml.example accounts.yaml
cp config.yaml.example config.yaml
# Edit accounts.yaml with your AWS account details
```

### 3. Initialize Database

```bash
cd ../database
sqlite3 awsui.db < schema.sql
```

### 4. Setup Backend

```bash
cd ../backend
bun install
cp .env.example .env
# Edit .env if needed
```

### 5. Setup Frontend

```bash
cd ../frontend
bun install
cp .env.example .env
# Edit .env if needed
```

### 6. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
bun run dev
```

**Terminal 2 - Frontend:**
```bash
cd frontend
bun run dev
```

**Terminal 3 - Run Scraper (one-time or scheduled):**
```bash
cd scraper
source venv/bin/activate
python -m src.cli
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:3000

## Configuration

### AWS Accounts (`scraper/accounts.yaml`)

```yaml
accounts:
  - name: "Production"
    account_id: "123456789012"
    profile: "prod-profile"
    regions:
      - "us-east-1"
      - "us-west-2"
```

### Scraper Settings (`scraper/config.yaml`)

Configure scraping behavior, services to scan, and retry logic.

### Environment Variables

See `.env.example` files in `backend/` and `frontend/` directories.

## Development

### Running Tests

**Scraper:**
```bash
cd scraper
pytest
pytest --cov=src --cov-report=html
```

**Backend:**
```bash
cd backend
bun test
```

**Frontend:**
```bash
cd frontend
bun test
```

### Project Structure

```
awsui/
├── scraper/          # Python AWS data scraper
│   ├── src/          # Source code
│   ├── tests/        # Tests
│   └── requirements.txt
├── backend/          # Bun/TypeScript API
│   ├── src/          # Source code
│   ├── tests/        # Tests
│   └── package.json
├── frontend/         # React application
│   ├── src/          # Source code
│   ├── tests/        # Tests
│   └── package.json
├── database/         # Database schema
│   └── schema.sql
├── docs/            # Documentation
└── ROADMAP.md       # Development roadmap
```

## Documentation

- [ROADMAP.md](ROADMAP.md) - Development roadmap and architecture
- [Database Schema](database/schema.sql) - Database structure
- API Documentation - Available at http://localhost:3000/docs (coming soon)

## AWS Permissions Required

The AWS credentials used must have read permissions for:
- IAM: `iam:List*`, `iam:Get*`
- SecurityHub: `securityhub:GetFindings`, `securityhub:DescribeHub`
- GuardDuty: `guardduty:ListDetectors`, `guardduty:ListFindings`, `guardduty:GetFindings`
- Config: `config:DescribeConfigurationRecorders`, `config:GetComplianceDetailsByConfigRule`
- Lambda: `lambda:ListFunctions`, `lambda:GetFunction`
- S3: `s3:ListAllMyBuckets`, `s3:GetBucketLocation`, `s3:GetBucketVersioning`, `s3:GetEncryptionConfiguration`
- EKS: `eks:ListClusters`, `eks:DescribeCluster`
- ECR: `ecr:DescribeRepositories`, `ecr:DescribeImages`

## Contributing

Contributions are welcome! Please follow these guidelines:
1. Follow test-driven development (TDD)
2. Write tests for new features
3. Ensure all tests pass
4. Update documentation

## License

See [LICENSE](LICENSE) file for details.

## Support

For issues and questions, please open an issue on GitHub.
