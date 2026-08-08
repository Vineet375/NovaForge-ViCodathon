"use client"

import * as React from "react"
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Target, Brain, Download, ChevronRight, CheckCircle2 } from "lucide-react"

interface InterviewReportProps {
  feedback: any
  onClose: () => void
}

export function InterviewReport({ feedback, onClose }: InterviewReportProps) {
  // Gracefully handle both string and structured JSON responses
  const isObject = typeof feedback === "object" && feedback !== null
  const summary = isObject ? (feedback.interview_summary || feedback.summary || "No summary provided.") : (feedback || "No summary provided.")
  const overallScore = isObject && feedback.overall_score ? feedback.overall_score : "N/A"
  
  const strengths = isObject && Array.isArray(feedback.strengths) && feedback.strengths.length > 0 
    ? feedback.strengths 
    : ["No specific strengths identified."]
    
  const weaknesses = isObject && Array.isArray(feedback.weaknesses) && feedback.weaknesses.length > 0 
    ? feedback.weaknesses 
    : ["No specific growth areas identified."]

  return (
    <div className="space-y-8 animate-in fade-in zoom-in-95 duration-500">
      <div className="text-center space-y-2 mb-8">
        <div className="mx-auto w-16 h-16 bg-green-500/10 rounded-full flex items-center justify-center mb-4">
          <CheckCircle2 className="h-8 w-8 text-green-500" />
        </div>
        <h2 className="text-3xl font-bold tracking-tight">Interview Completed</h2>
        <p className="text-muted-foreground max-w-xl mx-auto">
          You've completed the assessment. Here is your detailed performance report and AI-generated learning roadmap.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {/* Left Column: Overall Score */}
        <div className="md:col-span-1 space-y-6">
          <Card className="shadow-premium overflow-hidden relative">
            <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-green-500 to-emerald-500" />
            <CardContent className="pt-8 text-center pb-6">
              <div className="text-sm font-medium text-muted-foreground uppercase tracking-wider mb-2">Overall Score</div>
              <div className="flex items-end justify-center gap-1 mb-2">
                <span className="text-5xl font-bold text-foreground">{overallScore}</span>
                {overallScore !== "N/A" && <span className="text-xl font-medium text-muted-foreground mb-1">/100</span>}
              </div>
              {overallScore !== "N/A" && overallScore >= 70 && (
                <Badge variant="secondary" className="bg-green-500/10 text-green-500 hover:bg-green-500/20 mt-2">
                  Strong Performance
                </Badge>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Right Column: Feedback & Action Plan */}
        <div className="md:col-span-2 space-y-6">
          <Card className="shadow-premium h-full flex flex-col">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Brain className="h-5 w-5 text-primary" />
                Performance Summary
              </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 space-y-6">
              <div className="prose prose-sm dark:prose-invert max-w-none text-muted-foreground leading-relaxed whitespace-pre-wrap">
                {summary}
              </div>

              <div className="grid sm:grid-cols-2 gap-4 pt-4 border-t border-border">
                <div className="space-y-3">
                  <h4 className="text-sm font-semibold text-green-500 flex items-center gap-1.5">
                    <Target className="h-4 w-4" />
                    Key Strengths
                  </h4>
                  <ul className="text-sm text-muted-foreground space-y-2">
                    {strengths.map((str: string, i: number) => (
                      <li key={i}>• {str}</li>
                    ))}
                  </ul>
                </div>
                <div className="space-y-3">
                  <h4 className="text-sm font-semibold text-amber-500 flex items-center gap-1.5">
                    <Target className="h-4 w-4" />
                    Growth Areas
                  </h4>
                  <ul className="text-sm text-muted-foreground space-y-2">
                    {weaknesses.map((wk: string, i: number) => (
                      <li key={i}>• {wk}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </CardContent>
            <CardFooter className="bg-muted/30 border-t border-border mt-auto p-4 flex justify-between items-center">
              <Button variant="outline" size="sm" className="bg-background">
                <Download className="mr-2 h-4 w-4" />
                Download PDF
              </Button>
              <Button onClick={onClose} className="shadow-premium-sm">
                Return to Dashboard
                <ChevronRight className="ml-2 h-4 w-4" />
              </Button>
            </CardFooter>
          </Card>
        </div>
      </div>
    </div>
  )
}
