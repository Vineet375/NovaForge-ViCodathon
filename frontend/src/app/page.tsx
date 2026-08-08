"use client"
import { DashboardLayout } from "@/components/layout/dashboard-layout"
import { PageContainer, Section, SectionHeader, SectionTitle, SectionDescription } from "@/components/layout/layout-foundation"
import { Button } from "@/components/ui/button"
import { Play } from "lucide-react"
import { CandidateSelector } from "@/components/dashboard/candidate-selector"
import { CurriculumProgress } from "@/components/dashboard/curriculum-progress"
import { ActivityTimeline } from "@/components/dashboard/activity-timeline"
import { DashboardStats } from "@/components/dashboard/dashboard-stats"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { InterviewAPI, ActiveSessionResponse } from "@/lib/api"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Clock, Users, ArrowRight } from "lucide-react"

export default function Home() {
  const [activeSessions, setActiveSessions] = useState<ActiveSessionResponse[]>([])
  const [loadingSessions, setLoadingSessions] = useState(true)
  const router = useRouter()

  useEffect(() => {
    InterviewAPI.getActiveSessions()
      .then(sessions => {
        setActiveSessions(sessions)
        setLoadingSessions(false)
      })
      .catch(() => {
        setLoadingSessions(false)
      })
  }, [])

  const handleResume = (sessionId: string) => {
    router.push(`/interview/${sessionId}`)
  }

  return (
    <DashboardLayout>
      <PageContainer className="py-6 sm:py-8 space-y-8">
        <Section className="py-0 md:py-0 lg:py-0">
          <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <SectionHeader className="pb-0 md:pb-0">
              <SectionTitle className="text-3xl sm:text-4xl">Good morning, Alex</SectionTitle>
              <SectionDescription>
                You have an interview scheduled for tomorrow. Keep preparing!
              </SectionDescription>
            </SectionHeader>
          </div>
        </Section>

        {/* Active Sessions Section */}
        <Section className="py-0 md:py-0 lg:py-0">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-semibold tracking-tight">Active Interviews</h3>
          </div>
          
          {loadingSessions ? (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {[1, 2].map(i => (
                <Card key={i} className="shadow-premium opacity-70">
                  <CardContent className="p-6 space-y-4">
                    <div className="flex justify-between items-start">
                      <div className="space-y-2 w-full">
                        <div className="h-5 w-1/2 bg-muted animate-pulse rounded-md"></div>
                        <div className="h-4 w-1/3 bg-muted animate-pulse rounded-md"></div>
                      </div>
                    </div>
                    <div className="h-2 w-full bg-muted animate-pulse rounded-full mt-4"></div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : activeSessions.length > 0 ? (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {activeSessions.map(session => (
                <Card 
                  key={session.session_id} 
                  className="shadow-premium group hover:shadow-premium-lg transition-all duration-300 border-border/50 overflow-hidden relative cursor-pointer"
                  onClick={() => handleResume(session.session_id)}
                >
                  <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-primary to-blue-500 opacity-50 group-hover:opacity-100 transition-opacity" />
                  <CardContent className="p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h4 className="font-semibold text-lg">{session.candidate_name}</h4>
                        <p className="text-sm text-muted-foreground flex items-center gap-1 mt-1">
                          <Users className="h-3.5 w-3.5" /> Frontend Developer
                        </p>
                      </div>
                      <Badge variant={session.status === 'waiting_for_ai' ? 'destructive' : 'secondary'} className="capitalize text-xs">
                        {session.status.replaceAll('_', ' ')}
                      </Badge>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between text-xs text-muted-foreground font-medium">
                        <span>Question {session.current_question_number} of 8</span>
                        <span>{Math.max(0, Math.round(((session.current_question_number - 1) / 8) * 100))}%</span>
                      </div>
                      <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-primary transition-all duration-500" 
                          style={{ width: `${Math.max(0, ((session.current_question_number - 1) / 8) * 100)}%` }}
                        />
                      </div>
                    </div>
                    
                    <div className="mt-5 flex items-center justify-between text-sm">
                      <div className="flex items-center text-muted-foreground text-xs gap-1.5">
                        <Clock className="h-3.5 w-3.5" /> Last updated recently
                      </div>
                      <Button variant="ghost" size="sm" className="h-8 px-2 group-hover:text-primary transition-colors">
                        Resume <ArrowRight className="ml-1 h-3.5 w-3.5" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card className="shadow-premium border-dashed bg-muted/10">
              <CardContent className="flex flex-col items-center justify-center py-12 text-center">
                <div className="h-12 w-12 rounded-full bg-muted flex items-center justify-center mb-4">
                  <Play className="h-6 w-6 text-muted-foreground ml-1" />
                </div>
                <h3 className="text-lg font-semibold">No Active Interviews</h3>
                <p className="text-sm text-muted-foreground mt-1 max-w-sm">
                  You don't have any interviews in progress. Select a candidate below to start a new session.
                </p>
              </CardContent>
            </Card>
          )}
        </Section>

        <Section className="py-0 md:py-0 lg:py-0">
          <DashboardStats />
        </Section>

        <Section className="py-0 md:py-0 lg:py-0">
          <div className="grid gap-8 lg:grid-cols-3">
            <div className="lg:col-span-2 space-y-8">
              <CurriculumProgress />
              <ActivityTimeline />
            </div>
            
            <div className="space-y-8">
              <div>
                <h3 className="text-lg font-medium mb-4">Select Candidate</h3>
                <CandidateSelector />
              </div>
            </div>
          </div>
        </Section>
      </PageContainer>
    </DashboardLayout>
  )
}
