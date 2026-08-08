import { fetchApi } from "./api"

export interface StartInterviewRequest {
  candidate_id: string
}

export interface StartInterviewResponse {
  session_id: string
  candidate_id: string
  planned_difficulty: string
  current_day: number
}

export interface NextQuestionResponse {
  question_text: string
}

export interface AnswerRequest {
  answer_text: string
}

export interface AnswerResponse {
  feedback: string
  follow_up_question: string | null
}

export interface InterviewSessionState {
  session_id: string
  status: string
  current_question_number: number
  questions_asked: any[]
}

export const InterviewAPI = {
  start: (data: StartInterviewRequest) => 
    fetchApi<StartInterviewResponse>("/interview/start", {
      method: "POST",
      body: JSON.stringify(data)
    }),
    
  getNextQuestion: (sessionId: string) =>
    fetchApi<NextQuestionResponse>(`/interview/${sessionId}/next`, {
      method: "POST"
    }),
    
  answerQuestion: (sessionId: string, data: AnswerRequest) =>
    fetchApi<AnswerResponse>(`/interview/${sessionId}/answer`, {
      method: "POST",
      body: JSON.stringify(data)
    }),
    
  getSession: (sessionId: string) =>
    fetchApi<InterviewSessionState>(`/interview/${sessionId}`),
    
  getFeedback: (sessionId: string) =>
    fetchApi<any>(`/interview/${sessionId}/feedback`)
}
