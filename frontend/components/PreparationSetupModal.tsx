"use client";

import React, { useState } from "react";
import { useAuth } from "@/lib/auth-context";
import { api, InterviewProfile } from "@/lib/api";
import {
  X,
  Upload,
  Sparkles,
  ChevronRight,
  ChevronLeft,
  AlertCircle,
  Loader2,
  ShieldCheck,
} from "lucide-react";

interface PreparationSetupModalProps {
  isOpen: boolean;
  onClose: () => void;
  onInterviewCreated: (interviewId: string) => void;
  initialPreset?: {
    company: string;
    role: string;
    stage: string;
    nature: string;
  } | null;
}

const POPULAR_COMPANIES = ["Stripe", "Google", "Meta", "Amazon", "OpenAI", "Anthropic"];

const INTERVIEW_STAGES = [
  "Technical Round 1",
  "Screening",
  "System Design",
  "Behavioral",
  "Hiring Manager",
  "Final Round",
];

const INTERVIEW_NATURES = [
  { id: "ML/AI Technical", label: "ML/AI Technical", desc: "Transformers, RAG, embeddings, evaluation metrics" },
  { id: "System Design", label: "System Design", desc: "Distributed systems, scalability, trade-offs, storage" },
  { id: "Coding", label: "Coding / Algorithms", desc: "Data structures, problem-solving, complexity, edge-cases" },
  { id: "Behavioral", label: "Behavioral / Leadership", desc: "STAR method, ownership, collaboration, handling ambiguity" },
];

