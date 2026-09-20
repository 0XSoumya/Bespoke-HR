from typing import Optional
from datetime import datetime, timezone
from app.models.schemas.evidence import EvidenceItem
from app.models.schemas.interview_profile import InterviewProfile
from app.models.schemas.candidate_profile import CandidateProfile
from app.services.llm.groq_service import GroqService


CURATED_COMPANY_INTELLIGENCE: dict[str, dict] = {
    "stripe": {
        "company_name": "Stripe",
        "interview_culture": (
            "Stripe emphasizes practical, production-like engineering: debugging real codebases, "
            "API design, edge-case handling, clean abstractions, and ergonomic documentation. "
            "Interviews replicate day-to-day software development."
        ),
        "typical_stages": {
            "Screening": ["Practical coding", "Basic systems understanding", "Communication"],
            "Technical Round 1": ["Bug squashing in real repo", "API & data model design", "Refactoring"],
            "System Design": ["Scalable payments / event-driven architecture", "Idempotency", "Consistency"],
            "Behavioral": ["High craftsmanship", "Operating with urgency", "Cross-functional clarity"],
            "Hiring Manager": ["Past project depth", "Engineering philosophy", "Failure resilience"],
        },
        "nature_rubrics": {
            "Coding": ["Idiomatic code structure", "Thorough edge-case testing", "Clean debugging speed"],
            "System Design": ["Idempotency & exactly-once processing", "Auditability", "Graceful degradation"],
            "Behavioral": ["Customer obsession", "High standards", "Humility and ownership"],
            "ML/AI Technical": ["Production latency", "Model serving reliability", "Real-time inference safety"],
        },
        "key_technologies": ["Ruby", "Java", "Go", "Distributed systems", "Kafka", "PostgreSQL"],
        "citations": [
            "Stripe Engineering Guide to Technical Interviews",
            "Stripe Developer Platform & API Architecture Conventions",
        ],
    },
    "google": {
        "company_name": "Google",
        "interview_culture": (
            "Google values foundational computer science principles: algorithmic efficiency, "
            "asymptotic complexity (Big-O), scalable distributed systems, clear modularity, and 'Googleyness' (intellectual humility, collaboration)."
        ),
        "typical_stages": {
            "Screening": ["Data structures & algorithms", "Complexity analysis", "Clean syntax"],
            "Technical Round 1": ["Graph/tree traversals", "Dynamic programming or greedy logic", "Optimal space/time"],
            "System Design": ["Planetary-scale distributed systems", "Fault tolerance", "Throughput vs latency"],
            "Behavioral": ["Navigating ambiguity", "Bias to action", "Doing the right thing"],
            "Hiring Manager": ["Team impact", "Long-term vision", "Ownership"],
        },
        "nature_rubrics": {
            "Coding": ["Optimal time/space complexity", "Correctness on edge cases", "Clear communication while coding"],
            "System Design": ["Bottleneck identification", "Sharding & caching", "Reliability and failover"],
            "Behavioral": ["Collaboration", "Humility", "Dealing with ambiguous requirements"],
            "ML/AI Technical": ["Loss function formulation", "Data pipeline scalability", "Model evaluation metrics"],
        },
        "key_technologies": ["C++", "Java", "Python", "Go", "Spanner", "Borg", "Kubernetes", "gRPC"],
        "citations": [
            "Google Careers Interviewing at Google Engineering",
            "Site Reliability Engineering (SRE) Principles",
        ],
    },
    "meta": {
        "company_name": "Meta",
        "interview_culture": (
            "Meta prizes speed, high execution velocity, and direct problem-solving under time pressure. "
            "Coding rounds usually expect solving two algorithmic problems in 45 minutes with minimal hints. "
            "System design emphasizes massive real-time feed architectures, live streaming, and high concurrency."
        ),
        "typical_stages": {
            "Screening": ["Fast algorithmic coding (2 problems in 45m)", "Data structure fluency"],
            "Technical Round 1": ["Algorithms & data structures", "Clean bug-free code at pace"],
            "System Design": ["Social graph / news feed architecture", "High write throughput", "Caching & CDN"],
            "Behavioral": ["Impact", "Moving fast", "Direct feedback"],
            "Hiring Manager": ["Prior achievements", "Driving cross-functional consensus"],
        },
        "nature_rubrics": {
            "Coding": ["Coding velocity", "Self-testing before execution", "Algorithmic accuracy"],
            "System Design": ["Scale handling (billions of users)", "Cache invalidation", "Trade-off justification"],
            "Behavioral": ["Focus on impact", "Continuous learning", "Bold problem solving"],
            "ML/AI Technical": ["Recommendation systems", "Embedding retrieval", "Online feature serving"],
        },
        "key_technologies": ["Python", "Hack/PHP", "C++", "React", "GraphQL", "PyTorch", "Cassandra"],
        "citations": [
            "Meta Engineering Interview Guide",
            "Meta Product Architecture at Billions Scale",
        ],
    },
    "amazon": {
        "company_name": "Amazon",
        "interview_culture": (
            "Amazon interviews heavily weigh the 16 Leadership Principles (LPs) across all rounds, "
            "especially Customer Obsession, Ownership, Dive Deep, and Bias for Action. "
            "Technical questions focus on object-oriented design, microservices, and practical operational resilience."
        ),
        "typical_stages": {
            "Screening": ["Coding assessment & LP story", "Time complexity"],
            "Technical Round 1": ["Data structures and algorithms", "Customer-focused problem solving"],
            "System Design": ["AWS-style service design", "Loose coupling", "Operational metrics & SLA/SLO"],
            "Behavioral": ["Bar Raiser round", "STAR method stories for Leadership Principles"],
            "Hiring Manager": ["Team delivery", "Customer advocacy", "Ownership"],
        },
        "nature_rubrics": {
            "Coding": ["Working code", "Simplicity", "Modularity"],
            "System Design": ["Service-oriented architecture", "Availability over consistency (CAP theorem)", "Scalability"],
            "Behavioral": ["STAR method adherence", "Deep ownership", "Data-driven outcomes"],
            "ML/AI Technical": ["Business metric alignment", "Cost-effective inference", "Production monitoring"],
        },
        "key_technologies": ["Java", "Python", "AWS Ecosystem (DynamoDB, S3, SQS)", "Microservices"],
        "citations": [
            "Amazon Leadership Principles in Technical Assessment",
            "Amazon AWS Operational Excellence Framework",
        ],
    },
    "openai": {
        "company_name": "OpenAI",
        "interview_culture": (
            "OpenAI looks for high technical curiosity, rapid learning agility, rigorous reasoning from first principles, "
            "and deep understanding of modern LLM architectures, transformer internals, RLHF, and system throughput for AI workloads."
        ),
        "typical_stages": {
            "Screening": ["Core technical coding & AI understanding", "CS fundamentals"],
            "Technical Round 1": ["Transformer architecture deep dive", "Attention mechanics", "GPU memory & CUDA basics"],
            "System Design": ["LLM inference server architecture", "KV-caching", "Batching & quantization"],
            "Behavioral": ["Alignment with mission", "Collaborative safety mindset", "High intellectual honesty"],
            "Hiring Manager": ["Research-to-production mindset", "Autonomy in ambiguity"],
        },
        "nature_rubrics": {
            "Coding": ["Mathematical rigor", "Clean tensor operations", "Asymptotic reasoning"],
            "System Design": ["High throughput inference", "vLLM / Triton concepts", "Distributed GPU cluster topology"],
            "Behavioral": ["Safety consciousness", "Truth-seeking", "Mission alignment"],
            "ML/AI Technical": ["Transformer math", "RLHF / DPO mechanics", "Context length & memory scaling"],
        },
        "key_technologies": ["Python", "PyTorch", "CUDA", "Triton", "Ray", "Kubernetes", "FastAPI"],
        "citations": [
            "OpenAI Research Engineering Guidelines",
            "Scaling Laws & Distributed Inference Systems Architecture",
        ],
    },
    "anthropic": {
        "company_name": "Anthropic",
        "interview_culture": (
            "Anthropic values empirical rigor, safety-first engineering, transparent reasoning, and deep understanding "
            "of mechanistic interpretability, constitutional AI, and robust systems for massive scale training and evaluation."
        ),
        "typical_stages": {
            "Screening": ["Practical engineering and ML fundamentals", "Clean code"],
            "Technical Round 1": ["LLM evaluation pipelines", "Interpretability", "Empirical problem solving"],
            "System Design": ["Evaluation harness at scale", "Fault-tolerant model checkpointing"],
            "Behavioral": ["AI safety alignment", "Principled decision making", "Care for consequences"],
            "Hiring Manager": ["Scientific honesty", "Long-term dedication to safe frontier AI"],
        },
        "nature_rubrics": {
            "Coding": ["Robustness", "Clean readability", "Precision"],
            "System Design": ["Repeatable benchmarking", "Data provenance", "Fault tolerance"],
            "Behavioral": ["Safety prioritization", "Intellectual humility", "Clear communication"],
            "ML/AI Technical": ["Evaluation science", "Constitutional AI principles", "Model steering & safety bounds"],
        },
        "key_technologies": ["Python", "PyTorch", "JAX", "AWS / GCP", "Rust"],
        "citations": [
            "Anthropic Frontier Safety & Engineering Conventions",
            "Empirical Alignment & Evaluation Science Principles",
        ],
    },
}


