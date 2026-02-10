import { useQuery } from '@tanstack/react-query'
import { useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000'

interface Account {
  id: number
  account_id: string
  account_name: string
  account_alias?: string
}

interface DashboardStats {
  total_accounts: { count: number }
  total_iam_users: { count: number }
  total_iam_roles: { count: number }
  total_security_findings: { count: number }
  recent_scans: any[]
}

function App() {
  const [selectedAccount, setSelectedAccount] = useState<string | null>(null)

  // Fetch dashboard stats
  const { data: dashboard } = useQuery<DashboardStats>({
    queryKey: ['dashboard'],
    queryFn: async () => {
      const res = await fetch(`${API_URL}/api/dashboard`)
      return res.json()
    },
  })

  // Fetch accounts
  const { data: accounts } = useQuery<Account[]>({
    queryKey: ['accounts'],
    queryFn: async () => {
      const res = await fetch(`${API_URL}/api/accounts`)
      return res.json()
    },
  })

  // Fetch IAM users for selected account
  const { data: iamUsers } = useQuery({
    queryKey: ['iam-users', selectedAccount],
    queryFn: async () => {
      const res = await fetch(`${API_URL}/api/accounts/${selectedAccount}/iam/users`)
      return res.json()
    },
    enabled: !!selectedAccount,
  })

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">
            AWS Multi-Account Dashboard
          </h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {/* Dashboard Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500">Total Accounts</h3>
            <p className="mt-2 text-3xl font-semibold text-gray-900">
              {dashboard?.total_accounts.count || 0}
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500">IAM Users</h3>
            <p className="mt-2 text-3xl font-semibold text-gray-900">
              {dashboard?.total_iam_users.count || 0}
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500">IAM Roles</h3>
            <p className="mt-2 text-3xl font-semibold text-gray-900">
              {dashboard?.total_iam_roles.count || 0}
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500">Security Findings</h3>
            <p className="mt-2 text-3xl font-semibold text-gray-900">
              {dashboard?.total_security_findings.count || 0}
            </p>
          </div>
        </div>

        {/* Accounts List */}
        <div className="bg-white rounded-lg shadow mb-8">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">AWS Accounts</h2>
          </div>
          <div className="p-6">
            {accounts && accounts.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {accounts.map((account) => (
                  <button
                    key={account.account_id}
                    onClick={() => setSelectedAccount(account.account_id)}
                    className={`p-4 border rounded-lg text-left hover:border-blue-500 transition ${
                      selectedAccount === account.account_id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200'
                    }`}
                  >
                    <h3 className="font-semibold text-gray-900">{account.account_name}</h3>
                    <p className="text-sm text-gray-500">{account.account_id}</p>
                    {account.account_alias && (
                      <p className="text-xs text-gray-400 mt-1">{account.account_alias}</p>
                    )}
                  </button>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">
                No accounts found. Run the scraper to collect data.
              </p>
            )}
          </div>
        </div>

        {/* IAM Users (when account selected) */}
        {selectedAccount && (
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900">
                IAM Users - {accounts?.find(a => a.account_id === selectedAccount)?.account_name}
              </h2>
            </div>
            <div className="overflow-x-auto">
              {iamUsers && iamUsers.length > 0 ? (
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        User Name
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        ARN
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        MFA
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Created
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {iamUsers.map((user: any) => (
                      <tr key={user.id}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {user.user_name}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {user.arn}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          <span
                            className={`px-2 py-1 rounded-full text-xs ${
                              user.mfa_enabled
                                ? 'bg-green-100 text-green-800'
                                : 'bg-red-100 text-red-800'
                            }`}
                          >
                            {user.mfa_enabled ? 'Enabled' : 'Disabled'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {user.create_date ? new Date(user.create_date).toLocaleDateString() : 'N/A'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <div className="p-6 text-center text-gray-500">
                  No IAM users found for this account.
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
