import { fetchApi } from "./api"

export interface Candidate {
  candidate_id: string
  name: string
  experience_level: string
  preferred_role: string
  tech_stack: string[]
  learning_goals: string[]
}

export const CandidateAPI = {
  getAll: () => fetchApi<Candidate[]>("/candidates"),
  getById: (id: string) => fetchApi<Candidate>(`/candidates/${id}`),
}
