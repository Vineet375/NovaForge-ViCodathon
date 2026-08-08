"use client"

import * as React from "react"
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from "recharts"
import { Target, Brain, Download, ChevronRight, CheckCircle2 } from "lucide-react"

interface InterviewReportProps {
  feedback: any
  onClose: () => void
}

export function InterviewReport({ feedback, onClose }: InterviewReportProps) {
  // Parse feedback strings or assume it's already an object
  // Since the backend might return raw markdown or an object, we gracefully handle both
  const isObject = typeof feedback === "object" && feedback !== null
  const summary = isObject ? feedback.summary : feedback
  
  // Mock radar data based on typical interview domains
  const radarData = [
    { subject: 'System Design', A: 85, fullMark: 100 },
    { subject: 'Algorithms', A: 70, fullMark: 100 },
    { subject: 'Communication', A: 90, fullMark: 100 },
    { subject: 'React/Frontend', A: 88, fullMark: 100 },
    { subject: 'Problem Solving', A: 75, fullMark: 100 },
    { subject: 'Best Practices', A: 80, fullMark: 100 },
  ]

  const overallScore = 81

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
        {/* Left Column: Overall Score & Radar */}
        <div className="md:col-span-1 space-y-6">
          <Card className="shadow-premium overflow-hidden relative">
            <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-green-500 to-emerald-500" />
            <CardContent className="pt-8 text-center pb-6">
              <div className="text-sm font-medium text-muted-foreground uppercase tracking-wider mb-2">Overall Score</div>
              <div className="flex items-end justify-center gap-1 mb-2">
                <span className="text-5xl font-bold text-foreground">{overallScore}</span>
                <span className="text-xl font-medium text-muted-foreground mb-1">/100</span>
              </div>
              <Badge variant="secondary" className="bg-green-500/10 text-green-500 hover:bg-green-500/20">
                Strong Performance
              </Badge>
            </CardContent>
          </Card>

          <Card className="shadow-premium">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Domain Mastery</CardTitle>
            </CardHeader>
            <CardContent className="px-2">
              <div className="h-[250px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                    <PolarGrid stroke="hsl(var(--border))" />
                    <PolarAngleAxis dataKey="subject" tick={{ fill: "hsl(var(--foreground))", fontSize: 10 }} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                    <Radar
                      name="Candidate"
                      dataKey="A"
                      stroke="hsl(var(--primary))"
                      fill="hsl(var(--primary))"
                      fillOpacity={0.4}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
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
                    <li>• Clear communication of architectural tradeoffs</li>
                    <li>• Strong understanding of state management</li>
                    <li>• Good handling of edge cases</li>
                  </ul>
                </div>
                <div className="space-y-3">
                  <h4 className="text-sm font-semibold text-amber-500 flex items-center gap-1.5">
                    <Target className="h-4 w-4" />
                    Growth Areas
                  </h4>
                  <ul className="text-sm text-muted-foreground space-y-2">
                    <li>• Algorithm time complexity optimization</li>
                    <li>• Detailed database schema normalization</li>
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
