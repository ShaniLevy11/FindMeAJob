import { useEffect, useState } from 'react'
import { fetchJobs } from './api'
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
        {loading && <p className="status">Loading jobs, this can take up to 30 seconds...</p>}
        {error && <p className="status error">Could not load jobs: {error}</p>}

        {!loading && !error && (
          <>
            <p className="status">
              Showing {visibleJobs.length} of {jobs.length} jobs
            </p>

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
