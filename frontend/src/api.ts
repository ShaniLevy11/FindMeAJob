import type { Job } from './types'

export async function fetchJobs(signal: AbortSignal): Promise<Job[]> {
  const response = await fetch('/api/jobs', { signal })
  if (!response.ok) {
    throw new Error(`Server returned ${response.status}`)
  }
  return response.json()
}
