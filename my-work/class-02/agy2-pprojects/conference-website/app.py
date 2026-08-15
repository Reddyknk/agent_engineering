import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Sample Data for GCP Tech Summit 2026
CONFERENCE_INFO = {
    "title": "Google Cloud Tech Summit 2026",
    "subtitle": "Architecting the Future with GenAI, Kubernetes, and Modern Cloud Infrastructure",
    "date": "Wednesday, October 14, 2026",
    "location": "San Francisco Tech Convention Center & Hybrid Live Stream",
    "timezone": "PST (UTC-8)",
    "lunch_break": {
        "title": "Lunch Break & Networking Expo",
        "time": "12:00 PM - 1:00 PM",
        "duration_minutes": 60,
        "description": "Enjoy complimentary gourmet lunch, connect with Google Cloud experts, explore partner booths, and attend live lightning demos in the expo hall."
    }
}

SPEAKERS = {
    "spk_1": {
        "id": "spk_1",
        "first_name": "Sundar",
        "last_name": "Ramanathan",
        "role": "Principal AI Architect",
        "company": "Google Cloud",
        "linkedin": "https://www.linkedin.com/in/sundar-ramanathan-gcp"
    },
    "spk_2": {
        "id": "spk_2",
        "first_name": "Elena",
        "last_name": "Rostova",
        "role": "Lead Cloud Infrastructure Engineer",
        "company": "Enterprise Cloud Systems",
        "linkedin": "https://www.linkedin.com/in/elena-rostova-cloud"
    },
    "spk_3": {
        "id": "spk_3",
        "first_name": "Marcus",
        "last_name": "Vance",
        "role": "Staff Engineer - Kubernetes & GKE",
        "company": "ContainerOps Labs",
        "linkedin": "https://www.linkedin.com/in/marcus-vance-gke"
    },
    "spk_4": {
        "id": "spk_4",
        "first_name": "Aaliyah",
        "last_name": "Chen",
        "role": "Director of Security Engineering",
        "company": "Google Cloud Security",
        "linkedin": "https://www.linkedin.com/in/aaliyah-chen-sec"
    },
    "spk_5": {
        "id": "spk_5",
        "first_name": "David",
        "last_name": "Miller",
        "role": "Head of Data Platforms",
        "company": "BigData Dynamics",
        "linkedin": "https://www.linkedin.com/in/david-miller-bigquery"
    },
    "spk_6": {
        "id": "spk_6",
        "first_name": "Priya",
        "last_name": "Sharma",
        "role": "Senior ML Solutions Architect",
        "company": "Vertex AI Labs",
        "linkedin": "https://www.linkedin.com/in/priya-sharma-vertexai"
    },
    "spk_7": {
        "id": "spk_7",
        "first_name": "Liam",
        "last_name": "O'Connor",
        "role": "Serverless Lead Specialist",
        "company": "CloudNative Solutions",
        "linkedin": "https://www.linkedin.com/in/liam-oconnor-serverless"
    },
    "spk_8": {
        "id": "spk_8",
        "first_name": "Sophia",
        "last_name": "Nguyen",
        "role": "DevOps Transformation Director",
        "company": "Google Cloud Partner Ecosystem",
        "linkedin": "https://www.linkedin.com/in/sophia-nguyen-devops"
    },
    "spk_9": {
        "id": "spk_9",
        "first_name": "Carlos",
        "last_name": "Mendoza",
        "role": "Database Reliability Engineer",
        "company": "Spanner Systems",
        "linkedin": "https://www.linkedin.com/in/carlos-mendoza-db"
    },
    "spk_10": {
        "id": "spk_10",
        "first_name": "Hannah",
        "last_name": "Kim",
        "role": "GenAI Advocate",
        "company": "Google Developer Relations",
        "linkedin": "https://www.linkedin.com/in/hannah-kim-genai"
    }
}

