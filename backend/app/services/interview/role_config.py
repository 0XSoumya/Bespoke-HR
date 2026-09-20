ROLE_CONFIGS = {
    "AI/ML Engineer": {
        "default_difficulty": "intermediate",
        "preferred_domains": [
            "machine learning",
            "deep learning",
            "ai"
        ],
        "interview_focus_areas": [
            "Machine Learning",
            "Deep Learning",
            "Model Evaluation",
            "Feature Engineering",
            "Optimization",
            "Neural Networks",
            "Transformers",
            "MLOps"
        ],
        "priority_topics": {
            "Machine Learning": 10,
            "Deep Learning": 10,
            "Transformers": 9,
            "Model Evaluation": 8,
            "MLOps": 7,
        },
    },

    "GenAI Engineer": {
        "default_difficulty": "intermediate",
        "preferred_domains": [
            "genai",
            "llm",
            "rag"
        ],
        "interview_focus_areas": [
            "RAG",
            "Embeddings",
            "Vector Retrieval",
            "Prompt Engineering",
            "LLM Evaluation",
            "LLM Applications",
            "Fine Tuning",
            "Deployment"
        ],
        "priority_topics": {
            "RAG": 10,
            "Embeddings": 10,
            "Vector Retrieval": 9,
            "Prompt Engineering": 8,
            "LLM Evaluation": 8,
        },
    },

    "Backend Engineer": {
        "default_difficulty": "intermediate",
        "preferred_domains": [
            "backend"
        ],
        "interview_focus_areas": [
            "API Design",
            "Authentication",
            "Databases",
            "Caching",
            "Async Programming",
            "Docker",
            "Scalability",
            "System Design"
        ],
        "priority_topics": {
            "API Design": 10,
            "Databases": 10,
            "System Design": 9,
            "Scalability": 8,
            "Docker": 7,
        },
    },

    "Data Scientist": {
        "default_difficulty": "intermediate",
        "preferred_domains": [
            "data science"
        ],
        "interview_focus_areas": [
            "Statistics",
            "EDA",
            "Feature Engineering",
            "Machine Learning",
            "Experimentation",
            "Visualization"
        ],
        "priority_topics": {
            "Statistics": 10,
            "Machine Learning": 10,
            "EDA": 9,
            "Experimentation": 8,
        },
    },

    "MLOps Engineer": {
        "default_difficulty": "intermediate",
        "preferred_domains": [
            "mlops"
        ],
        "interview_focus_areas": [
            "Model Deployment",
            "Monitoring",
            "CI/CD",
            "Docker",
            "Kubernetes",
            "Model Serving",
            "Pipelines"
        ],
        "priority_topics": {
            "Model Deployment": 10,
            "Monitoring": 9,
            "CI/CD": 8,
            "Kubernetes": 8,
        },
    },
}

NATURE_CONFIGS = {
    "Coding": {
        "priority_topics": {
            "Data Structures & Algorithms": 10,
            "Algorithmic Complexity": 9,
            "Implementation & Edge Cases": 9,
            "Clean Code & Modularity": 8,
            "Problem Solving": 8,
        },
        "default_style": "hands_on_problem_solving",
    },
    "System Design": {
        "priority_topics": {
            "Distributed Systems": 10,
            "Scalability & Caching": 10,
            "Storage & Data Modeling": 9,
            "API & Protocol Architecture": 8,
            "Fault Tolerance & Reliability": 8,
        },
        "default_style": "open_ended_architecture_and_tradeoffs",
    },
    "Behavioral": {
        "priority_topics": {
            "Project Ownership & Initiative": 10,
            "Technical Conflict & Collaboration": 10,
            "Navigating Ambiguity": 9,
            "Failure Recovery & Lessons": 8,
            "Customer Impact": 8,
        },
        "default_style": "star_behavioral_inquiry",
    },
    "ML/AI Technical": {
        "priority_topics": {
            "RAG Architecture": 10,
            "Embeddings & Vector Search": 10,
            "Model Evaluation & Metrics": 9,
            "LLM Orchestration & Prompting": 8,
            "Production Inference & Latency": 8,
        },
        "default_style": "deep_dive_conceptual_and_architectural",
    },
}