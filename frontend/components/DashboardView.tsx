"use client";

import React, { useState, useEffect } from "react";
import { useAuth } from "@/lib/auth-context";
import { api, InterviewSessionData } from "@/lib/api";
import {
  Sparkles,
  PlusCircle,
  Play,
  ArrowRight,
  TrendingUp,
  ShieldCheck,
  Building2,
  Clock,
  CheckCircle2,
  ChevronRight,
  Layers,
  Terminal,
  Cpu,
  Brain,
  Award,
  Loader2,
} from "lucide-react";

interface DashboardViewProps {
  onStartNewSession: (preset?: {
    company: string;
    role: string;
    stage: string;
    nature: string;
  }) => void;
  onOpenReport: (interviewId: string) => void;
  onResumeInterview: (interviewId: string) => void;
  onOpenAuth: (mode?: "login" | "register") => void;
}

const QUICK_PRESETS = [
  {
    company: "Stripe",
    role: "Staff Backend Engineer",
    stage: "Technical Round 1",
    nature: "Coding",
    icon: Terminal,
    description: "Idempotency, distributed transactions, webhooks, and production resilience.",
    badge: "High Depth",
  },
  {
    company: "Google",
    role: "Senior Systems Engineer",
    stage: "System Design",
    nature: "System Design",
    icon: Cpu,
    description: "Global replication, consistent hashing, consensus algorithms, and fault tolerance.",
    badge: "Distributed Systems",
  },
  {
    company: "OpenAI",
    role: "GenAI & Foundations Engineer",
    stage: "Technical Round 1",
    nature: "ML/AI Technical",
    icon: Brain,
    description: "Attention mechanisms, RAG architectures, prompt latency, and LLM evaluation.",
    badge: "AI Engineering",
  },
  {
    company: "Amazon",
    role: "Principal Engineer",
    stage: "Hiring Manager",
    nature: "Behavioral",
    icon: Award,
    description: "Leadership Principles, deep dive architectural trade-offs, and bias for action.",
    badge: "Leadership & STAR",
  },
];

