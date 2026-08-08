export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"

export class ApiError extends Error {
  constructor(public status: number, public message: string, public data?: any) {
    super(message)
    this.name = "ApiError"
  }
}

export async function fetchApi<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`
  
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  }

  try {
    const response = await fetch(url, { ...options, headers })
    
    let data
    const text = await response.text()
    try {
      data = text ? JSON.parse(text) : {}
    } catch (e) {
      throw new ApiError(response.status, "Invalid JSON response")
    }

    if (!response.ok) {
      throw new ApiError(response.status, data.detail || "API request failed", data)
    }

    return data as T
  } catch (error) {
    if (error instanceof ApiError) {
      throw error
    }
    throw new ApiError(0, "Network error or request timeout")
  }
}