# Exactly 8 Talks for the 1-Day Event (Each talk has 1 or max 2 speakers)
TALKS = [
    {
        "id": 1,
        "title": "Keynote: Next-Gen AI Applications with Gemini & Vertex AI",
        "time": "09:00 AM - 09:45 AM",
        "start_minutes": 540,
        "categories": ["AI & Machine Learning"],
        "description": "Discover how enterprise teams are building autonomous AI agents and multimodal search workflows utilizing Google Gemini 1.5 Pro and Vertex AI Agent Builder. Learn architecture patterns for low-latency RAG systems.",
        "speaker_ids": ["spk_1", "spk_6"]
    },
    {
        "id": 2,
        "title": "Mastering GKE (Google Kubernetes Engine) & Multicluster Service Mesh",
        "time": "09:45 AM - 10:30 AM",
        "start_minutes": 585,
        "categories": ["Cloud Infrastructure"],
        "description": "Deep dive into Google Kubernetes Engine (GKE) Autopilot for zero-friction container management, auto-scaling microservices, and securing cross-region traffic with Anthos Service Mesh.",
        "speaker_ids": ["spk_3"]
    },
    {
        "id": 3,
        "title": "Zero-Trust Architecture in Google Cloud & Identity Platform",
        "time": "10:30 AM - 11:15 AM",
        "start_minutes": 630,
        "categories": ["Security & Governance"],
        "description": "Implement robust BeyondCorp Enterprise zero-trust security model. Explore Workload Identity Federation, Chronicle Security Operations, and automated IAM policy enforcement.",
        "speaker_ids": ["spk_4", "spk_2"]
    },
    {
        "id": 4,
        "title": "Petabyte-Scale Real-Time Analytics with BigQuery & Dataflow",
        "time": "11:15 AM - 12:00 PM",
        "start_minutes": 675,
        "categories": ["Data & Analytics"],
        "description": "Learn real-time streaming architectures using Apache Beam on Cloud Dataflow coupled with BigQuery Continuous Queries for instant business insights and vector embeddings.",
        "speaker_ids": ["spk_5"]
    },
    # Lunch break occurs from 12:00 PM to 1:00 PM (60 mins)
    {
        "id": 5,
        "title": "Building Event-Driven Microservices with Cloud Run & Eventarc",
        "time": "01:00 PM - 01:45 PM",
        "start_minutes": 780,
        "categories": ["Cloud Infrastructure", "App Modernization"],
        "description": "Harness serverless container execution with Cloud Run, Cloud Pub/Sub, and Eventarc. Achieve sub-second cold starts, zero-scale cost savings, and seamless API gateway routing.",
        "speaker_ids": ["spk_7"]
    },
    {
        "id": 6,
        "title": "Global Consistency & High Availability with Cloud Spanner",
        "time": "01:45 PM - 02:30 PM",
        "start_minutes": 825,
        "categories": ["Data & Analytics"],
        "description": "Explore the internal architecture of Cloud Spanner, TrueTime API synchronization, multi-region replication, and SQL query optimizations for enterprise applications requiring 99.999% uptime.",
        "speaker_ids": ["spk_9", "spk_5"]
    },
    {
        "id": 7,
        "title": "Infrastructure as Code & GitOps with Terraform on GCP",
        "time": "02:30 PM - 03:15 PM",
        "start_minutes": 870,
        "categories": ["Cloud Infrastructure", "DevOps"],
        "description": "Best practices for managing GCP Landing Zones, VPC networks, and IAM using Terraform modules, Cloud Build pipelines, and GitOps workflows.",
        "speaker_ids": ["spk_8", "spk_2"]
    },
    {
        "id": 8,
        "title": "Fine-Tuning & Deploying Custom LLMs on Cloud TPUs & GPUs",
        "time": "03:15 PM - 04:00 PM",
        "start_minutes": 915,
        "categories": ["AI & Machine Learning"],
        "description": "Hands-on techniques for distributed LLM fine-tuning using TPU v5p pods and NVIDIA H100 GPU clusters on Cloud Life Sciences and Vertex AI Training pipelines.",
        "speaker_ids": ["spk_6", "spk_10"]
    },
    {
        "id": 9,
        "title": "Securing Cloud-Native Supply Chains with Artifact Registry & Binary Authorization",
        "time": "04:00 PM - 04:45 PM",
        "start_minutes": 960,
        "categories": ["Security & Governance", "DevOps"],
        "description": "Learn how to enforce end-to-end software supply chain security using Google Artifact Registry, container vulnerability scanning, SLSA compliance, and Binary Authorization policies on GKE.",
        "speaker_ids": ["spk_4", "spk_8"]
    },
    {
        "id": 10,
        "title": "Closing Keynote: The Next Frontier of Hybrid Cloud & Quantum Infrastructure",
        "time": "04:45 PM - 05:30 PM",
        "start_minutes": 1005,
        "categories": ["Cloud Infrastructure", "AI & Machine Learning"],
        "description": "An inspiring closing session exploring Google Cloud's roadmap for quantum-assisted optimization, ultra-low latency optical networking, and sustainable green cloud data center operations.",
        "speaker_ids": ["spk_1"]
    }
]

def get_hydrated_talks():
    """Helper to attach full speaker objects to each talk."""
    hydrated = []
    for talk in TALKS:
        talk_copy = talk.copy()
        talk_copy["speakers"] = [SPEAKERS[spk_id] for spk_id in talk["speaker_ids"] if spk_id in SPEAKERS]
        hydrated.append(talk_copy)
    return hydrated

@app.route("/")
def index():
    return render_template("index.html", conference=CONFERENCE_INFO)

@app.route("/api/talks")
def api_talks():
    category_filter = request.args.get("category", "").strip().lower()
    speaker_filter = request.args.get("speaker", "").strip().lower()
    search_query = request.args.get("q", "").strip().lower()

    all_talks = get_hydrated_talks()
    filtered_talks = []

    for talk in all_talks:
        # Category Filter (matches if any category contains filter string)
        if category_filter:
            cat_match = any(category_filter in cat.lower() for cat in talk["categories"])
            if not cat_match:
                continue

        # Speaker Filter (matches first name, last name, or full name)
        if speaker_filter:
            spk_match = any(
                speaker_filter in f"{spk['first_name']} {spk['last_name']}".lower() or
                speaker_filter == spk["id"].lower()
                for spk in talk["speakers"]
            )
            if not spk_match:
                continue

        # Search Query (matches title, description, or speaker names)
        if search_query:
            title_desc_match = (search_query in talk["title"].lower()) or (search_query in talk["description"].lower())
            speaker_match = any(
                search_query in f"{spk['first_name']} {spk['last_name']}".lower() or
                search_query in spk["company"].lower()
                for spk in talk["speakers"]
            )
            cat_match = any(search_query in cat.lower() for cat in talk["categories"])
            if not (title_desc_match or speaker_match or cat_match):
                continue

        filtered_talks.append(talk)

    return jsonify({
        "total": len(filtered_talks),
        "talks": filtered_talks,
        "lunch_break": CONFERENCE_INFO["lunch_break"]
    })

@app.route("/api/categories")
def api_categories():
    categories = set()
    for talk in TALKS:
        for cat in talk["categories"]:
            categories.add(cat)
    return jsonify(sorted(list(categories)))

@app.route("/api/speakers")
def api_speakers():
    speaker_list = list(SPEAKERS.values())
    return jsonify(speaker_list)

@app.route("/api/info")
def api_info():
    return jsonify(CONFERENCE_INFO)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
