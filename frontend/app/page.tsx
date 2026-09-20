"use client";

import React, { useState } from "react";
import { Navbar } from "@/components/Navbar";
import { DashboardView } from "@/components/DashboardView";
import { InterviewSessionView } from "@/components/InterviewSessionView";
import { PreparationReportView } from "@/components/PreparationReportView";
import { AuthModal } from "@/components/AuthModal";
import { PreparationSetupModal } from "@/components/PreparationSetupModal";

export default function Home() {
  const [activeView, setActiveView] = useState<"dashboard" | "interview" | "report">("dashboard");
  const [activeInterviewId, setActiveInterviewId] = useState<string | null>(null);

  // Modals
  const [isAuthModalOpen, setIsAuthModalOpen] = useState<boolean>(false);
  const [authModalMode, setAuthModalMode] = useState<"login" | "register">("login");

  const [isSetupModalOpen, setIsSetupModalOpen] = useState<boolean>(false);
  const [setupPreset, setSetupPreset] = useState<{
    company: string;
    role: string;
    stage: string;
    nature: string;
  } | null>(null);

  const handleOpenAuth = (mode: "login" | "register" = "login") => {
    setAuthModalMode(mode);
    setIsAuthModalOpen(true);
  };

  const handleStartNewSession = (preset?: {
    company: string;
    role: string;
    stage: string;
    nature: string;
  }) => {
    setSetupPreset(preset || null);
    setIsSetupModalOpen(true);
  };

  const handleInterviewCreated = (interviewId: string) => {
    setActiveInterviewId(interviewId);
    setActiveView("interview");
  };

  const handleInterviewCompleted = React.useCallback((interviewId: string) => {
    setActiveInterviewId(interviewId);
    setActiveView("report");
  }, []);

  const handleOpenReport = (interviewId: string) => {
    setActiveInterviewId(interviewId);
    setActiveView("report");
  };

  const handleResumeInterview = (interviewId: string) => {
    setActiveInterviewId(interviewId);
    setActiveView("interview");
  };

  const handleGoHome = () => {
    setActiveView("dashboard");
  };

  return (
    <div className="min-h-screen flex flex-col bg-zinc-50 dark:bg-black text-zinc-900 dark:text-zinc-100 font-sans">
      {/* Top Navigation */}
      <Navbar
        onOpenAuth={handleOpenAuth}
        onOpenNewSession={() => handleStartNewSession()}
        onGoHome={handleGoHome}
      />

      {/* Main App Surfaces */}
      <main className="flex-1">
        {activeView === "dashboard" && (
          <DashboardView
            onStartNewSession={handleStartNewSession}
            onOpenReport={handleOpenReport}
            onResumeInterview={handleResumeInterview}
            onOpenAuth={handleOpenAuth}
          />
        )}

        {activeView === "interview" && activeInterviewId && (
          <InterviewSessionView
            interviewId={activeInterviewId}
            onInterviewCompleted={handleInterviewCompleted}
            onExit={handleGoHome}
          />
        )}

        {activeView === "report" && activeInterviewId && (
          <PreparationReportView
            interviewId={activeInterviewId}
            onBackToDashboard={handleGoHome}
            onPracticeAgain={() => handleStartNewSession()}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="mt-auto border-t border-zinc-200/80 bg-white/60 dark:border-zinc-800/80 dark:bg-zinc-950/60 py-8 px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-zinc-500">
          <div>
            <span className="font-semibold text-zinc-700 dark:text-zinc-300">Bespoke</span> — Candidate-first AI Technical Interview Preparation.
          </div>
          <div className="flex items-center gap-4">
            <span>Server-isolated candidate sessions</span>
            <span>•</span>
            <span>Grounded evidence provenance</span>
          </div>
        </div>
      </footer>

      {/* Modals */}
      <AuthModal
        key={authModalMode}
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        initialMode={authModalMode}
      />

      <PreparationSetupModal
        key={setupPreset ? `${setupPreset.company}-${setupPreset.stage}-${setupPreset.nature}` : "new-session"}
        isOpen={isSetupModalOpen}
        onClose={() => setIsSetupModalOpen(false)}
        onInterviewCreated={handleInterviewCreated}
        initialPreset={setupPreset}
      />
    </div>
  );
}
