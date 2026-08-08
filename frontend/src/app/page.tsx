import { DashboardLayout } from "@/components/layout/dashboard-layout"
import { PageContainer, Section, SectionHeader, SectionTitle, SectionDescription } from "@/components/layout/layout-foundation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Play, TrendingUp, Target, Clock, Zap } from "lucide-react"
import { CandidateSelector } from "@/components/dashboard/candidate-selector"

export default function Home() {
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
            <div className="flex shrink-0 items-center gap-3">
              <Button size="lg" className="w-full sm:w-auto shadow-premium-sm">
                <Play className="mr-2 h-4 w-4" />
                Resume Interview
              </Button>
            </div>
          </div>
        </Section>

        <Section className="py-0 md:py-0 lg:py-0">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Completed Interviews</CardTitle>
                <Target className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">12</div>
                <p className="text-xs text-muted-foreground mt-1">
                  +2 from last month
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Average Score</CardTitle>
                <TrendingUp className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">84%</div>
                <p className="text-xs text-muted-foreground mt-1">
                  +5% improvement
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Questions Answered</CardTitle>
                <Zap className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">142</div>
                <p className="text-xs text-muted-foreground mt-1">
                  Across 6 domains
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Active Session</CardTitle>
                <Clock className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">Frontend System Design</div>
                <p className="text-xs text-muted-foreground mt-1">
                  45 minutes remaining
                </p>
              </CardContent>
            </Card>
          </div>
        </Section>

        <Section className="py-0 md:py-0 lg:py-0">
          <div className="grid gap-8 lg:grid-cols-3">
            <div className="lg:col-span-2 space-y-8">
              {/* Future Interview Overview and Curriculum Progress will go here */}
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
