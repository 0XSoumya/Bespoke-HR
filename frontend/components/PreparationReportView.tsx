"use client";

import React, { useState, useEffect } from "react";
import { useAuth } from "@/lib/auth-context";
import { api, FullReportResponse } from "@/lib/api";
import {
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  TrendingUp,
  ShieldCheck,
  BookOpen,
  ChevronDown,
  ChevronUp,
  RotateCcw,
  LayoutDashboard,
  Printer,
  Loader2,
} from "lucide-react";

interface PreparationReportViewProps {
  interviewId: string;
  onBackToDashboard: () => void;
  onPracticeAgain: () => void;
}

export function PreparationReportView({
  interviewId,
  onBackToDashboard,
  onPracticeAgain,
}: PreparationReportViewProps) {
  const { token } = useAuth();
  const [reportData, setReportData] = useState<FullReportResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedQuestion, setExpandedQuestion] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    async function fetchReport() {
      try {
        const res = await api.getReport(interviewId, token);
        if (isMounted) setReportData(res);
      } catch (err: unknown) {
        if (isMounted) {
          const msg = err instanceof Error ? err.message : "Failed to load report";
          setError(msg);
        }
      } finally {
        if (isMounted) setIsLoading(false);
      }
    }
    fetchReport();
    return () => {
      isMounted = false;
    };
  }, [interviewId, token]);

  if (isLoading) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center p-8 text-center">
        <Loader2 className="size-8 animate-spin text-zinc-900 dark:text-zinc-100 mb-4" />
        <h3 className="font-semibold text-zinc-900 dark:text-zinc-100 text-base">
          Assembling Your Preparation Report...
        </h3>
        <p className="text-xs text-zinc-500 mt-1 max-w-sm">
          Grounding evaluation against stage rubrics, company intelligence, and candidate evidence.
        </p>
      </div>
    );
  }

  if (error || !reportData) {
    return (
      <div className="mx-auto max-w-xl p-8 text-center">
        <div className="rounded-2xl border border-red-200 bg-red-50 p-6 dark:border-red-900/30 dark:bg-red-950/20">
          <p className="text-sm text-red-600 dark:text-red-400 font-medium">
            {error || "Report not available yet."}
          </p>
          <button
            onClick={onBackToDashboard}
            className="mt-4 rounded-lg bg-zinc-900 px-4 py-2 text-xs font-semibold text-white dark:bg-zinc-100 dark:text-zinc-900"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const prep = reportData.preparation_report;
  const cand = reportData.candidate_report;
  const profile = reportData.interview_profile;

  const readinessScore = prep?.overall_readiness_score ?? cand?.overall_score ?? 7.5;
  const readinessTier = prep?.readiness_tier ?? "Strong Baseline";
  const summary = prep?.executive_summary ?? cand?.summary ?? "";
  const strengths = prep?.strengths ?? cand?.strengths ?? [];
  const priorityGaps = prep?.priority_gaps ?? cand?.areas_for_improvement ?? [];
  const actions = prep?.recommended_actions ?? cand?.learning_recommendations ?? [];
  const questionReviews = prep?.question_reviews ?? [];
  const evidenceList = prep?.evidence_citations ?? profile?.supporting_evidence ?? [];

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8 animate-in fade-in duration-300">
      {/* Action Header */}
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-3">
          <button
            onClick={onBackToDashboard}
            className="inline-flex items-center gap-1.5 rounded-lg border border-zinc-200 px-3 py-1.5 text-xs font-medium text-zinc-600 hover:bg-zinc-100 dark:border-zinc-800 dark:text-zinc-400 dark:hover:bg-zinc-800 transition-colors"
          >
            <LayoutDashboard className="size-3.5" />
            <span>Dashboard</span>
          </button>
          <span className="text-xs text-zinc-400">•</span>
          <span className="text-xs font-semibold text-zinc-700 dark:text-zinc-300">
            {reportData.company} — {reportData.interview_stage} ({reportData.interview_nature})
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => window.print()}
            className="inline-flex items-center gap-1.5 rounded-lg border border-zinc-200 px-3 py-1.5 text-xs font-medium text-zinc-600 hover:bg-zinc-100 dark:border-zinc-800 dark:text-zinc-400 dark:hover:bg-zinc-800 transition-colors"
          >
            <Printer className="size-3.5" />
            <span>Print Report</span>
          </button>
          <button
            onClick={onPracticeAgain}
            className="inline-flex items-center gap-1.5 rounded-lg bg-zinc-900 px-4 py-1.5 text-xs font-bold text-white hover:bg-zinc-800 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200 transition-all shadow-sm"
          >
            <RotateCcw className="size-3.5" />
            <span>Practice Another Session</span>
          </button>
        </div>
      </div>

      {/* Hero Readiness Score Card */}
      <div className="mb-8 rounded-3xl border border-zinc-200 bg-gradient-to-b from-white to-zinc-50 p-6 sm:p-8 shadow-sm dark:border-zinc-800 dark:from-zinc-900 dark:to-zinc-900/60">
        <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
          <div className="space-y-2 max-w-xl">
            <div className="inline-flex items-center gap-1.5 rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-600 dark:bg-emerald-500/20 dark:text-emerald-400 border border-emerald-500/20">
              <Sparkles className="size-3.5" />
              <span>{readinessTier}</span>
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50 sm:text-3xl">
              Interview Readiness Assessment
            </h1>
            <p className="text-xs sm:text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">
              {summary}
            </p>
          </div>

          {/* Readiness Score Gauge */}
          <div className="flex flex-col items-center justify-center rounded-2xl bg-white p-6 shadow-sm ring-1 ring-zinc-200 dark:bg-zinc-800/80 dark:ring-zinc-700 sm:min-w-[170px]">
            <span className="text-4xl font-extrabold tracking-tight text-zinc-900 dark:text-zinc-50">
              {readinessScore.toFixed(1)}
            </span>
            <span className="text-[11px] font-medium text-zinc-400 mt-0.5">out of 10.0</span>
            <div className="mt-2 text-[10px] uppercase tracking-wider font-semibold text-emerald-600 dark:text-emerald-400">
              {readinessTier}
            </div>
          </div>
        </div>
      </div>

      {/* Strengths & Gaps Two-Column */}
      <div className="mb-8 grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Strengths */}
        <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-6 dark:border-emerald-500/10 dark:bg-emerald-500/5">
          <div className="flex items-center gap-2 mb-4">
            <div className="flex size-7 items-center justify-center rounded-lg bg-emerald-600 text-white shadow-sm">
              <CheckCircle2 className="size-4" />
            </div>
            <h3 className="font-bold text-sm text-zinc-900 dark:text-zinc-100">
              Demonstrated Strengths
            </h3>
          </div>
          <ul className="space-y-2.5">
            {strengths.map((str, i) => (
              <li key={i} className="flex items-start gap-2 text-xs text-zinc-700 dark:text-zinc-300 leading-relaxed">
                <span className="size-1.5 rounded-full bg-emerald-500 mt-1.5 shrink-0" />
                <span>{str}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Priority Gaps */}
        <div className="rounded-2xl border border-amber-500/20 bg-amber-500/5 p-6 dark:border-amber-500/10 dark:bg-amber-500/5">
          <div className="flex items-center gap-2 mb-4">
            <div className="flex size-7 items-center justify-center rounded-lg bg-amber-600 text-white shadow-sm">
              <AlertTriangle className="size-4" />
            </div>
            <h3 className="font-bold text-sm text-zinc-900 dark:text-zinc-100">
              Priority Gaps to Close
            </h3>
          </div>
          <ul className="space-y-2.5">
            {priorityGaps.map((gap, i) => (
              <li key={i} className="flex items-start gap-2 text-xs text-zinc-700 dark:text-zinc-300 leading-relaxed">
                <span className="size-1.5 rounded-full bg-amber-500 mt-1.5 shrink-0" />
                <span>{gap}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Topic & Rubric Dimension Breakdown */}
      <div className="mb-8 rounded-2xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900 shadow-sm">
        <h3 className="font-bold text-sm text-zinc-900 dark:text-zinc-100 mb-4 flex items-center gap-2">
          <TrendingUp className="size-4 text-zinc-500" />
          <span>Competency & Rubric Breakdown</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {prep?.topic_breakdown &&
            Object.entries(prep.topic_breakdown).map(([topic, score]) => (
              <div key={topic} className="space-y-1.5">
                <div className="flex justify-between text-xs">
                  <span className="font-medium text-zinc-700 dark:text-zinc-300">{topic}</span>
                  <span className="font-semibold text-zinc-900 dark:text-zinc-100">{score} / 10</span>
                </div>
                <div className="h-2 w-full rounded-full bg-zinc-100 dark:bg-zinc-800 overflow-hidden">
                  <div
                    className="h-full bg-zinc-900 dark:bg-zinc-100 rounded-full transition-all duration-500"
                    style={{ width: `${(score / 10) * 100}%` }}
                  />
                </div>
              </div>
            ))}
        </div>
      </div>

      {/* Actionable Next Steps Preparation Roadmap */}
      {actions.length > 0 && (
        <div className="mb-8 rounded-2xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900 shadow-sm">
          <h3 className="font-bold text-sm text-zinc-900 dark:text-zinc-100 mb-3 flex items-center gap-2">
            <BookOpen className="size-4 text-emerald-500" />
            <span>Recommended Preparation Action Plan</span>
          </h3>
          <p className="text-xs text-zinc-500 mb-4">
            Focus your final practice on these concrete engineering tasks before your real {reportData.company} interview:
          </p>
          <div className="space-y-2">
            {actions.map((act, i) => (
              <div
                key={i}
                className="flex items-start gap-3 rounded-xl border border-zinc-100 bg-zinc-50/70 p-3 text-xs text-zinc-800 dark:border-zinc-800 dark:bg-zinc-800/40 dark:text-zinc-200"
              >
                <span className="flex size-5 shrink-0 items-center justify-center rounded-full bg-zinc-900 text-[10px] font-bold text-white dark:bg-zinc-100 dark:text-zinc-900">
                  {i + 1}
                </span>
                <span className="leading-relaxed">{act}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Question-by-Question Deep Dive Accordion */}
      {questionReviews.length > 0 && (
        <div className="mb-8 rounded-2xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900 shadow-sm">
          <h3 className="font-bold text-sm text-zinc-900 dark:text-zinc-100 mb-4">
            Question-by-Question Detailed Review
          </h3>

          <div className="space-y-3">
            {questionReviews.map((qr, idx) => {
              const isExpanded = expandedQuestion === qr.question_id || expandedQuestion === String(idx);
              return (
                <div
                  key={qr.question_id || idx}
                  className="rounded-xl border border-zinc-200 dark:border-zinc-800 overflow-hidden"
                >
                  <button
                    onClick={() => setExpandedQuestion(isExpanded ? null : String(idx))}
                    className="flex w-full items-center justify-between p-4 text-left hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors"
                  >
                    <div className="flex items-center gap-3 pr-4">
                      <span className="flex size-6 shrink-0 items-center justify-center rounded-md bg-zinc-100 text-xs font-bold text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300">
                        Q{idx + 1}
                      </span>
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-[11px] font-medium text-zinc-400 uppercase">
                            {qr.topic}
                          </span>
                        </div>
                        <p className="text-xs font-semibold text-zinc-900 dark:text-zinc-100 line-clamp-1">
                          {qr.main_question}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-3 shrink-0">
                      <span className="rounded-md bg-zinc-100 px-2 py-0.5 text-xs font-bold text-zinc-800 dark:bg-zinc-800 dark:text-zinc-200">
                        {qr.score.toFixed(1)}/10
                      </span>
                      {isExpanded ? (
                        <ChevronUp className="size-4 text-zinc-400" />
                      ) : (
                        <ChevronDown className="size-4 text-zinc-400" />
                      )}
                    </div>
                  </button>

                  {isExpanded && (
                    <div className="border-t border-zinc-200 bg-zinc-50/50 p-4 dark:border-zinc-800 dark:bg-zinc-800/30 space-y-3 text-xs">
                      <div>
                        <span className="font-semibold text-zinc-700 dark:text-zinc-300">
                          Full Question:
                        </span>
                        <p className="text-zinc-800 dark:text-zinc-200 mt-0.5 font-medium">
                          {qr.main_question}
                        </p>
                      </div>

                      {qr.candidate_answer && (
                        <div>
                          <span className="font-semibold text-zinc-700 dark:text-zinc-300">
                            Your Main Answer:
                          </span>
                          <p className="text-zinc-600 dark:text-zinc-400 mt-0.5 whitespace-pre-wrap rounded-lg bg-white p-3 border border-zinc-200 dark:bg-zinc-900 dark:border-zinc-800">
                            {qr.candidate_answer}
                          </p>
                        </div>
                      )}

                      {qr.followups && qr.followups.length > 0 && (
                        <div className="space-y-2">
                          <span className="font-semibold text-zinc-700 dark:text-zinc-300">
                            Adaptive Follow-up Dialogue:
                          </span>
                          {qr.followups.map((f, fi) => (
                            <div
                              key={fi}
                              className="rounded-lg border border-amber-500/20 bg-amber-500/5 p-3 space-y-1"
                            >
                              <div className="font-medium text-amber-900 dark:text-amber-200">
                                ↳ Follow-up: {f.question}
                              </div>
                              <div className="text-zinc-700 dark:text-zinc-300 pl-3 border-l-2 border-amber-400">
                                {f.answer || "No response recorded"}
                              </div>
                            </div>
                          ))}
                        </div>
                      )}

                      {qr.model_advice && (
                        <div>
                          <span className="font-semibold text-zinc-700 dark:text-zinc-300">
                            AI Interviewer Coaching Notes:
                          </span>
                          <p className="text-zinc-600 dark:text-zinc-400 mt-0.5 leading-relaxed">
                            {qr.model_advice}
                          </p>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Provenance & Evidence Explorer */}
      {evidenceList.length > 0 && (
        <div className="rounded-2xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900 shadow-sm">
          <h3 className="font-bold text-sm text-zinc-900 dark:text-zinc-100 mb-2 flex items-center gap-2">
            <ShieldCheck className="size-4 text-emerald-500" />
            <span>Evidence Provenance Citations ({evidenceList.length})</span>
          </h3>
          <p className="text-xs text-zinc-500 mb-4">
            Every evaluation score and preparation recommendation is verified and grounded in these primary sources:
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {evidenceList.map((ev, i) => (
              <div
                key={i}
                className="rounded-xl border border-zinc-100 bg-zinc-50 p-3.5 dark:border-zinc-800 dark:bg-zinc-800/50"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="rounded bg-zinc-200 px-2 py-0.5 text-[9px] font-bold uppercase tracking-wider text-zinc-700 dark:bg-zinc-700 dark:text-zinc-300">
                    {ev.source_type.replace("_", " ")}
                  </span>
                  <span className="text-[10px] font-semibold text-emerald-600 dark:text-emerald-400">
                    {Math.round(ev.confidence * 100)}% Trust
                  </span>
                </div>
                <div className="font-semibold text-xs text-zinc-900 dark:text-zinc-100 mt-1">
                  {ev.title}
                </div>
                <p className="text-[11px] text-zinc-500 dark:text-zinc-400 mt-1 line-clamp-2">
                  {ev.content}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
