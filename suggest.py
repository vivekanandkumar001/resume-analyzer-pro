# suggest.py — Resume improvement tips based on job role categories

role_profiles = {
    "Data Science": {
        "tips": [
            "Include machine learning projects with links to GitHub.",
            "Highlight tools like Python, Pandas, NumPy, and Scikit-learn.",
            "Mention experience with data cleaning, EDA, and preprocessing.",
            "Add details of data visualization tools: Matplotlib, Seaborn, or Tableau.",
            "Include participation in Kaggle competitions or online data challenges.",
            "Mention any experience with deep learning using TensorFlow or PyTorch."
        ]
    },

    "Python Developer": {
        "tips": [
            "Mention backend frameworks like Django, Flask, or FastAPI.",
            "Highlight API development, authentication, and testing experience.",
            "Include GitHub projects with proper documentation and version control.",
            "List any DevOps experience (CI/CD, Docker, cloud deployment).",
            "Mention use of relational and NoSQL databases (e.g., PostgreSQL, MongoDB).",
            "Include links to live applications or deployed services."
        ]
    },
    "AI Developer": {
    "tips": [
        "Include projects using deep learning frameworks like TensorFlow or PyTorch.",
        "Mention experience with neural networks, transformers, or large language models.",
        "Highlight hands-on work with model training, fine-tuning, or deployment.",
        "List AI tools/platforms like Hugging Face, OpenAI, or LangChain.",
        "Include research publications, hackathons, or AI competitions.",
        "Showcase use of GPUs, cloud computing, and model optimization."
    ]
},

    "Web Developer": {
        "tips": [
            "List frontend skills: HTML, CSS, JavaScript, React, or Angular.",
            "Mention backend skills like Node.js, Express, or Django.",
            "Include live project/demo links and GitHub repositories.",
            "Highlight experience with responsive design and mobile-first development.",
            "Mention integration with REST APIs and third-party services.",
            "Include UI/UX design tools knowledge like Figma or Adobe XD."
        ]
    },

    "Android Developer": {
        "tips": [
            "Mention Android SDK, Java/Kotlin, and Android Studio.",
            "Include published apps or demo projects with GitHub/APK links.",
            "Show understanding of Android components like Activities, Services, and Fragments.",
            "Mention Firebase integration, SQLite, and Jetpack libraries.",
            "Add any experience with material design or performance optimization.",
            "Include experience with testing, CI/CD, or app store deployment."
        ]
    },

    "UI/UX Designer": {
        "tips": [
            "Add portfolio link with detailed case studies.",
            "List design tools: Figma, Adobe XD, Sketch, or Photoshop.",
            "Show wireframes, prototypes, and high-fidelity designs.",
            "Include experience in usability testing and user research.",
            "Mention collaboration with developers and agile teams.",
            "Highlight certifications like Google UX or Interaction Design Foundation."
        ]
    },

    "Arts": {
        "tips": [
            "Include a portfolio or digital gallery link (Behance, Dribbble, etc.).",
            "Mention design tools used: Photoshop, Illustrator, Figma.",
            "List participation in exhibitions or contests.",
            "Highlight both traditional and digital art skills.",
            "Include any awards, recognitions, or public showcases.",
            "Mention creative storytelling or conceptual art experience."
        ]
    },

    "HR": {
        "tips": [
            "Mention recruitment tools/platforms like Naukri, LinkedIn Recruiter.",
            "List HR functions: onboarding, payroll, compliance, employee engagement.",
            "Include experience with HR software (SAP, Zoho, BambooHR, etc.).",
            "Highlight soft skills like communication, conflict resolution, and training.",
            "Mention HR certifications (e.g., SHRM, PHR, or local labor law training).",
            "Include metrics: time-to-hire, retention rate improvements, etc."
        ]
    },

    "Sales & Marketing": {
        "tips": [
            "Highlight CRM tools like Salesforce, HubSpot, Zoho.",
            "Include metrics like conversion rate, lead generation, or revenue growth.",
            "Mention campaign management, digital marketing, and SEO skills.",
            "List certifications: Google Ads, Facebook Blueprint, HubSpot Inbound.",
            "Include examples of email marketing, automation tools, or analytics tools.",
            "Demonstrate communication and negotiation achievements."
        ]
    },

    "DevOps Engineer": {
        "tips": [
            "List tools like Docker, Kubernetes, Jenkins, and GitHub Actions.",
            "Mention CI/CD pipelines, automation scripts, and monitoring tools.",
            "Include cloud platforms experience: AWS, Azure, or GCP.",
            "Showcase infrastructure as code (Terraform, Ansible).",
            "Highlight version control and collaboration tools (Git, GitLab).",
            "Include examples of production deployments or incident handling."
        ]
    },

    "Cloud Engineer": {
        "tips": [
            "Mention cloud platforms: AWS, Azure, or Google Cloud.",
            "List services used: EC2, S3, Lambda, RDS, VPC, IAM, etc.",
            "Include certifications: AWS Certified Solutions Architect, Azure Fundamentals.",
            "Highlight infrastructure setup, cost optimization, and scalability.",
            "Show use of tools like Terraform, CloudFormation, or Kubernetes.",
            "Include security policies and backup strategies knowledge."
        ]
    }
}
