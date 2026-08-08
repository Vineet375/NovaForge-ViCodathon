import { DashboardLayout } from "@/components/layout/dashboard-layout"
import { CandidateSelector } from "@/components/dashboard/candidate-selector"

export default function CandidatesPage() {
  return (
    <DashboardLayout>
      <div className="p-8 max-w-5xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">Candidates</h1>
          <p className="text-muted-foreground">
            Select a candidate to review their profile or start an interview session.
          </p>
        </div>
        
        <CandidateSelector />
      </div>
    </DashboardLayout>
  )
}
