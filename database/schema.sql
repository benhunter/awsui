-- AWS UI Database Schema
-- SQLite Database for storing AWS account information

-- Accounts table
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id TEXT NOT NULL UNIQUE,
    account_name TEXT NOT NULL,
    account_alias TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- IAM Users
CREATE TABLE IF NOT EXISTS iam_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id TEXT NOT NULL,
    user_name TEXT NOT NULL,
    user_id TEXT,
    arn TEXT,
    create_date TIMESTAMP,
    password_last_used TIMESTAMP,
    mfa_enabled BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    UNIQUE(account_id, user_name)
);

-- IAM Roles
CREATE TABLE IF NOT EXISTS iam_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id TEXT NOT NULL,
    role_name TEXT NOT NULL,
    role_id TEXT,
    arn TEXT,
    create_date TIMESTAMP,
    description TEXT,
    max_session_duration INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    UNIQUE(account_id, role_name)
);

-- IAM Policies
CREATE TABLE IF NOT EXISTS iam_policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id TEXT NOT NULL,
    policy_name TEXT NOT NULL,
    policy_id TEXT,
    arn TEXT,
    default_version_id TEXT,
    attachment_count INTEGER DEFAULT 0,
    create_date TIMESTAMP,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    UNIQUE(account_id, arn)
);

-- SecurityHub Findings
CREATE TABLE IF NOT EXISTS security_hub_findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id TEXT NOT NULL,
    finding_id TEXT NOT NULL,
    title TEXT NOT NULL,
    severity TEXT,
    resource_type TEXT,
    resource_id TEXT,
    compliance_status TEXT,
    workflow_status TEXT,
    record_state TEXT,
    updated_at_aws TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    UNIQUE(account_id, finding_id)
);

-- GuardDuty Findings
CREATE TABLE IF NOT EXISTS guardduty_findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id TEXT NOT NULL,
    finding_id TEXT NOT NULL,
    finding_type TEXT,
    severity REAL,
    resource_type TEXT,
    service TEXT,
    region TEXT,
    updated_at_aws TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    UNIQUE(account_id, finding_id)
);

-- Config Resources
CREATE TABLE IF NOT EXISTS config_resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id TEXT NOT NULL,
    resource_id TEXT NOT NULL,
    resource_type TEXT,
    resource_name TEXT,
    compliance_status TEXT,
    region TEXT,
    configuration TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    UNIQUE(account_id, resource_id, region)
);

-- Lambda Functions
CREATE TABLE IF NOT EXISTS lambda_functions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id TEXT NOT NULL,
    function_name TEXT NOT NULL,
    function_arn TEXT,
    runtime TEXT,
    handler TEXT,
    memory_size INTEGER,
    timeout INTEGER,
    last_modified TIMESTAMP,
    code_size INTEGER,
    region TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    UNIQUE(account_id, function_name, region)
);

-- S3 Buckets
CREATE TABLE IF NOT EXISTS s3_buckets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id TEXT NOT NULL,
    bucket_name TEXT NOT NULL,
    creation_date TIMESTAMP,
    region TEXT,
    versioning_enabled BOOLEAN DEFAULT 0,
    encryption_enabled BOOLEAN DEFAULT 0,
    public_access_blocked BOOLEAN DEFAULT 1,
    logging_enabled BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    UNIQUE(account_id, bucket_name)
);

-- EKS Clusters
CREATE TABLE IF NOT EXISTS eks_clusters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id TEXT NOT NULL,
    cluster_name TEXT NOT NULL,
    cluster_arn TEXT,
    version TEXT,
    status TEXT,
    endpoint TEXT,
    region TEXT,
    created_at_aws TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    UNIQUE(account_id, cluster_name, region)
);

-- ECR Repositories
CREATE TABLE IF NOT EXISTS ecr_repositories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id TEXT NOT NULL,
    repository_name TEXT NOT NULL,
    repository_arn TEXT,
    repository_uri TEXT,
    created_at_aws TIMESTAMP,
    image_count INTEGER DEFAULT 0,
    region TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    UNIQUE(account_id, repository_name, region)
);

-- Scan History
CREATE TABLE IF NOT EXISTS scan_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id TEXT NOT NULL,
    service_name TEXT NOT NULL,
    scan_start TIMESTAMP NOT NULL,
    scan_end TIMESTAMP,
    status TEXT NOT NULL,
    error_message TEXT,
    records_collected INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_iam_users_account ON iam_users(account_id);
CREATE INDEX IF NOT EXISTS idx_iam_roles_account ON iam_roles(account_id);
CREATE INDEX IF NOT EXISTS idx_iam_policies_account ON iam_policies(account_id);
CREATE INDEX IF NOT EXISTS idx_security_hub_account ON security_hub_findings(account_id);
CREATE INDEX IF NOT EXISTS idx_security_hub_severity ON security_hub_findings(severity);
CREATE INDEX IF NOT EXISTS idx_guardduty_account ON guardduty_findings(account_id);
CREATE INDEX IF NOT EXISTS idx_guardduty_severity ON guardduty_findings(severity);
CREATE INDEX IF NOT EXISTS idx_config_account ON config_resources(account_id);
CREATE INDEX IF NOT EXISTS idx_config_compliance ON config_resources(compliance_status);
CREATE INDEX IF NOT EXISTS idx_lambda_account ON lambda_functions(account_id);
CREATE INDEX IF NOT EXISTS idx_s3_account ON s3_buckets(account_id);
CREATE INDEX IF NOT EXISTS idx_eks_account ON eks_clusters(account_id);
CREATE INDEX IF NOT EXISTS idx_ecr_account ON ecr_repositories(account_id);
CREATE INDEX IF NOT EXISTS idx_scan_history_account ON scan_history(account_id);
CREATE INDEX IF NOT EXISTS idx_scan_history_service ON scan_history(service_name);
