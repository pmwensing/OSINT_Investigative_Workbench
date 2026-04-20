import React, { useEffect, useMemo, useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8088'

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '')
  const [email, setEmail] = useState('admin@example.com')
  const [password, setPassword] = useState('ChangeMe123!')
  const [fullName, setFullName] = useState('Admin')
  const [investigations, setInvestigations] = useState([])
  const [selectedInvestigation, setSelectedInvestigation] = useState(null)
  const [targets, setTargets] = useState([])
  const [jobs, setJobs] = useState([])
  const [graph, setGraph] = useState({ nodes: [], edges: [] })
  const [timeline, setTimeline] = useState({ events: [], contradictions: [] })
  const [artifacts, setArtifacts] = useState([])
  const authHeaders = useMemo(() => ({ 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }), [token])

  async function register() {
    const res = await fetch(`${API_BASE}/api/v1/auth/register`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ email, password, full_name: fullName })
    })
    const data = await res.json()
    if (data.access_token) {
      localStorage.setItem('token', data.access_token)
      setToken(data.access_token)
    } else {
      alert(JSON.stringify(data))
    }
  }

  async function login() {
    const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ email, password })
    })
    const data = await res.json()
    if (data.access_token) {
      localStorage.setItem('token', data.access_token)
      setToken(data.access_token)
    } else {
      alert(JSON.stringify(data))
    }
  }

  async function loadInvestigations() {
    const res = await fetch(`${API_BASE}/api/v1/investigations`, { headers: authHeaders })
    if (res.ok) {
      const data = await res.json()
      setInvestigations(data)
      if (!selectedInvestigation && data.length) setSelectedInvestigation(data[0])
    }
  }

  async function createInvestigation() {
    const name = prompt('Investigation name')
    if (!name) return
    const res = await fetch(`${API_BASE}/api/v1/investigations`, {
      method: 'POST',
      headers: authHeaders,
      body: JSON.stringify({ name, description: 'Created from UI' })
    })
    if (res.ok) loadInvestigations()
  }

  async function loadCaseData(inv) {
    setSelectedInvestigation(inv)
    const [tRes, jRes, gRes, tiRes, aRes] = await Promise.all([
      fetch(`${API_BASE}/api/v1/investigations/${inv.id}/targets`, { headers: authHeaders }),
      fetch(`${API_BASE}/api/v1/investigations/${inv.id}/jobs`, { headers: authHeaders }),
      fetch(`${API_BASE}/api/v1/investigations/${inv.id}/graph`, { headers: authHeaders }),
      fetch(`${API_BASE}/api/v1/investigations/${inv.id}/timeline`, { headers: authHeaders }),
      fetch(`${API_BASE}/api/v1/investigations/${inv.id}/artifacts`, { headers: authHeaders }),
    ])
    if (tRes.ok) setTargets(await tRes.json())
    if (jRes.ok) setJobs(await jRes.json())
    if (gRes.ok) setGraph(await gRes.json())
    if (tiRes.ok) setTimeline(await tiRes.json())
    if (aRes.ok) setArtifacts(await aRes.json())
  }

  async function addTarget() {
    if (!selectedInvestigation) return
    const target_type = prompt('Target type (email/ip/username/domain)')
    const value = prompt('Target value')
    if (!target_type || !value) return
    const res = await fetch(`${API_BASE}/api/v1/investigations/${selectedInvestigation.id}/targets`, {
      method: 'POST',
      headers: authHeaders,
      body: JSON.stringify({ target_type, value, display_name: value })
    })
    if (res.ok) loadCaseData(selectedInvestigation)
  }

  async function runConnector() {
    if (!selectedInvestigation || !targets.length) return
    const targetId = prompt(`Target ID:\n${targets.map(t => `${t.id} - ${t.value}`).join('\n')}`)
    const connectorList = prompt('Connectors comma-separated (manual_import,ipinfo,shodan)', 'manual_import')
    if (!targetId || !connectorList) return
    const res = await fetch(`${API_BASE}/api/v1/investigations/${selectedInvestigation.id}/jobs`, {
      method: 'POST',
      headers: authHeaders,
      body: JSON.stringify({ target_id: targetId, connectors: connectorList.split(',').map(v => v.trim()).filter(Boolean) })
    })
    if (res.ok) {
      await loadCaseData(selectedInvestigation)
      alert('Jobs queued. Refresh case data in a few seconds.')
    } else {
      alert(await res.text())
    }
  }

  useEffect(() => {
    if (token) loadInvestigations()
  }, [token])

  return (
    <div style={{fontFamily: 'Arial, sans-serif', padding: 20}}>
      <h1>OSINT Workbench v1</h1>
      {!token ? (
        <div style={{display:'grid', gap:8, maxWidth:360}}>
          <input value={fullName} onChange={e => setFullName(e.target.value)} placeholder="Full name" />
          <input value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" />
          <input value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" type="password" />
          <div style={{display:'flex', gap:8}}>
            <button onClick={register}>Register</button>
            <button onClick={login}>Login</button>
          </div>
        </div>
      ) : (
        <div style={{display:'grid', gridTemplateColumns:'280px 1fr', gap:20}}>
          <div>
            <button onClick={createInvestigation}>New Investigation</button>
            <button onClick={() => loadInvestigations()} style={{marginLeft:8}}>Refresh</button>
            <h3>Investigations</h3>
            <ul>
              {investigations.map(inv => (
                <li key={inv.id}>
                  <button onClick={() => loadCaseData(inv)}>{inv.name}</button>
                </li>
              ))}
            </ul>
          </div>
          <div>
            {selectedInvestigation ? (
              <>
                <h2>{selectedInvestigation.name}</h2>
                <div style={{display:'flex', gap:8, marginBottom:16}}>
                  <button onClick={addTarget}>Add Target</button>
                  <button onClick={runConnector}>Run Connector</button>
                  <button onClick={() => loadCaseData(selectedInvestigation)}>Reload Case</button>
                </div>

                <h3>Targets</h3>
                <pre>{JSON.stringify(targets, null, 2)}</pre>

                <h3>Jobs</h3>
                <pre>{JSON.stringify(jobs, null, 2)}</pre>

                <h3>Graph</h3>
                <pre>{JSON.stringify(graph, null, 2)}</pre>

                <h3>Timeline</h3>
                <pre>{JSON.stringify(timeline, null, 2)}</pre>

                <h3>Artifacts</h3>
                <pre>{JSON.stringify(artifacts, null, 2)}</pre>
              </>
            ) : (
              <p>Select or create an investigation.</p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