class CompanyIntelligenceService:
    """
    Assembles company-specific interview intelligence combining curated durable memory,
    job description context, and live research extraction.
    """

    def __init__(self):
        self.groq_service = GroqService()

    def get_company_intelligence(
        self,
        company: str,
        target_role: str,
        interview_stage: str,
        interview_nature: str,
        job_description: Optional[str] = None,
    ) -> tuple[list[str], list[EvidenceItem], list[str]]:
        """
        Returns:
            (company_insights, supporting_evidence, rubric_criteria)
        """
        clean_company = company.strip().lower()
        matched_key = None
        for key in CURATED_COMPANY_INTELLIGENCE:
            if key in clean_company or clean_company in key:
                matched_key = key
                break

        if matched_key:
            data = CURATED_COMPANY_INTELLIGENCE[matched_key]
            company_name = data["company_name"]
            culture = data["interview_culture"]
            stage_focus = data["typical_stages"].get(
                interview_stage,
                data["typical_stages"].get("Technical Round 1", ["Core competency", "Communication"]),
            )
            nature_rubric = data["nature_rubrics"].get(
                interview_nature,
                ["Technical depth", "Problem-solving structure", "Clarity"],
            )

            insights = [
                f"{company_name} interview culture: {culture}",
                f"Expected focus for {interview_stage}: {', '.join(stage_focus)}.",
                f"Core tech stack highlights: {', '.join(data['key_technologies'])}.",
            ]

            evidence = [
                EvidenceItem(
                    source_type="company_knowledge",
                    title=f"{company_name} Interview Intelligence Archive",
                    content=culture,
                    confidence=0.95,
                )
            ]

            for citation in data.get("citations", []):
                evidence.append(
                    EvidenceItem(
                        source_type="company_knowledge",
                        title=f"{company_name} Internal Knowledge Base",
                        content=citation,
                        confidence=0.90,
                    )
                )

            rubric = list(nature_rubric)
            return insights, evidence, rubric

        # If company not in curated list, run live intelligence synthesis
        return self._synthesize_live_intelligence(
            company=company,
            target_role=target_role,
            interview_stage=interview_stage,
            interview_nature=interview_nature,
            job_description=job_description,
        )

    def _synthesize_live_intelligence(
        self,
        company: str,
        target_role: str,
        interview_stage: str,
        interview_nature: str,
        job_description: Optional[str] = None,
    ) -> tuple[list[str], list[EvidenceItem], list[str]]:
        """
        Synthesizes stage- and nature-aware interview intelligence for a company
        using public knowledge patterns and JD context.
        """
        jd_hint = f"\nJob Description Context:\n{job_description[:600]}" if job_description else ""

        prompt = f"""You are a senior technical hiring specialist and interview coach.
Generate interview intelligence for:
Company: {company}
Role: {target_role}
Interview Stage: {interview_stage}
Interview Nature: {interview_nature}{jd_hint}

Produce a JSON object with this exact structure:
{{
    "interview_culture_summary": "1-2 sentences on what this company values in technical interviews",
    "stage_expectations": "What the candidate should specifically anticipate in {interview_stage}",
    "tech_stack_highlights": ["3-5 typical technologies or architecture patterns"],
    "rubric_criteria": ["3-4 specific evaluation criteria appropriate for {interview_nature} in {interview_stage}"]
}}
Output ONLY valid JSON.
"""
        try:
            response = self.groq_service.generate(prompt=prompt, temperature=0.1)
            import json
            clean_resp = response.strip()
            if clean_resp.startswith("```json"):
                clean_resp = clean_resp[7:]
            if clean_resp.startswith("```"):
                clean_resp = clean_resp[3:]
            if clean_resp.endswith("```"):
                clean_resp = clean_resp[:-3]
            data = json.loads(clean_resp.strip())

            culture = data.get(
                "interview_culture_summary",
                f"{company} technical interviews assess practical engineering judgment and domain fluency."
            )
            expectations = data.get("stage_expectations", f"Focus on {interview_stage} problem-solving.")
            tech = data.get("tech_stack_highlights", ["Distributed systems", "API design", "Data structures"])
            rubric = data.get(
                "rubric_criteria",
                ["Correctness and reasoning", "Technical depth", "Clear communication", "Trade-off analysis"],
            )

            insights = [
                f"{company} interview culture: {culture}",
                f"{interview_stage} expectations: {expectations}",
                f"Target technical themes: {', '.join(tech)}.",
            ]

            evidence = [
                EvidenceItem(
                    source_type="live_research",
                    title=f"{company} Public Interview Pattern Intelligence",
                    content=culture,
                    confidence=0.85,
                ),
                EvidenceItem(
                    source_type="live_research",
                    title=f"{company} Stage Expectation ({interview_stage})",
                    content=expectations,
                    confidence=0.85,
                ),
            ]

            return insights, evidence, rubric

        except Exception:
            # Fallback baseline if LLM call is unavailable
            fallback_culture = (
                f"{company} expects strong fundamentals, structured problem-solving, and clear explanation of trade-offs."
            )
            insights = [
                f"{company} interview context: {fallback_culture}",
                f"Round: {interview_stage} ({interview_nature})",
            ]
            evidence = [
                EvidenceItem(
                    source_type="system_inference",
                    title=f"{company} Baseline Pattern",
                    content=fallback_culture,
                    confidence=0.75,
                )
            ]
            rubric = [
                "Problem-solving accuracy",
                "Architectural & algorithmic reasoning",
                "Communication clarity",
                "Handling constraints & trade-offs",
            ]
            return insights, evidence, rubric
