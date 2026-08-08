import { fetchApi } from "./api"

export interface CandidateMember {
  id: string
  name: string
  jobRole: string
  yearsExperience: number
  education: string
  status: string
}

export interface CandidateMission {
  day: number
  title: string
  passed?: boolean
  attempts?: number
  skipped?: boolean
}

export interface CandidateSignals {
  commitDays: number
  missionsCompleted: number
  missionsFirstTry: number
}

export interface Candidate {
  member: CandidateMember
  missions: CandidateMission[]
  signals: CandidateSignals
}

export const CandidateAPI = {
  getAll: () => fetchApi<Candidate[]>("/candidates"),
  getById: (id: string) => fetchApi<Candidate>(`/candidates/${id}`),
}
