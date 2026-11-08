export interface Job {
  source: string
  external_id: string
  title: string
  company: string
  location: string | null
  url: string
  updated_at: string | null
  company_key: string | null
  categories: string[]
  first_seen_at: string | null
  last_seen_at: string | null
  closed_at: string | null
}

export interface SyncResult {
  fetched: number
  new_jobs: number
  open_jobs_in_db: number
}
