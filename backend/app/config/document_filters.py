DOCUMENT_FILTERS = {
    "AI Agents.pdf": {
        "skip_ranges": [
            (1, 12),
        ],
    },

    "AI Engineering.pdf": {
        "skip_ranges": [
            (1, 18),
            (495, 535),
        ],
    },

    "Data_Science_From_Scratch.pdf": {
        "skip_ranges": [
            (1, 12),
        ],
    },

    "Effective DevOps.pdf": {
        "skip_ranges": [
            (1, 15),
        ],
    },

    "Introducing MLOps.pdf": {
        "skip_ranges": [
            (1, 12),
            (175, 185),
        ],
    },

    "Learning DevOps.pdf": {
        "skip_ranges": [
            (1, 18),
            (520, 559),
        ],
    },

    "LLM Engineers Handbook.pdf": {
        "skip_ranges": [
            (1, 12),
        ],
    },

    "Practical Statistics for Data Scientists.pdf": {
        "skip_ranges": [
            (1, 12),
            (540, 562),
        ],
    },
}


BAD_PHRASES = [
    "table of contents",
    "contents",
    "index",
    "bibliography",
    "references",
    "acknowledgments",
    "acknowledgements",
    "about the author",
    "about the authors",
    "contributors",
]