export function PreparationSetupModal({
  isOpen,
  onClose,
  onInterviewCreated,
  initialPreset,
}: PreparationSetupModalProps) {
  const { token } = useAuth();
  const [step, setStep] = useState<number>(1);

  // Form State
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [candidateId, setCandidateId] = useState<string>("");

  const [company, setCompany] = useState<string>(initialPreset?.company || "Stripe");
  const [role, setRole] = useState<string>(initialPreset?.role || "Senior Backend Engineer");
  const [jobDescription, setJobDescription] = useState<string>("");

  const [stage, setStage] = useState<string>(initialPreset?.stage || "Technical Round 1");
  const [nature, setNature] = useState<string>(initialPreset?.nature || "Coding");
  const [numQuestions, setNumQuestions] = useState<number>(3);
  const [numFollowups, setNumFollowups] = useState<number>(1);

  // Profile Preview State
  const [profilePreview, setProfilePreview] = useState<InterviewProfile | null>(null);
  const [isPreviewLoading, setIsPreviewLoading] = useState<boolean>(false);

  // Async submission states
  const [isParsingResume, setIsParsingResume] = useState<boolean>(false);
  const [isCreatingSession, setIsCreatingSession] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  // Handle Resume Parsing
  const handleUploadResume = async () => {
    if (!resumeFile && !candidateId) {
      setError("Please select a PDF resume file to upload");
      return;
    }

    setError(null);
    setIsParsingResume(true);

    try {
      if (resumeFile) {
        const res = await api.uploadResume(resumeFile, role, token);
        setCandidateId(res.candidate_id);
      }
      setStep(2);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to parse resume PDF. Please check the file format.";
      setError(msg);
    } finally {
      setIsParsingResume(false);
    }
  };

  // Quick fallback to use sample profile if candidate has no PDF handy
  const handleUseSampleProfile = async () => {
    setError(null);
    setIsParsingResume(true);
    try {
      setCandidateId("sample_candidate_id");
      setStep(2);
    } finally {
      setIsParsingResume(false);
    }
  };

  // Fetch Live Interview Profile Preview
  const handleFetchPreview = async () => {
    setError(null);
    setIsPreviewLoading(true);

    try {
      const preview = await api.previewProfile(
        {
          candidate_id: candidateId || "sample_candidate_id",
          role,
          company,
          job_description: jobDescription,
          interview_stage: stage,
          interview_nature: nature,
          number_of_questions: numQuestions,
          number_of_followups: numFollowups,
        },
        token
      );
      setProfilePreview(preview);
      setStep(4);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to generate Interview Profile preview";
      setError(msg);
      // Still proceed to step 4 with defaults
      setStep(4);
    } finally {
      setIsPreviewLoading(false);
    }
  };

  // Launch Session
  const handleLaunchSession = async () => {
    setError(null);
    setIsCreatingSession(true);

    try {
      const res = await api.createInterview(
        {
          candidate_id: candidateId || "sample_candidate_id",
          role,
          company,
          job_description: jobDescription,
          interview_stage: stage,
          interview_nature: nature,
          number_of_questions: numQuestions,
          number_of_followups: numFollowups,
        },
        token
      );

      onInterviewCreated(res.interview_id);
      onClose();
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to create preparation session";
      setError(msg);
    } finally {
      setIsCreatingSession(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-2xl rounded-2xl border border-zinc-200 bg-white p-6 shadow-2xl dark:border-zinc-800 dark:bg-zinc-900 sm:p-8 max-h-[92vh] overflow-y-auto">
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute right-4 top-4 rounded-lg p-1.5 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-600 dark:hover:bg-zinc-800 dark:hover:text-zinc-200"
        >
          <X className="size-5" />
        </button>

        {/* Header & Step progress */}
        <div className="mb-6">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
              Step {step} of 4
            </span>
            <span className="text-zinc-300 dark:text-zinc-700">•</span>
            <span className="text-xs text-zinc-500">
              {step === 1 && "Resume Intake"}
              {step === 2 && "Target Company & JD"}
              {step === 3 && "Round Calibration"}
              {step === 4 && "Interview Profile Preview"}
            </span>
          </div>
          <h2 className="text-xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
            {step === 1 && "Upload your resume"}
            {step === 2 && "Select company & opportunity"}
            {step === 3 && "Calibrate interview stage & nature"}
            {step === 4 && "Review tailored Interview Profile"}
          </h2>

          {/* Progress bar */}
          <div className="mt-3 h-1.5 w-full rounded-full bg-zinc-100 dark:bg-zinc-800 overflow-hidden">
            <div
              className="h-full bg-zinc-900 dark:bg-zinc-100 transition-all duration-300 rounded-full"
              style={{ width: `${(step / 4) * 100}%` }}
            />
          </div>
        </div>

        {error && (
          <div className="mb-4 flex items-center gap-2 rounded-lg border border-red-500/20 bg-red-500/10 p-3 text-xs text-red-600 dark:text-red-400">
            <AlertCircle className="size-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* STEP 1: RESUME INTAKE */}
        {step === 1 && (
          <div className="space-y-4">
            <p className="text-xs text-zinc-500 dark:text-zinc-400">
              Bespoke parses your real technical competencies, projects, and domain depth to generate
              personalized questions and grounded preparation reports.
            </p>

            <div className="rounded-xl border-2 border-dashed border-zinc-200 p-8 text-center hover:border-zinc-400 dark:border-zinc-800 dark:hover:border-zinc-600 transition-colors">
              <input
                type="file"
                id="resume-input"
                accept=".pdf"
                className="hidden"
                onChange={(e) => {
                  if (e.target.files && e.target.files[0]) {
                    setResumeFile(e.target.files[0]);
                  }
                }}
              />
              <label htmlFor="resume-input" className="cursor-pointer flex flex-col items-center">
                <div className="mb-3 flex size-12 items-center justify-center rounded-xl bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300">
                  <Upload className="size-6" />
                </div>
                <span className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
                  {resumeFile ? resumeFile.name : "Click to select or drag PDF resume"}
                </span>
                <span className="mt-1 text-xs text-zinc-500">Only PDF files up to 10MB</span>
              </label>
            </div>

            <div className="flex items-center justify-between pt-2">
              <button
                type="button"
                onClick={handleUseSampleProfile}
                disabled={isParsingResume}
                className="text-xs text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-300 underline"
              >
                Or use sample Senior Engineer profile
              </button>

              <button
                type="button"
                disabled={isParsingResume || (!resumeFile && !candidateId)}
                onClick={handleUploadResume}
                className="inline-flex items-center gap-2 rounded-lg bg-zinc-900 px-5 py-2.5 text-xs font-semibold text-white shadow hover:bg-zinc-800 disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200 transition-all"
              >
                {isParsingResume ? (
                  <>
                    <Loader2 className="size-3.5 animate-spin" />
                    <span>Analyzing Resume...</span>
                  </>
                ) : (
                  <>
                    <span>Next: Target Opportunity</span>
                    <ChevronRight className="size-4" />
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {/* STEP 2: TARGET COMPANY & JD */}
        {step === 2 && (
          <div className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-1.5">
                Target Company
              </label>
              <div className="flex flex-wrap gap-2 mb-2">
                {POPULAR_COMPANIES.map((c) => (
                  <button
                    key={c}
                    type="button"
                    onClick={() => setCompany(c)}
                    className={`rounded-lg px-3 py-1.5 text-xs font-medium border transition-all ${
                      company.toLowerCase() === c.toLowerCase()
                        ? "border-zinc-900 bg-zinc-900 text-white dark:border-zinc-100 dark:bg-zinc-100 dark:text-zinc-900"
                        : "border-zinc-200 bg-zinc-50 text-zinc-700 hover:bg-zinc-100 dark:border-zinc-800 dark:bg-zinc-800/60 dark:text-zinc-300"
                    }`}
                  >
                    {c}
                  </button>
                ))}
              </div>
              <input
                type="text"
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                placeholder="Or enter any company name (e.g. Databricks, Snowflake)"
                className="w-full rounded-lg border border-zinc-300 bg-white px-3 py-2 text-sm text-zinc-900 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-100"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-1.5">
                Target Role
              </label>
              <input
                type="text"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                placeholder="e.g. Senior Backend Engineer, GenAI Engineer"
                className="w-full rounded-lg border border-zinc-300 bg-white px-3 py-2 text-sm text-zinc-900 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-100"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-1.5">
                Job Description (Optional but recommended)
              </label>
              <textarea
                rows={3}
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste requirements, tech stack, or JD excerpt to align questions..."
                className="w-full rounded-lg border border-zinc-300 bg-white px-3 py-2 text-xs text-zinc-900 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-100"
              />
            </div>

            <div className="flex items-center justify-between pt-3">
              <button
                type="button"
                onClick={() => setStep(1)}
                className="inline-flex items-center gap-1.5 text-xs font-medium text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-300"
              >
                <ChevronLeft className="size-4" />
                <span>Back</span>
              </button>

              <button
                type="button"
                onClick={() => setStep(3)}
                className="inline-flex items-center gap-2 rounded-lg bg-zinc-900 px-5 py-2.5 text-xs font-semibold text-white shadow hover:bg-zinc-800 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200 transition-all"
              >
                <span>Next: Round Calibration</span>
                <ChevronRight className="size-4" />
              </button>
            </div>
          </div>
        )}

        {/* STEP 3: ROUND CALIBRATION */}
        {step === 3 && (
          <div className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-2">
                Interview Stage
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {INTERVIEW_STAGES.map((s) => (
                  <button
                    key={s}
                    type="button"
                    onClick={() => setStage(s)}
                    className={`rounded-lg p-2.5 text-left border text-xs font-medium transition-all ${
                      stage === s
                        ? "border-zinc-900 bg-zinc-900 text-white dark:border-zinc-100 dark:bg-zinc-100 dark:text-zinc-900 shadow-sm"
                        : "border-zinc-200 bg-zinc-50 hover:bg-zinc-100 text-zinc-800 dark:border-zinc-800 dark:bg-zinc-800/60 dark:text-zinc-200"
                    }`}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-2">
                Round Nature
              </label>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {INTERVIEW_NATURES.map((n) => (
                  <button
                    key={n.id}
                    type="button"
                    onClick={() => setNature(n.id)}
                    className={`rounded-xl p-3 text-left border transition-all ${
                      nature === n.id
                        ? "border-zinc-900 bg-zinc-900 text-white dark:border-zinc-100 dark:bg-zinc-100 dark:text-zinc-900 shadow-sm"
                        : "border-zinc-200 bg-zinc-50 hover:bg-zinc-100 text-zinc-800 dark:border-zinc-800 dark:bg-zinc-800/60 dark:text-zinc-200"
                    }`}
                  >
                    <div className="font-semibold text-xs">{n.label}</div>
                    <div
                      className={`text-[10px] mt-0.5 ${
                        nature === n.id ? "text-zinc-200 dark:text-zinc-700" : "text-zinc-500 dark:text-zinc-400"
                      }`}
                    >
                      {n.desc}
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Questions & Followups sliders */}
            <div className="grid grid-cols-2 gap-4 pt-1">
              <div className="rounded-xl border border-zinc-200 p-3.5 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800/40">
                <div className="flex justify-between items-center mb-1.5">
                  <span className="text-xs font-medium text-zinc-700 dark:text-zinc-300">
                    Primary Questions
                  </span>
                  <span className="text-xs font-bold text-zinc-900 dark:text-zinc-100">
                    {numQuestions}
                  </span>
                </div>
                <input
                  type="range"
                  min={1}
                  max={5}
                  value={numQuestions}
                  onChange={(e) => setNumQuestions(parseInt(e.target.value))}
                  className="w-full accent-zinc-900 dark:accent-zinc-100"
                />
                <span className="text-[10px] text-zinc-400">1 to 5 questions per run</span>
              </div>

              <div className="rounded-xl border border-zinc-200 p-3.5 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800/40">
                <div className="flex justify-between items-center mb-1.5">
                  <span className="text-xs font-medium text-zinc-700 dark:text-zinc-300">
                    Follow-ups / Question
                  </span>
                  <span className="text-xs font-bold text-zinc-900 dark:text-zinc-100">
                    {numFollowups}
                  </span>
                </div>
                <input
                  type="range"
                  min={0}
                  max={3}
                  value={numFollowups}
                  onChange={(e) => setNumFollowups(parseInt(e.target.value))}
                  className="w-full accent-zinc-900 dark:accent-zinc-100"
                />
                <span className="text-[10px] text-zinc-400">Adaptive depth control</span>
              </div>
            </div>

            <div className="flex items-center justify-between pt-3">
              <button
                type="button"
                onClick={() => setStep(2)}
                className="inline-flex items-center gap-1.5 text-xs font-medium text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-300"
              >
                <ChevronLeft className="size-4" />
                <span>Back</span>
              </button>

              <button
                type="button"
                disabled={isPreviewLoading}
                onClick={handleFetchPreview}
                className="inline-flex items-center gap-2 rounded-lg bg-zinc-900 px-5 py-2.5 text-xs font-semibold text-white shadow hover:bg-zinc-800 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200 transition-all"
              >
                {isPreviewLoading ? (
                  <>
                    <Loader2 className="size-3.5 animate-spin" />
                    <span>Synthesizing Profile...</span>
                  </>
                ) : (
                  <>
                    <span>Preview Interview Profile</span>
                    <ChevronRight className="size-4" />
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {/* STEP 4: INTERVIEW PROFILE PREVIEW */}
        {step === 4 && (
          <div className="space-y-4">
            <div className="rounded-xl border border-zinc-200 bg-zinc-50/80 p-4 dark:border-zinc-800 dark:bg-zinc-800/40">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-sm text-zinc-900 dark:text-zinc-100">
                    {company}
                  </span>
                  <span className="rounded-md bg-zinc-200 px-2 py-0.5 text-[10px] font-semibold text-zinc-700 dark:bg-zinc-700 dark:text-zinc-300">
                    {stage}
                  </span>
                  <span className="rounded-md bg-emerald-500/10 px-2 py-0.5 text-[10px] font-semibold text-emerald-600 dark:bg-emerald-500/20 dark:text-emerald-400">
                    {nature}
                  </span>
                </div>
                <span className="text-[11px] text-zinc-400">
                  {numQuestions} questions • {numFollowups} max follow-ups
                </span>
              </div>

              {/* Company Insights */}
              {profilePreview?.company_insights && profilePreview.company_insights.length > 0 && (
                <div className="mb-3">
                  <span className="text-[11px] font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">
                    Company Intelligence
                  </span>
                  <ul className="mt-1 space-y-1 text-xs text-zinc-700 dark:text-zinc-300">
                    {profilePreview.company_insights.map((ins, i) => (
                      <li key={i} className="flex items-start gap-1.5">
                        <Sparkles className="size-3.5 text-amber-500 shrink-0 mt-0.5" />
                        <span>{ins}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Evaluation Rubric Dimensions */}
              {profilePreview?.rubric_criteria && profilePreview.rubric_criteria.length > 0 && (
                <div className="mb-3">
                  <span className="text-[11px] font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">
                    Evaluation Dimensions
                  </span>
                  <div className="mt-1.5 flex flex-wrap gap-1.5">
                    {profilePreview.rubric_criteria.map((crit, i) => (
                      <span
                        key={i}
                        className="inline-flex items-center gap-1 rounded-md bg-white px-2 py-1 text-[11px] text-zinc-700 shadow-sm ring-1 ring-zinc-200 dark:bg-zinc-800 dark:text-zinc-300 dark:ring-zinc-700"
                      >
                        <ShieldCheck className="size-3 text-emerald-500" />
                        <span>{crit}</span>
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Evidence citations */}
              {profilePreview?.supporting_evidence && profilePreview.supporting_evidence.length > 0 && (
                <div>
                  <span className="text-[11px] font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">
                    Grounded Evidence Sources ({profilePreview.supporting_evidence.length})
                  </span>
                  <div className="mt-1 flex flex-wrap gap-1.5">
                    {profilePreview.supporting_evidence.map((ev, i) => (
                      <span
                        key={i}
                        className="rounded bg-zinc-200/60 px-2 py-0.5 text-[10px] text-zinc-600 dark:bg-zinc-700/60 dark:text-zinc-400"
                      >
                        {ev.title} ({Math.round(ev.confidence * 100)}% trust)
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className="flex items-center justify-between pt-3">
              <button
                type="button"
                onClick={() => setStep(3)}
                className="inline-flex items-center gap-1.5 text-xs font-medium text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-300"
              >
                <ChevronLeft className="size-4" />
                <span>Adjust Settings</span>
              </button>

              <button
                type="button"
                disabled={isCreatingSession}
                onClick={handleLaunchSession}
                className="inline-flex items-center gap-2 rounded-lg bg-emerald-600 px-6 py-2.5 text-xs font-bold text-white shadow hover:bg-emerald-500 disabled:opacity-50 transition-all active:scale-[0.98]"
              >
                {isCreatingSession ? (
                  <>
                    <Loader2 className="size-4 animate-spin" />
                    <span>Orchestrating Interview Engine...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="size-4" />
                    <span>Launch Tailored Interview</span>
                  </>
                )}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
