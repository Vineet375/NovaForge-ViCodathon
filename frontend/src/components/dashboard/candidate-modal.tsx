"use client"
import * as React from "react"
import { Candidate } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { X, Play, Briefcase, Code, Brain, Target, User } from "lucide-react"

interface CandidateModalProps {
  candidate: Candidate
  onClose: () => void
  onStart: (id: string) => void
  isStarting: boolean
}

export function CandidateModal({ candidate, onClose, onStart, isStarting }: CandidateModalProps) {
  // Prevent body scroll when modal is open
  React.useEffect(() => {
    document.body.style.overflow = "hidden"
    return () => {
      document.body.style.overflow = "unset"
    }
  }, [])

  const techStack = Array.from(new Set(
    candidate.missions
      .filter(m => m.passed)
      .map(m => {
        if (m.title.includes("Embeddings") || m.title.includes("Vector")) return "Vector DB"
        if (m.title.includes("Prompt")) return "Prompt Eng"
        if (m.title.includes("API") || m.title.includes("Backend")) return "Backend API"
        if (m.title.includes("Agent")) return "Agentic AI"
        if (m.title.includes("Frontend")) return "React"
        if (m.title.includes("Data")) return "Data Processing"
        return "AI Core"
      })
  ))

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-background/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="absolute inset-0" onClick={onClose} />
      <Card className="relative z-10 w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl animate-in zoom-in-95 duration-200 border-border">
        <Button 
          variant="ghost" 
          size="icon" 
          className="absolute right-4 top-4 rounded-full" 
          onClick={onClose}
        >
          <X className="h-4 w-4" />
        </Button>
        <CardHeader className="pb-4 border-b border-border">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center border-2 border-primary/20 text-xl font-bold text-primary">
              {candidate.member.name.substring(0, 2).toUpperCase()}
            </div>
            <div>
              <CardTitle className="text-2xl">{candidate.member.name}</CardTitle>
              <div className="flex items-center gap-2 mt-1 text-muted-foreground">
                <Briefcase className="h-4 w-4" />
                <span>{candidate.member.jobRole} • {candidate.member.yearsExperience} yrs exp</span>
              </div>
            </div>
          </div>
        </CardHeader>
        <CardContent className="pt-6 space-y-8">
          {/* Tech Stack */}
          <div className="space-y-3">
            <h4 className="text-sm font-semibold flex items-center gap-2">
              <Code className="h-4 w-4 text-primary" />
              Technical Stack
            </h4>
            <div className="flex flex-wrap gap-2">
              {techStack.length > 0 ? (
                techStack.map(skill => (
                  <Badge key={skill} variant="secondary" className="px-2.5 py-1">
                    {skill}
                  </Badge>
                ))
              ) : (
                <span className="text-sm text-muted-foreground">No specific stack derived from missions.</span>
              )}
            </div>
          </div>

          <div className="grid sm:grid-cols-2 gap-6">
            {/* Strengths */}
            <div className="space-y-3">
              <h4 className="text-sm font-semibold flex items-center gap-2 text-green-500">
                <Brain className="h-4 w-4" />
                Strong Areas
              </h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">•</span>
                  {candidate.signals.missionsFirstTry > 10 ? "Fast Learner (High first-try rate)" : "Persistent Problem Solver"}
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">•</span>
                  Completion Rate: {Math.round((candidate.signals.missionsCompleted / 31) * 100)}%
                </li>
              </ul>
            </div>

            {/* Areas to Improve */}
            <div className="space-y-3">
              <h4 className="text-sm font-semibold flex items-center gap-2 text-amber-500">
                <Target className="h-4 w-4" />
                Areas to Improve
              </h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                {candidate.missions.filter(m => !m.passed && m.attempts && m.attempts > 2).slice(0, 2).map((m, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-amber-500 mt-0.5">•</span>
                    Struggles with {m.title}
                  </li>
                ))}
                {candidate.missions.filter(m => !m.passed && m.attempts && m.attempts > 2).length === 0 && (
                  <li className="flex items-start gap-2">
                    <span className="text-amber-500 mt-0.5">•</span>
                    Consistent performer across topics
                  </li>
                )}
              </ul>
            </div>
          </div>
          
          <div className="space-y-3">
             <h4 className="text-sm font-semibold flex items-center gap-2">
              <User className="h-4 w-4 text-primary" />
              AI Recommendation
            </h4>
            <p className="text-sm leading-relaxed text-muted-foreground p-4 bg-muted/30 rounded-lg border border-border">
              {candidate.member.name} demonstrates a solid grasp of core {candidate.member.jobRole} concepts. Focus the upcoming interview on real-world system design tradeoffs to assess their senior potential.
            </p>
          </div>
        </CardContent>
        <CardFooter className="border-t border-border pt-4 pb-4 px-6 justify-end gap-3">
          <Button variant="outline" onClick={onClose} disabled={isStarting}>Cancel</Button>
          <Button onClick={() => onStart(candidate.member.id)} disabled={isStarting} className="shadow-premium-sm">
            {isStarting ? "Starting..." : "Begin Interview"}
            {!isStarting && <Play className="ml-2 h-4 w-4" />}
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}
