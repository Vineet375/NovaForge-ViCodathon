"use client"
import { useState, useEffect, useCallback } from "react"
import { CurriculumAPI, Curriculum, ApiError } from "@/lib/api"

export function useCurriculum() {
  const [curriculum, setCurriculum] = useState<Curriculum | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchCurriculum = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await CurriculumAPI.getCurriculum()
      setCurriculum(data)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError("Failed to fetch curriculum")
      }
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchCurriculum()
  }, [fetchCurriculum])

  return { curriculum, loading, error, refetch: fetchCurriculum }
}

