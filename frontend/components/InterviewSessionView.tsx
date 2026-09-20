"use client";

import React, { useState, useEffect, useRef } from "react";
import { useAuth } from "@/lib/auth-context";
import { api, QuestionRecord, InterviewSessionData } from "@/lib/api";
import {
  Sparkles,
  Send,
  Loader2,
  HelpCircle,
  Code,
  AlertCircle,
} from "lucide-react";

interface InterviewSessionViewProps {
  interviewId: string;
  onInterviewCompleted: (interviewId: string) => void;
  onExit: () => void;
}

export function InterviewSessionView({
  interviewId,
  onInterviewCompleted,
  onExit,
}: InterviewSessionViewProps) {
  const { token } = useAuth();
  const [interview, setInterview] = useState<InterviewSessionData | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<QuestionRecord | null>(null);
  const [answer, setAnswer] = useState<string>("");
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [submissionStatus, setSubmissionStatus] = useState<string>("");
  const [isCodeMode, setIsCodeMode] = useState<boolean>(false);
  const [showHint, setShowHint] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationHistory, setConversationHistory] = useState<
    Array<{ type: "main_q" | "followup_q" | "answer"; text: string; topic?: string }>
  >([]);

  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Load initial interview state & question
  useEffect(() => {
    let isMounted = true;

    async function loadData() {
      try {
        const intData = await api.getInterview(interviewId, token);
        if (!isMounted) return;
        setInterview(intData);

        // If interview is already completed, go directly to report
        if (intData.status === "completed" || intData.report) {
          onInterviewCompleted(interviewId);
          return;
        }

        const qData = await api.getCurrentQuestion(interviewId, token);
        if (!isMounted) return;
        setCurrentQuestion(qData);

        if (qData) {
          setConversationHistory([
            { type: "main_q", text: qData.main_question, topic: qData.topic },
          ]);
        }
      } catch (err: unknown) {
        if (isMounted) {
          const msg = err instanceof Error ? err.message : "Failed to load interview";
          setError(msg);
        }
      }
    }

    loadData();
    return () => {
      isMounted = false;
    };
  }, [interviewId, token, onInterviewCompleted]);

  const handleSubmitAnswer = async () => {
    if (!answer.trim() || isSubmitting) return;

    setError(null);
    setIsSubmitting(true);
    setSubmissionStatus("Analyzing candidate response...");

    const submittedText = answer.trim();

    // Optimistically push answer to conversation stream
    setConversationHistory((prev) => [
      ...prev,
      { type: "answer", text: submittedText },
    ]);
    setAnswer("");

    try {
      setSubmissionStatus("Evaluating against stage rubric & generating follow-up...");
      const res = await api.submitAnswer(interviewId, submittedText, token);

      if (res.report_available || res.status === "completed") {
        setSubmissionStatus("Session complete! Generating evidence-grounded report...");
        setTimeout(() => {
          onInterviewCompleted(interviewId);
        }, 1200);
        return;
      }

      if (res.pending_followup && res.current_question) {
        const followups = res.current_question.followups || [];
        const latestFollowup = followups[followups.length - 1];
        if (latestFollowup) {
          setConversationHistory((prev) => [
            ...prev,
            { type: "followup_q", text: latestFollowup.question },
          ]);
        }
      } else if (res.current_question) {
        // Advanced to a new question!
        setCurrentQuestion(res.current_question);
        setConversationHistory([
          {
            type: "main_q",
            text: res.current_question.main_question,
            topic: res.current_question.topic,
          },
        ]);
        setShowHint(false);
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to process answer submission";
      setError(msg);
    } finally {
      setIsSubmitting(false);
      setSubmissionStatus("");
      if (textareaRef.current) {
        textareaRef.current.focus();
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      handleSubmitAnswer();
    }
  };

  const company = interview?.company || interview?.interview_profile?.company || "Target Company";
  const role = interview?.role || interview?.interview_profile?.target_role || "Candidate";
  const stage = interview?.interview_profile?.interview_stage || "Technical Round 1";
  const nature = interview?.interview_profile?.interview_nature || "Coding";
  const totalQuestions = interview?.number_of_questions || 3;
  const currentQIndex = interview?.session?.current_question_index ?? 0;

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8 animate-in fade-in duration-300">
      {/* Top Cockpit Header */}
      <div className="mb-6 rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-3">
            <div className="flex size-11 items-center justify-center rounded-xl bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900 shadow-sm font-bold text-base">
              {company[0]}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-bold text-zinc-900 dark:text-zinc-50 text-base">
                  {company}
                </h1>
                <span className="rounded-full bg-zinc-100 px-2.5 py-0.5 text-xs font-semibold text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300">
                  {stage}
                </span>
                <span className="rounded-full bg-emerald-500/10 px-2.5 py-0.5 text-xs font-semibold text-emerald-600 dark:bg-emerald-500/20 dark:text-emerald-400">
                  {nature}
                </span>
              </div>
              <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">{role}</p>
            </div>
          </div>

          {/* Question progress */}
          <div className="flex items-center gap-4">
            <div className="text-right">
              <span className="text-xs font-semibold text-zinc-900 dark:text-zinc-100">
                Question {Math.min(currentQIndex + 1, totalQuestions)} of {totalQuestions}
              </span>
              <div className="mt-1 h-1.5 w-32 rounded-full bg-zinc-100 dark:bg-zinc-800 overflow-hidden">
                <div
                  className="h-full bg-emerald-500 rounded-full transition-all duration-300"
                  style={{
                    width: `${((currentQIndex + 1) / totalQuestions) * 100}%`,
                  }}
                />
              </div>
            </div>

            <button
              onClick={onExit}
              className="rounded-lg border border-zinc-200 px-3 py-1.5 text-xs font-medium text-zinc-600 hover:bg-zinc-50 dark:border-zinc-800 dark:text-zinc-400 dark:hover:bg-zinc-800 transition-colors"
            >
              Exit Session
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="mb-6 flex items-center gap-2 rounded-xl border border-red-500/20 bg-red-500/10 p-4 text-xs text-red-600 dark:text-red-400">
          <AlertCircle className="size-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Main Conversation Flow */}
      <div className="space-y-6">
        {/* Conversation Message Stream */}
        <div className="space-y-4">
          {conversationHistory.map((item, idx) => (
            <div
              key={idx}
              className={`rounded-2xl p-6 transition-all ${
                item.type === "main_q"
                  ? "border border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-900 shadow-sm"
                  : item.type === "followup_q"
                  ? "border border-amber-500/30 bg-amber-500/5 dark:border-amber-500/20 dark:bg-amber-500/10"
                  : "border border-emerald-500/20 bg-emerald-500/5 dark:border-emerald-500/10 dark:bg-emerald-500/10 ml-6"
              }`}
            >
              {/* Header badge */}
              <div className="flex items-center justify-between mb-2.5">
                <div className="flex items-center gap-2">
                  {item.type === "main_q" && (
                    <>
                      <span className="rounded bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider">
                        Main Question
                      </span>
                      {item.topic && (
                        <span className="rounded bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300 px-2 py-0.5 text-[10px] font-medium">
                          {item.topic}
                        </span>
                      )}
                    </>
                  )}
                  {item.type === "followup_q" && (
                    <span className="rounded bg-amber-500 text-white px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider flex items-center gap-1">
                      <Sparkles className="size-3" />
                      <span>Adaptive Follow-up</span>
                    </span>
                  )}
                  {item.type === "answer" && (
                    <span className="rounded bg-emerald-600 text-white px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider">
                      Your Response
                    </span>
                  )}
                </div>

                {item.type === "main_q" && currentQuestion?.expected_concepts && (
                  <button
                    onClick={() => setShowHint(!showHint)}
                    className="inline-flex items-center gap-1 text-[11px] text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200 transition-colors"
                  >
                    <HelpCircle className="size-3" />
                    <span>{showHint ? "Hide Expected Focus" : "Show Expected Focus"}</span>
                  </button>
                )}
              </div>

              {/* Text content */}
              <div className="prose dark:prose-invert max-w-none text-sm leading-relaxed text-zinc-900 dark:text-zinc-100 whitespace-pre-wrap font-sans">
                {item.text}
              </div>

              {/* Toggleable Hint for Main Question */}
              {item.type === "main_q" && showHint && currentQuestion?.expected_concepts && (
                <div className="mt-3.5 pt-3 border-t border-zinc-100 dark:border-zinc-800 text-xs text-zinc-500">
                  <span className="font-semibold text-zinc-700 dark:text-zinc-300">
                    Interviewer Expected Concepts:
                  </span>{" "}
                  {currentQuestion.expected_concepts.join(", ")}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Answer Input Card */}
        <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-zinc-700 dark:text-zinc-300">
              Provide your technical explanation or reasoning:
            </span>
            <button
              type="button"
              onClick={() => setIsCodeMode(!isCodeMode)}
              className={`inline-flex items-center gap-1 rounded-md px-2.5 py-1 text-[11px] font-medium border transition-colors ${
                isCodeMode
                  ? "bg-zinc-900 text-white border-zinc-900 dark:bg-zinc-100 dark:text-zinc-900"
                  : "bg-zinc-50 text-zinc-600 border-zinc-200 hover:bg-zinc-100 dark:bg-zinc-800 dark:text-zinc-400 dark:border-zinc-700"
              }`}
            >
              <Code className="size-3" />
              <span>{isCodeMode ? "Monospace Code Mode" : "Standard Text"}</span>
            </button>
          </div>

          <textarea
            ref={textareaRef}
            rows={6}
            disabled={isSubmitting}
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              isCodeMode
                ? "// Write code, pseudocode, or algorithmic steps here..."
                : "Explain your architectural decisions, trade-offs, edge cases, and concrete implementation approach..."
            }
            className={`w-full rounded-xl border border-zinc-200 bg-zinc-50 p-4 text-sm text-zinc-900 placeholder:text-zinc-400 focus:border-zinc-900 focus:bg-white focus:outline-none focus:ring-1 focus:ring-zinc-900 dark:border-zinc-800 dark:bg-zinc-800/60 dark:text-zinc-100 dark:focus:border-zinc-400 dark:focus:bg-zinc-800 ${
              isCodeMode ? "font-mono text-xs leading-relaxed" : "font-sans leading-relaxed"
            }`}
          />

          <div className="mt-3 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center gap-3 text-[11px] text-zinc-400">
              <span>{answer.length} characters</span>
              <span>•</span>
              <span className="hidden sm:inline">Press Cmd+Enter or Ctrl+Enter to submit</span>
            </div>

            <div className="flex items-center gap-2">
              {submissionStatus && (
                <div className="flex items-center gap-1.5 text-xs text-emerald-600 dark:text-emerald-400 animate-pulse">
                  <Loader2 className="size-3.5 animate-spin" />
                  <span>{submissionStatus}</span>
                </div>
              )}

              <button
                type="button"
                disabled={isSubmitting || !answer.trim()}
                onClick={handleSubmitAnswer}
                className="inline-flex items-center gap-2 rounded-xl bg-zinc-900 px-6 py-2.5 text-xs font-bold text-white shadow-sm hover:bg-zinc-800 disabled:opacity-40 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200 transition-all active:scale-[0.98]"
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="size-4 animate-spin" />
                    <span>Processing...</span>
                  </>
                ) : (
                  <>
                    <span>Submit Response</span>
                    <Send className="size-3.5" />
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
