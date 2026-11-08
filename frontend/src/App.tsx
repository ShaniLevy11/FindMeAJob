import { useEffect, useState } from 'react'
import { fetchJobs, syncJobs } from './api'
import CoffeeCup from './components/CoffeeCup'
import JobTable from './components/JobTable'
import type { Job } from './types'

const PAGE_SIZE = 50

function sortNewestFirst(jobs: Job[]): Job[] {
  return [...jobs].sort((a, b) => {
    const dateA = a.updated_at ? Date.parse(a.updated_at) : 0
    const dateB = b.updated_at ? Date.parse(b.updated_at) : 0
    return dateB - dateA
  })
}

export default function App() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE)
  const [syncing, setSyncing] = useState(false)
  const [syncMessage, setSyncMessage] = useState<string | null>(null)

  useEffect(() => {
    const controller = new AbortController()

    fetchJobs(controller.signal)
      .then((data) => {
        setJobs(sortNewestFirst(data))
        setLoading(false)
      })
      .catch((err: Error) => {
        if (err.name === 'AbortError') {
          return
        }
        setError(err.message)
        setLoading(false)
      })

    return () => controller.abort()
  }, [])

  async function handleSync() {
    setSyncing(true)
    setSyncMessage(null)

    try {
      const result = await syncJobs()
      const data = await fetchJobs()
      setJobs(sortNewestFirst(data))
      setError(null)
      setSyncMessage(`Sync finished: ${result.new_jobs} new jobs, ${result.open_jobs_in_db} open in total`)
    } catch (err) {
      setSyncMessage(`Sync failed: ${(err as Error).message}`)
    } finally {
      setSyncing(false)
    }
  }

  const visibleJobs = jobs.slice(0, visibleCount)

  return (
    <div className="app">
      <header className="app-header">
        <div>
          <h1>FindMeAJob</h1>
          <p>Tech jobs in Israel</p>
        </div>
        <CoffeeCup />
      </header>

      <main>
        <div className="toolbar">
          <p className="status">
            {loading && 'Loading jobs...'}
            {!loading && !error && `Showing ${visibleJobs.length} of ${jobs.length} jobs`}
            {error && <span className="error">Could not load jobs: {error}</span>}
          </p>

          <div className="sync">
            {syncing && <span className="status">Syncing, this can take up to 30 seconds...</span>}
            {!syncing && syncMessage && <span className="status">{syncMessage}</span>}
            <button className="sync-button" onClick={handleSync} disabled={syncing}>
              {syncing ? 'Syncing...' : 'Sync jobs'}
            </button>
          </div>
        </div>

        {!loading && !error && (
          <>
            <JobTable jobs={visibleJobs} />

            {visibleCount < jobs.length && (
              <button className="more" onClick={() => setVisibleCount(visibleCount + PAGE_SIZE)}>
                Show more
              </button>
            )}
          </>
        )}
      </main>
    </div>
  )
}
