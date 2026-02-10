import express from 'express'
import cors from 'cors'
import sqlite3 from 'sqlite3'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const app = express()

// Middleware
app.use(cors())
app.use(express.json())
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path}`)
  next()
})

// Database connection
const dbPath = process.env.DATABASE_PATH || join(__dirname, '../../database/awsui.db')
const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error opening database:', err)
  } else {
    console.log('✅ Connected to database:', dbPath)
  }
})

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() })
})

// Get all accounts
app.get('/api/accounts', (req, res) => {
  db.all('SELECT * FROM accounts ORDER BY account_name', [], (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message })
      return
    }
    res.json(rows)
  })
})

// Get specific account
app.get('/api/accounts/:id', (req, res) => {
  const accountId = req.params.id
  db.get('SELECT * FROM accounts WHERE account_id = ?', [accountId], (err, row) => {
    if (err) {
      res.status(500).json({ error: err.message })
      return
    }
    if (!row) {
      res.status(404).json({ error: 'Account not found' })
      return
    }
    res.json(row)
  })
})

// Get IAM users for an account
app.get('/api/accounts/:id/iam/users', (req, res) => {
  const accountId = req.params.id
  db.all('SELECT * FROM iam_users WHERE account_id = ? ORDER BY user_name', [accountId], (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message })
      return
    }
    res.json(rows)
  })
})

// Get IAM roles for an account
app.get('/api/accounts/:id/iam/roles', (req, res) => {
  const accountId = req.params.id
  db.all('SELECT * FROM iam_roles WHERE account_id = ? ORDER BY role_name', [accountId], (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message })
      return
    }
    res.json(rows)
  })
})

// Get IAM policies for an account
app.get('/api/accounts/:id/iam/policies', (req, res) => {
  const accountId = req.params.id
  db.all('SELECT * FROM iam_policies WHERE account_id = ? ORDER BY policy_name', [accountId], (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message })
      return
    }
    res.json(rows)
  })
})

// Get SecurityHub findings for an account
app.get('/api/accounts/:id/security-hub/findings', (req, res) => {
  const accountId = req.params.id
  const severity = req.query.severity
  
  let query = 'SELECT * FROM security_hub_findings WHERE account_id = ?'
  const params = [accountId]
  
  if (severity) {
    query += ' AND severity = ?'
    params.push(severity)
  }
  
  query += ' ORDER BY updated_at_aws DESC'
  
  db.all(query, params, (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message })
      return
    }
    res.json(rows)
  })
})

// Get scan history
app.get('/api/scans/history', (req, res) => {
  const accountId = req.query.account_id
  const service = req.query.service
  
  let query = 'SELECT * FROM scan_history WHERE 1=1'
  const params = []
  
  if (accountId) {
    query += ' AND account_id = ?'
    params.push(accountId)
  }
  
  if (service) {
    query += ' AND service_name = ?'
    params.push(service)
  }
  
  query += ' ORDER BY scan_start DESC LIMIT 100'
  
  db.all(query, params, (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message })
      return
    }
    res.json(rows)
  })
})

// Dashboard overview
app.get('/api/dashboard', (req, res) => {
  const stats = {}
  
  // Use promises to get all stats
  const promises = [
    new Promise((resolve) => {
      db.get('SELECT COUNT(*) as count FROM accounts', [], (err, row) => {
        stats.total_accounts = row || { count: 0 }
        resolve()
      })
    }),
    new Promise((resolve) => {
      db.get('SELECT COUNT(*) as count FROM iam_users', [], (err, row) => {
        stats.total_iam_users = row || { count: 0 }
        resolve()
      })
    }),
    new Promise((resolve) => {
      db.get('SELECT COUNT(*) as count FROM iam_roles', [], (err, row) => {
        stats.total_iam_roles = row || { count: 0 }
        resolve()
      })
    }),
    new Promise((resolve) => {
      db.get('SELECT COUNT(*) as count FROM security_hub_findings', [], (err, row) => {
        stats.total_security_findings = row || { count: 0 }
        resolve()
      })
    }),
    new Promise((resolve) => {
      db.all('SELECT * FROM scan_history ORDER BY scan_start DESC LIMIT 10', [], (err, rows) => {
        stats.recent_scans = rows || []
        resolve()
      })
    })
  ]
  
  Promise.all(promises).then(() => {
    res.json(stats)
  })
})

const port = parseInt(process.env.PORT || '3000')

app.listen(port, () => {
  console.log(`🚀 Server running on port ${port}`)
})
