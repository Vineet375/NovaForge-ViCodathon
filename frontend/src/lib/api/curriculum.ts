import { fetchApi } from "./api"

export interface CurriculumDay {
  day: number
  title: string
  type: string
  tools: string[]
  objectives: string[]
}

export interface CurriculumModule {
  n: number
  title: string
  days: number[]
}

export interface Curriculum {
  cohort: string
  modules: CurriculumModule[]
  days: CurriculumDay[]
}

export const CurriculumAPI = {
  getCurriculum: () => fetchApi<Curriculum>("/curriculum"),
  getDay: (dayNum: number) => fetchApi<CurriculumDay>(`/curriculum/day/${dayNum}`),
}
