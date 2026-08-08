"use client"
import { useState, useCallback, useEffect } from "react"
import { InterviewAPI, InterviewSessionState, ApiError, FeedbackResponse } from "@/lib/api"
import { useRouter } from "next/navigation"
import { toast } from "sonner"

export function useInterview() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const startInterview = useCallback(async (candidateId: string) => {
    try {
      setLoading(true)
      setError(null)
      const res = await InterviewAPI.start({ candidate_id: candidateId })
      localStorage.setItem("active_session_id", res.session_id)
      toast.success("Interview session started")
      router.push(`/interview/${res.session_id}`)
      return res
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
        toast.error(`Failed to start: ${err.message}`)
      } else {
        setError("Failed to start interview")
        toast.error("Failed to start interview")
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
  const [feedback, setFeedback] = useState<FeedbackResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

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
        } catch {
          // ignore feedback error temporarily
        }
      }
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.message.includes("404") || err.message.toLowerCase().includes("not found")) {
            localStorage.removeItem("active_session_id")
            router.push("/")
            toast.error("Session expired or not found")
            return
        }
        setError(err.message)
      } else {
        setError("Failed to fetch session")
      }
      toast.error("Failed to load interview session")
    } finally {
      setLoading(false)
    }
  }, [sessionId, router])

  useEffect(() => {
    fetchSession()
  }, [fetchSession])

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
        toast.error(`Failed to load question: ${err.message}`)
      } else {
        setError("Failed to get next question")
        toast.error("Failed to load question")
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
      
      toast.success("Answer submitted successfully")
      
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
        toast.error(`Failed to submit answer: ${err.message}`)
      } else {
        setError("Failed to submit answer")
        toast.error("Failed to submit answer")
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
