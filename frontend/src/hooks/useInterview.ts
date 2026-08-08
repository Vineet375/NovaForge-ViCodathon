"use client"
import { useState, useCallback, useEffect, useRef } from "react"
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
  const [report, setReport] = useState<FeedbackResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [retryAfter, setRetryAfter] = useState<number | null>(null)
  
  const router = useRouter()
  
  // Guard against duplicate concurrent requests
  const requestInProgress = useRef(false)
  const isMounted = useRef(true)

  useEffect(() => {
    isMounted.current = true
    return () => {
      isMounted.current = false
    }
  }, [])

  const handleApiError = useCallback((err: unknown, defaultMessage: string) => {
    if (err instanceof ApiError) {
      if (err.status === 409) {
        // Safe to ignore duplicate request errors
        return
      }
      if (err.status === 429 && err.headers) {
        const retryHeader = err.headers.get("Retry-After")
        if (retryHeader) {
          const parsed = parseInt(retryHeader, 10)
          if (!isNaN(parsed)) {
            setRetryAfter(parsed)
            return // Prevent triggering hard error UI
          }
        }
      }
      if (isMounted.current) setError(err.message)
      toast.error(err.message)
    } else {
      if (isMounted.current) setError(defaultMessage)
      toast.error(defaultMessage)
    }
  }, [])

  const fetchSession = useCallback(async () => {
    if (!sessionId) return
    try {
      setLoading(true)
      setError(null)
      const res = await InterviewAPI.getSession(sessionId)
      if (!isMounted.current) return
      setSession(res)
      
      if (res.status === "completed") {
        try {
          const fb = await InterviewAPI.getFeedback(sessionId)
          if (isMounted.current) setReport(fb)
        } catch {
          // ignore feedback error temporarily
        }
      }
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.message.includes("404") || err.message.toLowerCase().includes("not found")) {
            localStorage.removeItem("active_session_id")
            if (isMounted.current) router.push("/")
            toast.error("Session expired or not found")
            return
        }
      }
      handleApiError(err, "Failed to load interview session")
    } finally {
      if (isMounted.current) setLoading(false)
    }
  }, [sessionId, router, handleApiError])

  useEffect(() => {
    fetchSession()
  }, [fetchSession])

  const nextQuestion = useCallback(async () => {
    if (!sessionId || requestInProgress.current) return
    try {
      requestInProgress.current = true
      setActionLoading(true)
      setError(null)
      setRetryAfter(null)
      await InterviewAPI.getNextQuestion(sessionId)
      await fetchSession()
    } catch (err) {
      if (!isMounted.current) return
      handleApiError(err, "Failed to get next question")
    } finally {
      requestInProgress.current = false
      if (isMounted.current) setActionLoading(false)
    }
  }, [sessionId, fetchSession, handleApiError])

  const answerQuestion = useCallback(async (answer: string) => {
    if (!sessionId || requestInProgress.current) return
    try {
      requestInProgress.current = true
      setActionLoading(true)
      setError(null)
      setRetryAfter(null)
      await InterviewAPI.answerQuestion(sessionId, { answer_text: answer })
      await fetchSession()
    } catch (err) {
      if (!isMounted.current) return
      handleApiError(err, "Failed to submit answer")
    } finally {
      requestInProgress.current = false
      if (isMounted.current) setActionLoading(false)
    }
  }, [sessionId, fetchSession, handleApiError])

  return {
    session,
    report,
    loading,
    actionLoading,
    error,
    retryAfter,
    setRetryAfter,
    fetchSession,
    nextQuestion,
    answerQuestion
  }
}
