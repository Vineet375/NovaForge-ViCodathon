"use client"
import { useState, useCallback } from "react"
import { InterviewAPI, StartInterviewRequest, AnswerRequest, InterviewSessionState, ApiError } from "@/lib/api"
import { useRouter } from "next/navigation"

export function useInterview() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const startInterview = useCallback(async (candidateId: string) => {
    try {
      setLoading(true)
      setError(null)
      const res = await InterviewAPI.start({ candidate_id: candidateId })
      router.push(`/interview/${res.session_id}`)
      return res
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError("Failed to start interview")
      }
      return null
    } finally {
      setLoading(false)
    }
  }, [router])

  return { startInterview, loading, error }
}

export function useInterviewSession(sessionId: string) {
  const [session, setSession] = useState<InterviewSessionState | null>(null)
  const [currentQuestion, setCurrentQuestion] = useState<string | null>(null)
  const [feedback, setFeedback] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchSession = useCallback(async () => {
    if (!sessionId) return
    try {
      setLoading(true)
      setError(null)
      const res = await InterviewAPI.getSession(sessionId)
      setSession(res)
      
      if (res.status === "completed") {
        try {
          const fb = await InterviewAPI.getFeedback(sessionId)
          setFeedback(fb)
        } catch (e) {
          // ignore feedback error temporarily
        }
      }
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError("Failed to fetch session")
      }
    } finally {
      setLoading(false)
    }
  }, [sessionId])

  const nextQuestion = useCallback(async () => {
    if (!sessionId) return
    try {
      setActionLoading(true)
      setError(null)
      const res = await InterviewAPI.getNextQuestion(sessionId)
      setCurrentQuestion(res.question_text)
      await fetchSession() // update session state
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError("Failed to get next question")
      }
    } finally {
      setActionLoading(false)
    }
  }, [sessionId, fetchSession])

  const answerQuestion = useCallback(async (answer: string) => {
    if (!sessionId) return
    try {
      setActionLoading(true)
      setError(null)
      const res = await InterviewAPI.answerQuestion(sessionId, { answer_text: answer })
      await fetchSession() // update session state
      
      // If there's a follow-up question, we set it as the current question
      if (res.follow_up_question) {
        setCurrentQuestion(res.follow_up_question)
      } else {
        setCurrentQuestion(null)
      }
      return res
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError("Failed to submit answer")
      }
      return null
    } finally {
      setActionLoading(false)
    }
  }, [sessionId, fetchSession])

  return {
    session,
    currentQuestion,
    feedback,
    loading,
    actionLoading,
    error,
    fetchSession,
    nextQuestion,
    answerQuestion
  }
}

