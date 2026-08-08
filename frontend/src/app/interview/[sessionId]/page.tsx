"use client"

import * as React from "react"
import { useParams, useRouter } from "next/navigation"
import { useInterviewSession } from "@/hooks/useInterview"
import { DashboardLayout } from "@/components/layout/dashboard-layout"
import { PageContainer, Section } from "@/components/layout/layout-foundation"
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Loader2, ArrowRight, CheckCircle2, MessageSquare, Play, AlertCircle, Clock, Brain } from "lucide-react"
import { TypingIndicator } from "@/components/ui/typing-indicator"
import { InterviewReport } from "@/components/interview/interview-report"
import { AskedQuestion } from "@/lib/api"

export default function InterviewPage() {
  const params = useParams()
  const router = useRouter()
  const sessionId = params.sessionId as string
  
  const {
    session,
    currentQuestion,
    feedback,
    loading,
    actionLoading,
    error,
    retryAfter,
    nextQuestion,
    answerQuestion
  } = useInterviewSession(sessionId)

  const [answer, setAnswer] = React.useState("")
  const [currentFeedback, setCurrentFeedback] = React.useState<string | null>(null)
  const [countdown, setCountdown] = React.useState<number | null>(null)
  const textareaRef = React.useRef<HTMLTextAreaElement>(null)

  React.useEffect(() => {
    if (retryAfter) {
      setCountdown(retryAfter)
    }
  }, [retryAfter])

  React.useEffect(() => {
    if (countdown !== null && countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000)
      return () => clearTimeout(timer)
    }
  }, [countdown])

  // Auto-focus textarea when a new question is loaded and no feedback is shown
  React.useEffect(() => {
    if (currentQuestion && !currentFeedback && textareaRef.current) {
      textareaRef.current.focus()
    }
  }, [currentQuestion, currentFeedback])

  // Auto-fetch first question if none exists and session is initializing
  React.useEffect(() => {
    if (session?.status === "initializing" && !currentQuestion && session.questions_asked.length === 0) {
      nextQuestion()
    }
  }, [session?.status, session?.questions_asked.length, currentQuestion, nextQuestion])

  const handleSubmit = async () => {
    if (!answer.trim() || actionLoading) return
    const res = await answerQuestion(answer)
    if (res) {
      setCurrentFeedback(res.feedback)
      setAnswer("")
    }
  }

  const handleNext = async () => {
    setCurrentFeedback(null)
    await nextQuestion()
  }

  if (loading && !session) {
    return (
      <DashboardLayout>
        <PageContainer className="py-6 space-y-6">
          <Section className="py-0 md:py-0 lg:py-0">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
              <div className="space-y-2">
                <div className="h-8 w-64 bg-muted animate-pulse rounded-md"></div>
                <div className="h-4 w-48 bg-muted animate-pulse rounded-md"></div>
              </div>
              <div className="w-full md:w-64 space-y-2">
                <div className="h-4 w-full bg-muted animate-pulse rounded-md"></div>
                <div className="h-2 w-full bg-muted animate-pulse rounded-md"></div>
              </div>
            </div>
          </Section>
          <div className="grid gap-6 lg:grid-cols-3">
            <div className="lg:col-span-2 space-y-6">
              <Card className="shadow-premium overflow-hidden">
                <div className="h-1.5 w-full bg-muted animate-pulse" />
                <CardHeader>
                  <div className="h-6 w-3/4 bg-muted animate-pulse rounded-md"></div>
                  <div className="h-6 w-1/2 bg-muted animate-pulse rounded-md mt-2"></div>
                </CardHeader>
                <CardContent>
                  <div className="w-full min-h-[200px] bg-muted animate-pulse rounded-xl"></div>
                </CardContent>
              </Card>
            </div>
            <div className="space-y-6">
              <Card className="shadow-premium">
                <CardHeader>
                  <div className="h-5 w-40 bg-muted animate-pulse rounded-md"></div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="h-4 w-full bg-muted animate-pulse rounded-md"></div>
                  <div className="h-4 w-5/6 bg-muted animate-pulse rounded-md"></div>
                  <div className="h-4 w-4/6 bg-muted animate-pulse rounded-md"></div>
                </CardContent>
              </Card>
            </div>
          </div>
        </PageContainer>
      </DashboardLayout>
    )
  }

  if (error || !session) {
    return (
      <DashboardLayout>
        <PageContainer className="py-8">
          <Card className="border-red-500/20 bg-red-500/5 shadow-premium">
            <CardContent className="p-8 flex flex-col items-center justify-center text-center gap-4">
              <AlertCircle className="h-10 w-10 text-red-500" />
              <h2 className="text-xl font-bold">Failed to load session</h2>
              <p className="text-muted-foreground">{error || "The session could not be found."}</p>
              <Button onClick={() => router.push("/")} variant="outline" className="mt-4">
                Return to Dashboard
              </Button>
            </CardContent>
          </Card>
        </PageContainer>
      </DashboardLayout>
    )
  }

  const progress = Math.min(Math.round(((session.current_question_number - 1) / 8) * 100), 100)
  const isCompleted = session.status === "completed"

  return (
    <DashboardLayout>
      <PageContainer className="py-6 space-y-6">
        {/* Header / Overview */}
        <Section className="py-0 md:py-0 lg:py-0">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold tracking-tight mb-2">Technical Interview</h1>
              <div className="flex items-center gap-3 text-sm text-muted-foreground">
                <Badge variant={isCompleted ? "secondary" : "default"} className="px-2 py-0.5">
                  {isCompleted ? "Completed" : "In Progress"}
                </Badge>
                <span>•</span>
                <span>Question {session.current_question_number} of 8</span>
              </div>
            </div>
            <div className="w-full md:w-64 space-y-2">
              <div className="flex justify-between text-xs font-medium">
                <span>Progress</span>
                <span>{progress}%</span>
              </div>
              <Progress value={progress} className="h-2" />
            </div>
          </div>
        </Section>

        {isCompleted ? (
          /* Final Report State */
          <Section className="py-0 md:py-0 lg:py-0">
            <InterviewReport 
              feedback={feedback || "Generating comprehensive feedback..."} 
              onClose={() => router.push("/")} 
            />
          </Section>
        ) : (
          /* Interview Flow State */
          <div className="grid gap-6 lg:grid-cols-3">
            <div className="lg:col-span-2 space-y-6">
              
              {/* Current Question */}
              <Card className="shadow-premium overflow-hidden transition-all duration-300">
                <div className="h-1.5 w-full bg-gradient-to-r from-primary to-blue-500" />
                <CardHeader>
                  <CardTitle className="text-lg leading-relaxed">
                    {session.status === "waiting_for_ai" || (countdown !== null && countdown > 0) ? (
                      <div className="flex flex-col items-center justify-center py-12 text-center space-y-6 animate-in fade-in zoom-in-95 duration-500">
                        <div className="relative flex h-16 w-16 items-center justify-center">
                          <span className="absolute inline-flex h-full w-full rounded-full bg-amber-500/20 animate-ping"></span>
                          <Clock className="h-8 w-8 text-amber-500 relative z-10" />
                        </div>
                        <div className="space-y-2">
                          <h3 className="text-xl font-semibold tracking-tight">AI is currently processing requests.</h3>
                          <p className="text-sm text-muted-foreground font-medium">Retry available in:</p>
                          <div className="text-5xl font-mono tracking-wider text-amber-500 font-bold py-2">
                            00:{countdown?.toString().padStart(2, '0') || '60'}
                          </div>
                        </div>
                        <Button 
                          onClick={handleNext} 
                          disabled={countdown !== null && countdown > 0} 
                          className="mt-4 w-40 shadow-premium-sm"
                          variant="outline"
                        >
                          {countdown !== null && countdown > 0 ? "Wait..." : "Retry"}
                        </Button>
                      </div>
                    ) : (!currentQuestion) ? (
                      <div className="flex flex-col items-center justify-center py-16 space-y-8 animate-in fade-in duration-500">
                        <div className="flex items-center gap-4">
                          <div className="relative flex h-12 w-12">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-20 duration-1000"></span>
                            <span className="relative inline-flex rounded-full h-12 w-12 bg-primary/10 flex items-center justify-center border border-primary/20">
                              <Brain className="h-6 w-6 text-primary animate-pulse" />
                            </span>
                          </div>
                          <h3 className="text-xl font-medium tracking-tight">NovaForge AI is generating your interview...</h3>
                        </div>
                        <div className="w-full max-w-md space-y-3">
                          <Progress value={undefined} className="h-1.5 w-full bg-muted overflow-hidden relative">
                            <div className="absolute inset-0 bg-primary/50 animate-[indeterminate_2s_infinite_linear]" style={{width: '50%', transformOrigin: 'left'}} />
                          </Progress>
                          <p className="text-xs text-center text-muted-foreground animate-pulse">Analyzing your curriculum profile and framing the next technical question.</p>
                        </div>
                      </div>
                    ) : (
                      <div className="animate-in fade-in slide-in-from-bottom-2 duration-500">
                        {currentQuestion}
                      </div>
                    )}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <label htmlFor="answer" className="text-sm font-medium text-foreground">
                      Your Answer
                    </label>
                      <textarea
                        id="answer"
                        value={answer}
                        onChange={(e) => setAnswer(e.target.value)}
                        disabled={actionLoading || !!currentFeedback || session.status === "waiting_for_ai" || !currentQuestion}
                        placeholder={!currentQuestion ? "Waiting for question..." : "Type your answer here. Be as detailed as possible..."}
                        className="w-full min-h-[200px] p-4 rounded-xl border border-input bg-background text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary disabled:opacity-50 disabled:cursor-not-allowed resize-y transition-all"
                        aria-label="Answer textarea"
                        ref={textareaRef}
                      />
                  </div>
                </CardContent>
                <CardFooter className="flex justify-end pt-2">
                  {!currentFeedback ? (
                    <Button 
                      onClick={handleSubmit} 
                      disabled={!answer.trim() || actionLoading || (countdown !== null && countdown > 0) || !currentQuestion}
                      className="shadow-premium-sm transition-all duration-300"
                    >
                      {actionLoading ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Evaluating...
                        </>
                      ) : (
                        <>
                          Submit Answer
                          <ArrowRight className="ml-2 h-4 w-4" />
                        </>
                      )}
                    </Button>
                  ) : (
                    <Button 
                      onClick={handleNext} 
                      disabled={actionLoading || (countdown !== null && countdown > 0)}
                      variant="secondary"
                      className="shadow-premium-sm transition-all duration-300"
                    >
                      {actionLoading ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Loading...
                        </>
                      ) : (
                        <>
                          Next Question
                          <Play className="ml-2 h-4 w-4" />
                        </>
                      )}
                    </Button>
                  )}
                </CardFooter>
              </Card>

              {/* Immediate Feedback Panel */}
              {(currentFeedback || (actionLoading && answer.trim())) && (
                <Card className="shadow-premium bg-muted/20 border-l-4 border-l-primary animate-in slide-in-from-bottom-4 fade-in duration-500">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base flex items-center gap-2">
                      <MessageSquare className="h-4 w-4 text-primary" />
                      AI Feedback
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    {!currentFeedback && actionLoading ? (
                      <div className="flex items-center gap-3 text-sm text-muted-foreground">
                        <TypingIndicator />
                        <span className="animate-pulse">Evaluating your response...</span>
                      </div>
                    ) : (
                      <p className="text-sm leading-relaxed text-muted-foreground whitespace-pre-wrap">
                        {currentFeedback}
                      </p>
                    )}
                  </CardContent>
                </Card>
              )}
            </div>

            {/* Right Sidebar */}
            <div className="space-y-6">
              <Card className="shadow-premium">
                <CardHeader>
                  <CardTitle className="text-base">Interview Guidelines</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="text-sm text-muted-foreground space-y-3">
                    <p><strong>1. Be structured:</strong> Use the STAR method for behavioral questions.</p>
                    <p><strong>2. Think aloud:</strong> For technical questions, explain your reasoning before arriving at the solution.</p>
                    <p><strong>3. Edge cases:</strong> Always mention potential edge cases or bottlenecks in your design.</p>
                  </div>
                </CardContent>
              </Card>

              {session.questions_asked.length > 0 && (
                <Card className="shadow-premium">
                  <CardHeader>
                    <CardTitle className="text-base">Session History</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4 relative before:absolute before:inset-0 before:ml-[11px] before:w-px before:bg-border">
                      {session.questions_asked.map((q: AskedQuestion, i: number) => (
                        <div key={i} className="relative flex gap-3 text-sm">
                          <div className={`mt-0.5 w-6 h-6 rounded-full flex items-center justify-center border-2 bg-background z-10 shrink-0 ${q.answer_given ? 'border-primary' : 'border-muted'}`}>
                            {q.answer_given && <CheckCircle2 className="h-3 w-3 text-primary" />}
                          </div>
                          <div>
                            <p className="font-medium text-foreground">Question {i + 1}</p>
                            <p className="text-xs text-muted-foreground truncate w-[200px]">{q.question_text}</p>
                            {q.score !== undefined && (
                              <Badge variant="secondary" className="mt-1 text-[10px] px-1.5 py-0">Score: {q.score}/10</Badge>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        )}
      </PageContainer>
    </DashboardLayout>
  )
}
