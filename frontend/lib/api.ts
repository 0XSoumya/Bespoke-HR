export interface User {
  id: string;
  email: string;
  full_name: string;
  role: "candidate" | "interviewer";
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface EvidenceItem {
  source_type: string;
  title: string;
  content: string;
  url?: string;
  confidence: number;
  timestamp: string;
}

export interface InterviewProfile {
  company: string;
  target_role: string;
  interview_stage: string;
  interview_nature: string;
  focus_areas: string[];
  question_style: string;
  difficulty: string;
  number_of_questions: number;
  number_of_followups: number;
  rubric_criteria: string[];
  company_insights: string[];
  job_description_snippet?: string;
  supporting_evidence: EvidenceItem[];
}

export interface CandidateProfile {
  candidate_summary: string;
  skills: string[];
  projects: Array<{ title: string; description: string }>;
  domains: string[];
  claimed_competencies: string[];
  experience_level: string;
  education: Array<string | { degree?: string; field?: string; institution?: string }>;
  strengths: string[];
}

export interface FollowUpRecord {
  question: string;
  answer: string;
}

export interface QuestionEvaluation {
  score: number;
  conceptual_accuracy: number;
  completeness: number;
  technical_depth: number;
  communication: number;
  rubric_scores: Record<string, number>;
  strengths: string[];
  weaknesses: string[];
  missed_concepts: string[];
  evidence: string[];
  summary: string;
}

export interface QuestionRecord {
  question_id: string;
  topic: string;
  difficulty: string;
  main_question: string;
  expected_concepts: string[];
  evaluation_criteria: string[];
  main_answer: string;
  followups: FollowUpRecord[];
  evaluation?: QuestionEvaluation;
  completed: boolean;
}

export interface QuestionPreparationReview {
  question_id: string;
  topic: string;
  main_question: string;
  candidate_answer: string;
  followups: Array<{ question: string; answer: string }>;
  score: number;
  strengths: string[];
  gaps: string[];
  model_advice: string;
  evidence: string[];
}

export interface PreparationReport {
  overall_readiness_score: number;
  readiness_tier: string;
  executive_summary: string;
  strengths: string[];
  priority_gaps: string[];
  topic_breakdown: Record<string, number>;
  nature_rubric_scores: Record<string, number>;
  company_context_insights: string[];
  recommended_actions: string[];
  question_reviews: QuestionPreparationReview[];
  evidence_citations: EvidenceItem[];
}

export interface FullReportResponse {
  interview_id: string;
  company: string;
  role: string;
  interview_stage: string;
  interview_nature: string;
  preparation_report?: PreparationReport;
  candidate_report?: {
    overall_score: number;
    strengths: string[];
    areas_for_improvement: string[];
    learning_recommendations: string[];
    summary: string;
  };
  interview_profile?: InterviewProfile;
}

export interface CreateInterviewPayload {
  candidate_id: string;
  role: string;
  company: string;
  job_description?: string;
  interview_stage: string;
  interview_nature: string;
  number_of_questions: number;
  number_of_followups: number;
}

const API_BASE = typeof window !== "undefined"
  ? (process.env.NEXT_PUBLIC_API_URL || "/api/v1")
  : (process.env.BACKEND_INTERNAL_URL ? `${process.env.BACKEND_INTERNAL_URL}/api/v1` : "http://127.0.0.1:8000/api/v1");

function getHeaders(token?: string | null): Record<string, string> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

export interface InterviewSessionData {
  _id: string;
  candidate_id?: string;
  company?: string;
  role?: string;
  interview_stage?: string;
  interview_nature?: string;
  status: string;
  number_of_questions?: number;
  number_of_followups?: number;
  overall_score?: number;
  readiness_tier?: string;
  interview_profile?: InterviewProfile;
  current_question?: QuestionRecord;
  session?: {
    current_question_index: number;
    status: string;
  };
  report?: FullReportResponse;
  created_at?: string;
}

export const api = {
  // Auth
  async register(payload: { email: string; password: string; full_name: string }): Promise<AuthResponse> {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: getHeaders(),
      body: JSON.stringify({ ...payload, role: "candidate" }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Registration failed" }));
      throw new Error(err.detail || "Registration failed");
    }
    return res.json();
  },

  async login(payload: { email: string; password: string }): Promise<AuthResponse> {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: getHeaders(),
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Invalid credentials" }));
      throw new Error(err.detail || "Invalid email or password");
    }
    return res.json();
  },

  async getMe(token: string): Promise<User> {
    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: getHeaders(token),
    });
    if (!res.ok) {
      throw new Error("Session expired or invalid token");
    }
    return res.json();
  },

  // Resume Upload
  async uploadResume(
    file: File,
    targetRole: string,
    token?: string | null
  ): Promise<{ candidate_id: string; candidate_profile: CandidateProfile }> {
    const formData = new FormData();
    formData.append("resume_file", file);
    formData.append("target_role", targetRole);

    const headers: Record<string, string> = {};
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const res = await fetch(`${API_BASE}/resume/upload`, {
      method: "POST",
      headers,
      body: formData,
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Resume upload failed" }));
      throw new Error(err.detail || "Failed to process resume");
    }
    return res.json();
  },

  // Interviews
  async previewProfile(payload: CreateInterviewPayload, token?: string | null): Promise<InterviewProfile> {
    const res = await fetch(`${API_BASE}/interviews/profile-preview`, {
      method: "POST",
      headers: getHeaders(token),
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Profile preview failed" }));
      throw new Error(err.detail || "Failed to generate interview profile preview");
    }
    return res.json();
  },

  async createInterview(payload: CreateInterviewPayload, token?: string | null): Promise<{
    interview_id: string;
    status: string;
    company: string;
    role: string;
    number_of_questions: number;
    interview_profile?: InterviewProfile;
    current_question?: QuestionRecord;
  }> {
    const res = await fetch(`${API_BASE}/interviews/create`, {
      method: "POST",
      headers: getHeaders(token),
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Interview creation failed" }));
      throw new Error(err.detail || "Failed to create preparation session");
    }
    return res.json();
  },

  async listInterviews(token?: string | null): Promise<InterviewSessionData[]> {
    const res = await fetch(`${API_BASE}/interviews`, {
      headers: getHeaders(token),
    });
    if (!res.ok) {
      return [];
    }
    return res.json();
  },

  async getInterview(interviewId: string, token?: string | null): Promise<InterviewSessionData> {
    const res = await fetch(`${API_BASE}/interviews/${interviewId}`, {
      headers: getHeaders(token),
    });
    if (!res.ok) {
      throw new Error("Interview not found");
    }
    return res.json();
  },

  async getCurrentQuestion(interviewId: string, token?: string | null): Promise<QuestionRecord> {
    const res = await fetch(`${API_BASE}/interviews/${interviewId}/current-question`, {
      headers: getHeaders(token),
    });
    if (!res.ok) {
      throw new Error("Question not found");
    }
    return res.json();
  },

  async submitAnswer(
    interviewId: string,
    answer: string,
    token?: string | null
  ): Promise<{
    status: string;
    pending_followup: boolean;
    current_question?: QuestionRecord;
    report_available: boolean;
  }> {
    const res = await fetch(`${API_BASE}/interviews/${interviewId}/answer`, {
      method: "POST",
      headers: getHeaders(token),
      body: JSON.stringify({ answer }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Failed to submit answer" }));
      throw new Error(err.detail || "Submission failed");
    }
    return res.json();
  },

  async getReport(interviewId: string, token?: string | null): Promise<FullReportResponse> {
    const res = await fetch(`${API_BASE}/interviews/${interviewId}/report`, {
      headers: getHeaders(token),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Report not ready or not found" }));
      throw new Error(err.detail || "Report not found");
    }
    return res.json();
  },
};
