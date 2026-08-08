"use client"
import { useState, useEffect, useCallback } from "react"
import { CandidateAPI, Candidate, ApiError } from "@/lib/api"

export function useCandidates() {
  const [candidates, setCandidates] = useState<Candidate[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchCandidates = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await CandidateAPI.getAll()
      setCandidates(data)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError("Failed to fetch candidates")
      }
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchCandidates()
  }, [fetchCandidates])

  return { candidates, loading, error, refetch: fetchCandidates }
}

export function useCandidate(id: string | null) {
  const [candidate, setCandidate] = useState<Candidate | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchCandidate = useCallback(async () => {
    if (!id) return
    try {
      setLoading(true)
      setError(null)
      const data = await CandidateAPI.getById(id)
      setCandidate(data)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError("Failed to fetch candidate")
      }
    } finally {
      setLoading(false)
    }
  }, [id])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchCandidate()
  }, [fetchCandidate])

  return { candidate, loading, error, refetch: fetchCandidate }
}