export function DashboardView({
  onStartNewSession,
  onOpenReport,
  onResumeInterview,
  onOpenAuth,
}: DashboardViewProps) {
  const { user, token } = useAuth();
  const [interviews, setInterviews] = useState<InterviewSessionData[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    let isMounted = true;
    async function loadSessions() {
      if (!token) {
        setIsLoading(false);
        return;
      }
      try {
        const data = await api.listInterviews(token);
        if (isMounted) setInterviews(data);
      } catch (err) {
        console.error("Failed to load interview history:", err);
      } finally {
        if (isMounted) setIsLoading(false);
      }
    }

    loadSessions();
    return () => {
      isMounted = false;
    };
  }, [token]);

  // Derived candidate metrics
  const completedCount = interviews.filter((i) => i.status === "completed").length;
  const inProgressCount = interviews.filter((i) => i.status !== "completed").length;
  const scores = interviews
    .map((i) => i.overall_score)
    .filter((s): s is number => typeof s === "number");
  const avgScore = scores.length > 0 ? (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1) : null;
  const uniqueCompanies = Array.from(
    new Set(interviews.map((i) => i.company).filter(Boolean))
  ).length;

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-12 animate-in fade-in duration-300">
      {/* Hero Welcome & Value Proposition */}
      <div className="relative overflow-hidden rounded-3xl border border-zinc-200 bg-white p-6 sm:p-10 shadow-sm dark:border-zinc-800 dark:bg-zinc-900/90">
        <div className="relative z-10 flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
          <div className="max-w-2xl space-y-3">
            <div className="inline-flex items-center gap-2 rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-600 dark:bg-emerald-500/20 dark:text-emerald-400 border border-emerald-500/20">
              <Sparkles className="size-3.5" />
              <span>Company-Calibrated Technical Interview Preparation</span>
            </div>

            <h1 className="text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-zinc-50 sm:text-4xl">
              {user ? `Welcome back, ${user.full_name || "Engineer"}` : "Master Your High-Stakes Tech Interviews"}
            </h1>

            <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed max-w-xl">
              Simulate company-specific rounds with resume intelligence, adaptive follow-up questioning,
              and stage-calibrated rubrics. Receive evidence-grounded feedback with readiness scoring and actionable preparation steps.
            </p>

            <div className="pt-2 flex flex-wrap items-center gap-3">
              <button
                type="button"
                onClick={() => onStartNewSession()}
                className="inline-flex items-center gap-2 rounded-xl bg-zinc-900 px-5 py-2.5 text-xs font-bold text-white shadow-sm hover:bg-zinc-800 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200 transition-all active:scale-[0.98]"
              >
                <PlusCircle className="size-4" />
                <span>Start Tailored Practice</span>
              </button>

              {!user && (
                <button
                  type="button"
                  onClick={() => onOpenAuth("register")}
                  className="inline-flex items-center gap-2 rounded-xl border border-zinc-200 bg-zinc-50 px-4 py-2.5 text-xs font-semibold text-zinc-700 hover:bg-zinc-100 dark:border-zinc-800 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700 transition-colors"
                >
                  <span>Create Free Account</span>
                  <ChevronRight className="size-3.5" />
                </button>
              )}
            </div>
          </div>

          {/* Quick Stats Grid */}
          <div className="grid grid-cols-2 gap-3 sm:gap-4 sm:min-w-[320px]">
            <div className="rounded-2xl border border-zinc-200 bg-zinc-50/70 p-4 dark:border-zinc-800 dark:bg-zinc-850/50">
              <div className="flex items-center gap-1.5 text-xs text-zinc-500">
                <CheckCircle2 className="size-3.5 text-emerald-500" />
                <span>Completed</span>
              </div>
              <div className="mt-1 text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">
                {completedCount}
              </div>
              <div className="text-[10px] text-zinc-400 mt-0.5">Mock sessions</div>
            </div>

            <div className="rounded-2xl border border-zinc-200 bg-zinc-50/70 p-4 dark:border-zinc-800 dark:bg-zinc-850/50">
              <div className="flex items-center gap-1.5 text-xs text-zinc-500">
                <TrendingUp className="size-3.5 text-blue-500" />
                <span>Avg Readiness</span>
              </div>
              <div className="mt-1 text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">
                {avgScore ? `${avgScore}/10` : "—"}
              </div>
              <div className="text-[10px] text-zinc-400 mt-0.5">Across all rounds</div>
            </div>

            <div className="rounded-2xl border border-zinc-200 bg-zinc-50/70 p-4 dark:border-zinc-800 dark:bg-zinc-850/50">
              <div className="flex items-center gap-1.5 text-xs text-zinc-500">
                <Building2 className="size-3.5 text-indigo-500" />
                <span>Target Orgs</span>
              </div>
              <div className="mt-1 text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">
                {uniqueCompanies}
              </div>
              <div className="text-[10px] text-zinc-400 mt-0.5">Companies practiced</div>
            </div>

            <div className="rounded-2xl border border-zinc-200 bg-zinc-50/70 p-4 dark:border-zinc-800 dark:bg-zinc-850/50">
              <div className="flex items-center gap-1.5 text-xs text-zinc-500">
                <ShieldCheck className="size-3.5 text-amber-500" />
                <span>In Progress</span>
              </div>
              <div className="mt-1 text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">
                {inProgressCount}
              </div>
              <div className="text-[10px] text-zinc-400 mt-0.5">Active interviews</div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Launch Pre-Calibrated Targets */}
      <div>
        <div className="mb-4 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
              Target Company Presets
            </h2>
            <p className="text-xs text-zinc-500">
              Jump straight into curated question architectures and evaluation standards.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {QUICK_PRESETS.map((preset, idx) => {
            const Icon = preset.icon;
            return (
              <div
                key={idx}
                className="group relative flex flex-col justify-between rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm transition-all hover:border-zinc-400 hover:shadow-md dark:border-zinc-800 dark:bg-zinc-900 dark:hover:border-zinc-700"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex size-9 items-center justify-center rounded-xl bg-zinc-100 text-zinc-800 dark:bg-zinc-800 dark:text-zinc-200 group-hover:bg-zinc-900 group-hover:text-white dark:group-hover:bg-zinc-100 dark:group-hover:text-zinc-900 transition-colors">
                      <Icon className="size-4" />
                    </div>
                    <span className="rounded-md bg-zinc-100 px-2 py-0.5 text-[10px] font-semibold text-zinc-600 dark:bg-zinc-800 dark:text-zinc-300">
                      {preset.badge}
                    </span>
                  </div>

                  <h3 className="font-bold text-sm text-zinc-900 dark:text-zinc-100">
                    {preset.company}
                  </h3>
                  <div className="text-xs font-medium text-zinc-500 dark:text-zinc-400 mb-2">
                    {preset.role}
                  </div>
                  <p className="text-xs text-zinc-600 dark:text-zinc-400 leading-relaxed mb-4">
                    {preset.description}
                  </p>
                </div>

                <div className="pt-2 border-t border-zinc-100 dark:border-zinc-800 flex items-center justify-between">
                  <span className="text-[10px] font-medium text-emerald-600 dark:text-emerald-400">
                    {preset.nature}
                  </span>
                  <button
                    type="button"
                    onClick={() => onStartNewSession(preset)}
                    className="inline-flex items-center gap-1 text-xs font-semibold text-zinc-900 dark:text-zinc-100 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors"
                  >
                    <span>Practice</span>
                    <ArrowRight className="size-3.5 group-hover:translate-x-0.5 transition-transform" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Interview History & Reports */}
      <div>
        <div className="mb-4 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
              Your Preparation Sessions
            </h2>
            <p className="text-xs text-zinc-500">
              Review completed performance reports, examine evidence citations, or resume active sessions.
            </p>
          </div>
        </div>

        {isLoading ? (
          <div className="flex items-center justify-center rounded-2xl border border-zinc-200 bg-white p-12 dark:border-zinc-800 dark:bg-zinc-900 text-zinc-400">
            <Loader2 className="size-5 animate-spin mr-2 text-zinc-600 dark:text-zinc-300" />
            <span className="text-xs">Loading preparation sessions...</span>
          </div>
        ) : interviews.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-zinc-300 p-8 text-center dark:border-zinc-800">
            <div className="mx-auto flex size-12 items-center justify-center rounded-2xl bg-zinc-100 dark:bg-zinc-800 text-zinc-500 mb-3">
              <Layers className="size-6" />
            </div>
            <h3 className="font-semibold text-sm text-zinc-900 dark:text-zinc-100">
              No preparation sessions yet
            </h3>
            <p className="text-xs text-zinc-500 max-w-sm mx-auto mt-1 mb-4">
              Start your first tailored interview session by uploading your resume and specifying your target company and round nature.
            </p>
            <button
              type="button"
              onClick={() => onStartNewSession()}
              className="inline-flex items-center gap-2 rounded-xl bg-zinc-900 px-4 py-2 text-xs font-semibold text-white shadow hover:bg-zinc-800 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200 transition-all"
            >
              <PlusCircle className="size-3.5" />
              <span>Start First Session</span>
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {interviews.map((session) => {
              const isCompleted = session.status === "completed";
              const dateStr = session.created_at
                ? new Date(session.created_at).toLocaleDateString("en-US", {
                    month: "short",
                    day: "numeric",
                    year: "numeric",
                  })
                : "Recent";

              return (
                <div
                  key={session._id}
                  className="flex flex-col justify-between rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm dark:border-zinc-800 dark:bg-zinc-900 hover:border-zinc-400 dark:hover:border-zinc-700 transition-all"
                >
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-bold text-sm text-zinc-900 dark:text-zinc-100">
                        {session.company || "Target Company"}
                      </span>
                      <span
                        className={`rounded-full px-2 py-0.5 text-[10px] font-semibold ${
                          isCompleted
                            ? "bg-emerald-500/10 text-emerald-600 dark:bg-emerald-500/20 dark:text-emerald-400"
                            : "bg-amber-500/10 text-amber-600 dark:bg-amber-500/20 dark:text-amber-400"
                        }`}
                      >
                        {isCompleted ? "Completed" : "In Progress"}
                      </span>
                    </div>

                    <div className="text-xs font-medium text-zinc-600 dark:text-zinc-300">
                      {session.role}
                    </div>

                    <div className="mt-1 flex flex-wrap gap-1.5 text-[11px] text-zinc-500">
                      <span>{session.interview_stage || "Round 1"}</span>
                      <span>•</span>
                      <span>{session.interview_nature || "Technical"}</span>
                    </div>

                    {isCompleted && session.overall_score && (
                      <div className="mt-3 flex items-center gap-3 rounded-xl bg-zinc-50 p-2.5 dark:bg-zinc-800/40">
                        <div>
                          <div className="text-[10px] text-zinc-400">Readiness Score</div>
                          <div className="text-base font-bold text-zinc-900 dark:text-zinc-100">
                            {session.overall_score.toFixed(1)} / 10
                          </div>
                        </div>
                        {session.readiness_tier && (
                          <div className="ml-auto rounded bg-zinc-200/70 px-2 py-0.5 text-[10px] font-semibold text-zinc-700 dark:bg-zinc-700 dark:text-zinc-300">
                            {session.readiness_tier}
                          </div>
                        )}
                      </div>
                    )}
                  </div>

                  <div className="mt-4 pt-3 border-t border-zinc-100 dark:border-zinc-800 flex items-center justify-between">
                    <span className="text-[10px] text-zinc-400 flex items-center gap-1">
                      <Clock className="size-3" />
                      <span>{dateStr}</span>
                    </span>

                    {isCompleted ? (
                      <button
                        type="button"
                        onClick={() => onOpenReport(session._id)}
                        className="inline-flex items-center gap-1 text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline"
                      >
                        <span>View Report</span>
                        <ChevronRight className="size-3.5" />
                      </button>
                    ) : (
                      <button
                        type="button"
                        onClick={() => onResumeInterview(session._id)}
                        className="inline-flex items-center gap-1 rounded-lg bg-zinc-900 px-3 py-1 text-xs font-semibold text-white dark:bg-zinc-100 dark:text-zinc-900"
                      >
                        <Play className="size-3" />
                        <span>Resume</span>
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
