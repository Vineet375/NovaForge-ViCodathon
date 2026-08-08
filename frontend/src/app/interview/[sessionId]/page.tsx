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
import { Loader2, ArrowRight, CheckCircle2, MessageSquare, Play, AlertCircle } from "lucide-react"
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
    nextQuestion,
    answerQuestion
  } = useInterviewSession(sessionId)

  const [answer, setAnswer] = React.useState("")
  const [currentFeedback, setCurrentFeedback] = React.useState<string | null>(null)

  // Auto-fetch first question if none exists and session is active
  React.useEffect(() => {
    if (session?.status === "in_progress" && !currentQuestion && session.questions_asked.length === 0) {
      nextQuestion()
    }
    // If a question was already asked but not answered, set it
    if (session?.status === "in_progress" && !currentQuestion && session.questions_asked.length > 0) {
      const lastQ = session.questions_asked[session.questions_asked.length - 1]
      if (!lastQ.answer_given) {
        // We'd need a way to get the text of the current question, but it's in the session state
        // The hook state manages it, but let's just trigger nextQuestion if there's an issue
        // Actually, the hook should initialize currentQuestion if it fetches session. 
        // For now, let's just show it.
      }
    }
  }, [session, currentQuestion, nextQuestion])

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
        <PageContainer className="flex items-center justify-center min-h-[60vh]">
          <div className="flex flex-col items-center gap-4">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
            <p className="text-muted-foreground font-medium">Loading Interview Session...</p>
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
                    {currentQuestion || (session.questions_asked.length > 0 && !session.questions_asked[session.questions_asked.length - 1].answer_given ? session.questions_asked[session.questions_asked.length - 1].question_text : "Loading next question...")}
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
                      disabled={actionLoading || !!currentFeedback}
                      placeholder="Type your answer here. Be as detailed as possible..."
                      className="w-full min-h-[200px] p-4 rounded-xl border border-input bg-background text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50 disabled:cursor-not-allowed resize-y"
                      aria-label="Answer textarea"
                    />
                  </div>
                </CardContent>
                <CardFooter className="flex justify-end pt-2">
                  {!currentFeedback ? (
                    <Button 
                      onClick={handleSubmit} 
                      disabled={!answer.trim() || actionLoading}
                      className="shadow-premium-sm"
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
                      disabled={actionLoading}
                      variant="secondary"
                      className="shadow-premium-sm"
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
