import type { Job, SyncResult } from './types'

export async function fetchJobs(signal?: AbortSignal): Promise<Job[]> {
  const response = await fetch('/api/jobs', { signal })
  if (!response.ok) {
    throw new Error(`Server returned ${response.status}`)
  }
  return response.json()
}

export async function syncJobs(): Promise<SyncResult> {
  const response = await fetch('/api/jobs/sync', { method: 'POST' })
  if (response.status === 409) {
    throw new Error('A sync is already running')
  }
  if (!response.ok) {
    throw new Error(`Server returned ${response.status}`)
  }
  return response.json()
}
