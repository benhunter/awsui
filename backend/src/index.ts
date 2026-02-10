import { Hono } from 'hono'
import { cors } from 'hono/cors'
import { logger } from 'hono/logger'
import Database from 'better-sqlite3'

const app = new Hono()

// Middleware
app.use('*', logger())
app.use('*', cors())

// Database connection
const dbPath = process.env.DATABASE_PATH || '../database/awsui.db'
const db = new Database(dbPath)

// Health check
app.get('/health', (c) => {
  return c.json({ status: 'ok', timestamp: new Date().toISOString() })
})

// Get all accounts
app.get('/api/accounts', (c) => {
  const accounts = db.prepare('SELECT * FROM accounts ORDER BY account_name').all()
  return c.json(accounts)
})

// Get specific account
app.get('/api/accounts/:id', (c) => {
  const accountId = c.req.param('id')
  const account = db.prepare('SELECT * FROM accounts WHERE account_id = ?').get(accountId)
  
  if (!account) {
    return c.json({ error: 'Account not found' }, 404)
  }
  
  return c.json(account)
})

// Get IAM users for an account
app.get('/api/accounts/:id/iam/users', (c) => {
  const accountId = c.req.param('id')
  const users = db.prepare('SELECT * FROM iam_users WHERE account_id = ? ORDER BY user_name').all(accountId)
  return c.json(users)
})

// Get IAM roles for an account
app.get('/api/accounts/:id/iam/roles', (c) => {
  const accountId = c.req.param('id')
  const roles = db.prepare('SELECT * FROM iam_roles WHERE account_id = ? ORDER BY role_name').all(accountId)
  return c.json(roles)
})

// Get IAM policies for an account
app.get('/api/accounts/:id/iam/policies', (c) => {
  const accountId = c.req.param('id')
  const policies = db.prepare('SELECT * FROM iam_policies WHERE account_id = ? ORDER BY policy_name').all(accountId)
  return c.json(policies)
})

// Get SecurityHub findings for an account
app.get('/api/accounts/:id/security-hub/findings', (c) => {
  const accountId = c.req.param('id')
  const severity = c.req.query('severity')
  
  let query = 'SELECT * FROM security_hub_findings WHERE account_id = ?'
  const params: any[] = [accountId]
  
  if (severity) {
    query += ' AND severity = ?'
    params.push(severity)
  }
  
  query += ' ORDER BY updated_at_aws DESC'
  
  const findings = db.prepare(query).all(...params)
  return c.json(findings)
})

// Get scan history
app.get('/api/scans/history', (c) => {
  const accountId = c.req.query('account_id')
  const service = c.req.query('service')
  
  let query = 'SELECT * FROM scan_history WHERE 1=1'
  const params: any[] = []
  
  if (accountId) {
    query += ' AND account_id = ?'
    params.push(accountId)
  }
  
  if (service) {
    query += ' AND service_name = ?'
    params.push(service)
  }
  
  query += ' ORDER BY scan_start DESC LIMIT 100'
  
  const scans = db.prepare(query).all(...params)
  return c.json(scans)
})

// Dashboard overview
app.get('/api/dashboard', (c) => {
  const stats = {
    total_accounts: db.prepare('SELECT COUNT(*) as count FROM accounts').get(),
    total_iam_users: db.prepare('SELECT COUNT(*) as count FROM iam_users').get(),
    total_iam_roles: db.prepare('SELECT COUNT(*) as count FROM iam_roles').get(),
    total_security_findings: db.prepare('SELECT COUNT(*) as count FROM security_hub_findings').get(),
    recent_scans: db.prepare('SELECT * FROM scan_history ORDER BY scan_start DESC LIMIT 10').all()
  }
  
  return c.json(stats)
})

const port = parseInt(process.env.PORT || '3000')

console.log(`🚀 Server starting on port ${port}`)

export default {
  port,
  fetch: app.fetch,
}
