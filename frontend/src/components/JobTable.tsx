import type { Job } from '../types'

interface JobTableProps {
  jobs: Job[]
}

function formatDate(value: string | null): string {
  if (!value) {
    return ''
  }
  return new Date(value).toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

export default function JobTable({ jobs }: JobTableProps) {
  return (
    <div className="table-wrapper">
      <table className="job-table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Company</th>
            <th>Location</th>
            <th>Source</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map((job) => (
            <tr key={`${job.source}-${job.external_id}`}>
              <td>
                <a className="job-title" href={job.url} target="_blank" rel="noreferrer">
                  {job.title}
                </a>
              </td>
              <td>{job.company}</td>
              <td>{job.location}</td>
              <td>
                <span className="source">{job.source}</span>
              </td>
              <td className="nowrap">{formatDate(job.updated_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
