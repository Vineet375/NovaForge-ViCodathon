import { fetchApi } from "./api"

export interface CurriculumDay {
  day_number: number
  title: string
  focus_areas: string[]
  key_concepts: string[]
}

export interface Curriculum {
  days: CurriculumDay[]
}

export const CurriculumAPI = {
  getCurriculum: () => fetchApi<Curriculum>("/curriculum"),
  getDay: (dayNum: number) => fetchApi<CurriculumDay>(`/curriculum/day/${dayNum}`),
}
