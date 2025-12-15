from flask import Flask, render_template, request, redirect, session
import sqlite3
import pickle
import pandas as pd

app = Flask(__name__)
app.secret_key = "career_predictor_secret_key"


# =========================
# DATABASE CONNECTION
# =========================
def get_db():
    return sqlite3.connect("users.db")

# =========================
# LOAD ML MODEL
# =========================
model, encoders = pickle.load(open("model.pkl", "rb"))

# =========================
# CAREER ROADMAPS
# =========================

career_roadmaps = {
    # TECHNOLOGY CAREERS
    "Software Developer":
      "Foundation: Learn programming (Python/Java/C++), basic DSA, Git/GitHub.\nSkill Building: Web development, backend, databases."
      "\nPractical: Build projects, internships."
      "\nExpertise: System design, cloud deployment, leadership.",
    "Data Scientist":
      "Foundation: Python, statistics, probability, data visualization."
      "\nSkill Building: Machine Learning, Pandas, NumPy, SQL."
      "\nPractical: Real-world projects, Kaggle competitions."
      "\nExpertise: Advanced ML respectively/ML/DL, MLOps, research papers.",
    "AI Engineer":
      "Foundation: Python, linear algebra, ML basics."
      "\nSkill Building: Deep Learning, TensorFlow/PyTorch, NLP/Computer Vision."
      "\nPractical: AI projects, Kaggle, research contributions."
      "\nExpertise: Model optimization, MLOps, publications.",
    "ML Engineer": 
    "Foundation: ML algorithms, Python."
    "\nSkill Building: Model building, deep learning, ML libraries.\nPractical: Projects, internships, Kaggle."
    "\nExpertise: MLOps, model optimization, research.",
    "Web Developer": 
    "Foundation: HTML, CSS, JavaScript basics."
    "\nSkill Building: React/Angular, backend frameworks (Node, Flask), APIs.\nPractical: Build full-stack projects, internships, freelance work.\nExpertise: Deployment, SEO, performance optimization.",
    "App Developer": 
    "Foundation: Java/Kotlin/Flutter basics, UI/UX principles."
    "\nSkill Building: Mobile app development, Firebase/Backend integration.\nPractical: Build apps, publish on Play Store/App Store."
    "\nExpertise: Monetization, advanced app architecture, team leadership.",
    "Cloud Engineer":
      "Foundation: Linux basics, networking fundamentals."
      "\nSkill Building: AWS/Azure/GCP, virtualization, cloud architecture.\nPractical: Cloud deployment, certification, internships."
      "\nExpertise: Cloud security, automation, leadership roles.",
    "Cyber Security Analyst": 
    "Foundation: Networking, Linux, basics of security."
    "\nSkill Building: Ethical hacking, penetration testing, SOC tools.\nPractical: Internships, security audits, bug bounty programs.\nExpertise: Security certifications, advanced threat modeling, leadership.",
    "DevOps Engineer":
      "Foundation: Linux, Git, basic CI/CD."
      "\nSkill Building: Docker, Kubernetes, cloud platforms, scripting.\nPractical: Build pipelines, deploy apps, team experience."
      "\nExpertise: Advanced deployment, MLOps, leadership.",

    # SCIENCE & ANALYTICS
    "Research Scientist":
      "Foundation: Strong fundamentals in chosen domain."
      "\nSkill Building: Lab techniques, research methodology."
      "\nPractical: Projects, publications, internships."
      "\nExpertise: Advanced research, PhD, conferences.",
    "Data Analyst":
      "Foundation: Excel, SQL, basic Python."
      "\nSkill Building: Data visualization (Power BI/Tableau), reporting.\nPractical: Real datasets, business insights, internships."
      "\nExpertise: Advanced analytics, predictive modeling, domain expertise.",
    "Biotechnologist": 
    "Foundation: Core science, lab techniques."
    "\nSkill Building: Research methodology, domain-specific tools.\nPractical: Internship, applied projects, data analysis."
    "\nExpertise: Advanced research, specialization, leadership.",
    "Environmental Scientist": 
    "Foundation: Core science, environmental basics."
    "\nSkill Building: Fieldwork, lab experiments, data analysis."
    "\nPractical: Projects, internships."
    "\nExpertise: Research, policy contribution, leadership.",
    "Healthcare Analyst":
      "Foundation: Health science basics, statistics."
      "\nSkill Building: Data visualization, analytics tools.\nPractical: Hospital or research internships."
      "\nExpertise: Predictive modeling, reporting, leadership.",
    "AI Researcher":
      "Foundation: Python, Math, ML basics."
      "\nSkill Building: Deep Learning, NLP/CV."
      "\nPractical: Research projects, Kaggle competitions."
      "\nExpertise: Publications, model optimization, AI ethics.",

    # ARTS & DESIGN
    "Graphic Designer": 
    "Foundation: Design principles, color theory, typography."
    "\nSkill Building: Adobe Photoshop/Illustrator, Figma."
    "\nPractical: Portfolio, freelance projects, internships."
    "\nExpertise: Brand strategy, creative direction, specialization.",
    "UI/UX Designer":
      "Foundation: Design basics, user experience principles."
      "\nSkill Building: Wireframing, prototyping, Figma/Sketch."
      "\nPractical: Portfolio, client projects."
      "\nExpertise: UX research, advanced design, leadership.",
    "Animator": 
    "Foundation: Animation basics, principles of motion."
    "\nSkill Building: Blender, After Effects, 2D/3D animation.\nPractical: Short films, freelance projects."
    "\nExpertise: Motion graphics, creative direction, studio work.",
    "Illustrator":
      "Foundation: Drawing skills, design principles."
    "\nSkill Building: Adobe Illustrator, digital illustration."
    "\nPractical: Portfolio, freelance projects."
    "\nExpertise: Advanced illustration, brand identity, creative leadership.",
    "Film Editor": 
    "Foundation: Editing software, video fundamentals."
    "\nSkill Building: Storytelling, sound design."
    "\nPractical: Short films, client projects."
    "\nExpertise: Film direction, advanced editing, leadership.",
    "Game Designer":
      "Foundation: Game design principles, storytelling."
    "\nSkill Building: Unity/Unreal Engine, level design."
    "\nPractical: Build small games, internships."
    "\nExpertise: Game mechanics, creative leadership, portfolio.",
    "Art Director": 
    "Foundation: Design, color theory, typography."
    "\nSkill Building: Creative software, project management."
    "\nPractical: Projects, portfolios."
    "\nExpertise: Brand direction, creative leadership.",

    # EDUCATION & CONTENT
    "Teacher": 
    "Foundation: Subject mastery, basic teaching skills."
    "\nSkill Building: Certifications, lesson planning, classroom management.\nPractical: Teaching practice, internships, workshops."
    "\nExpertise: Research, curriculum development, leadership.",
    "Professor":
      "Foundation: Advanced subject knowledge, research basics."
      "\nSkill Building: Academic writing, teaching certifications.\nPractical: Lecturing, publishing papers."
      "\nExpertise: Research, supervision, leadership.",
    "Content Writer": 
    "Foundation: Writing skills, grammar, research basics."
    "\nSkill Building: SEO, content strategy."
    "\nPractical: Articles, blogs, internships."
    "\nExpertise: Editing, leadership, specialization.",
    "Journalist": 
    "Foundation: Writing skills, reporting basics."
    "\nSkill Building: Media tools, interviews."
    "\nPractical: Publishing articles, internships."
    "\nExpertise: Investigative journalism, editing, leadership.",
    "Academic Coordinator":
      "Foundation: Education principles, subject knowledge."
      "\nSkill Building: Planning, management, communication."
      "\nPractical: Organizing courses, workshops."
      "\nExpertise: Leadership, curriculum development.",

    # COMMERCE & MANAGEMENT
    "Accountant":
      "Foundation: Accounting basics, bookkeeping."
      "\nSkill Building: Taxation, auditing, financial software."
      "\nPractical: Internships, firm experience."
      "\nExpertise: Advisory, specialization, leadership.",
    "Chartered Accountant": 
    "Foundation: Accounting, taxation."
    "\nSkill Building: Auditing, certification (CA)."
    "\nPractical: Internships, firm experience."
    "\nExpertise: Advisory, specialization, leadership.",
    "Financial Analyst":
      "Foundation: Finance basics, Excel."
      "\nSkill Building: Financial modeling, corporate finance."
      "\nPractical: Internships, real-world projects."
      "\nExpertise: Investment strategies, leadership.",
    "Investment Banker": 
    "Foundation: Finance, market basics."
    "\nSkill Building: Financial analysis, corporate finance."
    "\nPractical: Projects, internships."
    "\nExpertise: Portfolio management, strategy, leadership.",
    "Business Analyst":
      "Foundation: Business basics, communication."
      "\nSkill Building: Process analysis, client management."
      "\nPractical: Case studies, internships.\nExpertise: Strategy, leadership, consulting.",
    "Management Consultant":
      "Foundation: Business knowledge, problem-solving."
      "\nSkill Building: Strategy, tools, client management."
      "\nPractical: Projects, internships."
      "\nExpertise: Leadership, advisory roles.",
    "Product Manager": 
    "Foundation: Business understanding, tech basics."
    "\nSkill Building: Product lifecycle, Agile, tools (Jira, Trello).\nPractical: Project handling, internships."
    "\nExpertise: Leadership, strategy, advanced product management.",
    "Project Manager": 
    "Foundation: Management principles, communication."
    "\nSkill Building: Project planning, Agile/Scrum."
    "\nPractical: Team projects, internships."
    "\nExpertise: Leadership, advanced project coordination.",
    "Operations Manager":
      "Foundation: Management basics, operations."
      "\nSkill Building: Process optimization, tools."
      "\nPractical: Internships, small projects."
      "\nExpertise: Strategy, leadership, advanced operations.",
    "HR Manager": 
    "Foundation: HR principles, labor laws."
    "\nSkill Building: Recruitment, employee management."
    "\nPractical: HR internships.\nExpertise: Leadership, strategic HR management.",
    "Marketing Manager": 
    "Foundation: Marketing principles, communication."
    "\nSkill Building: Digital marketing, tools."
    "\nPractical: Campaigns, internships."
    "\nExpertise: Leadership, strategy, brand management.",

    # MEDICAL
    "Doctor": 
    "Foundation: MBBS basics, anatomy, physiology."
    "\nSkill Building: Clinical practice, specialization."
    "\nPractical: Hospital internship, patient handling."
    "\nExpertise: Super-specialization, research, teaching.",
    "Nurse":
      "Foundation: Nursing basics, patient care."
      "\nSkill Building: Clinical skills, certifications."
      "\nPractical: Hospital experience, internships."
      "\nExpertise: Leadership, specialization.",
    "Pharmacist": 
    "Foundation: Pharmacy basics."
    "\nSkill Building: Drug knowledge, lab skills."
    "\nPractical: Internships, hospital/pharma projects."
    "\nExpertise: Specialization, research, leadership.",
    "Physiotherapist": 
    "Foundation: Anatomy, physiology."
    "\nSkill Building: Therapy techniques."
    "\nPractical: Hospital/clinic experience."
    "\nExpertise: Specialization, research.",
    "Clinical Researcher":
      "Foundation: Medical research basics."
      "\nSkill Building: Trial methodology, data analysis."
      "\nPractical: Internship, publications."
      "\nExpertise: Advanced research, leadership.",

    # LAW
    "Lawyer": 
    "Foundation: Law degree basics."
    "\nSkill Building: Case studies, internships."
    "\nPractical: Court practice, firm experience."
    "\nExpertise: Specialization, advisory, leadership.",
    "Corporate Lawyer": 
    "Foundation: Law basics."
    "\nSkill Building: Corporate law, internships."
    "\nPractical: Firm experience."
    "\nExpertise: Advisory, leadership.",
    "Public Prosecutor":
      "Foundation: Law degree, criminal law basics."
      "\nSkill Building: Case preparation, internships."
      "\nPractical: Court practice."
      "\nExpertise: Specialization, leadership.",
    "Legal Advisor":
      "Foundation: Law basics."
      "\nSkill Building: Advisory skills, case studies."
      "\nPractical: Firm projects, internships."
      "\nExpertise: Advisory, leadership.",

    # EDUCATION ADMINISTRATION
    "Education Counselor": 
    "Foundation: Education principles, counseling basics."
    "\nSkill Building: Certifications, counseling techniques."
    "\nPractical: Internships, practice."
    "\nExpertise: Leadership, strategy, specialization.",
    "School Administrator": 
    "Foundation: Education management basics."
    "\nSkill Building: Planning, coordination."
    "\nPractical: Internships, projects."
    "\nExpertise: Leadership, strategic management.",
    "Academic Coordinator": 
    "Foundation: Education principles, subject expertise."
    "\nSkill Building: Planning, course management."
    "\nPractical: Organizing workshops, teaching."
    "\nExpertise: Leadership, curriculum development."
}
# =======================
# LOGIN / SIGNUP
# =======================
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        name = request.form.get('name','')
        identifier = request.form['identifier']
        action = request.form['action']

        conn = get_db()
        cur = conn.cursor()

        if action == "signup":
            # Check if email/phone already exists
            cur.execute("SELECT id FROM users WHERE email=? OR phone=?", (identifier, identifier))
            existing_user = cur.fetchone()
            if existing_user:
                error = "This email or phone is already registered. Please login."
            else:
                # Insert new user
                cur.execute(
                    "INSERT INTO users (name,email,phone) VALUES (?,?,?)",
                    (name, identifier, identifier)
                )
                conn.commit()
                cur.execute("SELECT id FROM users WHERE email=?", (identifier,))
                user = cur.fetchone()
                session['user_id'] = user[0]
                conn.close()
                return redirect('/predict')

        elif action == "login":
            cur.execute("SELECT id FROM users WHERE email=? OR phone=?", (identifier, identifier))
            user = cur.fetchone()
            if user:
                session['user_id'] = user[0]
                conn.close()
                return redirect('/predict')
            else:
                error = "No account found with this email/phone. Please signup."

        conn.close()

    return render_template("login.html", error=error)

def get_user_day(user_id, career):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT day FROM progress WHERE user_id=? AND career=?",
        (user_id, career)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0


def update_user_day(user_id, career, day):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO progress (user_id, career, day) VALUES (?,?,?)",
        (user_id, career, day)
    )
    conn.commit()
    conn.close()
@app.route('/daily/<career>', methods=['GET', 'POST'])
def daily_plan(career):
    user_id = session.get('user_id')

    if not user_id:
        return redirect('/')

    day = get_user_day(user_id, career)
    tasks = daily_tasks.get(career, ["Learn basics", "Practice skills"])

    if request.method == 'POST':
        day += 1
        update_user_day(user_id, career, day)

    if day >= len(tasks):
        task = "🎉 Completed"
        show_day = "Completed"
    else:
        task = tasks[day]
        show_day = day + 1

    return render_template(
        "daily_plan.html",
        career=career,
        day=show_day,
        task=task
    )
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        input_data = pd.DataFrame([[ 
            request.form['Subjects'],
            request.form['Work_Style'],
            request.form['Career_Goal'],
            request.form['Education']
        ]], columns=["Subjects", "Work_Style", "Career_Goal", "Education"])

        for col in input_data.columns:
            input_data[col] = encoders[col].transform(input_data[col])

        prediction = model.predict(input_data)
        career = encoders["Career"].inverse_transform(prediction)[0]

        return render_template("index.html", result=career)

    return render_template("index.html")
@app.route('/roadmap/<career>')
def show_roadmap(career):
    roadmap = career_roadmaps.get(
        career,
        "Follow foundation learning, skill development, projects, and specialization."
    )
    return render_template("roadmap.html", career=career, roadmap=roadmap)

@app.route('/settings')
def settings():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')

    conn = get_db()
    cur = conn.cursor()

    # Fetch user info
    cur.execute("SELECT name, email FROM users WHERE id=?", (user_id,))
    user = cur.fetchone()

    # Fetch career & day from progress table (latest career)
    cur.execute("SELECT career, day FROM progress WHERE user_id=? ORDER BY id DESC LIMIT 1", (user_id,))
    progress = cur.fetchone()
    conn.close()

    user_name = user[0] if user else 'N/A'
    user_email = user[1] if user else 'N/A'
    career = progress[0] if progress else 'No career selected'
    day = progress[1] if progress else 'N/A'

    return render_template(
        "settings.html",
        name=user_name,
        email=user_email,
        career=career,
        day=day
    )

from flask import session
# Detailed daily tasks for selected careers
app.secret_key = "career_predictor_secret_key"

daily_tasks = {
    
    "Software Developer": [

  "Day 1: Understand what software development is & career overview",
  "Day 2: Install Python & VS Code, environment setup",
  "Day 3: Learn basic syntax, comments, print statements",
  "Day 4: Variables & data types",
  "Day 5: Type conversion & input/output",
  "Day 6: Practice problems on variables",
  "Day 7: Revision + small practice test",

  "Day 8: Operators (arithmetic, relational, logical)",
  "Day 9: Conditional statements (if)",
  "Day 10: if-else & nested if",
  "Day 11: elif ladder & practice",
  "Day 12: Real-life condition-based problems",
  "Day 13: Mini practice set",
  "Day 14: Revision day",

  "Day 15: Introduction to loops",
  "Day 16: for loop in detail",
  "Day 17: while loop",
  "Day 18: Loop control (break, continue, pass)",
  "Day 19: Pattern printing",
  "Day 20: Loop-based problems",
  "Day 21: Revision + test",

  "Day 22: Functions – basics",
  "Day 23: Function parameters & return",
  "Day 24: Scope of variables",
  "Day 25: Lambda functions (intro)",
  "Day 26: Practice problems on functions",
  "Day 27: Revision",
  "Day 28: Mini Project – Calculator",

  "Day 29: Introduction to lists",
  "Day 30: List methods & operations",
  "Day 31: Tuples & sets",
  "Day 32: Dictionaries",
  "Day 33: Nested data structures",
  "Day 34: Practice problems",
  "Day 35: Revision",

  "Day 36: Strings & string methods",
  "Day 37: String slicing & formatting",
  "Day 38: File handling – read",
  "Day 39: File handling – write & append",
  "Day 40: Exception handling",
  "Day 41: Practice set",
  "Day 42: Mini Project – Student Record System",

  "Day 43: Introduction to OOPs",
  "Day 44: Classes & objects",
  "Day 45: Constructors",
  "Day 46: Inheritance",
  "Day 47: Polymorphism & encapsulation",
  "Day 48: OOP practice problems",
  "Day 49: Revision",

  "Day 50: What is Git & version control",
  "Day 51: Git install & basic commands",
  "Day 52: Git commit & log",
  "Day 53: GitHub account & repositories",
  "Day 54: Push & pull code",
  "Day 55: GitHub project upload",
  "Day 56: Revision",

  "Day 57: Introduction to HTML",
  "Day 58: HTML elements & forms",
  "Day 59: Introduction to CSS",
  "Day 60: CSS layout & styling",
  "Day 61: Responsive design basics",
  "Day 62: Build simple webpage",
  "Day 63: Revision",

  "Day 64: Introduction to Flask",
  "Day 65: Flask setup & routing",
  "Day 66: Templates (Jinja2)",
  "Day 67: Forms & user input",
  "Day 68: Connecting frontend with backend",
  "Day 69: Practice",
  "Day 70: Mini Project – Simple Web App",

  "Day 71: Basics of databases",
  "Day 72: SQLite / MySQL introduction",
  "Day 73: CRUD operations",
  "Day 74: Database integration with Flask",
  "Day 75: Practice",
  "Day 76: Mini Project – Data-based App",

  "Day 77: Problem solving strategies",
  "Day 78: Basic DSA (arrays, searching)",
  "Day 79: Sorting techniques",
  "Day 80: Practice coding problems",
  "Day 81: Revision",

  "Day 82: Resume preparation",
  "Day 83: GitHub portfolio cleanup",
  "Day 84: Project documentation",
  "Day 85: Mock interview questions",
  "Day 86: HR interview preparation",
  "Day 87: Coding revision",

  "Day 88: Final Major Project planning",
  "Day 89: Final Project development",
  "Day 90: Final Project deployment & review"
],
   "Data Scientist": [

  "Day 1: Understand Data Science role, tools & career roadmap",
  "Day 2: Install Python, Anaconda & Jupyter Notebook",
  "Day 3: Python basics – syntax, variables, data types",
  "Day 4: Operators & input/output",
  "Day 5: Conditional statements",
  "Day 6: Loops (for, while)",
  "Day 7: Revision & practice problems",

  "Day 8: Functions & scope",
  "Day 9: Lists & list methods",
  "Day 10: Tuples, sets & dictionaries",
  "Day 11: String operations",
  "Day 12: File handling",
  "Day 13: Exception handling",
  "Day 14: Python practice set",

  "Day 15: Introduction to NumPy",
  "Day 16: NumPy arrays & operations",
  "Day 17: Indexing, slicing & reshaping",
  "Day 18: NumPy mathematical functions",
  "Day 19: NumPy practice problems",
  "Day 20: Mini Project – NumPy Data Analysis",
  "Day 21: Revision",

  "Day 22: Introduction to Pandas",
  "Day 23: Series & DataFrames",
  "Day 24: Data loading (CSV, Excel)",
  "Day 25: Data inspection & cleaning",
  "Day 26: Handling missing values",
  "Day 27: Data transformation",
  "Day 28: Mini Project – Data Cleaning Task",

  "Day 29: Exploratory Data Analysis (EDA)",
  "Day 30: Descriptive statistics",
  "Day 31: GroupBy & aggregation",
  "Day 32: Data filtering & sorting",
  "Day 33: EDA case study",
  "Day 34: Practice",
  "Day 35: Revision",

  "Day 36: Introduction to Matplotlib",
  "Day 37: Line, bar & scatter plots",
  "Day 38: Histograms & box plots",
  "Day 39: Customizing visualizations",
  "Day 40: Introduction to Seaborn",
  "Day 41: Statistical plots",
  "Day 42: Visualization mini project",

  "Day 43: Basics of statistics",
  "Day 44: Mean, median, mode, variance",
  "Day 45: Probability basics",
  "Day 46: Normal distribution",
  "Day 47: Hypothesis testing",
  "Day 48: Practice problems",
  "Day 49: Revision",

  "Day 50: Introduction to SQL",
  "Day 51: SELECT, WHERE, ORDER BY",
  "Day 52: GROUP BY & HAVING",
  "Day 53: Joins",
  "Day 54: Subqueries",
  "Day 55: SQL practice",
  "Day 56: Mini Project – SQL Analysis",

  "Day 57: Introduction to Machine Learning",
  "Day 58: Types of ML",
  "Day 59: Data preprocessing",
  "Day 60: Train-test split",
  "Day 61: Linear regression",
  "Day 62: Model evaluation",
  "Day 63: Regression mini project",

  "Day 64: Logistic regression",
  "Day 65: Classification metrics",
  "Day 66: K-Nearest Neighbors",
  "Day 67: Decision Trees",
  "Day 68: Random Forest",
  "Day 69: Classification project",
  "Day 70: Revision",

  "Day 71: Unsupervised learning",
  "Day 72: K-Means clustering",
  "Day 73: Dimensionality reduction (PCA)",
  "Day 74: Clustering project",
  "Day 75: Practice",
  "Day 76: Revision",

  "Day 77: Feature engineering",
  "Day 78: Feature scaling",
  "Day 79: Handling imbalanced data",
  "Day 80: Model tuning",
  "Day 81: Cross validation",
  "Day 82: Practice",
  "Day 83: Revision",

  "Day 84: Introduction to NLP",
  "Day 85: Text preprocessing",
  "Day 86: TF-IDF & vectorization",
  "Day 87: NLP mini project",
  "Day 88: Revision",

  "Day 89: Introduction to Time Series",
  "Day 90: Time series components",
  "Day 91: Forecasting basics",
  "Day 92: Time series project",
  "Day 93: Revision",

  "Day 94: Model deployment basics",
  "Day 95: Flask for ML apps",
  "Day 96: Deploy ML model",
  "Day 97: Project integration",
  "Day 98: Revision",

  "Day 99: Resume building for Data Scientist",
  "Day 100: GitHub portfolio organization",
  "Day 101: Case study preparation",
  "Day 102: Interview statistics questions",
  "Day 103: ML interview questions",
  "Day 104: SQL interview questions",
  "Day 105: Python interview questions",

  "Day 106: Major Project planning",
  "Day 107: Dataset selection",
  "Day 108: Data collection & cleaning",
  "Day 109: EDA & visualization",
  "Day 110: Model building",
  "Day 111: Model tuning",
  "Day 112: Evaluation & insights",

  "Day 113: Project documentation",
  "Day 114: Project presentation",
  "Day 115: GitHub final upload",
  "Day 116: Mock interviews",
  "Day 117: Weak area revision",
  "Day 118: Final assessment",
  "Day 119: Apply for internships/jobs",
  "Day 120: Review & next-step planning"
],
"AI Engineer": [

  "Day 1: Understand AI Engineer role, domains & career roadmap",
  "Day 2: Install Python, Anaconda & Jupyter Notebook",
  "Day 3: Python basics – syntax & variables",
  "Day 4: Data types & operators",
  "Day 5: Conditional statements",
  "Day 6: Loops & practice",
  "Day 7: Revision",

  "Day 8: Functions & scope",
  "Day 9: Lists & list methods",
  "Day 10: Tuples, sets & dictionaries",
  "Day 11: Strings & file handling",
  "Day 12: Exception handling",
  "Day 13: Python practice problems",
  "Day 14: Revision",

  "Day 15: Introduction to NumPy",
  "Day 16: NumPy arrays & operations",
  "Day 17: Indexing, slicing & reshaping",
  "Day 18: Mathematical operations",
  "Day 19: Practice",
  "Day 20: Mini Project – NumPy Analysis",
  "Day 21: Revision",

  "Day 22: Introduction to Pandas",
  "Day 23: DataFrames & Series",
  "Day 24: Data loading (CSV, Excel)",
  "Day 25: Data cleaning",
  "Day 26: Handling missing & duplicate data",
  "Day 27: Feature transformation",
  "Day 28: Mini Project – Data Cleaning",

  "Day 29: Exploratory Data Analysis (EDA)",
  "Day 30: Descriptive statistics",
  "Day 31: GroupBy & aggregation",
  "Day 32: Data filtering & sorting",
  "Day 33: EDA case study",
  "Day 34: Practice",
  "Day 35: Revision",

  "Day 36: Introduction to Matplotlib",
  "Day 37: Line, bar & scatter plots",
  "Day 38: Histograms & box plots",
  "Day 39: Advanced visualization",
  "Day 40: Seaborn basics",
  "Day 41: Statistical plots",
  "Day 42: Visualization mini project",

  "Day 43: Mathematics for AI – Linear Algebra basics",
  "Day 44: Vectors & matrices",
  "Day 45: Matrix operations",
  "Day 46: Probability basics",
  "Day 47: Statistics for AI",
  "Day 48: Practice",
  "Day 49: Revision",

  "Day 50: Introduction to Machine Learning",
  "Day 51: Types of ML & workflow",
  "Day 52: Data preprocessing",
  "Day 53: Train-test split & validation",
  "Day 54: Linear regression",
  "Day 55: Regression evaluation",
  "Day 56: Regression project",

  "Day 57: Logistic regression",
  "Day 58: Classification metrics",
  "Day 59: KNN algorithm",
  "Day 60: Decision Trees",
  "Day 61: Random Forest",
  "Day 62: Classification project",
  "Day 63: Revision",

  "Day 64: Support Vector Machines",
  "Day 65: Naive Bayes",
  "Day 66: Model comparison",
  "Day 67: Practice",
  "Day 68: Revision",

  "Day 69: Unsupervised learning overview",
  "Day 70: K-Means clustering",
  "Day 71: Hierarchical clustering",
  "Day 72: Dimensionality reduction (PCA)",
  "Day 73: Clustering project",
  "Day 74: Revision",

  "Day 75: Introduction to Deep Learning",
  "Day 76: Neural networks basics",
  "Day 77: Activation functions",
  "Day 78: Loss functions & optimizers",
  "Day 79: Build first neural network",
  "Day 80: Deep learning practice",
  "Day 81: Revision",

  "Day 82: Introduction to TensorFlow",
  "Day 83: Keras API",
  "Day 84: Build ANN model",
  "Day 85: Hyperparameter tuning",
  "Day 86: ANN mini project",
  "Day 87: Revision",

  "Day 88: Introduction to CNN",
  "Day 89: Convolution & pooling",
  "Day 90: Image classification",
  "Day 91: CNN project",
  "Day 92: Revision",

  "Day 93: Introduction to NLP",
  "Day 94: Text preprocessing",
  "Day 95: Word embeddings",
  "Day 96: RNN & LSTM basics",
  "Day 97: NLP mini project",
  "Day 98: Revision",

  "Day 99: Introduction to Transformers",
  "Day 100: Attention mechanism",
  "Day 101: Pretrained models (BERT)",
  "Day 102: Fine-tuning models",
  "Day 103: Transformer project",
  "Day 104: Revision",

  "Day 105: AI ethics & bias",
  "Day 106: Explainable AI",
  "Day 107: Model evaluation & monitoring",
  "Day 108: Practice",
  "Day 109: Revision",

  "Day 110: Model deployment basics",
  "Day 111: Flask/FastAPI for AI",
  "Day 112: Build AI API",
  "Day 113: Deploy model",
  "Day 114: Cloud basics (AWS/GCP overview)",
  "Day 115: Deployment project",

  "Day 116: Git & GitHub for AI projects",
  "Day 117: Portfolio organization",
  "Day 118: Resume building",
  "Day 119: AI interview questions",
  "Day 120: ML system design basics",

  "Day 121: Major AI project planning",
  "Day 122: Dataset selection",
  "Day 123: Data preprocessing",
  "Day 124: Model selection",
  "Day 125: Training & tuning",
  "Day 126: Evaluation",
  "Day 127: Deployment",

  "Day 128: Documentation",
  "Day 129: Presentation",
  "Day 130: GitHub final upload",
  "Day 131: Mock interviews",
  "Day 132: Weak area revision",
  "Day 133: Apply for internships/jobs",
  "Day 134: Review progress",
  "Day 135: Advanced topic exploration",
  "Day 136: Research paper reading",
  "Day 137: Implementation practice",
  "Day 138: Final assessment",
  "Day 139: Career planning",
  "Day 140: Industry trends study",
  "Day 141: Open-source contribution",
  "Day 142: Hackathon preparation",
  "Day 143: Hackathon participation",
  "Day 144: Feedback & improvement",
  "Day 145: Resume finalization",
  "Day 146: Portfolio polish",
  "Day 147: Interview practice",
  "Day 148: Final revision",
  "Day 149: Job applications",
  "Day 150: Next-step planning"
],
"ML Engineer": [

  "Day 1: Understand ML Engineer role vs Data Scientist vs AI Engineer",
  "Day 2: Install Python, Anaconda, Jupyter & VS Code",
  "Day 3: Python basics – syntax, variables",
  "Day 4: Data types & operators",
  "Day 5: Conditional statements",
  "Day 6: Loops & practice",
  "Day 7: Revision",

  "Day 8: Functions & scope",
  "Day 9: Lists & list methods",
  "Day 10: Tuples, sets & dictionaries",
  "Day 11: Strings & file handling",
  "Day 12: Exception handling",
  "Day 13: Python practice problems",
  "Day 14: Revision",

  "Day 15: NumPy introduction",
  "Day 16: NumPy arrays & operations",
  "Day 17: Indexing, slicing & reshaping",
  "Day 18: Mathematical operations",
  "Day 19: NumPy practice",
  "Day 20: Mini Project – NumPy Data Analysis",
  "Day 21: Revision",

  "Day 22: Pandas introduction",
  "Day 23: DataFrames & Series",
  "Day 24: Data loading (CSV, Excel)",
  "Day 25: Data cleaning techniques",
  "Day 26: Handling missing values",
  "Day 27: Feature transformation",
  "Day 28: Mini Project – Data Cleaning",

  "Day 29: Exploratory Data Analysis (EDA)",
  "Day 30: Descriptive statistics",
  "Day 31: GroupBy & aggregation",
  "Day 32: Data filtering & sorting",
  "Day 33: EDA case study",
  "Day 34: Practice",
  "Day 35: Revision",

  "Day 36: Data visualization with Matplotlib",
  "Day 37: Line, bar & scatter plots",
  "Day 38: Histograms & box plots",
  "Day 39: Advanced plotting",
  "Day 40: Seaborn basics",
  "Day 41: Visualization practice",
  "Day 42: Visualization mini project",

  "Day 43: Mathematics for ML – Linear Algebra basics",
  "Day 44: Vectors & matrices",
  "Day 45: Matrix operations",
  "Day 46: Probability basics",
  "Day 47: Statistics for ML",
  "Day 48: Practice",
  "Day 49: Revision",

  "Day 50: Introduction to Machine Learning",
  "Day 51: ML lifecycle & workflow",
  "Day 52: Data preprocessing",
  "Day 53: Train-test split & validation",
  "Day 54: Linear regression",
  "Day 55: Regression evaluation metrics",
  "Day 56: Regression mini project",

  "Day 57: Logistic regression",
  "Day 58: Classification metrics",
  "Day 59: K-Nearest Neighbors (KNN)",
  "Day 60: Decision Trees",
  "Day 61: Random Forest",
  "Day 62: Classification project",
  "Day 63: Revision",

  "Day 64: Support Vector Machines (SVM)",
  "Day 65: Naive Bayes",
  "Day 66: Model comparison techniques",
  "Day 67: Practice",
  "Day 68: Revision",

  "Day 69: Unsupervised learning overview",
  "Day 70: K-Means clustering",
  "Day 71: Hierarchical clustering",
  "Day 72: Dimensionality reduction (PCA)",
  "Day 73: Clustering project",
  "Day 74: Revision",

  "Day 75: Feature engineering techniques",
  "Day 76: Feature scaling",
  "Day 77: Handling imbalanced datasets",
  "Day 78: Cross-validation",
  "Day 79: Hyperparameter tuning",
  "Day 80: Practice",
  "Day 81: Revision",

  "Day 82: Introduction to Deep Learning",
  "Day 83: Neural network basics",
  "Day 84: Activation functions & loss",
  "Day 85: Optimizers",
  "Day 86: Build ANN using Keras",
  "Day 87: ANN mini project",

  "Day 88: Model evaluation & overfitting",
  "Day 89: Regularization techniques",
  "Day 90: Revision",

  "Day 91: ML model deployment basics",
  "Day 92: Flask/FastAPI introduction",
  "Day 93: Build ML REST API",
  "Day 94: Model serialization (pickle/joblib)",
  "Day 95: Deploy ML model",
  "Day 96: Deployment mini project",

  "Day 97: SQL basics for ML engineers",
  "Day 98: Data querying & joins",
  "Day 99: SQL practice",
  "Day 100: Mini Project – SQL + ML",

  "Day 101: Git & GitHub fundamentals",
  "Day 102: Version control for ML projects",
  "Day 103: ML project structuring",
  "Day 104: Experiment tracking basics",
  "Day 105: Practice",

  "Day 106: MLOps introduction",
  "Day 107: Model monitoring",
  "Day 108: Data drift & concept drift",
  "Day 109: ML pipelines overview",
  "Day 110: Practice",

  "Day 111: Resume building for ML Engineer",
  "Day 112: GitHub portfolio optimization",
  "Day 113: ML interview questions",
  "Day 114: Python interview questions",
  "Day 115: Statistics interview questions",

  "Day 116: Major ML project planning",
  "Day 117: Dataset selection",
  "Day 118: Data preprocessing",
  "Day 119: Feature engineering",
  "Day 120: Model building",
  "Day 121: Model tuning",
  "Day 122: Evaluation",
  "Day 123: Deployment",

  "Day 124: Documentation",
  "Day 125: Project presentation",
  "Day 126: GitHub final upload",
  "Day 127: Mock interviews",
  "Day 128: Weak area revision",
  "Day 129: Apply for internships/jobs",
  "Day 130: Review progress",
  "Day 131: Advanced ML topics exploration",
  "Day 132: Research paper reading",
  "Day 133: Implementation practice",
  "Day 134: Final assessment",
  "Day 135: Next-step career planning"
],
"Web Developer": [

  "Day 1: Understand Web Development roles (Frontend, Backend, Full Stack)",
  "Day 2: How the web works (HTTP, browser, server)",
  "Day 3: Install VS Code & set up environment",
  "Day 4: Introduction to HTML",
  "Day 5: HTML elements & attributes",
  "Day 6: HTML forms & inputs",
  "Day 7: Revision + practice",

  "Day 8: Introduction to CSS",
  "Day 9: CSS selectors & properties",
  "Day 10: Box model & positioning",
  "Day 11: Flexbox",
  "Day 12: CSS Grid",
  "Day 13: Responsive design (media queries)",
  "Day 14: Mini Project – Static Web Page",

  "Day 15: Advanced HTML semantics",
  "Day 16: Advanced CSS (animations & transitions)",
  "Day 17: CSS frameworks intro (Bootstrap/Tailwind)",
  "Day 18: Build responsive website",
  "Day 19: Practice",
  "Day 20: Revision",
  "Day 21: Mini Project – Responsive Website",

  "Day 22: Introduction to JavaScript",
  "Day 23: JS variables, data types & operators",
  "Day 24: Conditional statements",
  "Day 25: Loops & functions",
  "Day 26: Arrays & objects",
  "Day 27: Practice problems",
  "Day 28: Revision",

  "Day 29: DOM manipulation",
  "Day 30: Events & event handling",
  "Day 31: Form validation using JavaScript",
  "Day 32: LocalStorage & SessionStorage",
  "Day 33: Practice",
  "Day 34: Mini Project – Interactive Web Page",
  "Day 35: Revision",

  "Day 36: JavaScript ES6 features",
  "Day 37: Arrow functions & destructuring",
  "Day 38: Callbacks & promises",
  "Day 39: Async/Await",
  "Day 40: API basics",
  "Day 41: Fetch API",
  "Day 42: Mini Project – API Based App",

  "Day 43: Version control introduction",
  "Day 44: Git installation & basic commands",
  "Day 45: GitHub repositories",
  "Day 46: Branching & merging",
  "Day 47: Practice",
  "Day 48: Push projects to GitHub",

  "Day 49: Introduction to Backend development",
  "Day 50: Python & Flask basics",
  "Day 51: Flask routing & templates",
  "Day 52: Forms & request handling",
  "Day 53: Connecting frontend with backend",
  "Day 54: Practice",
  "Day 55: Mini Project – Flask App",

  "Day 56: Introduction to databases",
  "Day 57: SQL basics",
  "Day 58: CRUD operations",
  "Day 59: Database integration with Flask",
  "Day 60: Practice",
  "Day 61: Mini Project – Database App",

  "Day 62: Authentication basics",
  "Day 63: Login & signup system",
  "Day 64: Session & cookies",
  "Day 65: Practice",
  "Day 66: Revision",

  "Day 67: Web security basics",
  "Day 68: Input validation & protection",
  "Day 69: Deployment basics",
  "Day 70: Deploy web app (Render/Netlify)",
  "Day 71: Practice",
  "Day 72: Revision",

  "Day 73: Introduction to frameworks (React overview)",
  "Day 74: React setup & components",
  "Day 75: Props & state",
  "Day 76: Hooks (useState, useEffect)",
  "Day 77: Routing in React",
  "Day 78: Practice",
  "Day 79: Mini Project – React App",

  "Day 80: API integration in React",
  "Day 81: Form handling in React",
  "Day 82: Authentication flow",
  "Day 83: Practice",
  "Day 84: Revision",

  "Day 85: Full Stack project planning",
  "Day 86: UI design & layout",
  "Day 87: Frontend development",
  "Day 88: Backend API development",
  "Day 89: Database integration",
  "Day 90: Authentication",
  "Day 91: Testing & debugging",
  "Day 92: Deployment",

  "Day 93: Project documentation",
  "Day 94: GitHub final upload",
  "Day 95: Resume building",
  "Day 96: Portfolio website",
  "Day 97: Web interview questions",
  "Day 98: JavaScript interview prep",
  "Day 99: Backend interview prep",

  "Day 100: Mock interviews",
  "Day 101: Weak area revision",
  "Day 102: Performance optimization",
  "Day 103: Accessibility basics",
  "Day 104: SEO basics",
  "Day 105: Practice",

  "Day 106: Advanced project planning",
  "Day 107: Major web project development",
  "Day 108: Continue project",
  "Day 109: Testing",
  "Day 110: Deployment",
  "Day 111: Review & improvements",

  "Day 112: Open source contribution",
  "Day 113: Freelancing basics",
  "Day 114: Apply for internships/jobs",
  "Day 115: Interview practice",
  "Day 116: Resume finalization",
  "Day 117: Portfolio polish",
  "Day 118: Final assessment",
  "Day 119: Career planning",
  "Day 120: Industry trends study"
  ],
  "App Developer": [

  "Day 1: Understand App Development roles & mobile ecosystem",
  "Day 2: Android vs iOS vs Cross-platform overview",
  "Day 3: Install Android Studio & SDK setup",
  "Day 4: Introduction to Kotlin",
  "Day 5: Kotlin syntax, variables & data types",
  "Day 6: Operators & input/output",
  "Day 7: Revision & practice",

  "Day 8: Conditional statements in Kotlin",
  "Day 9: Loops (for, while, do-while)",
  "Day 10: Functions",
  "Day 11: Collections (List, Set, Map)",
  "Day 12: Null safety",
  "Day 13: Practice problems",
  "Day 14: Revision",

  "Day 15: Introduction to Android architecture",
  "Day 16: Activities & lifecycle",
  "Day 17: Layouts (Linear, Relative, Constraint)",
  "Day 18: Views (TextView, Button, EditText)",
  "Day 19: Event handling",
  "Day 20: Practice",
  "Day 21: Mini Project – Basic App UI",

  "Day 22: Intents & navigation",
  "Day 23: RecyclerView",
  "Day 24: Adapters & ViewHolder",
  "Day 25: Menus & dialogs",
  "Day 26: Practice",
  "Day 27: Revision",
  "Day 28: Mini Project – List Based App",

  "Day 29: Fragments",
  "Day 30: Fragment lifecycle",
  "Day 31: Navigation component",
  "Day 32: Bottom navigation & tabs",
  "Day 33: Practice",
  "Day 34: Revision",
  "Day 35: Mini Project – Multi-Screen App",

  "Day 36: Introduction to data storage",
  "Day 37: SharedPreferences",
  "Day 38: SQLite basics",
  "Day 39: Room database",
  "Day 40: CRUD operations",
  "Day 41: Practice",
  "Day 42: Mini Project – Notes App",

  "Day 43: Introduction to networking",
  "Day 44: REST APIs basics",
  "Day 45: Retrofit library",
  "Day 46: JSON parsing",
  "Day 47: API integration",
  "Day 48: Practice",
  "Day 49: Mini Project – API Based App",

  "Day 50: Background tasks",
  "Day 51: Threads & coroutines",
  "Day 52: WorkManager",
  "Day 53: Practice",
  "Day 54: Revision",

  "Day 55: MVVM architecture",
  "Day 56: ViewModel & LiveData",
  "Day 57: Data binding",
  "Day 58: State management",
  "Day 59: Practice",
  "Day 60: Mini Project – MVVM App",

  "Day 61: Firebase introduction",
  "Day 62: Firebase authentication",
  "Day 63: Firebase Firestore",
  "Day 64: Cloud storage",
  "Day 65: Practice",
  "Day 66: Mini Project – Login App",

  "Day 67: App permissions",
  "Day 68: Location & sensors",
  "Day 69: Camera & media access",
  "Day 70: Practice",
  "Day 71: Revision",

  "Day 72: App security basics",
  "Day 73: Data validation & encryption",
  "Day 74: Performance optimization",
  "Day 75: Debugging tools",
  "Day 76: Testing basics",
  "Day 77: Practice",
  "Day 78: Revision",

  "Day 79: App UI/UX principles",
  "Day 80: Material Design",
  "Day 81: Animations & transitions",
  "Day 82: Practice",
  "Day 83: UI polish project",

  "Day 84: App deployment process",
  "Day 85: Play Store policies",
  "Day 86: Generate APK / AAB",
  "Day 87: App signing",
  "Day 88: Publish test app",
  "Day 89: Revision",

  "Day 90: Resume building for App Developer",
  "Day 91: Git & GitHub for app projects",
  "Day 92: Portfolio preparation",
  "Day 93: App dev interview questions",
  "Day 94: Kotlin interview prep",

  "Day 95: Major App Project planning",
  "Day 96: UI design",
  "Day 97: App development",
  "Day 98: Continue development",
  "Day 99: Backend/API integration",
  "Day 100: Testing & debugging",
  "Day 101: Performance optimization",
  "Day 102: Deployment",

  "Day 103: Documentation",
  "Day 104: GitHub final upload",
  "Day 105: Mock interviews",
  "Day 106: Weak area revision",
  "Day 107: Apply for internships/jobs",
  "Day 108: Feedback & improvement",
  "Day 109: Advanced features addition",
  "Day 110: App update release",
  "Day 111: Freelancing basics",

  "Day 112: Open-source contribution",
  "Day 113: Hackathon preparation",
  "Day 114: Hackathon participation",
  "Day 115: Review & learnings",
  "Day 116: Portfolio polish",
  "Day 117: Interview practice",
  "Day 118: Final assessment",
  "Day 119: Career planning",
  "Day 120: Industry trends study"
],
"Cloud Engineer": [

  "Day 1: Understand Cloud Engineer role & career path",
  "Day 2: Cloud computing basics (IaaS, PaaS, SaaS)",
  "Day 3: Public vs Private vs Hybrid cloud",
  "Day 4: Introduction to AWS, Azure & GCP",
  "Day 5: Cloud service models & pricing basics",
  "Day 6: Create cloud free-tier account",
  "Day 7: Revision",

  "Day 8: Networking fundamentals (IP, DNS, ports)",
  "Day 9: OS basics (Linux vs Windows)",
  "Day 10: Linux commands (file & directory)",
  "Day 11: Linux permissions & users",
  "Day 12: Process & package management",
  "Day 13: Practice",
  "Day 14: Revision",

  "Day 15: Virtualization concepts",
  "Day 16: Virtual machines overview",
  "Day 17: AWS global infrastructure",
  "Day 18: EC2 instances",
  "Day 19: EC2 instance types & pricing",
  "Day 20: Launch & connect EC2",
  "Day 21: Practice & revision",

  "Day 22: Storage services overview",
  "Day 23: Amazon S3 basics",
  "Day 24: S3 buckets & objects",
  "Day 25: Versioning & lifecycle",
  "Day 26: S3 security & policies",
  "Day 27: Practice",
  "Day 28: Mini Project – Host static website on S3",

  "Day 29: Networking in AWS",
  "Day 30: VPC overview",
  "Day 31: Subnets & route tables",
  "Day 32: Internet gateway & NAT",
  "Day 33: Security groups",
  "Day 34: Network ACLs",
  "Day 35: VPC practice",

  "Day 36: Identity & Access Management (IAM)",
  "Day 37: Users, groups & roles",
  "Day 38: IAM policies",
  "Day 39: Best security practices",
  "Day 40: Practice",
  "Day 41: Revision",

  "Day 42: Databases in cloud",
  "Day 43: RDS overview",
  "Day 44: Launch RDS instance",
  "Day 45: Backup & snapshots",
  "Day 46: Practice",
  "Day 47: Mini Project – EC2 + RDS setup",

  "Day 48: Load balancing concepts",
  "Day 49: Elastic Load Balancer",
  "Day 50: Auto Scaling groups",
  "Day 51: High availability & fault tolerance",
  "Day 52: Practice",
  "Day 53: Revision",

  "Day 54: Monitoring & logging",
  "Day 55: CloudWatch basics",
  "Day 56: Alarms & metrics",
  "Day 57: Logging & alerts",
  "Day 58: Practice",
  "Day 59: Revision",

  "Day 60: Infrastructure as Code (IaC)",
  "Day 61: Introduction to Terraform",
  "Day 62: Terraform installation & basics",
  "Day 63: Write first Terraform script",
  "Day 64: Manage AWS resources with Terraform",
  "Day 65: Practice",
  "Day 66: Mini Project – Infrastructure automation",

  "Day 67: Containers basics",
  "Day 68: Docker introduction",
  "Day 69: Docker images & containers",
  "Day 70: Dockerfile & volumes",
  "Day 71: Practice",
  "Day 72: Mini Project – Dockerized app",

  "Day 73: Container orchestration basics",
  "Day 74: Kubernetes overview",
  "Day 75: Kubernetes architecture",
  "Day 76: Pods, services & deployments",
  "Day 77: Practice",
  "Day 78: Mini Project – Deploy app on Kubernetes",

  "Day 79: CI/CD basics",
  "Day 80: DevOps & cloud integration",
  "Day 81: GitHub Actions / Jenkins overview",
  "Day 82: Build simple CI/CD pipeline",
  "Day 83: Practice",
  "Day 84: Revision",

  "Day 85: Cloud security fundamentals",
  "Day 86: Encryption & key management",
  "Day 87: Shared responsibility model",
  "Day 88: Compliance basics",
  "Day 89: Practice",
  "Day 90: Revision",

  "Day 91: Cost management",
  "Day 92: Billing & budgets",
  "Day 93: Cost optimization techniques",
  "Day 94: Practice",
  "Day 95: Revision",

  "Day 96: Multi-cloud overview",
  "Day 97: Azure basics",
  "Day 98: GCP basics",
  "Day 99: Compare cloud platforms",
  "Day 100: Practice",

  "Day 101: Resume building for Cloud Engineer",
  "Day 102: GitHub portfolio setup",
  "Day 103: Cloud interview questions",
  "Day 104: Linux & networking interview prep",
  "Day 105: Practice tests",

  "Day 106: Major cloud project planning",
  "Day 107: Architecture design",
  "Day 108: Resource provisioning",
  "Day 109: Security & networking setup",
  "Day 110: Monitoring & optimization",
  "Day 111: Automation",
  "Day 112: Deployment",

  "Day 113: Documentation",
  "Day 114: GitHub final upload",
  "Day 115: Mock interviews",
  "Day 116: Weak area revision",
  "Day 117: Apply for internships/jobs",
  "Day 118: Review progress",
  "Day 119: Certification roadmap (AWS/Azure)",
  "Day 120: Career planning & industry trends"
],
"Cyber Security Analyst": [

  "Day 1: Understand Cyber Security Analyst role & career paths",
  "Day 2: Basics of cybersecurity & threat landscape",
  "Day 3: CIA triad (Confidentiality, Integrity, Availability)",
  "Day 4: Types of cyber attacks overview",
  "Day 5: Security concepts & terminology",
  "Day 6: Create learning lab environment",
  "Day 7: Revision",

  "Day 8: Networking fundamentals (TCP/IP, OSI model)",
  "Day 9: IP addressing & subnetting basics",
  "Day 10: Common network protocols (HTTP, HTTPS, FTP, DNS)",
  "Day 11: Firewalls & network security basics",
  "Day 12: Practice networking labs",
  "Day 13: Revision",
  "Day 14: Mini Lab – Network Traffic Analysis",

  "Day 15: Operating system basics",
  "Day 16: Linux fundamentals",
  "Day 17: Linux file system & permissions",
  "Day 18: Linux users & processes",
  "Day 19: Practice Linux commands",
  "Day 20: Windows security basics",
  "Day 21: Revision",

  "Day 22: Introduction to security tools",
  "Day 23: Kali Linux overview",
  "Day 24: Nmap scanning",
  "Day 25: Wireshark basics",
  "Day 26: Vulnerability scanning concepts",
  "Day 27: Practice",
  "Day 28: Mini Project – Vulnerability Scan Report",

  "Day 29: Types of malware",
  "Day 30: Malware behavior analysis",
  "Day 31: Antivirus & endpoint security",
  "Day 32: Practice malware detection",
  "Day 33: Revision",
  "Day 34: Case study analysis",
  "Day 35: Mini Lab – Malware Investigation",

  "Day 36: Web security fundamentals",
  "Day 37: OWASP Top 10 overview",
  "Day 38: SQL Injection",
  "Day 39: Cross-Site Scripting (XSS)",
  "Day 40: Authentication & authorization issues",
  "Day 41: Practice labs",
  "Day 42: Mini Project – Web Vulnerability Testing",

  "Day 43: Cryptography basics",
  "Day 44: Symmetric & asymmetric encryption",
  "Day 45: Hashing & digital signatures",
  "Day 46: SSL/TLS basics",
  "Day 47: Practice",
  "Day 48: Revision",

  "Day 49: Security monitoring & logging",
  "Day 50: SIEM overview",
  "Day 51: Log analysis basics",
  "Day 52: Incident detection",
  "Day 53: Practice",
  "Day 54: Mini Project – SIEM Log Analysis",

  "Day 55: Incident response lifecycle",
  "Day 56: Threat detection & analysis",
  "Day 57: Incident handling procedures",
  "Day 58: Digital forensics basics",
  "Day 59: Practice",
  "Day 60: Revision",

  "Day 61: Risk management basics",
  "Day 62: Vulnerability assessment & management",
  "Day 63: Patch management",
  "Day 64: Security policies & compliance",
  "Day 65: Practice",
  "Day 66: Mini Project – Risk Assessment Report",

  "Day 67: Cloud security basics",
  "Day 68: Shared responsibility model",
  "Day 69: Identity & access management",
  "Day 70: Cloud threat analysis",
  "Day 71: Practice",
  "Day 72: Revision",

  "Day 73: Endpoint detection & response (EDR)",
  "Day 74: Email security",
  "Day 75: Phishing attack analysis",
  "Day 76: Practice phishing detection",
  "Day 77: Mini Lab – Phishing Investigation",

  "Day 78: Security automation basics",
  "Day 79: Introduction to scripting for security (Python)",
  "Day 80: Automate basic security tasks",
  "Day 81: Practice",
  "Day 82: Revision",

  "Day 83: SOC operations overview",
  "Day 84: Threat intelligence basics",
  "Day 85: MITRE ATT&CK framework",
  "Day 86: Practice mapping attacks",
  "Day 87: Mini Project – Threat Intelligence Report",

  "Day 88: Ethics & legal aspects of cybersecurity",
  "Day 89: Cyber laws & compliance standards",
  "Day 90: Practice",
  "Day 91: Revision",

  "Day 92: Resume building for Cyber Security Analyst",
  "Day 93: GitHub portfolio setup",
  "Day 94: Cyber security interview questions",
  "Day 95: SOC analyst interview prep",
  "Day 96: Practice assessments",

  "Day 97: Major security project planning",
  "Day 98: Lab setup",
  "Day 99: Attack simulation",
  "Day 100: Detection & analysis",
  "Day 101: Incident response",
  "Day 102: Documentation & reporting",

  "Day 103: Project review",
  "Day 104: GitHub final upload",
  "Day 105: Mock interviews",
  "Day 106: Weak area revision",
  "Day 107: Apply for internships/jobs",
  "Day 108: Industry tools exploration",
  "Day 109: Certification roadmap (CEH, Security+)",
  "Day 110: Practice tests",

  "Day 111: Advanced threat hunting",
  "Day 112: Real-world attack case studies",
  "Day 113: Blue team vs Red team concepts",
  "Day 114: Practice",
  "Day 115: Portfolio polish",
  "Day 116: Interview practice",
  "Day 117: Final assessment",
  "Day 118: Career planning",
  "Day 119: Industry trend analysis",
  "Day 120: Continuous learning plan"
],
"DevOps Engineer": [

  "Day 1: Understand DevOps Engineer role & DevOps culture",
  "Day 2: SDLC & DevOps lifecycle",
  "Day 3: Agile & CI/CD overview",
  "Day 4: DevOps tools ecosystem",
  "Day 5: Set up learning environment",
  "Day 6: DevOps best practices",
  "Day 7: Revision",

  "Day 8: Operating system basics",
  "Day 9: Linux fundamentals",
  "Day 10: Linux file system & commands",
  "Day 11: Users, groups & permissions",
  "Day 12: Process & service management",
  "Day 13: Practice",
  "Day 14: Revision",

  "Day 15: Networking fundamentals",
  "Day 16: IP, DNS, ports & protocols",
  "Day 17: HTTP/HTTPS basics",
  "Day 18: Load balancing concepts",
  "Day 19: Practice",
  "Day 20: Revision",
  "Day 21: Mini Lab – Network Setup",

  "Day 22: Version control basics",
  "Day 23: Git installation & commands",
  "Day 24: Git branching & merging",
  "Day 25: GitHub workflows",
  "Day 26: Practice",
  "Day 27: Mini Project – Git Workflow",
  "Day 28: Revision",

  "Day 29: Introduction to cloud computing",
  "Day 30: AWS overview",
  "Day 31: AWS global infrastructure",
  "Day 32: EC2 instances",
  "Day 33: Storage services (S3)",
  "Day 34: Practice",
  "Day 35: Mini Project – Deploy app on EC2",

  "Day 36: Cloud networking",
  "Day 37: VPC basics",
  "Day 38: Subnets & route tables",
  "Day 39: Security groups & NACLs",
  "Day 40: Practice",
  "Day 41: Revision",

  "Day 42: Infrastructure as Code (IaC)",
  "Day 43: Terraform overview",
  "Day 44: Terraform installation & basics",
  "Day 45: Write Terraform scripts",
  "Day 46: Manage cloud infra with Terraform",
  "Day 47: Practice",
  "Day 48: Mini Project – Terraform Infrastructure",

  "Day 49: Containerization basics",
  "Day 50: Docker introduction",
  "Day 51: Docker images & containers",
  "Day 52: Dockerfile & volumes",
  "Day 53: Practice",
  "Day 54: Mini Project – Dockerized App",

  "Day 55: Container orchestration",
  "Day 56: Kubernetes overview",
  "Day 57: Kubernetes architecture",
  "Day 58: Pods, services & deployments",
  "Day 59: ConfigMaps & Secrets",
  "Day 60: Practice",
  "Day 61: Mini Project – Kubernetes Deployment",

  "Day 62: CI/CD basics",
  "Day 63: Jenkins overview",
  "Day 64: Jenkins installation & setup",
  "Day 65: Create CI pipeline",
  "Day 66: Create CD pipeline",
  "Day 67: Practice",
  "Day 68: Mini Project – CI/CD Pipeline",

  "Day 69: Configuration management",
  "Day 70: Ansible overview",
  "Day 71: Ansible playbooks",
  "Day 72: Manage servers with Ansible",
  "Day 73: Practice",
  "Day 74: Mini Project – Configuration Automation",

  "Day 75: Monitoring & logging basics",
  "Day 76: Prometheus overview",
  "Day 77: Grafana dashboards",
  "Day 78: Logging basics (ELK stack)",
  "Day 79: Alerts & monitoring",
  "Day 80: Practice",
  "Day 81: Mini Project – Monitoring Setup",

  "Day 82: DevSecOps basics",
  "Day 83: Security in CI/CD",
  "Day 84: Secrets management",
  "Day 85: Vulnerability scanning",
  "Day 86: Practice",
  "Day 87: Revision",

  "Day 88: Cloud cost management",
  "Day 89: Billing & budgets",
  "Day 90: Cost optimization strategies",
  "Day 91: Practice",
  "Day 92: Revision",

  "Day 93: Multi-cloud & hybrid cloud overview",
  "Day 94: Azure/GCP basics",
  "Day 95: Cloud comparison",
  "Day 96: Practice",

  "Day 97: Resume building for DevOps Engineer",
  "Day 98: GitHub portfolio setup",
  "Day 99: DevOps interview questions",
  "Day 100: Linux & cloud interview prep",
  "Day 101: Practice tests",

  "Day 102: Major DevOps project planning",
  "Day 103: Architecture design",
  "Day 104: Infrastructure provisioning",
  "Day 105: CI/CD implementation",
  "Day 106: Container orchestration",
  "Day 107: Monitoring & logging",
  "Day 108: Security integration",
  "Day 109: Deployment",

  "Day 110: Documentation",
  "Day 111: GitHub final upload",
  "Day 112: Mock interviews",
  "Day 113: Weak area revision",
  "Day 114: Apply for internships/jobs",
  "Day 115: Industry tools exploration",
  "Day 116: Certification roadmap (AWS DevOps Engineer)",
  "Day 117: Practice exams",
  "Day 118: Portfolio polish",
  "Day 119: Career planning",
  "Day 120: Industry trend analysis"
],



# for science and analysis careers
"Research Scientist": [

  "Day 1: Understand Research Scientist role & academic vs industry research",
  "Day 2: Research mindset, ethics & integrity",
  "Day 3: Research domains & problem selection",
  "Day 4: Reading & understanding research papers",
  "Day 5: Tools for research (Google Scholar, arXiv)",
  "Day 6: Lab & coding environment setup",
  "Day 7: Revision",

  "Day 8: Programming fundamentals (Python)",
  "Day 9: Data structures basics",
  "Day 10: Algorithms basics",
  "Day 11: Scientific computing with Python",
  "Day 12: NumPy & mathematical computing",
  "Day 13: Practice",
  "Day 14: Revision",

  "Day 15: Linear algebra for research",
  "Day 16: Vectors, matrices & transformations",
  "Day 17: Eigenvalues & eigenvectors",
  "Day 18: Probability theory basics",
  "Day 19: Statistics fundamentals",
  "Day 20: Practice",
  "Day 21: Revision",

  "Day 22: Data handling & preprocessing",
  "Day 23: Exploratory Data Analysis (EDA)",
  "Day 24: Visualization for research",
  "Day 25: Hypothesis formulation",
  "Day 26: Experimental design",
  "Day 27: Practice",
  "Day 28: Mini Study – Data Analysis Report",

  "Day 29: Introduction to Machine Learning",
  "Day 30: Supervised learning",
  "Day 31: Unsupervised learning",
  "Day 32: Model evaluation techniques",
  "Day 33: Bias, variance & overfitting",
  "Day 34: Practice",
  "Day 35: Revision",

  "Day 36: Advanced ML concepts",
  "Day 37: Optimization techniques",
  "Day 38: Feature engineering",
  "Day 39: Model interpretability",
  "Day 40: Reproducible experiments",
  "Day 41: Practice",
  "Day 42: Mini Research Experiment",

  "Day 43: Introduction to Deep Learning",
  "Day 44: Neural networks theory",
  "Day 45: Backpropagation",
  "Day 46: CNN fundamentals",
  "Day 47: RNN & sequence models",
  "Day 48: Practice",
  "Day 49: Revision",

  "Day 50: Transformers & attention mechanisms",
  "Day 51: Pretrained models & transfer learning",
  "Day 52: Fine-tuning techniques",
  "Day 53: Experiment tracking",
  "Day 54: Practice",
  "Day 55: Mini Research Project – DL Model",

  "Day 56: Research methodologies",
  "Day 57: Quantitative vs qualitative research",
  "Day 58: Evaluation metrics for research",
  "Day 59: Error analysis",
  "Day 60: Practice",
  "Day 61: Revision",

  "Day 62: Scientific writing basics",
  "Day 63: Structure of research papers",
  "Day 64: Writing abstract & introduction",
  "Day 65: Methodology section writing",
  "Day 66: Results & discussion writing",
  "Day 67: Practice",
  "Day 68: Draft paper writing",

  "Day 69: Literature review techniques",
  "Day 70: Citation & reference management",
  "Day 71: Research gap identification",
  "Day 72: Problem statement finalization",
  "Day 73: Practice",
  "Day 74: Revision",

  "Day 75: Reproducibility & open science",
  "Day 76: Version control for research",
  "Day 77: Dataset versioning",
  "Day 78: Experiment documentation",
  "Day 79: Practice",
  "Day 80: Mini Project – Reproducible Research",

  "Day 81: Ethics in AI & research bias",
  "Day 82: Responsible AI principles",
  "Day 83: Peer review process",
  "Day 84: Responding to reviewers",
  "Day 85: Practice",

  "Day 86: Research proposal writing",
  "Day 87: Funding & grant basics",
  "Day 88: Presentation of research",
  "Day 89: Poster & slide design",
  "Day 90: Practice",
  "Day 91: Revision",

  "Day 92: Advanced topic selection",
  "Day 93: Deep dive literature review",
  "Day 94: Experiment design",
  "Day 95: Dataset preparation",
  "Day 96: Model implementation",
  "Day 97: Training & tuning",
  "Day 98: Evaluation & analysis",

  "Day 99: Result validation",
  "Day 100: Visualization & interpretation",
  "Day 101: Paper drafting",
  "Day 102: Internal review",
  "Day 103: Improvements",
  "Day 104: Final draft",

  "Day 105: Conference/journal selection",
  "Day 106: Formatting & submission",
  "Day 107: Rebuttal preparation",
  "Day 108: Practice",

  "Day 109: Research presentation",
  "Day 110: Seminar delivery",
  "Day 111: Networking in academia/industry",
  "Day 112: Collaboration tools",

  "Day 113: GitHub research portfolio",
  "Day 114: Open-source research contribution",
  "Day 115: Research blog writing",
  "Day 116: Profile building (Google Scholar)",

  "Day 117: Mock research interviews",
  "Day 118: Weak area strengthening",
  "Day 119: Apply for research roles / PhD / RA",
  "Day 120: Review progress",

  "Day 121: Advanced experiments",
  "Day 122: Ablation studies",
  "Day 123: Hyperparameter studies",
  "Day 124: Robustness testing",
  "Day 125: Documentation",

  "Day 126: Paper revision",
  "Day 127: Final submission",
  "Day 128: Open-source release",
  "Day 129: Feedback analysis",
  "Day 130: Improvement iteration",

  "Day 131: Industry research case studies",
  "Day 132: Patents basics",
  "Day 133: Research commercialization",
  "Day 134: Ethics review",

  "Day 135: Long-term research roadmap",
  "Day 136: Skill gap analysis",
  "Day 137: Continuous learning plan",
  "Day 138: Teaching & mentoring basics",
  "Day 139: Knowledge sharing",

  "Day 140: Final portfolio polish",
  "Day 141: Interview preparation",
  "Day 142: Research vision statement",
  "Day 143: Career planning",
  "Day 144: Application follow-ups",
  "Day 145: Reflection & learning summary",
  "Day 146: Advanced reading",
  "Day 147: Experimental refinement",
  "Day 148: Final assessment",
  "Day 149: Next research direction",
  "Day 150: Long-term research plan"
],
"Data Analyst": [

  "Day 1: Understand Data Analyst role & responsibilities",
  "Day 2: Types of data & analytics lifecycle",
  "Day 3: Tools used by Data Analysts",
  "Day 4: Business problem understanding",
  "Day 5: Analytical thinking basics",
  "Day 6: Environment setup (Excel, Python, SQL)",
  "Day 7: Revision",

  "Day 8: Excel basics",
  "Day 9: Data types & formatting in Excel",
  "Day 10: Excel formulas & functions",
  "Day 11: Sorting, filtering & conditional formatting",
  "Day 12: Data cleaning in Excel",
  "Day 13: Practice",
  "Day 14: Mini Project – Excel Analysis",

  "Day 15: Advanced Excel",
  "Day 16: Pivot tables",
  "Day 17: Pivot charts & dashboards",
  "Day 18: Lookup functions (VLOOKUP, XLOOKUP)",
  "Day 19: Practice",
  "Day 20: Excel Dashboard Project",
  "Day 21: Revision",

  "Day 22: Introduction to SQL",
  "Day 23: Database basics",
  "Day 24: SELECT & WHERE",
  "Day 25: ORDER BY, LIMIT",
  "Day 26: Aggregate functions",
  "Day 27: Practice",
  "Day 28: Mini Project – SQL Queries",

  "Day 29: Joins (INNER, LEFT, RIGHT)",
  "Day 30: Subqueries",
  "Day 31: Group By & Having",
  "Day 32: Set operations",
  "Day 33: Practice",
  "Day 34: SQL Case Study",
  "Day 35: Revision",

  "Day 36: Python basics for data analysis",
  "Day 37: Variables, loops & functions",
  "Day 38: NumPy basics",
  "Day 39: Pandas – Series & DataFrames",
  "Day 40: Data cleaning with Pandas",
  "Day 41: Practice",
  "Day 42: Mini Project – Python Data Analysis",

  "Day 43: Exploratory Data Analysis (EDA)",
  "Day 44: Descriptive statistics",
  "Day 45: Data visualization with Matplotlib",
  "Day 46: Seaborn basics",
  "Day 47: Data insights extraction",
  "Day 48: Practice",
  "Day 49: EDA Project",

  "Day 50: Statistics for Data Analysts",
  "Day 51: Probability basics",
  "Day 52: Sampling techniques",
  "Day 53: Hypothesis testing",
  "Day 54: Correlation & regression basics",
  "Day 55: Practice",
  "Day 56: Revision",

  "Day 57: Business intelligence concepts",
  "Day 58: Power BI / Tableau overview",
  "Day 59: Data modeling",
  "Day 60: Creating reports & dashboards",
  "Day 61: Practice",
  "Day 62: BI Dashboard Project",

  "Day 63: Data storytelling",
  "Day 64: KPI & metrics",
  "Day 65: Writing insights & recommendations",
  "Day 66: Stakeholder communication",
  "Day 67: Practice",
  "Day 68: Revision",

  "Day 69: Data quality & governance",
  "Day 70: Handling missing & outliers",
  "Day 71: Feature engineering basics",
  "Day 72: Automation using Python",
  "Day 73: Practice",
  "Day 74: Mini Automation Project",

  "Day 75: Domain knowledge (Finance, Sales, Marketing)",
  "Day 76: Case study – Sales data",
  "Day 77: Case study – Customer data",
  "Day 78: Case study – Operations data",
  "Day 79: Practice",
  "Day 80: Revision",

  "Day 81: Resume building for Data Analyst",
  "Day 82: Portfolio projects setup",
  "Day 83: Git & GitHub for analysts",
  "Day 84: Interview SQL questions",
  "Day 85: Interview Excel questions",
  "Day 86: Interview Python questions",
  "Day 87: Mock interview",

  "Day 88: Advanced SQL problems",
  "Day 89: Window functions",
  "Day 90: CTEs",
  "Day 91: Practice",
  "Day 92: SQL Final Project",

  "Day 93: Advanced visualization",
  "Day 94: Dashboard optimization",
  "Day 95: Storytelling with dashboards",
  "Day 96: Practice",

  "Day 97: End-to-end Data Analyst project planning",
  "Day 98: Data collection",
  "Day 99: Data cleaning",
  "Day 100: EDA & visualization",
  "Day 101: Insights generation",
  "Day 102: Dashboard creation",
  "Day 103: Business recommendations",
  "Day 104: Documentation",

  "Day 105: GitHub final upload",
  "Day 106: Portfolio review",
  "Day 107: Interview practice",
  "Day 108: Apply for internships/jobs",
  "Day 109: Feedback incorporation",
  "Day 110: Skill gap improvement",

  "Day 111: Real-world dataset practice",
  "Day 112: Kaggle competition basics",
  "Day 113: Performance optimization",
  "Day 114: Revision",

  "Day 115: Advanced case studies",
  "Day 116: Business decision simulations",
  "Day 117: Certification roadmap",
  "Day 118: Practice exams",
  "Day 119: Career planning",
   "Day 120: Industry trend analysis"
],
"Biotechnologist": [

  "Day 1: Understand Biotechnologist role & career paths",
  "Day 2: Branches of biotechnology",
  "Day 3: Lab safety & biosafety levels",
  "Day 4: Ethics in biotechnology",
  "Day 5: Scientific terminology",
  "Day 6: Study & lab environment setup",
  "Day 7: Revision",

  "Day 8: Basics of biology",
  "Day 9: Cell structure & function",
  "Day 10: Biomolecules",
  "Day 11: Enzymes & metabolism",
  "Day 12: Practice",
  "Day 13: Revision",
  "Day 14: Concept test",

  "Day 15: Microbiology basics",
  "Day 16: Prokaryotic vs eukaryotic cells",
  "Day 17: Microbial growth & kinetics",
  "Day 18: Sterilization techniques",
  "Day 19: Practice",
  "Day 20: Lab observations",
  "Day 21: Revision",

  "Day 22: Genetics fundamentals",
  "Day 23: DNA structure & replication",
  "Day 24: Transcription & translation",
  "Day 25: Mutations & genetic variation",
  "Day 26: Practice",
  "Day 27: Revision",
  "Day 28: Mini Test",

  "Day 29: Molecular biology techniques",
  "Day 30: DNA & RNA isolation",
  "Day 31: PCR principles",
  "Day 32: Gel electrophoresis",
  "Day 33: Blotting techniques",
  "Day 34: Practice",
  "Day 35: Mini Project – PCR Workflow",

  "Day 36: Recombinant DNA technology",
  "Day 37: Vectors & cloning",
  "Day 38: Restriction enzymes & ligases",
  "Day 39: Transformation techniques",
  "Day 40: Practice",
  "Day 41: Revision",

  "Day 42: Cell culture techniques",
  "Day 43: Media preparation",
  "Day 44: Animal vs plant cell culture",
  "Day 45: Aseptic techniques",
  "Day 46: Practice",
  "Day 47: Lab documentation",

  "Day 48: Immunology basics",
  "Day 49: Antigens & antibodies",
  "Day 50: ELISA & immunoassays",
  "Day 51: Vaccines & immune response",
  "Day 52: Practice",
  "Day 53: Revision",

  "Day 54: Bioprocess engineering",
  "Day 55: Fermentation principles",
  "Day 56: Bioreactors",
  "Day 57: Downstream processing",
  "Day 58: Practice",
  "Day 59: Mini Project – Bioprocess Flow",

  "Day 60: Bioinformatics basics",
  "Day 61: Biological databases",
  "Day 62: Sequence alignment",
  "Day 63: BLAST & tools",
  "Day 64: Practice",
  "Day 65: Mini Project – Sequence Analysis",

  "Day 66: Genomics",
  "Day 67: Proteomics",
  "Day 68: Metabolomics",
  "Day 69: Systems biology overview",
  "Day 70: Revision",

  "Day 71: Plant biotechnology",
  "Day 72: Tissue culture",
  "Day 73: Genetic modification in plants",
  "Day 74: Practice",
  "Day 75: Mini Project – Plant Tissue Culture",

  "Day 76: Animal biotechnology",
  "Day 77: Stem cells & cloning",
  "Day 78: Transgenic animals",
  "Day 79: Practice",
  "Day 80: Revision",

  "Day 81: Industrial biotechnology",
  "Day 82: Enzyme production",
  "Day 83: Biotech products & applications",
  "Day 84: Practice",
  "Day 85: Mini Case Study",

  "Day 86: Pharmaceutical biotechnology",
  "Day 87: Drug discovery basics",
  "Day 88: Clinical trials overview",
  "Day 89: Regulatory affairs (FDA, CDSCO)",
  "Day 90: Practice",
  "Day 91: Revision",

  "Day 92: Quality control & assurance",
  "Day 93: GMP & GLP",
  "Day 94: Documentation standards",
  "Day 95: Practice",
  "Day 96: Audit simulation",

  "Day 97: Research methodology",
  "Day 98: Experimental design",
  "Day 99: Data analysis basics",
  "Day 100: Scientific writing",
  "Day 101: Practice",
  "Day 102: Mini Research Proposal",

  "Day 103: Emerging biotech fields",
  "Day 104: CRISPR & gene editing",
  "Day 105: Synthetic biology",
  "Day 106: Practice",
  "Day 107: Revision",

  "Day 108: Industry internships overview",
  "Day 109: Resume building for biotech",
  "Day 110: Interview preparation",
  "Day 111: Lab practical revision",

  "Day 112: Major biotech project planning",
  "Day 113: Literature review",
  "Day 114: Experiment design",
  "Day 115: Data collection",
  "Day 116: Analysis & interpretation",
  "Day 117: Documentation",
  "Day 118: Presentation",

  "Day 119: Project refinement",
  "Day 120: Final submission",
  "Day 121: Viva preparation",

  "Day 122: Career options (Industry / Research / Higher studies)",
  "Day 123: Certification roadmap",
  "Day 124: Apply for internships/jobs",
  "Day 125: Feedback incorporation",

  "Day 126: Advanced lab techniques",
  "Day 127: Troubleshooting experiments",
  "Day 128: Case studies",
  "Day 129: Ethics review",
  "Day 130: Revision",

  "Day 131: Portfolio documentation",
  "Day 132: Research presentation",
  "Day 133: Conference awareness",
  "Day 134: Networking in biotech",

  "Day 135: Skill gap analysis",
  "Day 136: Continuous learning plan",
  "Day 137: Future specialization choice",
  "Day 138: Final assessment",
  "Day 139: Career roadmap",
  "Day 140: Reflection & summary",
  "Day 141: Advanced reading",
  "Day 142: Lab safety refresh",
  "Day 143: Practical test",
  "Day 144: Industry trend study",
  "Day 145: Resume final polish",
  "Day 146: Mock interviews",
  "Day 147: Application follow-ups",
  "Day 148: Long-term planning",
  "Day 149: Personal biotech vision",
  "Day 150: Next steps in biotechnology career"
],
"Environmental Scientist": [

  "Day 1: Understand Environmental Scientist role & career paths",
  "Day 2: Scope of environmental science",
  "Day 3: Environmental ethics & sustainability",
  "Day 4: Environmental laws & policies overview",
  "Day 5: Environmental issues (global & local)",
  "Day 6: Study tools & environment setup",
  "Day 7: Revision",

  "Day 8: Basics of ecology",
  "Day 9: Ecosystems & biomes",
  "Day 10: Food chains & food webs",
  "Day 11: Energy flow & nutrient cycles",
  "Day 12: Practice",
  "Day 13: Revision",
  "Day 14: Concept test",

  "Day 15: Environmental chemistry basics",
  "Day 16: Air, water & soil chemistry",
  "Day 17: Pollutants & contaminants",
  "Day 18: Environmental sampling techniques",
  "Day 19: Practice",
  "Day 20: Field observation",
  "Day 21: Revision",

  "Day 22: Environmental microbiology",
  "Day 23: Role of microbes in environment",
  "Day 24: Biogeochemical cycles",
  "Day 25: Practice",
  "Day 26: Revision",
  "Day 27: Mini Test",

  "Day 28: Environmental physics",
  "Day 29: Radiation & noise pollution",
  "Day 30: Climate & atmospheric science",
  "Day 31: Weather vs climate",
  "Day 32: Practice",
  "Day 33: Revision",
  "Day 34: Case study",

  "Day 35: Water resources management",
  "Day 36: Hydrological cycle",
  "Day 37: Surface & groundwater",
  "Day 38: Water quality parameters",
  "Day 39: Practice",
  "Day 40: Mini Project – Water Analysis",

  "Day 41: Air pollution",
  "Day 42: Air pollutants & sources",
  "Day 43: Monitoring & control methods",
  "Day 44: Air quality standards",
  "Day 45: Practice",
  "Day 46: Field study",
  "Day 47: Revision",

  "Day 48: Soil science",
  "Day 49: Soil formation & classification",
  "Day 50: Soil pollution",
  "Day 51: Soil conservation techniques",
  "Day 52: Practice",
  "Day 53: Mini Project – Soil Study",

  "Day 54: Solid & hazardous waste management",
  "Day 55: Municipal solid waste",
  "Day 56: Biomedical & e-waste",
  "Day 57: Waste treatment technologies",
  "Day 58: Practice",
  "Day 59: Case study",

  "Day 60: Environmental impact assessment (EIA)",
  "Day 61: EIA process & methods",
  "Day 62: Risk assessment",
  "Day 63: Practice",
  "Day 64: Mini Project – EIA Report",

  "Day 65: Biodiversity conservation",
  "Day 66: Wildlife conservation",
  "Day 67: Protected areas",
  "Day 68: Practice",
  "Day 69: Revision",

  "Day 70: Climate change science",
  "Day 71: Greenhouse gases",
  "Day 72: Climate models",
  "Day 73: Climate mitigation & adaptation",
  "Day 74: Practice",
  "Day 75: Case study",

  "Day 76: Renewable energy sources",
  "Day 77: Solar, wind & hydro energy",
  "Day 78: Energy efficiency",
  "Day 79: Practice",
  "Day 80: Mini Project – Renewable Plan",

  "Day 81: GIS & remote sensing basics",
  "Day 82: Spatial data concepts",
  "Day 83: Environmental mapping",
  "Day 84: Practice",
  "Day 85: Mini GIS Project",

  "Day 86: Environmental economics",
  "Day 87: Cost-benefit analysis",
  "Day 88: Sustainable development goals (SDGs)",
  "Day 89: Practice",
  "Day 90: Revision",

  "Day 91: Environmental management systems",
  "Day 92: ISO 14001",
  "Day 93: Audits & compliance",
  "Day 94: Practice",
  "Day 95: Case study",

  "Day 96: Research methodology",
  "Day 97: Data collection & analysis",
  "Day 98: Environmental statistics basics",
  "Day 99: Scientific writing",
  "Day 100: Practice",
  "Day 101: Mini Research Proposal",

  "Day 102: Environmental health",
  "Day 103: Toxicology basics",
  "Day 104: Human health & environment",
  "Day 105: Practice",
  "Day 106: Revision",

  "Day 107: Disaster management",
  "Day 108: Natural & man-made disasters",
  "Day 109: Risk reduction strategies",
  "Day 110: Practice",
  "Day 111: Case study",

  "Day 112: Internship & fieldwork planning",
  "Day 113: Resume building for environmental roles",
  "Day 114: Interview preparation",
  "Day 115: Field practical revision",

  "Day 116: Major project planning",
  "Day 117: Literature review",
  "Day 118: Field data collection",
  "Day 119: Data analysis",
  "Day 120: Interpretation",
  "Day 121: Documentation",
  "Day 122: Presentation",

  "Day 123: Project refinement",
  "Day 124: Final submission",
  "Day 125: Viva preparation",

  "Day 126: Government environmental exams overview",
  "Day 127: Environmental laws revision",
  "Day 128: Policy analysis",
  "Day 129: Case studies",
  "Day 130: Revision",

  "Day 131: Industry trends in environmental science",
  "Day 132: Climate policy updates",
  "Day 133: Environmental NGOs & organizations",
  "Day 134: Networking & conferences",

  "Day 135: Skill gap analysis",
  "Day 136: Continuous learning plan",
  "Day 137: Specialization choice",
  "Day 138: Final assessment",
  "Day 139: Career roadmap",
  "Day 140: Reflection & summary",
  "Day 141: Advanced reading",
  "Day 142: Field safety refresh",
  "Day 143: Practical test",
  "Day 144: Industry report study",
  "Day 145: Resume final polish",
  "Day 146: Mock interviews",
  "Day 147: Application follow-ups",
  "Day 148: Long-term planning",
  "Day 149: Personal environmental vision",
  "Day 150: Next steps in environmental career"
],
"Healthcare Analyst": [

  "Day 1: Understand Healthcare Analyst role & career paths",
  "Day 2: Healthcare industry overview",
  "Day 3: Types of healthcare data",
  "Day 4: Healthcare workflows & stakeholders",
  "Day 5: HIPAA & healthcare ethics overview",
  "Day 6: Tools & environment setup",
  "Day 7: Revision",

  "Day 8: Basics of healthcare systems",
  "Day 9: Hospitals, clinics & insurance systems",
  "Day 10: Electronic Health Records (EHR)",
  "Day 11: Medical terminology basics",
  "Day 12: Practice",
  "Day 13: Revision",
  "Day 14: Concept test",

  "Day 15: Excel basics for healthcare data",
  "Day 16: Data cleaning in Excel",
  "Day 17: Formulas & healthcare KPIs",
  "Day 18: Pivot tables for patient data",
  "Day 19: Practice",
  "Day 20: Mini Project – Healthcare Excel Analysis",
  "Day 21: Revision",

  "Day 22: Introduction to SQL",
  "Day 23: Healthcare databases basics",
  "Day 24: SELECT & WHERE",
  "Day 25: Aggregate functions",
  "Day 26: Practice",
  "Day 27: Mini Project – SQL Healthcare Queries",
  "Day 28: Revision",

  "Day 29: Joins & subqueries",
  "Day 30: Healthcare metrics using SQL",
  "Day 31: Case study – Patient records",
  "Day 32: Practice",
  "Day 33: Revision",
  "Day 34: SQL Case Study",

  "Day 35: Python basics for analytics",
  "Day 36: Pandas & NumPy",
  "Day 37: Data cleaning with Python",
  "Day 38: Handling missing medical data",
  "Day 39: Practice",
  "Day 40: Mini Project – Python Healthcare Analysis",

  "Day 41: Exploratory Data Analysis (EDA)",
  "Day 42: Descriptive statistics",
  "Day 43: Healthcare data visualization",
  "Day 44: Identifying trends & patterns",
  "Day 45: Practice",
  "Day 46: EDA Project",

  "Day 47: Statistics for healthcare analytics",
  "Day 48: Probability basics",
  "Day 49: Hypothesis testing",
  "Day 50: Correlation & regression",
  "Day 51: Practice",
  "Day 52: Revision",

  "Day 53: Healthcare KPIs & metrics",
  "Day 54: Readmission rate analysis",
  "Day 55: Length of stay analysis",
  "Day 56: Mortality & outcome analysis",
  "Day 57: Practice",
  "Day 58: Case study – Hospital Performance",

  "Day 59: Data privacy & security",
  "Day 60: De-identification techniques",
  "Day 61: Healthcare compliance basics",
  "Day 62: Practice",
  "Day 63: Revision",

  "Day 64: BI tools overview (Power BI / Tableau)",
  "Day 65: Healthcare dashboards",
  "Day 66: Data modeling for healthcare",
  "Day 67: Practice",
  "Day 68: Dashboard Project",

  "Day 69: Healthcare cost analysis",
  "Day 70: Claims data analysis",
  "Day 71: Insurance & billing analytics",
  "Day 72: Practice",
  "Day 73: Case study – Cost Optimization",

  "Day 74: Population health analytics",
  "Day 75: Epidemiology basics",
  "Day 76: Disease trend analysis",
  "Day 77: Practice",
  "Day 78: Mini Project – Population Health",

  "Day 79: Predictive analytics basics",
  "Day 80: Risk stratification",
  "Day 81: Outcome prediction concepts",
  "Day 82: Practice",
  "Day 83: Revision",

  "Day 84: Data storytelling in healthcare",
  "Day 85: Communicating insights to clinicians",
  "Day 86: Report writing",
  "Day 87: Practice",

  "Day 88: Resume building for Healthcare Analyst",
  "Day 89: Portfolio project setup",
  "Day 90: Interview preparation",
  "Day 91: Mock interviews",

  "Day 92: Advanced SQL case studies",
  "Day 93: Window functions",
  "Day 94: Practice",
  "Day 95: SQL Final Project",

  "Day 96: Advanced dashboarding",
  "Day 97: Performance optimization",
  "Day 98: Practice",

  "Day 99: End-to-end Healthcare Analytics Project planning",
  "Day 100: Data collection",
  "Day 101: Data cleaning",
  "Day 102: EDA",
  "Day 103: Insight generation",
  "Day 104: Dashboard & report",
  "Day 105: Documentation",

  "Day 106: GitHub final upload",
  "Day 107: Portfolio review",
  "Day 108: Apply for internships/jobs",
  "Day 109: Feedback incorporation",
  "Day 110: Skill gap improvement",

  "Day 111: Real-world healthcare datasets practice",
  "Day 112: Case study – Clinical data",
  "Day 113: Practice",
  "Day 114: Revision",

  "Day 115: Certification roadmap (Healthcare Analytics)",
  "Day 116: Practice exams",
  "Day 117: Industry trends",
  "Day 118: Career planning",
  "Day 119: Final assessment",
  "Day 120: Next steps in healthcare analytics career"
],

"AI Researcher": [

  "Day 1: Understand AI Researcher role & career paths",
  "Day 2: AI research domains overview",
  "Day 3: Research ethics & responsible AI",
  "Day 4: Literature review basics",
  "Day 5: Tools for AI research (arXiv, Google Scholar, GitHub)",
  "Day 6: Environment setup (Python, Jupyter, PyTorch/TensorFlow)",
  "Day 7: Revision",

  "Day 8: Python fundamentals for AI research",
  "Day 9: Data structures & algorithms",
  "Day 10: Scientific computing (NumPy, Pandas)",
  "Day 11: Data visualization (Matplotlib, Seaborn)",
  "Day 12: Practice",
  "Day 13: Revision",
  "Day 14: Mini Project – Data Analysis",

  "Day 15: Linear algebra basics",
  "Day 16: Vectors, matrices, transformations",
  "Day 17: Eigenvalues & eigenvectors",
  "Day 18: Probability & statistics fundamentals",
  "Day 19: Practice",
  "Day 20: Revision",
  "Day 21: Concept test",

  "Day 22: Introduction to Machine Learning",
  "Day 23: Supervised learning algorithms",
  "Day 24: Unsupervised learning algorithms",
  "Day 25: Model evaluation metrics",
  "Day 26: Bias, variance & overfitting",
  "Day 27: Practice",
  "Day 28: Mini ML Project",

  "Day 29: Advanced ML concepts",
  "Day 30: Feature engineering & selection",
  "Day 31: Optimization techniques",
  "Day 32: Model interpretability",
  "Day 33: Practice",
  "Day 34: Mini ML Research Experiment",
  "Day 35: Revision",

  "Day 36: Introduction to Deep Learning",
  "Day 37: Neural networks theory",
  "Day 38: Backpropagation",
  "Day 39: CNN fundamentals",
  "Day 40: RNN & sequence models",
  "Day 41: Practice",
  "Day 42: Mini Project – DL Model",

  "Day 43: Transformers & attention mechanisms",
  "Day 44: Pretrained models & transfer learning",
  "Day 45: Fine-tuning models",
  "Day 46: Experiment tracking & reproducibility",
  "Day 47: Practice",
  "Day 48: Mini Project – Transformer Model",
  "Day 49: Revision",

  "Day 50: Research methodology",
  "Day 51: Problem formulation & hypothesis",
  "Day 52: Quantitative & qualitative research",
  "Day 53: Data collection & preprocessing",
  "Day 54: Practice",
  "Day 55: Mini Research Study",

  "Day 56: Scientific writing basics",
  "Day 57: Paper structure (abstract, intro, methods, results, discussion)",
  "Day 58: Literature review writing",
  "Day 59: Drafting methodology & experiments",
  "Day 60: Practice",
  "Day 61: Mini Paper Draft",

  "Day 62: Advanced DL architectures",
  "Day 63: GANs basics",
  "Day 64: Reinforcement learning basics",
  "Day 65: Practice",
  "Day 66: Mini Project – GAN or RL",
  "Day 67: Revision",

  "Day 68: Evaluation & ablation studies",
  "Day 69: Hyperparameter tuning",
  "Day 70: Model robustness & generalization",
  "Day 71: Practice",
  "Day 72: Mini Experiment",
  "Day 73: Revision",

  "Day 74: Open-source contribution",
  "Day 75: Git & GitHub for research",
  "Day 76: Collaborative research workflow",
  "Day 77: Practice",
  "Day 78: Revision",

  "Day 79: Advanced topics reading",
  "Day 80: Seminal AI papers study",
  "Day 81: AI conference papers overview",
  "Day 82: Practice",
  "Day 83: Paper summarization exercises",
  "Day 84: Mini Literature Review",

  "Day 85: Research proposal writing",
  "Day 86: Project planning",
  "Day 87: Experimental design",
  "Day 88: Dataset collection & preprocessing",
  "Day 89: Model implementation",
  "Day 90: Practice",
  "Day 91: Mini Research Project Phase 1",

  "Day 92: Model training & optimization",
  "Day 93: Evaluation & visualization",
  "Day 94: Documentation & reporting",
  "Day 95: Practice",
  "Day 96: Mini Research Project Phase 2",
  "Day 97: Revision",

  "Day 98: AI ethics & bias analysis",
  "Day 99: Responsible AI implementation",
  "Day 100: Practice",
  "Day 101: Revision",

  "Day 102: Resume & portfolio for AI research",
  "Day 103: GitHub research portfolio setup",
  "Day 104: Preparing for research interviews",
  "Day 105: Mock interviews",
  "Day 106: Revision",

  "Day 107: Major AI research project planning",
  "Day 108: Literature review finalization",
  "Day 109: Experimental setup",
  "Day 110: Model building",
  "Day 111: Training & evaluation",
  "Day 112: Analysis & visualization",
  "Day 113: Documentation & draft paper",

  "Day 114: Paper submission process",
  "Day 115: Conference/journal selection",
  "Day 116: Formatting & referencing",
  "Day 117: Peer review preparation",
  "Day 118: Revision & improvements",

  "Day 119: Open-source release of code & models",
  "Day 120: Research presentation preparation",
  "Day 121: Mock presentation",
  "Day 122: Networking with AI researchers",
  "Day 123: Applying for research roles",
  "Day 124: Revision",

  "Day 125: Advanced experiments",
  "Day 126: Ablation studies",
  "Day 127: Robustness testing",
  "Day 128: Feedback incorporation",
  "Day 129: Revision",

  "Day 130: Industry AI research case studies",
  "Day 131: Patents & IP basics",
  "Day 132: Research commercialization",
  "Day 133: Ethics & reproducibility review",

  "Day 134: Long-term AI research roadmap",
  "Day 135: Skill gap analysis",
  "Day 136: Continuous learning plan",
  "Day 137: Collaboration & mentorship",
  "Day 138: Knowledge sharing & seminars",
  "Day 139: Final portfolio polish",
  "Day 140: Advanced reading & papers",
  "Day 141: Final assessment",
  "Day 142: Reflection & learning summary",
  "Day 143: Career planning",
  "Day 144: Application follow-ups",
  "Day 145: Next research direction",
  "Day 146: Personal AI research vision",
  "Day 147: Advanced experiments iteration",
  "Day 148: Final project submission",
  "Day 149: Networking & conference presentation",
  "Day 150: Long-term AI research career plan"
],
#arts and design and more can be added here
"Graphic Designer": [

  "Day 1: Understand Graphic Designer role & career paths",
  "Day 2: Design principles overview",
  "Day 3: Color theory basics",
  "Day 4: Typography fundamentals",
  "Day 5: Visual hierarchy & composition",
  "Day 6: Tools & software setup (Photoshop, Illustrator, Figma)",
  "Day 7: Revision",

  "Day 8: Adobe Photoshop basics",
  "Day 9: Layers & masking",
  "Day 10: Selection & retouching tools",
  "Day 11: Color correction & adjustment",
  "Day 12: Practice",
  "Day 13: Mini Project – Photo Editing",
  "Day 14: Revision",

  "Day 15: Adobe Illustrator basics",
  "Day 16: Vector graphics & pen tool",
  "Day 17: Shapes, paths & layers",
  "Day 18: Typography in Illustrator",
  "Day 19: Practice",
  "Day 20: Mini Project – Vector Logo Design",
  "Day 21: Revision",

  "Day 22: Adobe Figma basics",
  "Day 23: UI/UX fundamentals",
  "Day 24: Wireframes & layout design",
  "Day 25: Components & prototyping",
  "Day 26: Practice",
  "Day 27: Mini Project – Mobile App UI",
  "Day 28: Revision",

  "Day 29: Branding basics",
  "Day 30: Logo design principles",
  "Day 31: Brand colors & typography",
  "Day 32: Practice",
  "Day 33: Mini Project – Brand Identity",
  "Day 34: Revision",

  "Day 35: Infographics & data visualization basics",
  "Day 36: Designing charts & diagrams",
  "Day 37: Tools for infographics",
  "Day 38: Practice",
  "Day 39: Mini Project – Infographic Design",
  "Day 40: Revision",

  "Day 41: Motion graphics basics",
  "Day 42: Adobe After Effects introduction",
  "Day 43: Keyframes & animation principles",
  "Day 44: Practice",
  "Day 45: Mini Project – Simple Animation",
  "Day 46: Revision",

  "Day 47: Print design basics",
  "Day 48: Flyers, posters & brochures",
  "Day 49: Print vs digital formats",
  "Day 50: Practice",
  "Day 51: Mini Project – Poster Design",
  "Day 52: Revision",

  "Day 53: Social media content design",
  "Day 54: Creating Instagram, Facebook posts",
  "Day 55: Carousel & banner design",
  "Day 56: Practice",
  "Day 57: Mini Project – Social Media Pack",
  "Day 58: Revision",

  "Day 59: Web graphics basics",
  "Day 60: Website banners & UI assets",
  "Day 61: Export & optimization for web",
  "Day 62: Practice",
  "Day 63: Mini Project – Web Banner Pack",
  "Day 64: Revision",

  "Day 65: Portfolio building basics",
  "Day 66: Organizing design projects",
  "Day 67: Personal branding for designers",
  "Day 68: Practice",
  "Day 69: Mini Portfolio Draft",
  "Day 70: Revision",

  "Day 71: Advanced Photoshop techniques",
  "Day 72: Compositing & masking advanced",
  "Day 73: Practice",
  "Day 74: Mini Project – Advanced Photo Manipulation",
  "Day 75: Revision",

  "Day 76: Advanced Illustrator techniques",
  "Day 77: Complex vector illustration",
  "Day 78: Practice",
  "Day 79: Mini Project – Illustrative Poster",
  "Day 80: Revision",

  "Day 81: UI/UX advanced design",
  "Day 82: User flows & high-fidelity prototype",
  "Day 83: Practice",
  "Day 84: Mini Project – App Prototype",
  "Day 85: Revision",

  "Day 86: Motion graphics advanced",
  "Day 87: Animation & transitions",
  "Day 88: Practice",
  "Day 89: Mini Project – Animated Social Post",
  "Day 90: Revision",

  "Day 91: Design thinking & problem solving",
  "Day 92: Creative ideation techniques",
  "Day 93: Practice",
  "Day 94: Mini Project – Design Challenge",
  "Day 95: Revision",

  "Day 96: Industry design trends",
  "Day 97: Case studies of famous brands",
  "Day 98: Practice",
  "Day 99: Mini Research Project",

  "Day 100: Resume building for designers",
  "Day 101: Portfolio finalization",
  "Day 102: LinkedIn & Behance setup",
  "Day 103: Apply for internships/jobs",
  "Day 104: Mock interviews",

  "Day 105: Freelance basics",
  "Day 106: Client communication",
  "Day 107: Pricing & contracts",
  "Day 108: Practice",
  "Day 109: Mini Freelance Project",

  "Day 110: Real-world design case studies",
  "Day 111: Branding project",
  "Day 112: Social media campaign",
  "Day 113: Practice",
  "Day 114: Revision",

  "Day 115: Time management & productivity for designers",
  "Day 116: Feedback incorporation",
  "Day 117: Portfolio updates",
  "Day 118: Practice",
  "Day 119: Final assessment",
  "Day 120: Next-step roadmap"
],
"UI/UX Designer": [

  "Day 1: Understand UI/UX Designer role & career paths",
  "Day 2: Basics of User Experience (UX)",
  "Day 3: Basics of User Interface (UI)",
  "Day 4: Design principles overview",
  "Day 5: Color theory & typography basics",
  "Day 6: Tools setup (Figma, Adobe XD, Sketch)",
  "Day 7: Revision",

  "Day 8: Introduction to Figma",
  "Day 9: Frames, components, and layers",
  "Day 10: Shapes, grids & layout basics",
  "Day 11: Typography & color application",
  "Day 12: Practice",
  "Day 13: Mini Project – Simple App Screen",
  "Day 14: Revision",

  "Day 15: User research basics",
  "Day 16: Personas & user journey mapping",
  "Day 17: User interviews & surveys",
  "Day 18: Practice",
  "Day 19: Mini Project – Persona & Journey Map",
  "Day 20: Revision",

  "Day 21: Wireframing basics",
  "Day 22: Low-fidelity wireframes",
  "Day 23: Wireframe tools & templates",
  "Day 24: Practice",
  "Day 25: Mini Project – Low-Fidelity Wireframes",
  "Day 26: Revision",

  "Day 27: Prototyping basics",
  "Day 28: High-fidelity prototypes",
  "Day 29: Interactive components & transitions",
  "Day 30: Practice",
  "Day 31: Mini Project – High-Fidelity Prototype",
  "Day 32: Revision",

  "Day 33: Usability testing basics",
  "Day 34: Test plan & script creation",
  "Day 35: Conduct usability testing",
  "Day 36: Analyze results & insights",
  "Day 37: Practice",
  "Day 38: Mini Project – Usability Test Report",
  "Day 39: Revision",

  "Day 40: UI patterns & components library",
  "Day 41: Design systems introduction",
  "Day 42: Accessibility & inclusive design",
  "Day 43: Practice",
  "Day 44: Mini Project – Design System Setup",
  "Day 45: Revision",

  "Day 46: Advanced Figma techniques",
  "Day 47: Auto-layout & constraints",
  "Day 48: Components variants & prototyping",
  "Day 49: Practice",
  "Day 50: Mini Project – Complex App Prototype",
  "Day 51: Revision",

  "Day 52: UX metrics & analytics",
  "Day 53: Conversion & engagement analysis",
  "Day 54: A/B testing basics",
  "Day 55: Practice",
  "Day 56: Mini Project – UX Analytics Report",
  "Day 57: Revision",

  "Day 58: UI design trends & best practices",
  "Day 59: Case studies of top apps",
  "Day 60: Style guides & branding in UI",
  "Day 61: Practice",
  "Day 62: Mini Project – Brand UI Kit",
  "Day 63: Revision",

  "Day 64: Mobile vs Web UI design",
  "Day 65: Responsive & adaptive design",
  "Day 66: Grids, breakpoints & layout adaptation",
  "Day 67: Practice",
  "Day 68: Mini Project – Responsive UI Screens",
  "Day 69: Revision",

  "Day 70: Interaction design basics",
  "Day 71: Micro-interactions & animations",
  "Day 72: Prototyping animations",
  "Day 73: Practice",
  "Day 74: Mini Project – Interactive Prototype",
  "Day 75: Revision",

  "Day 76: Collaboration & handoff with developers",
  "Day 77: Tools (Zeplin, Figma Inspect)",
  "Day 78: Design QA & feedback process",
  "Day 79: Practice",
  "Day 80: Mini Project – Developer Handoff",

  "Day 81: Portfolio planning",
  "Day 82: Selecting projects & case studies",
  "Day 83: Storytelling in UI/UX portfolio",
  "Day 84: Practice",
  "Day 85: Portfolio Draft",

  "Day 86: Resume building for UI/UX roles",
  "Day 87: LinkedIn & Behance setup",
  "Day 88: Apply for internships/jobs",
  "Day 89: Mock interviews",
  "Day 90: Revision",

  "Day 91: Advanced user research",
  "Day 92: Quantitative vs qualitative analysis",
  "Day 93: Surveys, heatmaps & analytics tools",
  "Day 94: Practice",
  "Day 95: Mini Project – Research Report",
  "Day 96: Revision",

  "Day 97: Advanced prototyping",
  "Day 98: Micro-interactions with Lottie/After Effects",
  "Day 99: Complex user flows",
  "Day 100: Practice",
  "Day 101: Mini Project – Interactive App Prototype",
  "Day 102: Revision",

  "Day 103: Accessibility testing",
  "Day 104: WCAG standards & guidelines",
  "Day 105: Tools for accessibility testing",
  "Day 106: Practice",
  "Day 107: Mini Project – Accessible Design Report",
  "Day 108: Revision",

  "Day 109: Industry design trends",
  "Day 110: Case studies of top products",
  "Day 111: UI/UX challenges & hackathons",
  "Day 112: Practice",
  "Day 113: Mini Research Project",

  "Day 114: Advanced portfolio preparation",
  "Day 115: Presenting design process & case studies",
  "Day 116: Feedback incorporation",
  "Day 117: Final portfolio",
  "Day 118: Mock presentation & interviews",
  "Day 119: Apply for jobs/internships",
  "Day 120: Downloadable portfolio creation"
],
"Animator": [

  "Day 1: Understand Animator role & career paths",
  "Day 2: Basics of animation & history",
  "Day 3: Principles of animation (12 principles)",
  "Day 4: Storytelling basics",
  "Day 5: Visual language & composition",
  "Day 6: Tools setup (Adobe Animate, After Effects, Blender)",
  "Day 7: Revision",

  "Day 8: Adobe Animate basics",
  "Day 9: Frames, layers & timeline",
  "Day 10: Keyframes & motion paths",
  "Day 11: Shape & character animation",
  "Day 12: Practice",
  "Day 13: Mini Project – Simple 2D Animation",
  "Day 14: Revision",

  "Day 15: Adobe After Effects basics",
  "Day 16: Layers, masks & compositions",
  "Day 17: Motion graphics basics",
  "Day 18: Text & shape animation",
  "Day 19: Practice",
  "Day 20: Mini Project – Animated Logo",
  "Day 21: Revision",

  "Day 22: Storyboarding basics",
  "Day 23: Visual storytelling techniques",
  "Day 24: Character design & poses",
  "Day 25: Practice",
  "Day 26: Mini Project – Storyboard 1 Scene",
  "Day 27: Revision",

  "Day 28: Timing & spacing in animation",
  "Day 29: Squash & stretch, anticipation, follow-through",
  "Day 30: Practice",
  "Day 31: Mini Project – Character Movement Animation",
  "Day 32: Revision",

  "Day 33: Blender basics (3D animation)",
  "Day 34: 3D modeling & rigging",
  "Day 35: Keyframe animation in 3D",
  "Day 36: Lighting & camera basics",
  "Day 37: Practice",
  "Day 38: Mini Project – Simple 3D Animation",
  "Day 39: Revision",

  "Day 40: Character rigging & skeleton setup",
  "Day 41: Skinning & weight painting",
  "Day 42: Animation cycles (walk, run, jump)",
  "Day 43: Practice",
  "Day 44: Mini Project – Character Walk Cycle",
  "Day 45: Revision",

  "Day 46: Lip-sync & facial animation",
  "Day 47: Expressions & emotions",
  "Day 48: Practice",
  "Day 49: Mini Project – Character Dialogue Animation",
  "Day 50: Revision",

  "Day 51: Motion graphics advanced",
  "Day 52: Effects, particle systems, transitions",
  "Day 53: Camera movements & parallax",
  "Day 54: Practice",
  "Day 55: Mini Project – Animated Promo Video",
  "Day 56: Revision",

  "Day 57: Compositing basics",
  "Day 58: Layers, masks & color grading",
  "Day 59: Video editing basics",
  "Day 60: Practice",
  "Day 61: Mini Project – Composited Scene",
  "Day 62: Revision",

  "Day 63: Animation workflow & pipeline",
  "Day 64: Asset management",
  "Day 65: Collaboration with team",
  "Day 66: Practice",
  "Day 67: Mini Project – Small Team Workflow Simulation",
  "Day 68: Revision",

  "Day 69: Advanced Blender animation",
  "Day 70: Physics & dynamics simulations",
  "Day 71: Particle effects & smoke",
  "Day 72: Practice",
  "Day 73: Mini Project – Simulation Scene",
  "Day 74: Revision",

  "Day 75: Environment & background design",
  "Day 76: Lighting & rendering",
  "Day 77: Camera animation & storytelling",
  "Day 78: Practice",
  "Day 79: Mini Project – Short Animated Scene",
  "Day 80: Revision",

  "Day 81: Portfolio planning",
  "Day 82: Selecting projects & clips",
  "Day 83: Storytelling in portfolio",
  "Day 84: Practice",
  "Day 85: Portfolio Draft",

  "Day 86: Resume building for animators",
  "Day 87: LinkedIn, ArtStation, Behance setup",
  "Day 88: Apply for internships/jobs",
  "Day 89: Mock interviews",
  "Day 90: Revision",

  "Day 91: Advanced motion graphics",
  "Day 92: 3D camera tracking & compositing",
  "Day 93: Visual effects integration",
  "Day 94: Practice",
  "Day 95: Mini Project – Advanced Promo Video",
  "Day 96: Revision",

  "Day 97: Character animation advanced",
  "Day 98: Acting & performance in animation",
  "Day 99: Practice",
  "Day 100: Mini Project – Short Character Animation",
  "Day 101: Revision",

  "Day 102: Animation for games basics",
  "Day 103: Sprite animation & rigging for game engines",
  "Day 104: Practice",
  "Day 105: Mini Project – Game Character Animation",
  "Day 106: Revision",

  "Day 107: Industry trends in animation",
  "Day 108: Case studies of top studios",
  "Day 109: Practice",
  "Day 110: Mini Research Project",

  "Day 111: Portfolio finalization",
  "Day 112: Presenting animation projects & reels",
  "Day 113: Feedback incorporation",
  "Day 114: Practice",
  "Day 115: Job/freelance applications",
  "Day 116: Mock interviews",
  "Day 117: Revision",

  "Day 118: Freelancing basics",
  "Day 119: Client communication & contracts",
  "Day 120: Downloadable portfolio creation"
],
"Illustrator": [

  "Day 1: Understand Illustrator/Digital Artist role & career paths",
  "Day 2: Basics of digital illustration",
  "Day 3: Design principles overview",
  "Day 4: Color theory basics",
  "Day 5: Typography basics",
  "Day 6: Tools setup (Adobe Illustrator, tablet if available)",
  "Day 7: Revision",

  "Day 8: Adobe Illustrator basics",
  "Day 9: Workspace, tools & panels overview",
  "Day 10: Shapes, paths & layers",
  "Day 11: Pen tool & basic vector drawing",
  "Day 12: Practice",
  "Day 13: Mini Project – Simple Vector Icons",
  "Day 14: Revision",

  "Day 15: Color application & gradients",
  "Day 16: Swatches & color palettes",
  "Day 17: Blending modes & opacity",
  "Day 18: Practice",
  "Day 19: Mini Project – Colored Vector Illustration",
  "Day 20: Revision",

  "Day 21: Typography in Illustrator",
  "Day 22: Working with text & fonts",
  "Day 23: Text effects & alignment",
  "Day 24: Practice",
  "Day 25: Mini Project – Typographic Poster",
  "Day 26: Revision",

  "Day 27: Advanced pen tool techniques",
  "Day 28: Curves, anchors & bezier paths",
  "Day 29: Tracing & image to vector conversion",
  "Day 30: Practice",
  "Day 31: Mini Project – Vector Trace Artwork",
  "Day 32: Revision",

  "Day 33: Layer management & organization",
  "Day 34: Masks & clipping paths",
  "Day 35: Symbols, patterns & brushes",
  "Day 36: Practice",
  "Day 37: Mini Project – Pattern Design",
  "Day 38: Revision",

  "Day 39: Character illustration basics",
  "Day 40: Anatomy & proportions",
  "Day 41: Sketch to vector workflow",
  "Day 42: Practice",
  "Day 43: Mini Project – Cartoon Character Illustration",
  "Day 44: Revision",

  "Day 45: Environment & background illustration",
  "Day 46: Perspective basics",
  "Day 47: Lighting & shadows in vector",
  "Day 48: Practice",
  "Day 49: Mini Project – Vector Landscape Illustration",
  "Day 50: Revision",

  "Day 51: Icon design",
  "Day 52: Flat & line icon styles",
  "Day 53: Grid & alignment for icons",
  "Day 54: Practice",
  "Day 55: Mini Project – Icon Set Design",
  "Day 56: Revision",

  "Day 57: Infographics design",
  "Day 58: Charts & diagrams in Illustrator",
  "Day 59: Data visualization basics",
  "Day 60: Practice",
  "Day 61: Mini Project – Infographic Illustration",
  "Day 62: Revision",

  "Day 63: Advanced vector techniques",
  "Day 64: Gradient mesh & blends",
  "Day 65: Advanced brushes & effects",
  "Day 66: Practice",
  "Day 67: Mini Project – Detailed Vector Illustration",
  "Day 68: Revision",

  "Day 69: Storytelling through illustration",
  "Day 70: Visual narrative basics",
  "Day 71: Scene composition & flow",
  "Day 72: Practice",
  "Day 73: Mini Project – Illustrated Story Scene",
  "Day 74: Revision",

  "Day 75: Branding & illustration",
  "Day 76: Logo illustration basics",
  "Day 77: Packaging & product illustration",
  "Day 78: Practice",
  "Day 79: Mini Project – Brand Illustration Package",
  "Day 80: Revision",

  "Day 81: Portfolio planning",
  "Day 82: Selecting illustration projects",
  "Day 83: Showcasing process & final artwork",
  "Day 84: Practice",
  "Day 85: Portfolio Draft",

  "Day 86: Resume & social media setup",
  "Day 87: Behance, ArtStation, Instagram setup",
  "Day 88: Apply for freelance or jobs",
  "Day 89: Mock interviews",
  "Day 90: Revision",

  "Day 91: Character illustration advanced",
  "Day 92: Action poses & dynamic compositions",
  "Day 93: Expressions & emotions",
  "Day 94: Practice",
  "Day 95: Mini Project – Advanced Character Illustration",
  "Day 96: Revision",

  "Day 97: Environment illustration advanced",
  "Day 98: Complex perspective & lighting",
  "Day 99: Atmospheric effects",
  "Day 100: Practice",
  "Day 101: Mini Project – Detailed Environment Illustration",
  "Day 102: Revision",

  "Day 103: Digital painting basics in Illustrator",
  "Day 104: Brush settings & textures",
  "Day 105: Shading & highlights",
  "Day 106: Practice",
  "Day 107: Mini Project – Digital Painting",
  "Day 108: Revision",

  "Day 109: Industry trends in illustration",
  "Day 110: Study works of top illustrators",
  "Day 111: Participate in illustration challenges",
  "Day 112: Practice",
  "Day 113: Mini Research Project",

  "Day 114: Portfolio finalization",
  "Day 115: Showcasing process & case studies",
  "Day 116: Feedback incorporation",
  "Day 117: Final portfolio",
  "Day 118: Mock interviews",
  "Day 119: Apply for jobs/freelance",
  "Day 120: Downloadable portfolio creation"
],
"Film Editor": [

  "Day 1: Understand Film Editor role & career paths",
  "Day 2: Basics of film editing & storytelling",
  "Day 3: Types of editing (linear vs non-linear)",
  "Day 4: Editing principles & pacing",
  "Day 5: Tools setup (Adobe Premiere Pro, Final Cut Pro, DaVinci Resolve)",
  "Day 6: Video formats & resolutions",
  "Day 7: Revision",

  "Day 8: Adobe Premiere Pro basics",
  "Day 9: Workspace, panels & tools overview",
  "Day 10: Importing & organizing media",
  "Day 11: Timeline basics & cuts",
  "Day 12: Practice",
  "Day 13: Mini Project – Simple Video Cut",
  "Day 14: Revision",

  "Day 15: Transitions & effects basics",
  "Day 16: Adding video/audio effects",
  "Day 17: Keyframes & motion effects",
  "Day 18: Practice",
  "Day 19: Mini Project – Short Edited Video",
  "Day 20: Revision",

  "Day 21: Audio editing basics",
  "Day 22: Audio levels, noise reduction",
  "Day 23: Background music & sound effects",
  "Day 24: Practice",
  "Day 25: Mini Project – Audio Integrated Video",
  "Day 26: Revision",

  "Day 27: Color correction basics",
  "Day 28: Color grading principles",
  "Day 29: Using scopes & LUTs",
  "Day 30: Practice",
  "Day 31: Mini Project – Color Corrected Scene",
  "Day 32: Revision",

  "Day 33: Multi-camera editing",
  "Day 34: Syncing & switching cameras",
  "Day 35: Practice",
  "Day 36: Mini Project – Multi-Camera Scene",
  "Day 37: Revision",

  "Day 38: Motion graphics basics",
  "Day 39: Titles & lower thirds",
  "Day 40: Intro/outro animations",
  "Day 41: Practice",
  "Day 42: Mini Project – Video with Motion Graphics",
  "Day 43: Revision",

  "Day 44: Advanced transitions & effects",
  "Day 45: Masking & tracking",
  "Day 46: Practice",
  "Day 47: Mini Project – Advanced Editing Scene",
  "Day 48: Revision",

  "Day 49: Visual effects basics",
  "Day 50: Green screen & keying",
  "Day 51: Compositing basics",
  "Day 52: Practice",
  "Day 53: Mini Project – VFX Scene",
  "Day 54: Revision",

  "Day 55: Storyboarding basics for editors",
  "Day 56: Understanding director's vision",
  "Day 57: Editing for narrative pacing",
  "Day 58: Practice",
  "Day 59: Mini Project – Storyboard to Edit",
  "Day 60: Revision",

  "Day 61: Export & delivery",
  "Day 62: Export formats & compression",
  "Day 63: Workflow for YouTube, TV & Cinema",
  "Day 64: Practice",
  "Day 65: Mini Project – Final Exported Video",
  "Day 66: Revision",

  "Day 67: Collaboration with filmmakers",
  "Day 68: Feedback & revisions workflow",
  "Day 69: Practice",
  "Day 70: Mini Project – Collaborative Editing Task",
  "Day 71: Revision",

  "Day 72: Editing short films",
  "Day 73: Editing music videos",
  "Day 74: Editing commercials",
  "Day 75: Practice",
  "Day 76: Mini Project – Short Film Edit",
  "Day 77: Revision",

  "Day 78: Advanced color grading",
  "Day 79: Creative LUTs & looks",
  "Day 80: Practice",
  "Day 81: Mini Project – Cinematic Scene",
  "Day 82: Revision",

  "Day 83: Sound design basics",
  "Day 84: Foley & ambient sounds",
  "Day 85: Mixing & mastering",
  "Day 86: Practice",
  "Day 87: Mini Project – Sound Designed Video",
  "Day 88: Revision",

  "Day 89: Portfolio planning",
  "Day 90: Selecting edited projects",
  "Day 91: Showcasing process & final videos",
  "Day 92: Practice",
  "Day 93: Portfolio Draft",
  "Day 94: Revision",

  "Day 95: Resume & social media setup",
  "Day 96: LinkedIn, Vimeo, YouTube setup",
  "Day 97: Apply for internships/jobs",
  "Day 98: Mock interviews",
  "Day 99: Revision",

  "Day 100: Advanced Premiere/DaVinci techniques",
  "Day 101: Motion tracking & stabilization",
  "Day 102: Practice",
  "Day 103: Mini Project – Complex Scene Edit",
  "Day 104: Revision",

  "Day 105: Editing feature-length films basics",
  "Day 106: Scene assembly & pacing",
  "Day 107: Practice",
  "Day 108: Mini Project – Feature Scene",
  "Day 109: Revision",

  "Day 110: Working with raw footage",
  "Day 111: Multi-format footage workflow",
  "Day 112: Practice",
  "Day 113: Mini Project – Raw Footage Edit",
  "Day 114: Revision",

  "Day 115: Industry trends in film editing",
  "Day 116: Case studies of top editors",
  "Day 117: Practice",
  "Day 118: Mini Research Project",

  "Day 119: Portfolio finalization",
  "Day 120: Job/freelance applications "
],
"Game Designer": [

  "Day 1: Understand Game Designer role & career paths",
  "Day 2: Basics of game design",
  "Day 3: Game genres & mechanics overview",
  "Day 4: Storytelling in games",
  "Day 5: Game design principles (balance, engagement, pacing)",
  "Day 6: Tools setup (Unity, Unreal Engine, Figma, Blender)",
  "Day 7: Revision",

  "Day 8: Game loop & gameplay mechanics basics",
  "Day 9: Player experience (UX in games)",
  "Day 10: Level design basics",
  "Day 11: Prototyping game ideas",
  "Day 12: Practice",
  "Day 13: Mini Project – Simple Game Prototype",
  "Day 14: Revision",

  "Day 15: Game storyboarding & narrative design",
  "Day 16: Character design basics",
  "Day 17: Environment design basics",
  "Day 18: Practice",
  "Day 19: Mini Project – Game Storyboard & Characters",
  "Day 20: Revision",

  "Day 21: User interface (UI) in games",
  "Day 22: HUD, menus & buttons",
  "Day 23: Prototyping UI in Figma/Unity",
  "Day 24: Practice",
  "Day 25: Mini Project – Game UI Prototype",
  "Day 26: Revision",

  "Day 27: Game mechanics advanced",
  "Day 28: Balancing gameplay",
  "Day 29: Player engagement & rewards system",
  "Day 30: Practice",
  "Day 31: Mini Project – Advanced Game Prototype",
  "Day 32: Revision",

  "Day 33: Level design advanced",
  "Day 34: Puzzles, challenges & pacing",
  "Day 35: Environment storytelling",
  "Day 36: Practice",
  "Day 37: Mini Project – Level Design Prototype",
  "Day 38: Revision",

  "Day 39: Game physics basics",
  "Day 40: Collision detection & movement",
  "Day 41: Game AI basics (enemies, NPCs)",
  "Day 42: Practice",
  "Day 43: Mini Project – AI Controlled NPC",
  "Day 44: Revision",

  "Day 45: Multiplayer basics",
  "Day 46: Networking & player interactions",
  "Day 47: Practice",
  "Day 48: Mini Project – Local Multiplayer Prototype",
  "Day 49: Revision",

  "Day 50: Sound design in games",
  "Day 51: Background music & effects",
  "Day 52: Implementation in Unity/Unreal",
  "Day 53: Practice",
  "Day 54: Mini Project – Game Sound Integration",
  "Day 55: Revision",

  "Day 56: Game prototyping tools (Unity/Unreal)",
  "Day 57: Asset import & animation basics",
  "Day 58: Scripting basic interactions",
  "Day 59: Practice",
  "Day 60: Mini Project – Interactive Game Prototype",
  "Day 61: Revision",

  "Day 62: Iterative design & playtesting",
  "Day 63: Gathering feedback & iteration",
  "Day 64: Practice",
  "Day 65: Mini Project – Playtesting Session",
  "Day 66: Revision",

  "Day 67: Visual style & art direction",
  "Day 68: UI/UX refinement",
  "Day 69: Story & dialogue integration",
  "Day 70: Practice",
  "Day 71: Mini Project – Refined Game Prototype",
  "Day 72: Revision",

  "Day 73: Advanced game mechanics",
  "Day 74: Power-ups, levels, progression systems",
  "Day 75: Practice",
  "Day 76: Mini Project – Feature-Rich Game Prototype",
  "Day 77: Revision",

  "Day 78: Animation basics for games",
  "Day 79: Character animation cycles",
  "Day 80: Environmental animation",
  "Day 81: Practice",
  "Day 82: Mini Project – Animated Game Scene",
  "Day 83: Revision",

  "Day 84: Advanced prototyping & integration",
  "Day 85: Scripting complex interactions",
  "Day 86: Practice",
  "Day 87: Mini Project – Interactive Game Level",
  "Day 88: Revision",

  "Day 89: Portfolio planning",
  "Day 90: Selecting game projects",
  "Day 91: Recording gameplay & demos",
  "Day 92: Practice",
  "Day 93: Portfolio Draft",
  "Day 94: Revision",

  "Day 95: Resume & social media setup",
  "Day 96: LinkedIn, ArtStation, YouTube setup",
  "Day 97: Apply for internships/jobs",
  "Day 98: Mock interviews",
  "Day 99: Revision",

  "Day 100: Game testing & QA",
  "Day 101: Bug fixing & polishing",
  "Day 102: Practice",
  "Day 103: Mini Project – Polished Game Prototype",
  "Day 104: Revision",

  "Day 105: Industry trends in game design",
  "Day 106: Study top game studios & games",
  "Day 107: Practice",
  "Day 108: Mini Research Project",

  "Day 109: Advanced mechanics & features",
  "Day 110: AI & advanced gameplay systems",
  "Day 111: Practice",
  "Day 112: Mini Project – Advanced Game Feature",
  "Day 113: Revision",

  "Day 114: Multiplayer & social features",
  "Day 115: Cloud saving & leaderboard integration",
  "Day 116: Practice",
  "Day 117: Mini Project – Social Game Prototype",
  "Day 118: Revision",

  "Day 119: Portfolio finalization",
  "Day 120: Job/freelance applications "
],
"Art Director": [

  "Day 1: Understand Art Director role & career paths",
  "Day 2: Basics of visual communication & design",
  "Day 3: Design principles overview (balance, contrast, hierarchy)",
  "Day 4: Color theory & typography basics",
  "Day 5: Composition & visual storytelling",
  "Day 6: Tools setup (Adobe Photoshop, Illustrator, Figma, After Effects)",
  "Day 7: Revision",

  "Day 8: Design research & inspiration",
  "Day 9: Mood boards & style exploration",
  "Day 10: Competitive analysis & trend study",
  "Day 11: Practice",
  "Day 12: Mini Project – Mood Board Creation",
  "Day 13: Revision",

  "Day 14: Branding basics",
  "Day 15: Logo design principles",
  "Day 16: Color palette & typography for brands",
  "Day 17: Practice",
  "Day 18: Mini Project – Brand Identity",
  "Day 19: Revision",

  "Day 20: Layout & composition advanced",
  "Day 21: Grid systems & alignment",
  "Day 22: Visual hierarchy & focal points",
  "Day 23: Practice",
  "Day 24: Mini Project – Poster/Print Design",
  "Day 25: Revision",

  "Day 26: Digital illustration basics",
  "Day 27: Adobe Illustrator & Photoshop fundamentals",
  "Day 28: Character & environment sketching",
  "Day 29: Practice",
  "Day 30: Mini Project – Illustration for Campaign",
  "Day 31: Revision",

  "Day 32: Motion graphics basics",
  "Day 33: Adobe After Effects introduction",
  "Day 34: Keyframes & animation principles",
  "Day 35: Practice",
  "Day 36: Mini Project – Animated Social Post",
  "Day 37: Revision",

  "Day 38: Photography basics for art direction",
  "Day 39: Composition, lighting & storytelling",
  "Day 40: Stock photo curation",
  "Day 41: Practice",
  "Day 42: Mini Project – Visual Concept Photo Board",
  "Day 43: Revision",

  "Day 44: UX/UI principles for Art Directors",
  "Day 45: Wireframes & prototypes overview",
  "Day 46: User experience basics",
  "Day 47: Practice",
  "Day 48: Mini Project – App Concept Mockup",
  "Day 49: Revision",

  "Day 50: Creative strategy basics",
  "Day 51: Campaign concept development",
  "Day 52: Messaging & storytelling alignment",
  "Day 53: Practice",
  "Day 54: Mini Project – Campaign Concept Board",
  "Day 55: Revision",

  "Day 56: Typography advanced",
  "Day 57: Custom fonts & visual impact",
  "Day 58: Hierarchy & readability in design",
  "Day 59: Practice",
  "Day 60: Mini Project – Typographic Poster",
  "Day 61: Revision",

  "Day 62: Art direction in advertising",
  "Day 63: Print & digital campaign basics",
  "Day 64: Practice",
  "Day 65: Mini Project – Advertising Visual Concept",
  "Day 66: Revision",

  "Day 67: Team leadership basics",
  "Day 68: Creative briefing & feedback",
  "Day 69: Managing projects & timelines",
  "Day 70: Practice",
  "Day 71: Mini Project – Team Creative Brief",
  "Day 72: Revision",

  "Day 73: Visual consistency & brand guidelines",
  "Day 74: Style guides & templates",
  "Day 75: Practice",
  "Day 76: Mini Project – Brand Style Guide",
  "Day 77: Revision",

  "Day 78: Portfolio planning",
  "Day 79: Selecting projects & case studies",
  "Day 80: Showcasing design process & leadership",
  "Day 81: Practice",
  "Day 82: Portfolio Draft",
  "Day 83: Revision",

  "Day 84: Resume & social media setup",
  "Day 85: LinkedIn, Behance, Dribbble setup",
  "Day 86: Apply for internships/jobs",
  "Day 87: Mock interviews",
  "Day 88: Revision",

  "Day 89: Advanced art direction projects",
  "Day 90: Integrated campaign design",
  "Day 91: Multi-channel visual storytelling",
  "Day 92: Practice",
  "Day 93: Mini Project – Campaign Mockup",
  "Day 94: Revision",

  "Day 95: Motion graphics advanced",
  "Day 96: Animation for social & web",
  "Day 97: Practice",
  "Day 98: Mini Project – Animated Campaign",
  "Day 99: Revision",

  "Day 100: Photography & image manipulation advanced",
  "Day 101: Photoshop composites & retouching",
  "Day 102: Practice",
  "Day 103: Mini Project – High-Quality Campaign Image",
  "Day 104: Revision",

  "Day 105: Creative problem solving",
  "Day 106: Ideation & brainstorming techniques",
  "Day 107: Practice",
  "Day 108: Mini Project – Creative Challenge",
  "Day 109: Revision",

  "Day 110: Industry trends & case studies",
  "Day 111: Study top agencies & art directors",
  "Day 112: Practice",
  "Day 113: Mini Research Project",

  "Day 114: Portfolio finalization",
  "Day 115: Showcasing process, campaigns & leadership",
  "Day 116: Feedback incorporation",
  "Day 117: Final portfolio",
  "Day 118: Mock interviews",
  "Day 119: Apply for jobs/freelance",
  "Day 120: Downloadable portfolio creation"
],

#education and content for more careers can be added here
"Teacher": [

  "Day 1: Understand Teacher role & career paths",
  "Day 2: Basics of pedagogy & teaching principles",
  "Day 3: Learning theories (Behaviorism, Constructivism, Cognitivism)",
  "Day 4: Classroom management basics",
  "Day 5: Teaching ethics & professionalism",
  "Day 6: Lesson planning basics",
  "Day 7: Revision",

  "Day 8: Curriculum understanding & standards",
  "Day 9: Subject knowledge review",
  "Day 10: Bloom’s Taxonomy & learning objectives",
  "Day 11: Practice",
  "Day 12: Mini Project – Draft a Lesson Plan",
  "Day 13: Revision",

  "Day 14: Teaching aids & multimedia in classroom",
  "Day 15: Visual aids, PPTs & props",
  "Day 16: Interactive teaching techniques",
  "Day 17: Practice",
  "Day 18: Mini Project – Create Teaching Aid",
  "Day 19: Revision",

  "Day 20: Questioning techniques & classroom interaction",
  "Day 21: Student engagement strategies",
  "Day 22: Practice",
  "Day 23: Mini Project – Conduct Mock Teaching Session",
  "Day 24: Revision",

  "Day 25: Lesson planning advanced",
  "Day 26: Unit planning & pacing",
  "Day 27: Differentiated instruction techniques",
  "Day 28: Practice",
  "Day 29: Mini Project – Detailed Lesson Plan",
  "Day 30: Revision",

  "Day 31: Assessment & evaluation basics",
  "Day 32: Formative & summative assessments",
  "Day 33: Creating quizzes & tests",
  "Day 34: Practice",
  "Day 35: Mini Project – Design Assessment Tools",
  "Day 36: Revision",

  "Day 37: Classroom management advanced",
  "Day 38: Handling discipline & conflicts",
  "Day 39: Motivating students",
  "Day 40: Practice",
  "Day 41: Mini Project – Classroom Management Strategy",
  "Day 42: Revision",

  "Day 43: Teaching soft skills",
  "Day 44: Communication & presentation skills",
  "Day 45: Critical thinking & problem-solving",
  "Day 46: Practice",
  "Day 47: Mini Project – Soft Skill Lesson",
  "Day 48: Revision",

  "Day 49: Technology in teaching",
  "Day 50: Using LMS (Google Classroom, Moodle)",
  "Day 51: Online teaching best practices",
  "Day 52: Practice",
  "Day 53: Mini Project – Online Lesson Plan",
  "Day 54: Revision",

  "Day 55: Inclusive education",
  "Day 56: Teaching students with learning disabilities",
  "Day 57: Adapted materials & strategies",
  "Day 58: Practice",
  "Day 59: Mini Project – Inclusive Lesson Plan",
  "Day 60: Revision",

  "Day 61: Feedback & reflection",
  "Day 62: Peer review & self-assessment",
  "Day 63: Practice",
  "Day 64: Mini Project – Feedback Implementation",
  "Day 65: Revision",

  "Day 66: Classroom observation",
  "Day 67: Note-taking & evaluation",
  "Day 68: Practice",
  "Day 69: Mini Project – Observe & Report",
  "Day 70: Revision",

  "Day 71: Lesson delivery advanced",
  "Day 72: Storytelling & engagement techniques",
  "Day 73: Practice",
  "Day 74: Mini Project – Conduct a Full Lesson",
  "Day 75: Revision",

  "Day 76: Student assessment advanced",
  "Day 77: Rubrics & grading standards",
  "Day 78: Practice",
  "Day 79: Mini Project – Grade Assignments",
  "Day 80: Revision",

  "Day 81: Professional development",
  "Day 82: Continuing education & workshops",
  "Day 83: Networking with educators",
  "Day 84: Practice",
  "Day 85: Mini Project – Professional Growth Plan",
  "Day 86: Revision",

  "Day 87: Mentoring & coaching students",
  "Day 88: Academic counseling basics",
  "Day 89: Practice",
  "Day 90: Mini Project – Mentoring Plan",
  "Day 91: Revision",

  "Day 92: Classroom innovation",
  "Day 93: Gamification & interactive learning",
  "Day 94: Practice",
  "Day 95: Mini Project – Innovative Lesson Plan",
  "Day 96: Revision",

  "Day 97: Research in education",
  "Day 98: Action research & reflective practice",
  "Day 99: Practice",
  "Day 100: Mini Project – Small Research Project",
  "Day 101: Revision",

  "Day 102: Handling exams & assessments",
  "Day 103: Remedial teaching & support",
  "Day 104: Practice",
  "Day 105: Mini Project – Exam Preparation Strategy",
  "Day 106: Revision",

  "Day 107: Communication with parents",
  "Day 108: Reporting & progress tracking",
  "Day 109: Practice",
  "Day 110: Mini Project – Parent-Teacher Report",
  "Day 111: Revision",

  "Day 112: Collaboration with colleagues",
  "Day 113: Team teaching & planning",
  "Day 114: Practice",
  "Day 115: Mini Project – Collaborative Lesson",
  "Day 116: Revision",

  "Day 117: Portfolio planning for teachers",
  "Day 118: Collecting teaching evidence & projects",
  "Day 119: Practice",
  "Day 120: Mini Project – Teaching Portfolio Creation"
],
"Professor": [

  "Day 1: Understand Professor role & career paths",
  "Day 2: Basics of higher education teaching",
  "Day 3: Academic responsibilities overview",
  "Day 4: Teaching ethics & professionalism",
  "Day 5: Pedagogy for university students",
  "Day 6: Curriculum & course design basics",
  "Day 7: Revision",

  "Day 8: Subject mastery review",
  "Day 9: Latest trends & research in subject",
  "Day 10: Learning objectives & outcomes",
  "Day 11: Practice",
  "Day 12: Mini Project – Draft a Course Outline",
  "Day 13: Revision",

  "Day 14: Lecture planning & structuring",
  "Day 15: Effective presentation & slide design",
  "Day 16: Storytelling for higher education",
  "Day 17: Practice",
  "Day 18: Mini Project – Prepare a Lecture",
  "Day 19: Revision",

  "Day 20: Student engagement strategies",
  "Day 21: Questioning & interactive teaching",
  "Day 22: Discussion facilitation techniques",
  "Day 23: Practice",
  "Day 24: Mini Project – Conduct Mock Lecture",
  "Day 25: Revision",

  "Day 26: Assessment & evaluation basics",
  "Day 27: Designing assignments & exams",
  "Day 28: Grading rubrics & feedback methods",
  "Day 29: Practice",
  "Day 30: Mini Project – Design Assessment Tools",
  "Day 31: Revision",

  "Day 32: Research basics",
  "Day 33: Literature review & research questions",
  "Day 34: Research methodology & design",
  "Day 35: Practice",
  "Day 36: Mini Project – Research Proposal Draft",
  "Day 37: Revision",

  "Day 38: Academic writing basics",
  "Day 39: Writing papers & journals",
  "Day 40: Referencing & citations",
  "Day 41: Practice",
  "Day 42: Mini Project – Write a Short Research Article",
  "Day 43: Revision",

  "Day 44: Seminar & conference presentation skills",
  "Day 45: Preparing posters & presentations",
  "Day 46: Practice",
  "Day 47: Mini Project – Present a Research Topic",
  "Day 48: Revision",

  "Day 49: Mentoring & advising students",
  "Day 50: Supervision techniques",
  "Day 51: Career guidance & counseling",
  "Day 52: Practice",
  "Day 53: Mini Project – Student Mentorship Plan",
  "Day 54: Revision",

  "Day 55: Online & hybrid teaching",
  "Day 56: Learning management systems (LMS)",
  "Day 57: Online teaching best practices",
  "Day 58: Practice",
  "Day 59: Mini Project – Online Course Module",
  "Day 60: Revision",

  "Day 61: Academic leadership basics",
  "Day 62: Departmental responsibilities",
  "Day 63: Team collaboration & management",
  "Day 64: Practice",
  "Day 65: Mini Project – Departmental Task Simulation",
  "Day 66: Revision",

  "Day 67: Advanced research skills",
  "Day 68: Data analysis & interpretation",
  "Day 69: Research ethics & compliance",
  "Day 70: Practice",
  "Day 71: Mini Project – Research Data Analysis",
  "Day 72: Revision",

  "Day 73: Grant writing basics",
  "Day 74: Research funding sources",
  "Day 75: Proposal writing & submission",
  "Day 76: Practice",
  "Day 77: Mini Project – Draft Research Grant Proposal",
  "Day 78: Revision",

  "Day 79: Publishing & peer review process",
  "Day 80: Selecting journals & conferences",
  "Day 81: Practice",
  "Day 82: Mini Project – Submit Paper Draft",
  "Day 83: Revision",

  "Day 84: Curriculum development advanced",
  "Day 85: Syllabus design for multiple courses",
  "Day 86: Practice",
  "Day 87: Mini Project – Multi-Course Curriculum",
  "Day 88: Revision",

  "Day 89: Interdisciplinary teaching & research",
  "Day 90: Collaborative project planning",
  "Day 91: Practice",
  "Day 92: Mini Project – Interdisciplinary Module",
  "Day 93: Revision",

  "Day 94: Academic networking",
  "Day 95: Conferences, workshops & online communities",
  "Day 96: Practice",
  "Day 97: Mini Project – Professional Networking Plan",
  "Day 98: Revision",

  "Day 99: Advanced teaching techniques",
  "Day 100: Case-based & problem-based learning",
  "Day 101: Practice",
  "Day 102: Mini Project – Case Study Lesson",
  "Day 103: Revision",

  "Day 104: Evaluating educational technologies",
  "Day 105: EdTech tools & innovations",
  "Day 106: Practice",
  "Day 107: Mini Project – EdTech Integration Plan",
  "Day 108: Revision",

  "Day 109: Professional development & certifications",
  "Day 110: Academic portfolio building",
  "Day 111: Practice",
  "Day 112: Mini Project – Academic Portfolio Draft",
  "Day 113: Revision",

  "Day 114: Student research supervision",
  "Day 115: Co-authoring papers & presentations",
  "Day 116: Practice",
  "Day 117: Mini Project – Supervise Small Research",
  "Day 118: Revision",

  "Day 119: Portfolio finalization",
  "Day 120: Job/faculty applications "
],
"Content Writer": [

  "Day 1: Understand Content Writer role & career paths",
  "Day 2: Basics of writing & communication",
  "Day 3: Grammar & vocabulary essentials",
  "Day 4: Sentence structure & paragraph flow",
  "Day 5: Types of content (blogs, articles, social media, copywriting)",
  "Day 6: Tools setup (Google Docs, Grammarly, Hemingway Editor)",
  "Day 7: Revision",

  "Day 8: Understanding audience & niche",
  "Day 9: Target audience research",
  "Day 10: Content planning basics",
  "Day 11: Practice",
  "Day 12: Mini Project – Audience Analysis",
  "Day 13: Revision",

  "Day 14: Blog writing basics",
  "Day 15: Structure, headings & readability",
  "Day 16: Writing engaging introductions",
  "Day 17: Practice",
  "Day 18: Mini Project – Draft First Blog",
  "Day 19: Revision",

  "Day 20: SEO basics for content writers",
  "Day 21: Keywords & search intent",
  "Day 22: Meta tags & on-page SEO",
  "Day 23: Practice",
  "Day 24: Mini Project – SEO Optimized Blog",
  "Day 25: Revision",

  "Day 26: Copywriting basics",
  "Day 27: Headlines & CTAs",
  "Day 28: Persuasive writing techniques",
  "Day 29: Practice",
  "Day 30: Mini Project – Sales Copy",
  "Day 31: Revision",

  "Day 32: Storytelling in content",
  "Day 33: Narrative techniques & hooks",
  "Day 34: Emotional engagement",
  "Day 35: Practice",
  "Day 36: Mini Project – Story-based Article",
  "Day 37: Revision",

  "Day 38: Social media content",
  "Day 39: Platform-specific writing (Instagram, Twitter, LinkedIn)",
  "Day 40: Content calendars & scheduling",
  "Day 41: Practice",
  "Day 42: Mini Project – Social Media Posts",
  "Day 43: Revision",

  "Day 44: Technical writing basics",
  "Day 45: Documentation & manuals",
  "Day 46: Practice",
  "Day 47: Mini Project – Technical Document Draft",
  "Day 48: Revision",

  "Day 49: Editing & proofreading basics",
  "Day 50: Self-editing techniques",
  "Day 51: Peer review & feedback incorporation",
  "Day 52: Practice",
  "Day 53: Mini Project – Edited Article",
  "Day 54: Revision",

  "Day 55: Long-form content writing",
  "Day 56: Research & references",
  "Day 57: Structuring long-form content",
  "Day 58: Practice",
  "Day 59: Mini Project – Long-form Article",
  "Day 60: Revision",

  "Day 61: Creative content writing",
  "Day 62: Poetry, short stories, scripts",
  "Day 63: Practice",
  "Day 64: Mini Project – Creative Piece",
  "Day 65: Revision",

  "Day 66: Guest posting & outreach",
  "Day 67: Networking with blogs & publications",
  "Day 68: Practice",
  "Day 69: Mini Project – Guest Blog Pitch",
  "Day 70: Revision",

  "Day 71: Advanced SEO writing",
  "Day 72: Backlinking & on-page optimization",
  "Day 73: Practice",
  "Day 74: Mini Project – Optimized Blog Series",
  "Day 75: Revision",

  "Day 76: Email marketing content",
  "Day 77: Newsletters & email campaigns",
  "Day 78: Practice",
  "Day 79: Mini Project – Email Sequence Draft",
  "Day 80: Revision",

  "Day 81: Content strategy basics",
  "Day 82: Planning content calendar",
  "Day 83: Metrics & KPIs",
  "Day 84: Practice",
  "Day 85: Mini Project – Content Strategy Plan",
  "Day 86: Revision",

  "Day 87: Portfolio planning",
  "Day 88: Selecting projects & samples",
  "Day 89: Formatting & presentation",
  "Day 90: Practice",
  "Day 91: Portfolio Draft",
  "Day 92: Revision",

  "Day 93: Resume & social media setup",
  "Day 94: LinkedIn, Medium, personal blog setup",
  "Day 95: Apply for freelance or jobs",
  "Day 96: Mock interviews",
  "Day 97: Revision",

  "Day 98: Writing for video scripts",
  "Day 99: Storyboarding & scripting techniques",
  "Day 100: Practice",
  "Day 101: Mini Project – Video Script Draft",
  "Day 102: Revision",

  "Day 103: Writing for e-commerce & product descriptions",
  "Day 104: SEO product copy & persuasive writing",
  "Day 105: Practice",
  "Day 106: Mini Project – Product Description Set",
  "Day 107: Revision",

  "Day 108: Advanced storytelling & content engagement",
  "Day 109: Hooks, pacing, and retention",
  "Day 110: Practice",
  "Day 111: Mini Project – Engaging Content Series",
  "Day 112: Revision",

  "Day 113: Analytics & performance review",
  "Day 114: Google Analytics & content metrics",
  "Day 115: Practice",
  "Day 116: Mini Project – Content Performance Report",
  "Day 117: Revision",

  "Day 118: Freelance content writing basics",
  "Day 119: Client communication & contracts",
  "Day 120: portfolio finalization"
],
"Journalist": [

  "Day 1: Understand Journalist role & career paths",
  "Day 2: Basics of journalism & media types",
  "Day 3: Journalism ethics & professionalism",
  "Day 4: News values & storytelling",
  "Day 5: Role of journalists in society",
  "Day 6: Tools setup (Notepad, Camera, Recording tools, CMS)",
  "Day 7: Revision",

  "Day 8: Understanding the audience & target media",
  "Day 9: Research techniques for journalism",
  "Day 10: Fact-checking & verification",
  "Day 11: Practice",
  "Day 12: Mini Project – Research & Verification Exercise",
  "Day 13: Revision",

  "Day 14: News writing basics",
  "Day 15: Inverted pyramid structure",
  "Day 16: Headlines, leads & news angles",
  "Day 17: Practice",
  "Day 18: Mini Project – Write a News Article",
  "Day 19: Revision",

  "Day 20: Feature writing basics",
  "Day 21: Narrative storytelling & human interest",
  "Day 22: Writing style & tone",
  "Day 23: Practice",
  "Day 24: Mini Project – Feature Article",
  "Day 25: Revision",

  "Day 26: Interviewing skills",
  "Day 27: Preparing questions & conducting interviews",
  "Day 28: Practice",
  "Day 29: Mini Project – Conduct & Report an Interview",
  "Day 30: Revision",

  "Day 31: Investigative journalism basics",
  "Day 32: Research, data collection & analysis",
  "Day 33: Practice",
  "Day 34: Mini Project – Investigative Report Draft",
  "Day 35: Revision",

  "Day 36: Multimedia journalism basics",
  "Day 37: Photography & videography for news",
  "Day 38: Audio recording & editing",
  "Day 39: Practice",
  "Day 40: Mini Project – Multimedia Story",
  "Day 41: Revision",

  "Day 42: Digital journalism",
  "Day 43: Blogs, online news, social media reporting",
  "Day 44: SEO & engagement basics",
  "Day 45: Practice",
  "Day 46: Mini Project – Publish Online Article",
  "Day 47: Revision",

  "Day 48: Reporting on politics & governance",
  "Day 49: Understanding laws & regulations",
  "Day 50: Practice",
  "Day 51: Mini Project – Political News Report",
  "Day 52: Revision",

  "Day 53: Reporting on business & finance",
  "Day 54: Understanding economic data",
  "Day 55: Practice",
  "Day 56: Mini Project – Business News Article",
  "Day 57: Revision",

  "Day 58: Reporting on science & technology",
  "Day 59: Interpreting technical data for readers",
  "Day 60: Practice",
  "Day 61: Mini Project – Science/Tech Article",
  "Day 62: Revision",

  "Day 63: Reporting on social issues & human rights",
  "Day 64: Field reporting techniques",
  "Day 65: Practice",
  "Day 66: Mini Project – Social Issue Report",
  "Day 67: Revision",

  "Day 68: Editing basics for journalists",
  "Day 69: Copy editing & proofreading",
  "Day 70: Headlines & layout for print/online",
  "Day 71: Practice",
  "Day 72: Mini Project – Edited Article",
  "Day 73: Revision",

  "Day 74: Investigative journalism advanced",
  "Day 75: Advanced data journalism",
  "Day 76: Practice",
  "Day 77: Mini Project – Data-Driven Story",
  "Day 78: Revision",

  "Day 79: Podcasting & audio journalism",
  "Day 80: Recording & editing for podcasts",
  "Day 81: Practice",
  "Day 82: Mini Project – Record & Publish Podcast",
  "Day 83: Revision",

  "Day 84: Video journalism advanced",
  "Day 85: Video editing & storyboarding",
  "Day 86: Practice",
  "Day 87: Mini Project – News Video Story",
  "Day 88: Revision",

  "Day 89: Press releases & PR writing",
  "Day 90: Media communication & networking",
  "Day 91: Practice",
  "Day 92: Mini Project – Draft Press Release",
  "Day 93: Revision",

  "Day 94: Crisis reporting & ethics",
  "Day 95: Conflict-sensitive reporting",
  "Day 96: Practice",
  "Day 97: Mini Project – Sensitive Issue Report",
  "Day 98: Revision",

  "Day 99: Portfolio planning",
  "Day 100: Selecting articles, multimedia & reports",
  "Day 101: Formatting & presentation",
  "Day 102: Practice",
  "Day 103: Portfolio Draft",
  "Day 104: Revision",

  "Day 105: Resume & social media setup",
  "Day 106: LinkedIn, Medium, personal blog setup",
  "Day 107: Apply for internships/jobs",
  "Day 108: Mock interviews",
  "Day 109: Revision",

  "Day 110: Investigative reporting advanced",
  "Day 111: Freedom of Information (FOI) & data access",
  "Day 112: Practice",
  "Day 113: Mini Project – Investigative Article",
  "Day 114: Revision",

  "Day 115: Advanced multimedia storytelling",
  "Day 116: Interactive articles & visualizations",
  "Day 117: Practice",
  "Day 118: Mini Project – Multimedia Storyboard",
  "Day 119: Revision",

  "Day 120: Portfolio finalization "
],
"Academic Coordinator": [

  "Day 1: Understand Academic Coordinator role & responsibilities",
  "Day 2: Basics of academic administration",
  "Day 3: Curriculum understanding & mapping",
  "Day 4: Educational policies & compliance",
  "Day 5: Role of coordinator in schools/colleges",
  "Day 6: Tools setup (MS Office, Google Workspace, LMS)",
  "Day 7: Revision",

  "Day 8: Teacher coordination basics",
  "Day 9: Scheduling & timetable management",
  "Day 10: Faculty communication & support",
  "Day 11: Practice",
  "Day 12: Mini Project – Draft Weekly Timetable",
  "Day 13: Revision",

  "Day 14: Student progress tracking",
  "Day 15: Assessment methods & grade analysis",
  "Day 16: Reports & documentation",
  "Day 17: Practice",
  "Day 18: Mini Project – Student Progress Report",
  "Day 19: Revision",

  "Day 20: Curriculum planning basics",
  "Day 21: Aligning syllabus with learning outcomes",
  "Day 22: Annual academic calendar preparation",
  "Day 23: Practice",
  "Day 24: Mini Project – Draft Academic Calendar",
  "Day 25: Revision",

  "Day 26: Academic meetings & coordination",
  "Day 27: Agenda preparation & documentation",
  "Day 28: Conducting teacher meetings effectively",
  "Day 29: Practice",
  "Day 30: Mini Project – Conduct Mock Meeting",
  "Day 31: Revision",

  "Day 32: Event & activity planning",
  "Day 33: Student clubs, workshops & seminars",
  "Day 34: Coordination with external vendors",
  "Day 35: Practice",
  "Day 36: Mini Project – Plan Academic Event",
  "Day 37: Revision",

  "Day 38: Student counseling & support",
  "Day 39: Identifying academic needs & interventions",
  "Day 40: Practice",
  "Day 41: Mini Project – Student Support Plan",
  "Day 42: Revision",

  "Day 43: Quality assurance & feedback",
  "Day 44: Teacher & student feedback collection",
  "Day 45: Data analysis & reporting",
  "Day 46: Practice",
  "Day 47: Mini Project – Feedback Report",
  "Day 48: Revision",

  "Day 49: Accreditation & compliance basics",
  "Day 50: Documentation for audits",
  "Day 51: Practice",
  "Day 52: Mini Project – Accreditation File Draft",
  "Day 53: Revision",

  "Day 54: Resource management",
  "Day 55: Library, lab, and classroom resources",
  "Day 56: Inventory tracking & planning",
  "Day 57: Practice",
  "Day 58: Mini Project – Resource Planning Sheet",
  "Day 59: Revision",

  "Day 60: Technology in academic coordination",
  "Day 61: LMS management & usage",
  "Day 62: Digital reporting & dashboards",
  "Day 63: Practice",
  "Day 64: Mini Project – LMS Module Setup",
  "Day 65: Revision",

  "Day 66: Budgeting basics for academic programs",
  "Day 67: Cost estimation & resource allocation",
  "Day 68: Practice",
  "Day 69: Mini Project – Academic Budget Draft",
  "Day 70: Revision",

  "Day 71: Parent-teacher coordination",
  "Day 72: Organizing meetings & reporting",
  "Day 73: Practice",
  "Day 74: Mini Project – Parent Communication Plan",
  "Day 75: Revision",

  "Day 76: Professional development planning",
  "Day 77: Teacher workshops & training sessions",
  "Day 78: Practice",
  "Day 79: Mini Project – Teacher Training Plan",
  "Day 80: Revision",

  "Day 81: Academic policy development",
  "Day 82: Drafting guidelines & regulations",
  "Day 83: Practice",
  "Day 84: Mini Project – Academic Policy Draft",
  "Day 85: Revision",

  "Day 86: Event & competition coordination",
  "Day 87: Scheduling inter-school/college events",
  "Day 88: Practice",
  "Day 89: Mini Project – Event Plan",
  "Day 90: Revision",

  "Day 91: Reporting to management",
  "Day 92: Monthly & quarterly reports",
  "Day 93: Data visualization & presentation",
  "Day 94: Practice",
  "Day 95: Mini Project – Monthly Report Draft",
  "Day 96: Revision",

  "Day 97: Conflict resolution & mediation",
  "Day 98: Handling faculty or student issues",
  "Day 99: Practice",
  "Day 100: Mini Project – Conflict Resolution Plan",
  "Day 101: Revision",

  "Day 102: Academic research coordination",
  "Day 103: Supporting faculty & student research",
  "Day 104: Practice",
  "Day 105: Mini Project – Research Support Plan",
  "Day 106: Revision",

  "Day 107: Alumni & industry coordination",
  "Day 108: Internship & placement support",
  "Day 109: Practice",
  "Day 110: Mini Project – Internship Program Draft",
  "Day 111: Revision",

  "Day 112: Portfolio planning",
  "Day 113: Collecting projects & reports",
  "Day 114: Formatting & presentation",
  "Day 115: Practice",
  "Day 116: Portfolio Draft",
  "Day 117: Revision",

  "Day 118: Resume & social media setup",
  "Day 119: LinkedIn, academic profiles setup",
  "Day 120: portfolio finalization"
],

# for commerce and management careers
"Accountant": [

  "Day 1: Understand Accountant role & career paths",
  "Day 2: Basics of accounting & finance",
  "Day 3: Accounting principles & concepts",
  "Day 4: Double-entry system",
  "Day 5: Basic financial statements overview",
  "Day 6: Tools setup (MS Excel, Tally, QuickBooks)",
  "Day 7: Revision",

  "Day 8: Recording transactions",
  "Day 9: Journal entries & ledgers",
  "Day 10: Trial balance preparation",
  "Day 11: Practice",
  "Day 12: Mini Project – Prepare Ledger & Trial Balance",
  "Day 13: Revision",

  "Day 14: Cash & bank management",
  "Day 15: Petty cash system",
  "Day 16: Bank reconciliation statements",
  "Day 17: Practice",
  "Day 18: Mini Project – Bank Reconciliation",
  "Day 19: Revision",

  "Day 20: Accounts receivable & payable",
  "Day 21: Managing invoices & payments",
  "Day 22: Practice",
  "Day 23: Mini Project – Accounts Receivable/Payable Sheet",
  "Day 24: Revision",

  "Day 25: Inventory accounting basics",
  "Day 26: Inventory valuation methods (FIFO, LIFO, Weighted Avg)",
  "Day 27: Practice",
  "Day 28: Mini Project – Inventory Valuation",
  "Day 29: Revision",

  "Day 30: Depreciation accounting",
  "Day 31: Methods of depreciation",
  "Day 32: Practice",
  "Day 33: Mini Project – Depreciation Schedule",
  "Day 34: Revision",

  "Day 35: Financial statements preparation",
  "Day 36: Income statement & balance sheet",
  "Day 37: Cash flow statement basics",
  "Day 38: Practice",
  "Day 39: Mini Project – Prepare Financial Statements",
  "Day 40: Revision",

  "Day 41: Budgeting basics",
  "Day 42: Forecasting & variance analysis",
  "Day 43: Practice",
  "Day 44: Mini Project – Draft Budget Plan",
  "Day 45: Revision",

  "Day 46: Taxation basics",
  "Day 47: GST/ VAT/Income Tax overview",
  "Day 48: Filing basics & compliance",
  "Day 49: Practice",
  "Day 50: Mini Project – GST/Tax Filing Simulation",
  "Day 51: Revision",

  "Day 52: Accounting software basics",
  "Day 53: Tally ERP/QuickBooks Introduction",
  "Day 54: Recording transactions in software",
  "Day 55: Practice",
  "Day 56: Mini Project – Accounting Software Practice",
  "Day 57: Revision",

  "Day 58: Payroll accounting",
  "Day 59: Salary calculations & statutory deductions",
  "Day 60: Practice",
  "Day 61: Mini Project – Payroll Sheet",
  "Day 62: Revision",

  "Day 63: Internal controls & audit basics",
  "Day 64: Accounting ethics & compliance",
  "Day 65: Practice",
  "Day 66: Mini Project – Internal Audit Checklist",
  "Day 67: Revision",

  "Day 68: Cost accounting basics",
  "Day 69: Direct & indirect costs",
  "Day 70: Cost allocation & budgeting",
  "Day 71: Practice",
  "Day 72: Mini Project – Cost Sheet Preparation",
  "Day 73: Revision",

  "Day 74: Financial analysis basics",
  "Day 75: Ratio analysis & interpretation",
  "Day 76: Practice",
  "Day 77: Mini Project – Financial Ratios Report",
  "Day 78: Revision",

  "Day 79: Advanced accounting topics",
  "Day 80: Accounting for fixed assets & investments",
  "Day 81: Practice",
  "Day 82: Mini Project – Asset Accounting",
  "Day 83: Revision",

  "Day 84: Audit preparation",
  "Day 85: Audit procedures & compliance",
  "Day 86: Practice",
  "Day 87: Mini Project – Audit Report Draft",
  "Day 88: Revision",

  "Day 89: Financial reporting standards (IFRS/GAAP)",
  "Day 90: Practice",
  "Day 91: Mini Project – Reporting Adjustment",
  "Day 92: Revision",

  "Day 93: Management accounting basics",
  "Day 94: Decision-making reports",
  "Day 95: Practice",
  "Day 96: Mini Project – Management Report Draft",
  "Day 97: Revision",

  "Day 98: Accounting for small businesses & startups",
  "Day 99: Bookkeeping setup",
  "Day 100: Practice",
  "Day 101: Mini Project – Small Business Accounting",
  "Day 102: Revision",

  "Day 103: Advanced Excel for accountants",
  "Day 104: Formulas, Pivot Tables, Charts",
  "Day 105: Practice",
  "Day 106: Mini Project – Excel Accounting Dashboard",
  "Day 107: Revision",

  "Day 108: Portfolio planning",
  "Day 109: Collecting projects & accounting sheets",
  "Day 110: Formatting & presentation",
  "Day 111: Practice",
  "Day 112: Portfolio Draft",
  "Day 113: Revision",

  "Day 114: Resume & social media setup",
  "Day 115: LinkedIn, professional profile setup",
  "Day 116: Apply for internships/jobs",
  "Day 117: Mock interviews",
  "Day 118: Revision",

  "Day 119: Final practice & revision of all topics",
  "Day 120: Portfolio finalization "
],
"Chartered Accountant": [

  "Day 1: Understand Chartered Accountant role & career paths",
  "Day 2: Basics of accounting & finance",
  "Day 3: Accounting principles & concepts",
  "Day 4: Double-entry system",
  "Day 5: Financial statements overview",
  "Day 6: Tools setup (MS Excel, Tally, QuickBooks, CA software)",
  "Day 7: Revision",

  "Day 8: Journal entries & ledgers",
  "Day 9: Trial balance preparation",
  "Day 10: Practice",
  "Day 11: Mini Project – Ledger & Trial Balance",
  "Day 12: Revision",

  "Day 13: Cash & bank management",
  "Day 14: Bank reconciliation & petty cash",
  "Day 15: Practice",
  "Day 16: Mini Project – Bank Reconciliation Statement",
  "Day 17: Revision",

  "Day 18: Accounts receivable & payable",
  "Day 19: Managing invoices & payments",
  "Day 20: Practice",
  "Day 21: Mini Project – AR/AP Sheet",
  "Day 22: Revision",

  "Day 23: Inventory accounting",
  "Day 24: Inventory valuation methods (FIFO, LIFO, Weighted Average)",
  "Day 25: Practice",
  "Day 26: Mini Project – Inventory Valuation",
  "Day 27: Revision",

  "Day 28: Depreciation accounting",
  "Day 29: Methods of depreciation",
  "Day 30: Practice",
  "Day 31: Mini Project – Depreciation Schedule",
  "Day 32: Revision",

  "Day 33: Final accounts preparation",
  "Day 34: Income statement & balance sheet",
  "Day 35: Cash flow statement",
  "Day 36: Practice",
  "Day 37: Mini Project – Financial Statements",
  "Day 38: Revision",

  "Day 39: Cost accounting basics",
  "Day 40: Direct & indirect costs, cost allocation",
  "Day 41: Practice",
  "Day 42: Mini Project – Cost Sheet",
  "Day 43: Revision",

  "Day 44: Financial management basics",
  "Day 45: Ratio analysis & interpretation",
  "Day 46: Practice",
  "Day 47: Mini Project – Financial Analysis Report",
  "Day 48: Revision",

  "Day 49: Taxation basics",
  "Day 50: GST, Income Tax & TDS",
  "Day 51: Filing & compliance overview",
  "Day 52: Practice",
  "Day 53: Mini Project – Tax Filing Simulation",
  "Day 54: Revision",

  "Day 55: Advanced taxation",
  "Day 56: Corporate tax, indirect taxes, exemptions",
  "Day 57: Practice",
  "Day 58: Mini Project – Advanced Tax Computation",
  "Day 59: Revision",

  "Day 60: Audit basics",
  "Day 61: Internal control & compliance",
  "Day 62: Audit procedures & documentation",
  "Day 63: Practice",
  "Day 64: Mini Project – Internal Audit Checklist",
  "Day 65: Revision",

  "Day 66: Corporate laws basics",
  "Day 67: Companies Act, LLP, partnership laws",
  "Day 68: Practice",
  "Day 69: Mini Project – Compliance Report Draft",
  "Day 70: Revision",

  "Day 71: Accounting standards (AS/IFRS)",
  "Day 72: Application of standards in accounts",
  "Day 73: Practice",
  "Day 74: Mini Project – Adjusted Financial Statements",
  "Day 75: Revision",

  "Day 76: Audit advanced",
  "Day 77: Statutory & internal audits",
  "Day 78: Practice",
  "Day 79: Mini Project – Audit Report Draft",
  "Day 80: Revision",

  "Day 81: Management accounting",
  "Day 82: Budgeting & variance analysis",
  "Day 83: Decision-making reports",
  "Day 84: Practice",
  "Day 85: Mini Project – Management Accounting Report",
  "Day 86: Revision",

  "Day 87: Risk management & internal control",
  "Day 88: Fraud detection & compliance monitoring",
  "Day 89: Practice",
  "Day 90: Mini Project – Risk Assessment Report",
  "Day 91: Revision",

  "Day 92: Advanced Excel & accounting software",
  "Day 93: Tally ERP/QuickBooks/Excel dashboards",
  "Day 94: Practice",
  "Day 95: Mini Project – Accounting Dashboard",
  "Day 96: Revision",

  "Day 97: Professional ethics & standards",
  "Day 98: CA Code of Conduct",
  "Day 99: Practice",
  "Day 100: Mini Project – Ethics Case Study",
  "Day 101: Revision",

  "Day 102: Portfolio planning",
  "Day 103: Collecting accounting sheets & projects",
  "Day 104: Formatting & presentation",
  "Day 105: Practice",
  "Day 106: Portfolio Draft",
  "Day 107: Revision",

  "Day 108: Resume & social media setup",
  "Day 109: LinkedIn & professional profile setup",
  "Day 110: Apply for internships/jobs",
  "Day 111: Mock interviews",
  "Day 112: Revision",

  "Day 113: Preparation for CA exams (Foundation/Intermediate/Final overview)",
  "Day 114: Study plan & subject strategy",
  "Day 115: Practice",
  "Day 116: Mini Project – Mock Exam Attempt",
  "Day 117: Revision",

  "Day 118: Advanced financial management & reporting",
  "Day 119: Final portfolio & practice of all topics",
  "Day 120: CA exam preparation strategy"
],
"Financial Analyst": [

  "Day 1: Understand Financial Analyst role & career paths",
  "Day 2: Basics of finance & accounting",
  "Day 3: Financial statements overview",
  "Day 4: Accounting principles & concepts",
  "Day 5: Tools setup (MS Excel, Google Sheets, Financial calculators, Bloomberg/Trading platforms)",
  "Day 6: Basics of business & economics",
  "Day 7: Revision",

  "Day 8: Recording & understanding transactions",
  "Day 9: Ledger & trial balance basics",
  "Day 10: Practice",
  "Day 11: Mini Project – Prepare Trial Balance",
  "Day 12: Revision",

  "Day 13: Cash flow analysis",
  "Day 14: Statement of cash flows preparation",
  "Day 15: Practice",
  "Day 16: Mini Project – Cash Flow Statement",
  "Day 17: Revision",

  "Day 18: Ratio analysis basics",
  "Day 19: Liquidity, solvency, profitability, efficiency ratios",
  "Day 20: Practice",
  "Day 21: Mini Project – Financial Ratio Analysis",
  "Day 22: Revision",

  "Day 23: Budgeting & forecasting basics",
  "Day 24: Preparing operating & capital budgets",
  "Day 25: Practice",
  "Day 26: Mini Project – Draft Budget Plan",
  "Day 27: Revision",

  "Day 28: Variance analysis",
  "Day 29: Comparing actual vs budget & analyzing deviations",
  "Day 30: Practice",
  "Day 31: Mini Project – Variance Report",
  "Day 32: Revision",

  "Day 33: Advanced Excel for financial analysis",
  "Day 34: Formulas, Pivot Tables, Charts",
  "Day 35: Practice",
  "Day 36: Mini Project – Excel Financial Dashboard",
  "Day 37: Revision",

  "Day 38: Investment analysis basics",
  "Day 39: Stock, bond, and mutual fund fundamentals",
  "Day 40: Practice",
  "Day 41: Mini Project – Investment Comparison Report",
  "Day 42: Revision",

  "Day 43: Valuation techniques",
  "Day 44: DCF (Discounted Cash Flow) & NPV",
  "Day 45: IRR & payback period",
  "Day 46: Practice",
  "Day 47: Mini Project – Company Valuation",
  "Day 48: Revision",

  "Day 49: Risk analysis basics",
  "Day 50: Financial risk, market risk, credit risk",
  "Day 51: Practice",
  "Day 52: Mini Project – Risk Assessment Report",
  "Day 53: Revision",

  "Day 54: Capital budgeting & project evaluation",
  "Day 55: Cost-benefit analysis & ROI calculations",
  "Day 56: Practice",
  "Day 57: Mini Project – Capital Project Evaluation",
  "Day 58: Revision",

  "Day 59: Financial modeling basics",
  "Day 60: Building models in Excel",
  "Day 61: Practice",
  "Day 62: Mini Project – Simple Financial Model",
  "Day 63: Revision",

  "Day 64: Corporate finance overview",
  "Day 65: Capital structure, dividends & funding",
  "Day 66: Practice",
  "Day 67: Mini Project – Corporate Finance Report",
  "Day 68: Revision",

  "Day 69: Financial reporting standards (IFRS/GAAP)",
  "Day 70: Application in analysis & reporting",
  "Day 71: Practice",
  "Day 72: Mini Project – Adjusted Financial Statements",
  "Day 73: Revision",

  "Day 74: Business performance analysis",
  "Day 75: KPIs & benchmarking",
  "Day 76: Practice",
  "Day 77: Mini Project – Performance Analysis Report",
  "Day 78: Revision",

  "Day 79: Macro & microeconomic analysis for finance",
  "Day 80: Understanding economic indicators",
  "Day 81: Practice",
  "Day 82: Mini Project – Economic Impact Report",
  "Day 83: Revision",

  "Day 84: Portfolio management basics",
  "Day 85: Diversification & asset allocation",
  "Day 86: Practice",
  "Day 87: Mini Project – Portfolio Analysis",
  "Day 88: Revision",

  "Day 89: Reporting & presentation skills",
  "Day 90: Creating dashboards & visualizations",
  "Day 91: Storytelling with financial data",
  "Day 92: Practice",
  "Day 93: Mini Project – Financial Report Presentation",
  "Day 94: Revision",

  "Day 95: Business valuation & mergers/acquisitions overview",
  "Day 96: Practice",
  "Day 97: Mini Project – Company Acquisition Analysis",
  "Day 98: Revision",

  "Day 99: Financial analytics tools overview",
  "Day 100: Bloomberg, Power BI, Tableau basics",
  "Day 101: Practice",
  "Day 102: Mini Project – Data Visualization Dashboard",
  "Day 103: Revision",

  "Day 104: Regulatory & compliance basics",
  "Day 105: Financial reporting compliance & ethics",
  "Day 106: Practice",
  "Day 107: Mini Project – Compliance Report",
  "Day 108: Revision",

  "Day 109: Portfolio planning",
  "Day 110: Collecting projects, dashboards & reports",
  "Day 111: Formatting & presentation",
  "Day 112: Practice",
  "Day 113: Portfolio Draft",
  "Day 114: Revision",

  "Day 115: Resume & LinkedIn profile setup",
  "Day 116: Job/internship applications",
  "Day 117: Mock interviews",
  "Day 118: Advanced Excel & modeling practice",
  "Day 119: Final review & revision",
  "Day 120: Portfolio finalization "
],
"Investment Banker": [

  "Day 1: Understand Investment Banker role & career paths",
  "Day 2: Basics of finance & accounting",
  "Day 3: Financial statements overview",
  "Day 4: Accounting principles & concepts",
  "Day 5: Tools setup (MS Excel, Google Sheets, Bloomberg Terminal, Financial calculators)",
  "Day 6: Basics of business & economics",
  "Day 7: Revision",

  "Day 8: Recording & understanding transactions",
  "Day 9: Ledger & trial balance basics",
  "Day 10: Practice",
  "Day 11: Mini Project – Prepare Trial Balance",
  "Day 12: Revision",

  "Day 13: Cash flow statement preparation",
  "Day 14: Cash flow analysis for companies",
  "Day 15: Practice",
  "Day 16: Mini Project – Cash Flow Analysis",
  "Day 17: Revision",

  "Day 18: Ratio analysis basics",
  "Day 19: Liquidity, solvency, profitability, efficiency ratios",
  "Day 20: Practice",
  "Day 21: Mini Project – Financial Ratio Analysis",
  "Day 22: Revision",

  "Day 23: Budgeting & forecasting basics",
  "Day 24: Operating & capital budgets",
  "Day 25: Practice",
  "Day 26: Mini Project – Draft Budget Plan",
  "Day 27: Revision",

  "Day 28: Valuation techniques basics",
  "Day 29: Discounted Cash Flow (DCF) & Net Present Value (NPV)",
  "Day 30: Internal Rate of Return (IRR) & Payback period",
  "Day 31: Practice",
  "Day 32: Mini Project – Company Valuation",
  "Day 33: Revision",

  "Day 34: Advanced valuation techniques",
  "Day 35: Comparable company analysis & precedent transactions",
  "Day 36: Practice",
  "Day 37: Mini Project – Valuation Report",
  "Day 38: Revision",

  "Day 39: Investment banking products overview",
  "Day 40: M&A, IPO, Debt Financing, Private Equity",
  "Day 41: Practice",
  "Day 42: Mini Project – Product Overview Presentation",
  "Day 43: Revision",

  "Day 44: Deal structuring basics",
  "Day 45: Financial modeling for deals",
  "Day 46: Practice",
  "Day 47: Mini Project – Simple Deal Structure",
  "Day 48: Revision",

  "Day 49: Corporate finance fundamentals",
  "Day 50: Capital structure, leverage, dividends",
  "Day 51: Practice",
  "Day 52: Mini Project – Corporate Finance Analysis",
  "Day 53: Revision",

  "Day 54: Mergers & acquisitions (M&A) overview",
  "Day 55: Deal lifecycle & due diligence",
  "Day 56: Practice",
  "Day 57: Mini Project – M&A Report Draft",
  "Day 58: Revision",

  "Day 59: Equity research basics",
  "Day 60: Analyzing stocks, sectors & industries",
  "Day 61: Practice",
  "Day 62: Mini Project – Equity Research Report",
  "Day 63: Revision",

  "Day 64: Debt & credit analysis",
  "Day 65: Bond valuation, credit risk, ratings",
  "Day 66: Practice",
  "Day 67: Mini Project – Debt Analysis Report",
  "Day 68: Revision",

  "Day 69: Financial modeling advanced",
  "Day 70: Building integrated financial models in Excel",
  "Day 71: Practice",
  "Day 72: Mini Project – Full Financial Model",
  "Day 73: Revision",

  "Day 74: Risk management basics",
  "Day 75: Market risk, credit risk, operational risk",
  "Day 76: Practice",
  "Day 77: Mini Project – Risk Assessment Report",
  "Day 78: Revision",

  "Day 79: Investment banking regulations & compliance",
  "Day 80: Regulatory frameworks (SEBI, SEC, etc.)",
  "Day 81: Practice",
  "Day 82: Mini Project – Compliance Checklist",
  "Day 83: Revision",

  "Day 84: Pitch books & presentations",
  "Day 85: Preparing deal pitch & client presentations",
  "Day 86: Practice",
  "Day 87: Mini Project – Pitch Book Draft",
  "Day 88: Revision",

  "Day 89: Negotiation & communication skills",
  "Day 90: Client handling & stakeholder management",
  "Day 91: Practice",
  "Day 92: Mini Project – Negotiation Simulation",
  "Day 93: Revision",

  "Day 94: Portfolio management basics",
  "Day 95: Diversification & asset allocation",
  "Day 96: Practice",
  "Day 97: Mini Project – Portfolio Analysis",
  "Day 98: Revision",

  "Day 99: Business performance analysis",
  "Day 100: KPIs, benchmarking & reporting",
  "Day 101: Practice",
  "Day 102: Mini Project – Performance Analysis Report",
  "Day 103: Revision",

  "Day 104: Advanced Excel & Power BI/Tableau for finance",
  "Day 105: Dashboards & data visualization",
  "Day 106: Practice",
  "Day 107: Mini Project – Dashboard for Financial Data",
  "Day 108: Revision",

  "Day 109: Professional ethics in investment banking",
  "Day 110: Compliance, confidentiality & ethics",
  "Day 111: Practice",
  "Day 112: Mini Project – Ethics Case Study",
  "Day 113: Revision",

  "Day 114: Portfolio planning",
  "Day 115: Collecting financial models & project reports",
  "Day 116: Formatting & presentation",
  "Day 117: Practice",
  "Day 118: Portfolio Draft",
  "Day 119: Revision",

  "Day 120: Resume finalization, LinkedIn setup "
],
"Business Analyst": [

  "Day 1: Understand Business Analyst role & career paths",
  "Day 2: Basics of business, management & operations",
  "Day 3: Introduction to Business Analysis",
  "Day 4: Key skills for BA (communication, analytical, problem-solving)",
  "Day 5: Tools setup (MS Excel, MS Visio, JIRA, Confluence, SQL basics)",
  "Day 6: Basics of business processes",
  "Day 7: Revision",

  "Day 8: Requirement gathering techniques",
  "Day 9: Stakeholder analysis & communication",
  "Day 10: Practice",
  "Day 11: Mini Project – Stakeholder Mapping",
  "Day 12: Revision",

  "Day 13: Business process modeling",
  "Day 14: Flowcharts, BPMN, process maps",
  "Day 15: Practice",
  "Day 16: Mini Project – Process Mapping",
  "Day 17: Revision",

  "Day 18: Functional & non-functional requirements",
  "Day 19: Writing clear requirement specifications",
  "Day 20: Practice",
  "Day 21: Mini Project – Requirement Document Draft",
  "Day 22: Revision",

  "Day 23: Data analysis basics",
  "Day 24: Excel functions, Pivot Tables, Charts",
  "Day 25: Practice",
  "Day 26: Mini Project – Data Analysis Report",
  "Day 27: Revision",

  "Day 28: SQL basics for business analysis",
  "Day 29: Querying data from databases",
  "Day 30: Practice",
  "Day 31: Mini Project – SQL Queries for Data Extraction",
  "Day 32: Revision",

  "Day 33: Advanced data analysis techniques",
  "Day 34: Filtering, aggregations, and reporting",
  "Day 35: Practice",
  "Day 36: Mini Project – Business Metrics Dashboard",
  "Day 37: Revision",

  "Day 38: Gap analysis & requirement validation",
  "Day 39: Prioritization techniques (MoSCoW, Kano Model)",
  "Day 40: Practice",
  "Day 41: Mini Project – Requirement Prioritization",
  "Day 42: Revision",

  "Day 43: SWOT & PESTLE analysis",
  "Day 44: Risk assessment & mitigation planning",
  "Day 45: Practice",
  "Day 46: Mini Project – SWOT/PESTLE Report",
  "Day 47: Revision",

  "Day 48: Agile & Scrum basics for BA",
  "Day 49: User stories, use cases & acceptance criteria",
  "Day 50: Practice",
  "Day 51: Mini Project – User Stories Draft",
  "Day 52: Revision",

  "Day 53: Project management basics",
  "Day 54: Understanding SDLC & project lifecycle",
  "Day 55: Practice",
  "Day 56: Mini Project – SDLC Documentation",
  "Day 57: Revision",

  "Day 58: Tools for business analysis",
  "Day 59: JIRA, Confluence, MS Visio, Tableau basics",
  "Day 60: Practice",
  "Day 61: Mini Project – Tool Demo Project",
  "Day 62: Revision",

  "Day 63: KPI definition & performance measurement",
  "Day 64: Business reporting & dashboards",
  "Day 65: Practice",
  "Day 66: Mini Project – Dashboard Creation",
  "Day 67: Revision",

  "Day 68: Communication & presentation skills",
  "Day 69: Writing reports & documentation",
  "Day 70: Practice",
  "Day 71: Mini Project – BA Report Draft",
  "Day 72: Revision",

  "Day 73: Change management basics",
  "Day 74: Implementing process improvements",
  "Day 75: Practice",
  "Day 76: Mini Project – Process Improvement Plan",
  "Day 77: Revision",

  "Day 78: Business analytics overview",
  "Day 79: Introduction to BI tools (Power BI/Tableau)",
  "Day 80: Practice",
  "Day 81: Mini Project – Simple BI Dashboard",
  "Day 82: Revision",

  "Day 83: Stakeholder management advanced",
  "Day 84: Negotiation & conflict resolution",
  "Day 85: Practice",
  "Day 86: Mini Project – Stakeholder Communication Plan",
  "Day 87: Revision",

  "Day 88: Risk & issue management",
  "Day 89: Tracking, reporting, and mitigation strategies",
  "Day 90: Practice",
  "Day 91: Mini Project – Risk Register",
  "Day 92: Revision",

  "Day 93: Process automation & RPA basics",
  "Day 94: Identifying automation opportunities",
  "Day 95: Practice",
  "Day 96: Mini Project – Automation Plan Draft",
  "Day 97: Revision",

  "Day 98: Financial basics for BA",
  "Day 99: Budgeting, cost analysis & forecasting",
  "Day 100: Practice",
  "Day 101: Mini Project – Budget Analysis Report",
  "Day 102: Revision",

  "Day 103: Portfolio planning",
  "Day 104: Collecting projects, dashboards & reports",
  "Day 105: Formatting & presentation",
  "Day 106: Practice",
  "Day 107: Portfolio Draft",
  "Day 108: Revision",

  "Day 109: Resume & LinkedIn setup",
  "Day 110: Apply for internships/jobs",
  "Day 111: Mock interviews",
  "Day 112: Advanced Excel & analytics practice",
  "Day 113: Final review of all topics",
  "Day 114: Mini Project – Final Dashboard & Report",
  "Day 115: Revision",

  "Day 116: Professional ethics & BA standards",
  "Day 117: Industry best practices & certifications overview",
  "Day 118: Practice",
  "Day 119: Final portfolio preparation",
  "Day 120: career planning"
],
"Management Consultant": [

  "Day 1: Understand Management Consultant role & career paths",
  "Day 2: Basics of business, management & organizational structure",
  "Day 3: Key consulting skills (analytical, communication, problem-solving)",
  "Day 4: Tools setup (MS Excel, PowerPoint, Google Workspace, Tableau)",
  "Day 5: Basics of business strategy",
  "Day 6: Basics of economics & finance for consultants",
  "Day 7: Revision",

  "Day 8: Problem-solving frameworks",
  "Day 9: Issue identification & hypothesis building",
  "Day 10: Practice",
  "Day 11: Mini Project – Define Client Problem Statement",
  "Day 12: Revision",

  "Day 13: Business process analysis",
  "Day 14: Mapping processes & identifying inefficiencies",
  "Day 15: Practice",
  "Day 16: Mini Project – Process Mapping Report",
  "Day 17: Revision",

  "Day 18: Stakeholder analysis & communication",
  "Day 19: Conducting client interviews & surveys",
  "Day 20: Practice",
  "Day 21: Mini Project – Stakeholder Map",
  "Day 22: Revision",

  "Day 23: Data collection & analysis",
  "Day 24: Excel data analysis, Pivot Tables, charts",
  "Day 25: Practice",
  "Day 26: Mini Project – Business Data Analysis",
  "Day 27: Revision",

  "Day 28: Market & industry research",
  "Day 29: Competitor analysis & benchmarking",
  "Day 30: Practice",
  "Day 31: Mini Project – Market Research Report",
  "Day 32: Revision",

  "Day 33: Strategic frameworks",
  "Day 34: SWOT, PESTLE, Porter’s Five Forces",
  "Day 35: Practice",
  "Day 36: Mini Project – Strategy Framework Application",
  "Day 37: Revision",

  "Day 38: Financial analysis basics for consulting",
  "Day 39: Reading financial statements & ratios",
  "Day 40: Practice",
  "Day 41: Mini Project – Financial Health Analysis",
  "Day 42: Revision",

  "Day 43: Operations consulting basics",
  "Day 44: Process improvement & efficiency optimization",
  "Day 45: Practice",
  "Day 46: Mini Project – Process Improvement Plan",
  "Day 47: Revision",

  "Day 48: Marketing & sales consulting",
  "Day 49: Market segmentation & targeting strategies",
  "Day 50: Practice",
  "Day 51: Mini Project – Marketing Strategy Draft",
  "Day 52: Revision",

  "Day 53: Human resources & organizational consulting",
  "Day 54: Organizational design, roles, & responsibilities",
  "Day 55: Practice",
  "Day 56: Mini Project – HR Optimization Plan",
  "Day 57: Revision",

  "Day 58: Change management basics",
  "Day 59: Implementing solutions & process changes",
  "Day 60: Practice",
  "Day 61: Mini Project – Change Implementation Plan",
  "Day 62: Revision",

  "Day 63: Client presentation & reporting",
  "Day 64: Storytelling with data & visuals",
  "Day 65: PowerPoint/report preparation",
  "Day 66: Practice",
  "Day 67: Mini Project – Client Presentation Draft",
  "Day 68: Revision",

  "Day 69: Project management basics",
  "Day 70: Project lifecycle & deliverables",
  "Day 71: Practice",
  "Day 72: Mini Project – Project Plan Draft",
  "Day 73: Revision",

  "Day 74: Consulting frameworks advanced",
  "Day 75: Business model canvas, Balanced Scorecard",
  "Day 76: Practice",
  "Day 77: Mini Project – Strategic Framework Application",
  "Day 78: Revision",

  "Day 79: Risk & issue management",
  "Day 80: Identifying, monitoring & mitigating risks",
  "Day 81: Practice",
  "Day 82: Mini Project – Risk Assessment Report",
  "Day 83: Revision",

  "Day 84: Negotiation & persuasion skills",
  "Day 85: Handling client objections",
  "Day 86: Practice",
  "Day 87: Mini Project – Negotiation Simulation",
  "Day 88: Revision",

  "Day 89: Business analytics & visualization",
  "Day 90: Tableau/Power BI dashboards",
  "Day 91: Practice",
  "Day 92: Mini Project – Dashboard for Client Project",
  "Day 93: Revision",

  "Day 94: Cost optimization & financial modeling basics",
  "Day 95: ROI & scenario analysis",
  "Day 96: Practice",
  "Day 97: Mini Project – Financial Model Draft",
  "Day 98: Revision",

  "Day 99: Mergers & acquisitions overview",
  "Day 100: Deal analysis & feasibility",
  "Day 101: Practice",
  "Day 102: Mini Project – M&A Case Study",
  "Day 103: Revision",

  "Day 104: Professional ethics & consulting standards",
  "Day 105: Industry best practices & certifications overview",
  "Day 106: Practice",
  "Day 107: Mini Project – Ethics Case Study",
  "Day 108: Revision",

  "Day 109: Portfolio planning",
  "Day 110: Collecting projects, dashboards & reports",
  "Day 111: Formatting & presentation",
  "Day 112: Practice",
  "Day 113: Portfolio Draft",
  "Day 114: Revision",

  "Day 115: Resume & LinkedIn setup",
  "Day 116: Apply for internships/jobs",
  "Day 117: Mock interviews",
  "Day 118: Advanced Excel & analytics practice",
  "Day 119: Final review of all topics",
  "Day 120: Portfolio finalization"
],
"Product Manager": [

  "Day 1: Understand Product Manager role & career paths",
  "Day 2: Basics of business, product lifecycle & strategy",
  "Day 3: Key skills for PM (communication, analytical, leadership)",
  "Day 4: Tools setup (MS Excel, Jira, Trello, Figma, Productboard)",
  "Day 5: Basics of market & customer research",
  "Day 6: Understanding user personas",
  "Day 7: Revision",

  "Day 8: Requirement gathering techniques",
  "Day 9: Writing clear product requirements (PRDs)",
  "Day 10: Practice",
  "Day 11: Mini Project – PRD Draft",
  "Day 12: Revision",

  "Day 13: Competitor & market analysis",
  "Day 14: SWOT & PESTLE analysis",
  "Day 15: Practice",
  "Day 16: Mini Project – Market Analysis Report",
  "Day 17: Revision",

  "Day 18: Product roadmap basics",
  "Day 19: Creating short-term & long-term roadmap",
  "Day 20: Practice",
  "Day 21: Mini Project – Product Roadmap Draft",
  "Day 22: Revision",

  "Day 23: Agile & Scrum basics for PM",
  "Day 24: Writing user stories & defining epics",
  "Day 25: Practice",
  "Day 26: Mini Project – User Story Mapping",
  "Day 27: Revision",

  "Day 28: Wireframing & prototyping basics",
  "Day 29: Figma/Adobe XD introduction",
  "Day 30: Practice",
  "Day 31: Mini Project – Simple Wireframe",
  "Day 32: Revision",

  "Day 33: Product development lifecycle",
  "Day 34: MVP definition & iterative development",
  "Day 35: Practice",
  "Day 36: Mini Project – MVP Planning",
  "Day 37: Revision",

  "Day 38: Metrics & analytics basics",
  "Day 39: Key Product Metrics (KPI, NPS, DAU/MAU, churn rate)",
  "Day 40: Practice",
  "Day 41: Mini Project – Product Metrics Dashboard",
  "Day 42: Revision",

  "Day 43: A/B testing & experimentation",
  "Day 44: Setting up experiments & analyzing results",
  "Day 45: Practice",
  "Day 46: Mini Project – A/B Test Report",
  "Day 47: Revision",

  "Day 48: Stakeholder management",
  "Day 49: Communication & negotiation skills",
  "Day 50: Practice",
  "Day 51: Mini Project – Stakeholder Communication Plan",
  "Day 52: Revision",

  "Day 53: Product launch planning",
  "Day 54: Go-to-market strategy & rollout plan",
  "Day 55: Practice",
  "Day 56: Mini Project – Launch Plan Draft",
  "Day 57: Revision",

  "Day 58: Customer feedback & iteration",
  "Day 59: Handling support & feature requests",
  "Day 60: Practice",
  "Day 61: Mini Project – Feature Prioritization",
  "Day 62: Revision",

  "Day 63: Roadmap review & iteration",
  "Day 64: Tracking progress & reporting",
  "Day 65: Practice",
  "Day 66: Mini Project – Updated Roadmap",
  "Day 67: Revision",

  "Day 68: Financial basics for PM",
  "Day 69: Product P&L, revenue models & pricing strategies",
  "Day 70: Practice",
  "Day 71: Mini Project – Product Pricing Analysis",
  "Day 72: Revision",

  "Day 73: Advanced analytics & dashboards",
  "Day 74: Tableau/Power BI basics for PM",
  "Day 75: Practice",
  "Day 76: Mini Project – Product Analytics Dashboard",
  "Day 77: Revision",

  "Day 78: Risk & issue management",
  "Day 79: Identifying, monitoring & mitigating risks",
  "Day 80: Practice",
  "Day 81: Mini Project – Risk Register",
  "Day 82: Revision",

  "Day 83: Leadership & team management",
  "Day 84: Motivating & guiding development teams",
  "Day 85: Practice",
  "Day 86: Mini Project – Team Management Plan",
  "Day 87: Revision",

  "Day 88: Business strategy & alignment",
  "Day 89: Linking product goals to business objectives",
  "Day 90: Practice",
  "Day 91: Mini Project – Product Strategy Draft",
  "Day 92: Revision",

  "Day 93: Product lifecycle optimization",
  "Day 94: Portfolio management & prioritization",
  "Day 95: Practice",
  "Day 96: Mini Project – Product Portfolio Plan",
  "Day 97: Revision",

  "Day 98: Customer journey mapping",
  "Day 99: Identifying pain points & opportunities",
  "Day 100: Practice",
  "Day 101: Mini Project – Customer Journey Map",
  "Day 102: Revision",

  "Day 103: Portfolio planning",
  "Day 104: Collecting projects, dashboards & reports",
  "Day 105: Formatting & presentation",
  "Day 106: Practice",
  "Day 107: Portfolio Draft",
  "Day 108: Revision",

  "Day 109: Resume & LinkedIn setup",
  "Day 110: Apply for internships/jobs",
  "Day 111: Mock interviews",
  "Day 112: Advanced analytics & roadmap practice",
  "Day 113: Final review of all topics",
  "Day 114: Mini Project – Final Product Portfolio",
  "Day 115: Revision",

  "Day 116: Professional ethics & PM standards",
  "Day 117: Industry best practices & certifications overview",
  "Day 118: Practice",
  "Day 119: Final portfolio preparation",
  "Day 120:career planning"
],
"Project Manager": [

  "Day 1: Understand Project Manager role & career paths",
  "Day 2: Basics of project management",
  "Day 3: Key skills for PM (communication, leadership, problem-solving)",
  "Day 4: Tools setup (MS Project, Jira, Trello, Asana, Google Workspace)",
  "Day 5: Basics of business & operations",
  "Day 6: Understanding project lifecycle",
  "Day 7: Revision",

  "Day 8: Project initiation & charter",
  "Day 9: Defining objectives & scope",
  "Day 10: Practice",
  "Day 11: Mini Project – Project Charter Draft",
  "Day 12: Revision",

  "Day 13: Stakeholder identification & analysis",
  "Day 14: Communication plan & engagement strategy",
  "Day 15: Practice",
  "Day 16: Mini Project – Stakeholder Map & Communication Plan",
  "Day 17: Revision",

  "Day 18: Work breakdown structure (WBS) basics",
  "Day 19: Task decomposition & timeline estimation",
  "Day 20: Practice",
  "Day 21: Mini Project – WBS Creation",
  "Day 22: Revision",

  "Day 23: Scheduling & Gantt charts",
  "Day 24: Dependencies, milestones, & critical path",
  "Day 25: Practice",
  "Day 26: Mini Project – Project Schedule Draft",
  "Day 27: Revision",

  "Day 28: Resource planning",
  "Day 29: Team roles & responsibilities",
  "Day 30: Practice",
  "Day 31: Mini Project – Resource Allocation Plan",
  "Day 32: Revision",

  "Day 33: Budgeting & cost management",
  "Day 34: Estimation, tracking, and reporting",
  "Day 35: Practice",
  "Day 36: Mini Project – Project Budget Draft",
  "Day 37: Revision",

  "Day 38: Risk management basics",
  "Day 39: Identifying risks & mitigation strategies",
  "Day 40: Practice",
  "Day 41: Mini Project – Risk Register",
  "Day 42: Revision",

  "Day 43: Quality management basics",
  "Day 44: Defining standards & metrics",
  "Day 45: Practice",
  "Day 46: Mini Project – Quality Plan Draft",
  "Day 47: Revision",

  "Day 48: Procurement & vendor management basics",
  "Day 49: Contracts & agreements overview",
  "Day 50: Practice",
  "Day 51: Mini Project – Vendor Selection Plan",
  "Day 52: Revision",

  "Day 53: Agile & Scrum basics",
  "Day 54: User stories, sprints & backlog management",
  "Day 55: Practice",
  "Day 56: Mini Project – Sprint Planning",
  "Day 57: Revision",

  "Day 58: Project execution & monitoring",
  "Day 59: Tracking progress & KPIs",
  "Day 60: Practice",
  "Day 61: Mini Project – Project Status Report",
  "Day 62: Revision",

  "Day 63: Communication & leadership skills",
  "Day 64: Conflict resolution & team management",
  "Day 65: Practice",
  "Day 66: Mini Project – Team Management Plan",
  "Day 67: Revision",

  "Day 68: Change management basics",
  "Day 69: Handling scope changes & approvals",
  "Day 70: Practice",
  "Day 71: Mini Project – Change Request Log",
  "Day 72: Revision",

  "Day 73: Project closure & documentation",
  "Day 74: Lessons learned & post-mortem analysis",
  "Day 75: Practice",
  "Day 76: Mini Project – Project Closure Report",
  "Day 77: Revision",

  "Day 78: Portfolio & program management basics",
  "Day 79: Managing multiple projects & prioritization",
  "Day 80: Practice",
  "Day 81: Mini Project – Project Portfolio Draft",
  "Day 82: Revision",

  "Day 83: Advanced scheduling & resource leveling",
  "Day 84: Earned Value Management (EVM) basics",
  "Day 85: Practice",
  "Day 86: Mini Project – EVM Report",
  "Day 87: Revision",

  "Day 88: Professional ethics & PM standards",
  "Day 89: PMI/Prince2/CAPM overview",
  "Day 90: Practice",
  "Day 91: Mini Project – Ethics Case Study",
  "Day 92: Revision",

  "Day 93: Business analytics for PM",
  "Day 94: Excel dashboards & reporting",
  "Day 95: Practice",
  "Day 96: Mini Project – Project Analytics Dashboard",
  "Day 97: Revision",

  "Day 98: Client management & reporting",
  "Day 99: Status updates & stakeholder communication",
  "Day 100: Practice",
  "Day 101: Mini Project – Client Report Draft",
  "Day 102: Revision",

  "Day 103: Risk & issue escalation",
  "Day 104: Monitoring & mitigation review",
  "Day 105: Practice",
  "Day 106: Mini Project – Risk Escalation Plan",
  "Day 107: Revision",

  "Day 108: Advanced project tools (MS Project, Jira, Asana)",
  "Day 109: Dashboards & visualization for stakeholders",
  "Day 110: Practice",
  "Day 111: Mini Project – Tool Implementation",
  "Day 112: Revision",

  "Day 113: Portfolio planning",
  "Day 114: Collecting projects, dashboards & reports",
  "Day 115: Formatting & presentation",
  "Day 116: Practice",
  "Day 117: Portfolio Draft",
  "Day 118: Revision",

  "Day 119: Resume & LinkedIn setup",
  "Day 120: Apply for internships/jobs"
],

"Operations Manager": [

  "Day 1: Understand Operations Manager role & career paths",
  "Day 2: Basics of business & operations management",
  "Day 3: Key skills for OM (analytical, leadership, problem-solving)",
  "Day 4: Tools setup (MS Excel, ERP software, Tableau, Google Workspace)",
  "Day 5: Basics of supply chain & logistics",
  "Day 6: Understanding process flows & workflow management",
  "Day 7: Revision",

  "Day 8: Process mapping & analysis",
  "Day 9: Identifying bottlenecks & inefficiencies",
  "Day 10: Practice",
  "Day 11: Mini Project – Process Flow Map",
  "Day 12: Revision",

  "Day 13: Inventory management basics",
  "Day 14: Stock control, reorder levels & safety stock",
  "Day 15: Practice",
  "Day 16: Mini Project – Inventory Management Plan",
  "Day 17: Revision",

  "Day 18: Procurement & vendor management",
  "Day 19: Contracts & supplier evaluation",
  "Day 20: Practice",
  "Day 21: Mini Project – Vendor Selection Plan",
  "Day 22: Revision",

  "Day 23: Production & operations planning",
  "Day 24: Capacity planning & scheduling",
  "Day 25: Practice",
  "Day 26: Mini Project – Production Schedule",
  "Day 27: Revision",

  "Day 28: Quality management basics",
  "Day 29: Metrics & KPIs for operational performance",
  "Day 30: Practice",
  "Day 31: Mini Project – Quality Plan Draft",
  "Day 32: Revision",

  "Day 33: Lean & Six Sigma basics",
  "Day 34: Waste reduction & process improvement",
  "Day 35: Practice",
  "Day 36: Mini Project – Process Optimization Plan",
  "Day 37: Revision",

  "Day 38: Supply chain management overview",
  "Day 39: Logistics, transportation & warehousing",
  "Day 40: Practice",
  "Day 41: Mini Project – Supply Chain Mapping",
  "Day 42: Revision",

  "Day 43: Forecasting & demand planning",
  "Day 44: Statistical & data-driven forecasting",
  "Day 45: Practice",
  "Day 46: Mini Project – Demand Forecast Report",
  "Day 47: Revision",

  "Day 48: Financial basics for operations",
  "Day 49: Cost analysis, budgeting & operational efficiency",
  "Day 50: Practice",
  "Day 51: Mini Project – Cost Analysis Report",
  "Day 52: Revision",

  "Day 53: Project management basics for OM",
  "Day 54: Planning, execution & monitoring operations projects",
  "Day 55: Practice",
  "Day 56: Mini Project – Operations Project Plan",
  "Day 57: Revision",

  "Day 58: Data analysis & reporting",
  "Day 59: Excel, Tableau & dashboards",
  "Day 60: Practice",
  "Day 61: Mini Project – Operations Dashboard",
  "Day 62: Revision",

  "Day 63: Risk management basics",
  "Day 64: Identifying operational risks & mitigation",
  "Day 65: Practice",
  "Day 66: Mini Project – Risk Register",
  "Day 67: Revision",

  "Day 68: Team & human resource management",
  "Day 69: Leadership & conflict resolution",
  "Day 70: Practice",
  "Day 71: Mini Project – Team Management Plan",
  "Day 72: Revision",

  "Day 73: Technology in operations",
  "Day 74: ERP systems, automation & process digitization",
  "Day 75: Practice",
  "Day 76: Mini Project – Automation Proposal",
  "Day 77: Revision",

  "Day 78: Performance measurement & KPIs",
  "Day 79: Benchmarking & continuous improvement",
  "Day 80: Practice",
  "Day 81: Mini Project – KPI Report",
  "Day 82: Revision",

  "Day 83: Customer & supplier relationship management",
  "Day 84: Communication & negotiation skills",
  "Day 85: Practice",
  "Day 86: Mini Project – CRM Plan Draft",
  "Day 87: Revision",

  "Day 88: Lean operations & cost optimization",
  "Day 89: Identifying efficiency opportunities",
  "Day 90: Practice",
  "Day 91: Mini Project – Cost Reduction Plan",
  "Day 92: Revision",

  "Day 93: Sustainability & operations ethics",
  "Day 94: Regulatory compliance & standards",
  "Day 95: Practice",
  "Day 96: Mini Project – Compliance Checklist",
  "Day 97: Revision",

  "Day 98: Strategic planning for operations",
  "Day 99: Aligning operations with business objectives",
  "Day 100: Practice",
  "Day 101: Mini Project – Strategic Operations Plan",
  "Day 102: Revision",

  "Day 103: Portfolio planning",
  "Day 104: Collecting projects, dashboards & reports",
  "Day 105: Formatting & presentation",
  "Day 106: Practice",
  "Day 107: Portfolio Draft",
  "Day 108: Revision",

  "Day 109: Resume & LinkedIn setup",
  "Day 110: Apply for internships/jobs",
  "Day 111: Mock interviews",
  "Day 112: Advanced analytics & process optimization practice",
  "Day 113: Final review of all topics",
  "Day 114: Mini Project – Final Operations Portfolio",
  "Day 115: Revision",

  "Day 116: Professional ethics & OM standards",
  "Day 117: Industry best practices & certifications overview",
  "Day 118: Practice",
  "Day 119: Final portfolio preparation",
  "Day 120:  career planning"
],
"HR Manager": [

  "Day 1: Understand HR Manager role & career paths",
  "Day 2: Basics of human resource management",
  "Day 3: Key HR skills (communication, leadership, conflict resolution)",
  "Day 4: Tools setup (HRMS, Excel, HR Analytics tools, Google Workspace)",
  "Day 5: Organizational structure & culture",
  "Day 6: Basics of labor laws & compliance",
  "Day 7: Revision",

  "Day 8: Recruitment & talent acquisition basics",
  "Day 9: Job description & specification preparation",
  "Day 10: Practice",
  "Day 11: Mini Project – JD & JD Analysis",
  "Day 12: Revision",

  "Day 13: Sourcing & screening candidates",
  "Day 14: Conducting interviews & assessment methods",
  "Day 15: Practice",
  "Day 16: Mini Project – Candidate Shortlisting",
  "Day 17: Revision",

  "Day 18: Onboarding & induction process",
  "Day 19: Orientation programs & employee integration",
  "Day 20: Practice",
  "Day 21: Mini Project – Onboarding Plan",
  "Day 22: Revision",

  "Day 23: Training & development basics",
  "Day 24: Identifying skill gaps & training needs",
  "Day 25: Practice",
  "Day 26: Mini Project – Training Plan Draft",
  "Day 27: Revision",

  "Day 28: Performance management systems",
  "Day 29: KPI & goal setting",
  "Day 30: Performance review techniques",
  "Day 31: Mini Project – Performance Appraisal Form",
  "Day 32: Revision",

  "Day 33: Compensation & benefits basics",
  "Day 34: Payroll management & salary structure",
  "Day 35: Practice",
  "Day 36: Mini Project – Salary Structure Draft",
  "Day 37: Revision",

  "Day 38: Employee engagement & retention",
  "Day 39: Motivation techniques & surveys",
  "Day 40: Practice",
  "Day 41: Mini Project – Engagement Plan",
  "Day 42: Revision",

  "Day 43: Labor laws & compliance overview",
  "Day 44: Industrial relations & dispute resolution",
  "Day 45: Practice",
  "Day 46: Mini Project – Compliance Checklist",
  "Day 47: Revision",

  "Day 48: HR analytics basics",
  "Day 49: Metrics & dashboards (attrition, productivity, satisfaction)",
  "Day 50: Practice",
  "Day 51: Mini Project – HR Dashboard Draft",
  "Day 52: Revision",

  "Day 53: Recruitment analytics & forecasting",
  "Day 54: Workforce planning & succession planning",
  "Day 55: Practice",
  "Day 56: Mini Project – Workforce Plan",
  "Day 57: Revision",

  "Day 58: Employee relations & counseling",
  "Day 59: Conflict resolution & mediation",
  "Day 60: Practice",
  "Day 61: Mini Project – Conflict Management Plan",
  "Day 62: Revision",

  "Day 63: Organizational development",
  "Day 64: Change management & culture building",
  "Day 65: Practice",
  "Day 66: Mini Project – OD Plan",
  "Day 67: Revision",

  "Day 68: HR policies & procedures",
  "Day 69: Employee handbook & guidelines",
  "Day 70: Practice",
  "Day 71: Mini Project – Policy Draft",
  "Day 72: Revision",

  "Day 73: Talent management & succession planning",
  "Day 74: Career development frameworks",
  "Day 75: Practice",
  "Day 76: Mini Project – Career Pathing Plan",
  "Day 77: Revision",

  "Day 78: HR technology overview",
  "Day 79: HRMS, payroll systems & automation tools",
  "Day 80: Practice",
  "Day 81: Mini Project – HR Tech Implementation Plan",
  "Day 82: Revision",

  "Day 83: Employee wellness & work-life balance",
  "Day 84: Mental health & employee assistance programs",
  "Day 85: Practice",
  "Day 86: Mini Project – Wellness Program Draft",
  "Day 87: Revision",

  "Day 88: Leadership & team management",
  "Day 89: Coaching & mentoring employees",
  "Day 90: Practice",
  "Day 91: Mini Project – Team Development Plan",
  "Day 92: Revision",

  "Day 93: Strategic HR planning",
  "Day 94: Aligning HR with business objectives",
  "Day 95: Practice",
  "Day 96: Mini Project – Strategic HR Plan",
  "Day 97: Revision",

  "Day 98: Professional ethics & HR standards",
  "Day 99: Industry best practices & certifications overview",
  "Day 100: Practice",
  "Day 101: Mini Project – Ethics Case Study",
  "Day 102: Revision",

  "Day 103: Portfolio planning",
  "Day 104: Collecting HR projects, dashboards & reports",
  "Day 105: Formatting & presentation",
  "Day 106: Practice",
  "Day 107: Portfolio Draft",
  "Day 108: Revision",

  "Day 109: Resume & LinkedIn setup",
  "Day 110: Apply for internships/jobs",
  "Day 111: Mock interviews",
  "Day 112: Advanced HR analytics practice",
  "Day 113: Final review of all topics",
  "Day 114: Mini Project – Final HR Portfolio",
  "Day 115: Revision",

  "Day 116: Industry trends & continuous learning",
  "Day 117: HR certifications overview (SHRM, HRCI)",
  "Day 118: Practice",
  "Day 119: Final portfolio preparation",
  "Day 120: Career planning"
],
"Marketing Manager": [

  "Day 1: Understand Marketing Manager role & career paths",
  "Day 2: Basics of marketing & business",
  "Day 3: Key marketing skills (communication, creativity, analytical thinking)",
  "Day 4: Tools setup (Google Analytics, Canva, HubSpot, Excel, Google Workspace)",
  "Day 5: Understanding market segmentation & targeting",
  "Day 6: Basics of branding & positioning",
  "Day 7: Revision",

  "Day 8: Marketing research basics",
  "Day 9: Competitor analysis & SWOT",
  "Day 10: Practice",
  "Day 11: Mini Project – Market Research Report",
  "Day 12: Revision",

  "Day 13: Marketing strategy fundamentals",
  "Day 14: Setting marketing goals & KPIs",
  "Day 15: Practice",
  "Day 16: Mini Project – Marketing Strategy Draft",
  "Day 17: Revision",

  "Day 18: Branding & positioning",
  "Day 19: Developing brand identity & messaging",
  "Day 20: Practice",
  "Day 21: Mini Project – Brand Guidelines Draft",
  "Day 22: Revision",

  "Day 23: Content marketing basics",
  "Day 24: Blogging, copywriting & social media",
  "Day 25: Practice",
  "Day 26: Mini Project – Content Calendar",
  "Day 27: Revision",

  "Day 28: Digital marketing overview",
  "Day 29: SEO, SEM, PPC basics",
  "Day 30: Practice",
  "Day 31: Mini Project – SEO Plan Draft",
  "Day 32: Revision",

  "Day 33: Social media marketing",
  "Day 34: Platforms, engagement & advertising",
  "Day 35: Practice",
  "Day 36: Mini Project – Social Media Campaign Draft",
  "Day 37: Revision",

  "Day 38: Email marketing & automation",
  "Day 39: Campaign planning & segmentation",
  "Day 40: Practice",
  "Day 41: Mini Project – Email Campaign Draft",
  "Day 42: Revision",

  "Day 43: Influencer & affiliate marketing",
  "Day 44: Partnerships & collaborations",
  "Day 45: Practice",
  "Day 46: Mini Project – Influencer Strategy",
  "Day 47: Revision",

  "Day 48: Product marketing basics",
  "Day 49: Launch strategies & go-to-market planning",
  "Day 50: Practice",
  "Day 51: Mini Project – Product Launch Plan",
  "Day 52: Revision",

  "Day 53: Marketing analytics basics",
  "Day 54: Google Analytics & dashboards",
  "Day 55: Practice",
  "Day 56: Mini Project – Marketing Analytics Report",
  "Day 57: Revision",

  "Day 58: Paid marketing campaigns",
  "Day 59: Facebook Ads, Google Ads, LinkedIn Ads basics",
  "Day 60: Practice",
  "Day 61: Mini Project – Paid Campaign Draft",
  "Day 62: Revision",

  "Day 63: Budgeting & ROI tracking",
  "Day 64: Cost optimization & campaign performance",
  "Day 65: Practice",
  "Day 66: Mini Project – Campaign Budget Report",
  "Day 67: Revision",

  "Day 68: Customer journey & segmentation",
  "Day 69: Personas & behavioral analysis",
  "Day 70: Practice",
  "Day 71: Mini Project – Customer Journey Map",
  "Day 72: Revision",

  "Day 73: PR & communication strategies",
  "Day 74: Press releases & media relations",
  "Day 75: Practice",
  "Day 76: Mini Project – PR Plan Draft",
  "Day 77: Revision",

  "Day 78: Event & experiential marketing",
  "Day 79: Planning & executing events",
  "Day 80: Practice",
  "Day 81: Mini Project – Event Plan Draft",
  "Day 82: Revision",

  "Day 83: Advanced marketing analytics",
  "Day 84: Tableau/Power BI for marketing",
  "Day 85: Practice",
  "Day 86: Mini Project – Marketing Dashboard",
  "Day 87: Revision",

  "Day 88: Crisis management & reputation",
  "Day 89: Handling negative publicity & social issues",
  "Day 90: Practice",
  "Day 91: Mini Project – Crisis Communication Plan",
  "Day 92: Revision",

  "Day 93: Leadership & team management",
  "Day 94: Coaching & motivating marketing teams",
  "Day 95: Practice",
  "Day 96: Mini Project – Team Management Plan",
  "Day 97: Revision",

  "Day 98: Strategic marketing planning",
  "Day 99: Aligning marketing with business objectives",
  "Day 100: Practice",
  "Day 101: Mini Project – Strategic Marketing Plan",
  "Day 102: Revision",

  "Day 103: Portfolio planning",
  "Day 104: Collecting projects, campaigns & reports",
  "Day 105: Formatting & presentation",
  "Day 106: Practice",
  "Day 107: Portfolio Draft",
  "Day 108: Revision",

  "Day 109: Resume & LinkedIn setup",
  "Day 110: Apply for internships/jobs",
  "Day 111: Mock interviews",
  "Day 112: Advanced digital marketing practice",
  "Day 113: Final review of all topics",
  "Day 114: Mini Project – Final Marketing Portfolio",
  "Day 115: Revision",

  "Day 116: Professional ethics & marketing standards",
  "Day 117: Industry best practices & certifications overview (Google, HubSpot, Meta)",
  "Day 118: Practice",
  "Day 119: Final portfolio preparation",
  "Day 120:  career planning"
],


#Medical
"Doctor": [

  "Day 1: Understand Doctor role & medical career paths",
  "Day 2: Basics of human anatomy",
  "Day 3: Physiology fundamentals",
  "Day 4: Medical terminology & abbreviations",
  "Day 5: Tools setup (Anatomy apps, medical journals, reference books)",
  "Day 6: Basics of medical ethics & patient confidentiality",
  "Day 7: Revision",

  "Day 8: Biochemistry fundamentals",
  "Day 9: Cellular biology & molecular mechanisms",
  "Day 10: Practice",
  "Day 11: Mini Project – Cell Structure & Function Summary",
  "Day 12: Revision",

  "Day 13: Pathology basics",
  "Day 14: Common disease mechanisms & terminology",
  "Day 15: Practice",
  "Day 16: Mini Project – Case Study Summary",
  "Day 17: Revision",

  "Day 18: Pharmacology fundamentals",
  "Day 19: Common drug classes & mechanisms",
  "Day 20: Practice",
  "Day 21: Mini Project – Drug Mechanism Table",
  "Day 22: Revision",

  "Day 23: Microbiology basics",
  "Day 24: Common pathogens & lab tests",
  "Day 25: Practice",
  "Day 26: Mini Project – Microorganism Chart",
  "Day 27: Revision",

  "Day 28: Immunology basics",
  "Day 29: Immune response & vaccinations",
  "Day 30: Practice",
  "Day 31: Mini Project – Immune System Flowchart",
  "Day 32: Revision",

  "Day 33: Clinical skills introduction",
  "Day 34: History taking & patient interview",
  "Day 35: Practice",
  "Day 36: Mini Project – Patient History Form",
  "Day 37: Revision",

  "Day 38: Physical examination basics",
  "Day 39: Vital signs & systemic examination",
  "Day 40: Practice",
  "Day 41: Mini Project – Physical Exam Checklist",
  "Day 42: Revision",

  "Day 43: Diagnostic tools basics",
  "Day 44: Lab tests, imaging, ECG basics",
  "Day 45: Practice",
  "Day 46: Mini Project – Diagnostic Test Summary",
  "Day 47: Revision",

  "Day 48: Emergency medicine basics",
  "Day 49: First aid & resuscitation techniques",
  "Day 50: Practice",
  "Day 51: Mini Project – Emergency Protocol Draft",
  "Day 52: Revision",

  "Day 53: Internal medicine basics",
  "Day 54: Common diseases & treatment guidelines",
  "Day 55: Practice",
  "Day 56: Mini Project – Case Report Draft",
  "Day 57: Revision",

  "Day 58: Surgery basics",
  "Day 59: Pre-op & post-op care",
  "Day 60: Practice",
  "Day 61: Mini Project – Surgical Case Summary",
  "Day 62: Revision",

  "Day 63: Pediatrics basics",
  "Day 64: Growth & development monitoring",
  "Day 65: Practice",
  "Day 66: Mini Project – Pediatric Case Draft",
  "Day 67: Revision",

  "Day 68: Obstetrics & gynecology basics",
  "Day 69: Maternal & fetal care",
  "Day 70: Practice",
  "Day 71: Mini Project – Antenatal Care Plan",
  "Day 72: Revision",

  "Day 73: Psychiatry basics",
  "Day 74: Common mental health conditions",
  "Day 75: Practice",
  "Day 76: Mini Project – Mental Health Case Draft",
  "Day 77: Revision",

  "Day 78: Community medicine basics",
  "Day 79: Preventive medicine & public health",
  "Day 80: Practice",
  "Day 81: Mini Project – Public Health Plan",
  "Day 82: Revision",

  "Day 83: Clinical rotations overview",
  "Day 84: Observing patient care & documentation",
  "Day 85: Practice",
  "Day 86: Mini Project – Rotation Observation Notes",
  "Day 87: Revision",

  "Day 88: Research basics for doctors",
  "Day 89: Reading & interpreting medical research",
  "Day 90: Practice",
  "Day 91: Mini Project – Literature Review Summary",
  "Day 92: Revision",

  "Day 93: Ethics & professional conduct",
  "Day 94: Patient communication & consent",
  "Day 95: Practice",
  "Day 96: Mini Project – Ethics Case Study",
  "Day 97: Revision",

  "Day 98: Medical documentation & record keeping",
  "Day 99: EMR basics & patient charts",
  "Day 100: Practice",
  "Day 101: Mini Project – Sample Patient Chart",
  "Day 102: Revision",

  "Day 103: Telemedicine basics",
  "Day 104: Remote consultation & patient monitoring",
  "Day 105: Practice",
  "Day 106: Mini Project – Telemedicine Protocol Draft",
  "Day 107: Revision",

  "Day 108: Continuing medical education",
  "Day 109: Staying updated with guidelines & research",
  "Day 110: Practice",
  "Day 111: Mini Project – CME Plan Draft",
  "Day 112: Revision",

  "Day 113: Portfolio planning",
  "Day 114: Collecting case studies, reports & observations",
  "Day 115: Formatting & presentation",
  "Day 116: Practice",
  "Day 117: Portfolio Draft",
  "Day 118: Revision",

  "Day 119: Resume & LinkedIn setup",
  "Day 120: Next-step roadmap for clinical exposure & career planning"
],
"Nurse": [

  "Day 1: Understand Nurse role & career paths",
  "Day 2: Basics of anatomy & physiology",
  "Day 3: Medical terminology & abbreviations",
  "Day 4: Tools setup (Nursing apps, medical journals, reference books)",
  "Day 5: Basics of patient care",
  "Day 6: Introduction to nursing ethics & professional conduct",
  "Day 7: Revision",

  "Day 8: Vital signs measurement (temperature, pulse, respiration, BP)",
  "Day 9: Recording & interpreting vital signs",
  "Day 10: Practice",
  "Day 11: Mini Project – Vital Signs Record Sheet",
  "Day 12: Revision",

  "Day 13: Infection control & hygiene",
  "Day 14: Handwashing, PPE, and sterilization techniques",
  "Day 15: Practice",
  "Day 16: Mini Project – Infection Control Checklist",
  "Day 17: Revision",

  "Day 18: Patient assessment basics",
  "Day 19: Physical examination & health history",
  "Day 20: Practice",
  "Day 21: Mini Project – Patient Assessment Form",
  "Day 22: Revision",

  "Day 23: Nursing care planning",
  "Day 24: Writing nursing care plans",
  "Day 25: Practice",
  "Day 26: Mini Project – Sample Nursing Care Plan",
  "Day 27: Revision",

  "Day 28: Medication administration basics",
  "Day 29: Dosage calculation & routes of administration",
  "Day 30: Practice",
  "Day 31: Mini Project – Medication Chart Draft",
  "Day 32: Revision",

  "Day 33: IV therapy & fluid management basics",
  "Day 34: Administering IV & monitoring patients",
  "Day 35: Practice",
  "Day 36: Mini Project – IV Therapy Record",
  "Day 37: Revision",

  "Day 38: Wound care & dressing techniques",
  "Day 39: Infection prevention & documentation",
  "Day 40: Practice",
  "Day 41: Mini Project – Wound Care Log",
  "Day 42: Revision",

  "Day 43: Patient safety & fall prevention",
  "Day 44: Emergency preparedness & basic life support (BLS)",
  "Day 45: Practice",
  "Day 46: Mini Project – Safety Protocol Draft",
  "Day 47: Revision",

  "Day 48: Nutrition & hydration for patients",
  "Day 49: Monitoring dietary requirements & feeding techniques",
  "Day 50: Practice",
  "Day 51: Mini Project – Patient Nutrition Plan",
  "Day 52: Revision",

  "Day 53: Documentation & record keeping",
  "Day 54: Electronic medical records & charting",
  "Day 55: Practice",
  "Day 56: Mini Project – Sample Patient Chart",
  "Day 57: Revision",

  "Day 58: Patient communication & counseling",
  "Day 59: Handling difficult patients & families",
  "Day 60: Practice",
  "Day 61: Mini Project – Communication Plan",
  "Day 62: Revision",

  "Day 63: Clinical rotations overview",
  "Day 64: Observing patient care & procedures",
  "Day 65: Practice",
  "Day 66: Mini Project – Rotation Observation Notes",
  "Day 67: Revision",

  "Day 68: Pediatric nursing basics",
  "Day 69: Growth monitoring & child care",
  "Day 70: Practice",
  "Day 71: Mini Project – Pediatric Care Plan",
  "Day 72: Revision",

  "Day 73: Maternal & neonatal nursing basics",
  "Day 74: Antenatal & postnatal care",
  "Day 75: Practice",
  "Day 76: Mini Project – Maternal Care Plan",
  "Day 77: Revision",

  "Day 78: Geriatric nursing basics",
  "Day 79: Care for elderly patients & chronic conditions",
  "Day 80: Practice",
  "Day 81: Mini Project – Geriatric Care Plan",
  "Day 82: Revision",

  "Day 83: Mental health & psychiatric nursing",
  "Day 84: Common mental health conditions & patient support",
  "Day 85: Practice",
  "Day 86: Mini Project – Mental Health Care Plan",
  "Day 87: Revision",

  "Day 88: Community & public health nursing",
  "Day 89: Preventive care & awareness programs",
  "Day 90: Practice",
  "Day 91: Mini Project – Community Health Project",
  "Day 92: Revision",

  "Day 93: Advanced nursing procedures overview",
  "Day 94: Catheterization, suctioning & oxygen therapy",
  "Day 95: Practice",
  "Day 96: Mini Project – Procedure Checklist",
  "Day 97: Revision",

  "Day 98: Leadership & team management in nursing",
  "Day 99: Mentoring & supervising junior staff",
  "Day 100: Practice",
  "Day 101: Mini Project – Team Management Plan",
  "Day 102: Revision",

  "Day 103: Strategic nursing & hospital operations",
  "Day 104: Aligning nursing goals with hospital objectives",
  "Day 105: Practice",
  "Day 106: Mini Project – Strategic Nursing Plan",
  "Day 107: Revision",

  "Day 108: Ethics & professional standards",
  "Day 109: Patient rights & confidentiality",
  "Day 110: Practice",
  "Day 111: Mini Project – Ethics Case Study",
  "Day 112: Revision",

  "Day 113: Portfolio planning",
  "Day 114: Collecting patient care logs, projects & reports",
  "Day 115: Formatting & presentation",
  "Day 116: Practice",
  "Day 117: Portfolio Draft",
  "Day 118: Revision",

  "Day 119: Resume & LinkedIn setup",
  "Day 120:  Nursing career progression"
],
"Pharmacist": [

  "Day 1: Understand Pharmacist role & career paths",
  "Day 2: Basics of human anatomy & physiology",
  "Day 3: Medical terminology & abbreviations",
  "Day 4: Tools setup (Pharmacy apps, drug reference books, journals)",
  "Day 5: Basics of pharmacology",
  "Day 6: Introduction to pharmacy ethics & professional conduct",
  "Day 7: Revision",

  "Day 8: Drug classifications & mechanisms",
  "Day 9: Common drug names & their uses",
  "Day 10: Practice",
  "Day 11: Mini Project – Drug Classification Chart",
  "Day 12: Revision",

  "Day 13: Pharmaceutical calculations basics",
  "Day 14: Dosage forms & routes of administration",
  "Day 15: Practice",
  "Day 16: Mini Project – Dosage Calculation Exercises",
  "Day 17: Revision",

  "Day 18: Prescription interpretation & dispensing",
  "Day 19: Prescription errors & safety checks",
  "Day 20: Practice",
  "Day 21: Mini Project – Prescription Review Sheet",
  "Day 22: Revision",

  "Day 23: Drug interactions & contraindications",
  "Day 24: Adverse drug reactions & reporting",
  "Day 25: Practice",
  "Day 26: Mini Project – ADR Log Draft",
  "Day 27: Revision",

  "Day 28: Clinical pharmacy basics",
  "Day 29: Patient counseling & medication adherence",
  "Day 30: Practice",
  "Day 31: Mini Project – Patient Counseling Notes",
  "Day 32: Revision",

  "Day 33: Pharmacokinetics & pharmacodynamics basics",
  "Day 34: Absorption, distribution, metabolism, excretion",
  "Day 35: Practice",
  "Day 36: Mini Project – PK/PD Chart",
  "Day 37: Revision",

  "Day 38: Hospital & community pharmacy overview",
  "Day 39: Workflow & inventory management",
  "Day 40: Practice",
  "Day 41: Mini Project – Pharmacy Inventory Plan",
  "Day 42: Revision",

  "Day 43: Compounding & formulation basics",
  "Day 44: Quality control & safety measures",
  "Day 45: Practice",
  "Day 46: Mini Project – Formulation Record",
  "Day 47: Revision",

  "Day 48: Drug regulations & legal aspects",
  "Day 49: Licensing & controlled substances",
  "Day 50: Practice",
  "Day 51: Mini Project – Regulatory Compliance Checklist",
  "Day 52: Revision",

  "Day 53: OTC medications & self-care products",
  "Day 54: Counseling patients on OTC use",
  "Day 55: Practice",
  "Day 56: Mini Project – OTC Counseling Draft",
  "Day 57: Revision",

  "Day 58: Herbal & alternative medicines basics",
  "Day 59: Drug-herb interactions & safety",
  "Day 60: Practice",
  "Day 61: Mini Project – Herbal Drug Chart",
  "Day 62: Revision",

  "Day 63: Advanced pharmacy calculations",
  "Day 64: Dilutions, compounding, and IV preparations",
  "Day 65: Practice",
  "Day 66: Mini Project – Calculation Exercises",
  "Day 67: Revision",

  "Day 68: Patient safety & pharmacovigilance",
  "Day 69: Reporting adverse events & errors",
  "Day 70: Practice",
  "Day 71: Mini Project – Pharmacovigilance Report",
  "Day 72: Revision",

  "Day 73: Clinical rotations overview",
  "Day 74: Observing pharmacists in hospital & community settings",
  "Day 75: Practice",
  "Day 76: Mini Project – Rotation Observation Notes",
  "Day 77: Revision",

  "Day 78: Pharmacy analytics & inventory optimization",
  "Day 79: Metrics for performance & stock management",
  "Day 80: Practice",
  "Day 81: Mini Project – Inventory Dashboard",
  "Day 82: Revision",

  "Day 83: Drug storage & stability",
  "Day 84: Temperature, light, and humidity control",
  "Day 85: Practice",
  "Day 86: Mini Project – Storage Compliance Checklist",
  "Day 87: Revision",

  "Day 88: Patient communication & counseling skills",
  "Day 89: Handling difficult patients & adherence issues",
  "Day 90: Practice",
  "Day 91: Mini Project – Communication Plan",
  "Day 92: Revision",

  "Day 93: Research & evidence-based pharmacy practice",
  "Day 94: Interpreting clinical studies & guidelines",
  "Day 95: Practice",
  "Day 96: Mini Project – Literature Review Summary",
  "Day 97: Revision",

  "Day 98: Leadership & team management in pharmacy",
  "Day 99: Mentoring junior staff & workflow management",
  "Day 100: Practice",
  "Day 101: Mini Project – Team Management Plan",
  "Day 102: Revision",

  "Day 103: Strategic pharmacy operations",
  "Day 104: Aligning pharmacy with hospital or business objectives",
  "Day 105: Practice",
  "Day 106: Mini Project – Strategic Pharmacy Plan",
  "Day 107: Revision",

  "Day 108: Ethics & professional standards",
  "Day 109: Patient confidentiality & professional conduct",
  "Day 110: Practice",
  "Day 111: Mini Project – Ethics Case Study",
  "Day 112: Revision",

  "Day 113: Portfolio planning",
  "Day 114: Collecting patient counseling notes, projects & reports",
  "Day 115: Formatting & presentation",
  "Day 116: Practice",
  "Day 117: Portfolio Draft",
  "Day 118: Revision",

  "Day 119: Resume & LinkedIn setup",
  "Day 120:  pharmacy career progression"
],
"Physiotherapist": [

  "Day 1: Understand Physiotherapist role & career paths",
  "Day 2: Basics of human anatomy",
  "Day 3: Physiology fundamentals",
  "Day 4: Medical terminology & abbreviations",
  "Day 5: Tools setup (Physio apps, anatomy atlases, journals)",
  "Day 6: Introduction to physiotherapy ethics & patient care",
  "Day 7: Revision",

  "Day 8: Biomechanics basics",
  "Day 9: Human movement analysis",
  "Day 10: Practice",
  "Day 11: Mini Project – Movement Analysis Chart",
  "Day 12: Revision",

  "Day 13: Musculoskeletal system overview",
  "Day 14: Common injuries & disorders",
  "Day 15: Practice",
  "Day 16: Mini Project – Musculoskeletal Case Summary",
  "Day 17: Revision",

  "Day 18: Neurological system overview",
  "Day 19: Common neurological disorders & rehabilitation",
  "Day 20: Practice",
  "Day 21: Mini Project – Neurological Case Draft",
  "Day 22: Revision",

  "Day 23: Cardiopulmonary system basics",
  "Day 24: Assessment & rehabilitation techniques",
  "Day 25: Practice",
  "Day 26: Mini Project – Cardiopulmonary Rehab Plan",
  "Day 27: Revision",

  "Day 28: Orthopedic assessment basics",
  "Day 29: Range of motion & strength testing",
  "Day 30: Practice",
  "Day 31: Mini Project – Orthopedic Assessment Sheet",
  "Day 32: Revision",

  "Day 33: Exercise therapy basics",
  "Day 34: Designing strength, flexibility & endurance exercises",
  "Day 35: Practice",
  "Day 36: Mini Project – Exercise Plan Draft",
  "Day 37: Revision",

  "Day 38: Electrotherapy & modalities overview",
  "Day 39: TENS, ultrasound, heat & cold therapy",
  "Day 40: Practice",
  "Day 41: Mini Project – Modalities Usage Record",
  "Day 42: Revision",

  "Day 43: Manual therapy basics",
  "Day 44: Soft tissue mobilization & joint techniques",
  "Day 45: Practice",
  "Day 46: Mini Project – Manual Therapy Log",
  "Day 47: Revision",

  "Day 48: Gait & posture assessment",
  "Day 49: Corrective interventions & exercises",
  "Day 50: Practice",
  "Day 51: Mini Project – Gait Analysis Report",
  "Day 52: Revision",

  "Day 53: Pediatric physiotherapy basics",
  "Day 54: Growth & developmental milestones",
  "Day 55: Practice",
  "Day 56: Mini Project – Pediatric Care Plan",
  "Day 57: Revision",

  "Day 58: Geriatric physiotherapy basics",
  "Day 59: Mobility & fall prevention techniques",
  "Day 60: Practice",
  "Day 61: Mini Project – Geriatric Care Plan",
  "Day 62: Revision",

  "Day 63: Sports physiotherapy basics",
  "Day 64: Injury prevention & rehabilitation",
  "Day 65: Practice",
  "Day 66: Mini Project – Sports Rehab Plan",
  "Day 67: Revision",

  "Day 68: Respiratory physiotherapy basics",
  "Day 69: Breathing exercises & patient monitoring",
  "Day 70: Practice",
  "Day 71: Mini Project – Respiratory Care Plan",
  "Day 72: Revision",

  "Day 73: Pain management & therapeutic techniques",
  "Day 74: Chronic pain & post-surgical care",
  "Day 75: Practice",
  "Day 76: Mini Project – Pain Management Plan",
  "Day 77: Revision",

  "Day 78: Patient assessment & treatment planning",
  "Day 79: Documentation & progress tracking",
  "Day 80: Practice",
  "Day 81: Mini Project – Patient Treatment Plan",
  "Day 82: Revision",

  "Day 83: Clinical rotations overview",
  "Day 84: Observing physiotherapy sessions",
  "Day 85: Practice",
  "Day 86: Mini Project – Clinical Observation Notes",
  "Day 87: Revision",

  "Day 88: Rehabilitation for post-surgical patients",
  "Day 89: Early mobilization & functional recovery",
  "Day 90: Practice",
  "Day 91: Mini Project – Rehab Plan Draft",
  "Day 92: Revision",

  "Day 93: Assistive devices & ergonomics",
  "Day 94: Wheelchairs, walkers & workplace ergonomics",
  "Day 95: Practice",
  "Day 96: Mini Project – Assistive Device Plan",
  "Day 97: Revision",

  "Day 98: Patient communication & counseling",
  "Day 99: Handling patient concerns & motivation",
  "Day 100: Practice",
  "Day 101: Mini Project – Patient Communication Log",
  "Day 102: Revision",

  "Day 103: Evidence-based physiotherapy practice",
  "Day 104: Reading & interpreting clinical research",
  "Day 105: Practice",
  "Day 106: Mini Project – Literature Review Summary",
  "Day 107: Revision",

  "Day 108: Leadership & team management in physiotherapy",
  "Day 109: Mentoring junior staff & organizing sessions",
  "Day 110: Practice",
  "Day 111: Mini Project – Team Management Plan",
  "Day 112: Revision",

  "Day 113: Strategic planning for physiotherapy services",
  "Day 114: Aligning with hospital or clinic objectives",
  "Day 115: Practice",
  "Day 116: Mini Project – Strategic Physiotherapy Plan",
  "Day 117: Revision",

  "Day 118: Ethics & professional standards",
  "Day 119: Patient rights & confidentiality",
  "Day 120:  Career progression"
],
"Clinical Researcher": [

  "Day 1: Understand Clinical Researcher role & career paths",
  "Day 2: Basics of medical and scientific terminology",
  "Day 3: Overview of human anatomy & physiology",
  "Day 4: Tools setup (SPSS, Excel, EDC systems, research journals)",
  "Day 5: Introduction to clinical research",
  "Day 6: Research ethics & GCP (Good Clinical Practice)",
  "Day 7: Revision",

  "Day 8: Types of clinical research (observational, interventional, epidemiological)",
  "Day 9: Understanding clinical trials phases (I-IV)",
  "Day 10: Practice",
  "Day 11: Mini Project – Clinical Trial Summary Table",
  "Day 12: Revision",

  "Day 13: Study design basics",
  "Day 14: Randomization, blinding, control groups",
  "Day 15: Practice",
  "Day 16: Mini Project – Study Design Draft",
  "Day 17: Revision",

  "Day 18: Protocol writing basics",
  "Day 19: Creating research objectives & endpoints",
  "Day 20: Practice",
  "Day 21: Mini Project – Protocol Draft",
  "Day 22: Revision",

  "Day 23: Literature review & scientific writing",
  "Day 24: Reference management (Mendeley, Zotero)",
  "Day 25: Practice",
  "Day 26: Mini Project – Literature Review Summary",
  "Day 27: Revision",

  "Day 28: Participant recruitment & informed consent",
  "Day 29: Inclusion & exclusion criteria",
  "Day 30: Practice",
  "Day 31: Mini Project – Recruitment Plan Draft",
  "Day 32: Revision",

  "Day 33: Data collection & source documentation",
  "Day 34: Case report forms (CRF) & electronic data capture",
  "Day 35: Practice",
  "Day 36: Mini Project – Sample CRF Form",
  "Day 37: Revision",

  "Day 38: Monitoring & site visits",
  "Day 39: Ensuring protocol compliance",
  "Day 40: Practice",
  "Day 41: Mini Project – Monitoring Checklist",
  "Day 42: Revision",

  "Day 43: Adverse event reporting & safety monitoring",
  "Day 44: Pharmacovigilance basics",
  "Day 45: Practice",
  "Day 46: Mini Project – AE Reporting Form",
  "Day 47: Revision",

  "Day 48: Regulatory affairs basics",
  "Day 49: FDA, EMA, DCGI guidelines overview",
  "Day 50: Practice",
  "Day 51: Mini Project – Regulatory Compliance Checklist",
  "Day 52: Revision",

  "Day 53: Statistical analysis basics",
  "Day 54: Descriptive & inferential statistics",
  "Day 55: Practice",
  "Day 56: Mini Project – Data Analysis Draft",
  "Day 57: Revision",

  "Day 58: Clinical trial software & EDC tools",
  "Day 59: Data entry, validation & query management",
  "Day 60: Practice",
  "Day 61: Mini Project – EDC Practice",
  "Day 62: Revision",

  "Day 63: Quality assurance & audits",
  "Day 64: SOPs & compliance monitoring",
  "Day 65: Practice",
  "Day 66: Mini Project – QA Checklist",
  "Day 67: Revision",

  "Day 68: Manuscript writing basics",
  "Day 69: Preparing abstracts & scientific papers",
  "Day 70: Practice",
  "Day 71: Mini Project – Manuscript Draft",
  "Day 72: Revision",

  "Day 73: Biostatistics & data interpretation",
  "Day 74: Graphs, tables & reporting",
  "Day 75: Practice",
  "Day 76: Mini Project – Data Interpretation Report",
  "Day 77: Revision",

  "Day 78: Project management in clinical research",
  "Day 79: Timelines, milestones & resource planning",
  "Day 80: Practice",
  "Day 81: Mini Project – Project Plan Draft",
  "Day 82: Revision",

  "Day 83: Clinical research collaborations",
  "Day 84: Interdisciplinary teamwork & stakeholder communication",
  "Day 85: Practice",
  "Day 86: Mini Project – Collaboration Plan",
  "Day 87: Revision",

  "Day 88: Clinical research ethics & compliance",
  "Day 89: IRB/IEC submissions & approvals",
  "Day 90: Practice",
  "Day 91: Mini Project – IRB Submission Draft",
  "Day 92: Revision",

  "Day 93: Grant writing & funding basics",
  "Day 94: Preparing research proposals",
  "Day 95: Practice",
  "Day 96: Mini Project – Grant Proposal Draft",
  "Day 97: Revision",

  "Day 98: Presentation skills & scientific communication",
  "Day 99: Conferences, posters & seminars",
  "Day 100: Practice",
  "Day 101: Mini Project – Presentation Draft",
  "Day 102: Revision",

  "Day 103: Career development & networking",
  "Day 104: Resume & LinkedIn setup",
  "Day 105: Job & internship applications",
  "Day 106: Practice",
  "Day 107: Portfolio Draft",
  "Day 108: Revision",

  "Day 109: Portfolio planning",
  "Day 110: Collecting study protocols, reports & data analyses",
  "Day 111: Formatting & presentation",
  "Day 112: Practice",
  "Day 113: Portfolio Draft Review",
  "Day 114: Revision",

  "Day 115: Mock interviews & career preparation",
  "Day 116: Advanced research tool practice",
  "Day 117: Final portfolio preparation",
  "Day 118: Final review of all topics",
  "Day 119: Certification & course planning (GCP, Biostatistics, Clinical Trial Design)",
  "Day 120: clinical research career progression"
],
#for lawyer
"Lawyer": [

  "Day 1: Understand Lawyer role & career paths",
  "Day 2: Basics of law & legal systems",
  "Day 3: Legal terminology & abbreviations",
  "Day 4: Tools setup (Legal research platforms, law journals, case databases)",
  "Day 5: Introduction to ethics & professional conduct",
  "Day 6: Understanding fundamental rights & duties",
  "Day 7: Revision",

  "Day 8: Contract law basics",
  "Day 9: Elements of contracts & types",
  "Day 10: Practice",
  "Day 11: Mini Project – Draft Sample Contract",
  "Day 12: Revision",

  "Day 13: Criminal law basics",
  "Day 14: Understanding offences, penalties & procedures",
  "Day 15: Practice",
  "Day 16: Mini Project – Case Study Draft",
  "Day 17: Revision",

  "Day 18: Civil law basics",
  "Day 19: Property, family, and tort law overview",
  "Day 20: Practice",
  "Day 21: Mini Project – Civil Case Draft",
  "Day 22: Revision",

  "Day 23: Constitutional law basics",
  "Day 24: Separation of powers & judicial review",
  "Day 25: Practice",
  "Day 26: Mini Project – Constitutional Case Summary",
  "Day 27: Revision",

  "Day 28: Legal research basics",
  "Day 29: Using legal databases & case laws",
  "Day 30: Practice",
  "Day 31: Mini Project – Legal Research Report",
  "Day 32: Revision",

  "Day 33: Legal writing & drafting",
  "Day 34: Pleadings, petitions & agreements",
  "Day 35: Practice",
  "Day 36: Mini Project – Draft Legal Document",
  "Day 37: Revision",

  "Day 38: Advocacy basics",
  "Day 39: Court procedures & etiquette",
  "Day 40: Practice",
  "Day 41: Mini Project – Mock Court Argument Draft",
  "Day 42: Revision",

  "Day 43: Evidence law basics",
  "Day 44: Gathering, presenting & evaluating evidence",
  "Day 45: Practice",
  "Day 46: Mini Project – Evidence Log Draft",
  "Day 47: Revision",

  "Day 48: Client consultation basics",
  "Day 49: Communication, documentation & confidentiality",
  "Day 50: Practice",
  "Day 51: Mini Project – Client Consultation Draft",
  "Day 52: Revision",

  "Day 53: Intellectual property law basics",
  "Day 54: Patents, copyrights, trademarks & licensing",
  "Day 55: Practice",
  "Day 56: Mini Project – IP Case Draft",
  "Day 57: Revision",

  "Day 58: Corporate law basics",
  "Day 59: Company formation, governance & compliance",
  "Day 60: Practice",
  "Day 61: Mini Project – Corporate Compliance Draft",
  "Day 62: Revision",

  "Day 63: Labour & employment law basics",
  "Day 64: Employee rights, contracts & regulations",
  "Day 65: Practice",
  "Day 66: Mini Project – Employment Case Draft",
  "Day 67: Revision",

  "Day 68: Tax law basics",
  "Day 69: Income tax, GST & compliance overview",
  "Day 70: Practice",
  "Day 71: Mini Project – Tax Case Draft",
  "Day 72: Revision",

  "Day 73: Negotiation & mediation skills",
  "Day 74: Conflict resolution & settlement drafting",
  "Day 75: Practice",
  "Day 76: Mini Project – Mediation Draft",
  "Day 77: Revision",

  "Day 78: Advanced legal research",
  "Day 79: Case law analysis & precedent study",
  "Day 80: Practice",
  "Day 81: Mini Project – Case Analysis Report",
  "Day 82: Revision",

  "Day 83: Ethics & professional responsibility",
  "Day 84: Client confidentiality & conflict of interest",
  "Day 85: Practice",
  "Day 86: Mini Project – Ethics Case Study",
  "Day 87: Revision",

  "Day 88: Legal technology tools",
  "Day 89: Case management software & research tools",
  "Day 90: Practice",
  "Day 91: Mini Project – Legal Tech Demo",
  "Day 92: Revision",

  "Day 93: Mock trials & courtroom practice",
  "Day 94: Drafting & presenting arguments",
  "Day 95: Practice",
  "Day 96: Mini Project – Mock Trial Report",
  "Day 97: Revision",

  "Day 98: Client management & professional communication",
  "Day 99: Handling queries & documentation",
  "Day 100: Practice",
  "Day 101: Mini Project – Client Interaction Log",
  "Day 102: Revision",

  "Day 103: Portfolio planning",
  "Day 104: Collecting case studies, legal drafts & research reports",
  "Day 105: Formatting & presentation",
  "Day 106: Practice",
  "Day 107: Portfolio Draft",
  "Day 108: Revision",

  "Day 109: Resume & LinkedIn setup",
  "Day 110: Apply for internships or clerkships",
  "Day 111: Networking & mentorship",
  "Day 112: Practice",
  "Day 113: Final portfolio preparation",
  "Day 114: Mock interviews",
  "Day 115: Revision",

  "Day 116: Specialization planning (Corporate, Criminal, IP, Tax, Civil, etc.)",
  "Day 117: Certification & course planning",
  "Day 118: Continuing legal education overview",
  "Day 119: Final review of all topics",
  "Day 120:legal career progression"
],
"Corporate Lawyer": [

  "Day 1: Understand Corporate Lawyer role & career paths",
  "Day 2: Basics of corporate law & legal systems",
  "Day 3: Legal terminology & abbreviations in business law",
  "Day 4: Tools setup (Legal research platforms, business law journals, company law books)",
  "Day 5: Introduction to ethics & professional conduct",
  "Day 6: Overview of corporate governance principles",
  "Day 7: Revision",

  "Day 8: Company formation & registration process",
  "Day 9: Types of companies & legal requirements",
  "Day 10: Practice",
  "Day 11: Mini Project – Company Formation Draft",
  "Day 12: Revision",

  "Day 13: Corporate contracts basics",
  "Day 14: Drafting agreements, MOUs & shareholder agreements",
  "Day 15: Practice",
  "Day 16: Mini Project – Contract Draft",
  "Day 17: Revision",

  "Day 18: Corporate compliance overview",
  "Day 19: Regulatory frameworks & filing requirements",
  "Day 20: Practice",
  "Day 21: Mini Project – Compliance Checklist",
  "Day 22: Revision",

  "Day 23: Corporate finance basics",
  "Day 24: Securities, capital raising & investment regulations",
  "Day 25: Practice",
  "Day 26: Mini Project – Financial Compliance Draft",
  "Day 27: Revision",

  "Day 28: Mergers & acquisitions basics",
  "Day 29: Due diligence, agreements & approvals",
  "Day 30: Practice",
  "Day 31: Mini Project – M&A Case Study",
  "Day 32: Revision",

  "Day 33: Intellectual property in business",
  "Day 34: Patents, trademarks & licensing in corporate settings",
  "Day 35: Practice",
  "Day 36: Mini Project – IP Compliance Draft",
  "Day 37: Revision",

  "Day 38: Employment & labor laws in corporations",
  "Day 39: Employee contracts & compliance",
  "Day 40: Practice",
  "Day 41: Mini Project – Employment Agreement Draft",
  "Day 42: Revision",

  "Day 43: Taxation & corporate law",
  "Day 44: Corporate tax, GST & filing compliance",
  "Day 45: Practice",
  "Day 46: Mini Project – Tax Compliance Draft",
  "Day 47: Revision",

  "Day 48: Corporate litigation basics",
  "Day 49: Handling disputes & representing clients",
  "Day 50: Practice",
  "Day 51: Mini Project – Corporate Case Draft",
  "Day 52: Revision",

  "Day 53: Negotiation & deal structuring",
  "Day 54: Contracts negotiation, stakeholder management",
  "Day 55: Practice",
  "Day 56: Mini Project – Negotiation Simulation Draft",
  "Day 57: Revision",

  "Day 58: Corporate ethics & governance compliance",
  "Day 59: Conflict of interest & corporate social responsibility",
  "Day 60: Practice",
  "Day 61: Mini Project – Ethics Case Study",
  "Day 62: Revision",

  "Day 63: Legal research in corporate context",
  "Day 64: Case law & statutory interpretation",
  "Day 65: Practice",
  "Day 66: Mini Project – Research Report Draft",
  "Day 67: Revision",

  "Day 68: Corporate reporting & documentation",
  "Day 69: Board minutes, resolutions & filings",
  "Day 70: Practice",
  "Day 71: Mini Project – Sample Corporate Documentation",
  "Day 72: Revision",

  "Day 73: Risk management & compliance audits",
  "Day 74: Identifying legal risks & mitigation strategies",
  "Day 75: Practice",
  "Day 76: Mini Project – Risk Assessment Report",
  "Day 77: Revision",

  "Day 78: Corporate strategy & advisory",
  "Day 79: Providing legal advice for business decisions",
  "Day 80: Practice",
  "Day 81: Mini Project – Advisory Draft",
  "Day 82: Revision",

  "Day 83: Mergers, acquisitions & corporate restructuring",
  "Day 84: Legal framework & documentation",
  "Day 85: Practice",
  "Day 86: Mini Project – Restructuring Case Study",
  "Day 87: Revision",

  "Day 88: Corporate governance & board advisory",
  "Day 89: Legal compliance with corporate governance codes",
  "Day 90: Practice",
  "Day 91: Mini Project – Governance Audit Draft",
  "Day 92: Revision",

  "Day 93: Client management & professional communication",
  "Day 94: Handling corporate clients & documentation",
  "Day 95: Practice",
  "Day 96: Mini Project – Client Interaction Log",
  "Day 97: Revision",

  "Day 98: Corporate research & report writing",
  "Day 99: Market & legal research for advisory services",
  "Day 100: Practice",
  "Day 101: Mini Project – Research Report Draft",
  "Day 102: Revision",

  "Day 103: Portfolio planning",
  "Day 104: Collecting contracts, compliance reports & case studies",
  "Day 105: Formatting & presentation",
  "Day 106: Practice",
  "Day 107: Portfolio Draft",
  "Day 108: Revision",

  "Day 109: Resume & LinkedIn setup",
  "Day 110: Apply for corporate law internships or clerkships",
  "Day 111: Networking & mentorship",
  "Day 112: Practice",
  "Day 113: Final portfolio preparation",
  "Day 114: Mock interviews",
  "Day 115: Revision",

  "Day 116: Specialization planning (M&A, Compliance, Corporate Litigation, IP, Tax)",
  "Day 117: Certification & course planning",
  "Day 118: Continuing legal education overview",
  "Day 119: Final review of all topics",
  "Day 120:  corporate law career progression"
],
"Public Prosecutor": [

  "Day 1: Understand Public Prosecutor role & career paths",
  "Day 2: Basics of criminal law & legal system overview",
  "Day 3: Legal terminology & abbreviations",
  "Day 4: Tools setup (Legal research platforms, case law databases, law journals)",
  "Day 5: Introduction to ethics & professional conduct",
  "Day 6: Understanding the role of prosecution in justice system",
  "Day 7: Revision",

  "Day 8: Criminal procedure basics",
  "Day 9: Filing FIRs, complaints & police reports",
  "Day 10: Practice",
  "Day 11: Mini Project – Sample FIR Draft",
  "Day 12: Revision",

  "Day 13: Investigation process & evidence collection",
  "Day 14: Role of prosecutor in investigation",
  "Day 15: Practice",
  "Day 16: Mini Project – Investigation Report Draft",
  "Day 17: Revision",

  "Day 18: Understanding offences & penal codes",
  "Day 19: Classification of crimes & punishments",
  "Day 20: Practice",
  "Day 21: Mini Project – Crime Classification Table",
  "Day 22: Revision",

  "Day 23: Court procedures & criminal trials",
  "Day 24: Filing charges, summons & documentation",
  "Day 25: Practice",
  "Day 26: Mini Project – Case Filing Draft",
  "Day 27: Revision",

  "Day 28: Evidence law basics",
  "Day 29: Gathering, presenting & examining evidence",
  "Day 30: Practice",
  "Day 31: Mini Project – Evidence Documentation",
  "Day 32: Revision",

  "Day 33: Witness examination & cross-examination techniques",
  "Day 34: Preparing witnesses & statements",
  "Day 35: Practice",
  "Day 36: Mini Project – Witness Prep Sheet",
  "Day 37: Revision",

  "Day 38: Criminal drafting skills",
  "Day 39: Charge sheets, legal notices & petitions",
  "Day 40: Practice",
  "Day 41: Mini Project – Draft Legal Document",
  "Day 42: Revision",

  "Day 43: Courtroom advocacy basics",
  "Day 44: Opening statements, arguments & closing statements",
  "Day 45: Practice",
  "Day 46: Mini Project – Mock Court Argument Draft",
  "Day 47: Revision",

  "Day 48: Plea bargaining & settlement procedures",
  "Day 49: Negotiation with defense & case strategy",
  "Day 50: Practice",
  "Day 51: Mini Project – Plea Draft Simulation",
  "Day 52: Revision",

  "Day 53: Criminal research & precedent analysis",
  "Day 54: Case law, statutes & judicial interpretations",
  "Day 55: Practice",
  "Day 56: Mini Project – Research Report Draft",
  "Day 57: Revision",

  "Day 58: Professional ethics in prosecution",
  "Day 59: Avoiding conflicts of interest & misconduct",
  "Day 60: Practice",
  "Day 61: Mini Project – Ethics Case Study",
  "Day 62: Revision",

  "Day 63: Forensic basics for prosecutors",
  "Day 64: Understanding forensic evidence & expert testimony",
  "Day 65: Practice",
  "Day 66: Mini Project – Forensic Evidence Draft",
  "Day 67: Revision",

  "Day 68: High-profile case study analysis",
  "Day 69: Strategy & legal argument planning",
  "Day 70: Practice",
  "Day 71: Mini Project – Case Analysis Report",
  "Day 72: Revision",

  "Day 73: Criminal appellate procedures",
  "Day 74: Filing appeals & drafting appellate documents",
  "Day 75: Practice",
  "Day 76: Mini Project – Appeal Draft",
  "Day 77: Revision",

  "Day 78: Time management & trial preparation",
  "Day 79: Scheduling, deadlines & court readiness",
  "Day 80: Practice",
  "Day 81: Mini Project – Trial Prep Checklist",
  "Day 82: Revision",

  "Day 83: Client management & communication",
  "Day 84: Interaction with police, witnesses & victims",
  "Day 85: Practice",
  "Day 86: Mini Project – Communication Log",
  "Day 87: Revision",

  "Day 88: Evidence presentation techniques",
  "Day 89: Using exhibits, charts & multimedia",
  "Day 90: Practice",
  "Day 91: Mini Project – Exhibit Presentation Draft",
  "Day 92: Revision",

  "Day 93: Mock trials & courtroom practice",
  "Day 94: Trial simulation & advocacy skills",
  "Day 95: Practice",
  "Day 96: Mini Project – Mock Trial Report",
  "Day 97: Revision",

  "Day 98: Legal technology tools for prosecutors",
  "Day 99: Case management & research software",
  "Day 100: Practice",
  "Day 101: Mini Project – Legal Tech Demo",
  "Day 102: Revision",

  "Day 103: Portfolio planning",
  "Day 104: Collecting case reports, research & trial drafts",
  "Day 105: Formatting & presentation",
  "Day 106: Practice",
  "Day 107: Portfolio Draft",
  "Day 108: Revision",

  "Day 109: Resume & LinkedIn setup",
  "Day 110: Apply for public prosecutor internships or clerkships",
  "Day 111: Networking & mentorship",
  "Day 112: Practice",
  "Day 113: Final portfolio preparation",
  "Day 114: Mock interviews",
  "Day 115: Revision",

  "Day 116: Specialization planning (Criminal, Anti-Corruption, Cybercrime, Forensic)",
  "Day 117: Certification & course planning",
  "Day 118: Continuing legal education overview",
  "Day 119: Final review of all topics",
  "Day 120: Public Prosecutor career progression"
],
"Legal Advisor": [

  "Day 1: Understand Legal Advisor role & career paths",
  "Day 2: Basics of law & legal systems",
  "Day 3: Legal terminology & abbreviations",
  "Day 4: Tools setup (Legal research platforms, contract management software, law journals)",
  "Day 5: Introduction to ethics & professional conduct",
  "Day 6: Overview of advisory roles in business & corporate settings",
  "Day 7: Revision",

  "Day 8: Corporate law fundamentals",
  "Day 9: Company formation, governance & regulatory compliance",
  "Day 10: Practice",
  "Day 11: Mini Project – Corporate Compliance Draft",
  "Day 12: Revision",

  "Day 13: Contract law basics",
  "Day 14: Drafting agreements, MOUs & NDAs",
  "Day 15: Practice",
  "Day 16: Mini Project – Contract Draft",
  "Day 17: Revision",

  "Day 18: Employment & labor law basics",
  "Day 19: Employee contracts, benefits & compliance",
  "Day 20: Practice",
  "Day 21: Mini Project – Employment Agreement Draft",
  "Day 22: Revision",

  "Day 23: Intellectual property law basics",
  "Day 24: Patents, trademarks, copyrights & licensing",
  "Day 25: Practice",
  "Day 26: Mini Project – IP Compliance Draft",
  "Day 27: Revision",

  "Day 28: Taxation basics",
  "Day 29: Corporate tax, GST & legal compliance",
  "Day 30: Practice",
  "Day 31: Mini Project – Tax Compliance Draft",
  "Day 32: Revision",

  "Day 33: Legal research & statutory interpretation",
  "Day 34: Case law study for advisory purposes",
  "Day 35: Practice",
  "Day 36: Mini Project – Legal Research Report",
  "Day 37: Revision",

  "Day 38: Regulatory compliance & advisory",
  "Day 39: Reporting, filings & corporate audits",
  "Day 40: Practice",
  "Day 41: Mini Project – Compliance Audit Draft",
  "Day 42: Revision",

  "Day 43: Risk management & legal mitigation strategies",
  "Day 44: Identifying legal risks & preventive measures",
  "Day 45: Practice",
  "Day 46: Mini Project – Risk Assessment Report",
  "Day 47: Revision",

  "Day 48: Client consultation & advisory skills",
  "Day 49: Communication, negotiation & documentation",
  "Day 50: Practice",
  "Day 51: Mini Project – Client Consultation Draft",
  "Day 52: Revision",

  "Day 53: Mergers, acquisitions & corporate restructuring basics",
  "Day 54: Legal advisory for corporate deals",
  "Day 55: Practice",
  "Day 56: Mini Project – M&A Advisory Draft",
  "Day 57: Revision",

  "Day 58: Intellectual property advisory",
  "Day 59: Licensing, commercialization & IP strategy",
  "Day 60: Practice",
  "Day 61: Mini Project – IP Advisory Report",
  "Day 62: Revision",

  "Day 63: Financial & banking law basics",
  "Day 64: Legal advisory in finance, investments & contracts",
  "Day 65: Practice",
  "Day 66: Mini Project – Financial Advisory Draft",
  "Day 67: Revision",

  "Day 68: Dispute resolution & negotiation",
  "Day 69: Arbitration, mediation & settlements",
  "Day 70: Practice",
  "Day 71: Mini Project – Dispute Resolution Draft",
  "Day 72: Revision",

  "Day 73: Legal drafting for advisory purposes",
  "Day 74: Reports, notices & advisory opinions",
  "Day 75: Practice",
  "Day 76: Mini Project – Advisory Document Draft",
  "Day 77: Revision",

  "Day 78: Ethics & professional responsibility",
  "Day 79: Confidentiality, conflicts of interest & compliance",
  "Day 80: Practice",
  "Day 81: Mini Project – Ethics Case Study",
  "Day 82: Revision",

  "Day 83: Legal technology tools",
  "Day 84: Contract management software & legal research tools",
  "Day 85: Practice",
  "Day 86: Mini Project – Legal Tech Demo",
  "Day 87: Revision",

  "Day 88: Case studies & advisory simulation",
  "Day 89: Handling client scenarios & legal opinion drafting",
  "Day 90: Practice",
  "Day 91: Mini Project – Advisory Case Study",
  "Day 92: Revision",

  "Day 93: Corporate governance advisory",
  "Day 94: Board meetings, resolutions & legal compliance",
  "Day 95: Practice",
  "Day 96: Mini Project – Governance Advisory Draft",
  "Day 97: Revision",

  "Day 98: Portfolio planning",
  "Day 99: Collecting advisory reports, contracts & case studies",
  "Day 100: Formatting & presentation",
  "Day 101: Practice",
  "Day 102: Portfolio Draft",
  "Day 103: Revision",

  "Day 104: Resume & LinkedIn setup",
  "Day 105: Apply for legal advisory internships or clerkships",
  "Day 106: Networking & mentorship",
  "Day 107: Practice",
  "Day 108: Final portfolio preparation",
  "Day 109: Mock interviews",
  "Day 110: Revision",

  "Day 111: Specialization planning (Corporate, Tax, IP, Employment, M&A, Financial Advisory)",
  "Day 112: Certification & course planning",
  "Day 113: Continuing legal education overview",
  "Day 114: Client communication & presentation practice",
  "Day 115: Mock advisory sessions",
  "Day 116: Review contracts & advisory templates",
  "Day 117: Advanced case simulations",
  "Day 118: Final review of all topics",
  "Day 119: Career planning & roadmap preparation",
  "Day 120: Legal Advisor career progression"
],
# Education adminstrator
"Education Counselor": [

  "Day 1: Understand Education Counselor role & career paths",
  "Day 2: Basics of counseling & guidance",
  "Day 3: Educational systems overview",
  "Day 4: Tools setup (Career assessment tools, student databases, counseling software)",
  "Day 5: Introduction to ethics & professional conduct",
  "Day 6: Communication skills fundamentals",
  "Day 7: Revision",

  "Day 8: Basics of psychology for counseling",
  "Day 9: Understanding student behavior & learning styles",
  "Day 10: Practice",
  "Day 11: Mini Project – Learning Style Assessment Draft",
  "Day 12: Revision",

  "Day 13: Academic counseling fundamentals",
  "Day 14: Study planning & time management strategies",
  "Day 15: Practice",
  "Day 16: Mini Project – Sample Academic Plan",
  "Day 17: Revision",

  "Day 18: Career counseling basics",
  "Day 19: Career assessment tools & aptitude tests",
  "Day 20: Practice",
  "Day 21: Mini Project – Career Assessment Report",
  "Day 22: Revision",

  "Day 23: College & university guidance",
  "Day 24: Admission procedures, eligibility & scholarships",
  "Day 25: Practice",
  "Day 26: Mini Project – College Guidance Draft",
  "Day 27: Revision",

  "Day 28: Vocational & skill-based counseling",
  "Day 29: Identifying student interests & aptitude",
  "Day 30: Practice",
  "Day 31: Mini Project – Skill Assessment Report",
  "Day 32: Revision",

  "Day 33: Counseling for competitive exams",
  "Day 34: Exam strategies & preparation planning",
  "Day 35: Practice",
  "Day 36: Mini Project – Exam Preparation Plan",
  "Day 37: Revision",

  "Day 38: Emotional & social counseling",
  "Day 39: Handling stress, anxiety & motivation",
  "Day 40: Practice",
  "Day 41: Mini Project – Counseling Session Notes",
  "Day 42: Revision",

  "Day 43: Special needs education counseling",
  "Day 44: Inclusive learning strategies & support",
  "Day 45: Practice",
  "Day 46: Mini Project – Special Needs Plan",
  "Day 47: Revision",

  "Day 48: Communication & interpersonal skills advanced",
  "Day 49: Listening, empathy & conflict resolution",
  "Day 50: Practice",
  "Day 51: Mini Project – Communication Skill Exercise",
  "Day 52: Revision",

  "Day 53: Student assessment & progress tracking",
  "Day 54: Academic reports & feedback sessions",
  "Day 55: Practice",
  "Day 56: Mini Project – Progress Report Draft",
  "Day 57: Revision",

  "Day 58: Technology in counseling",
  "Day 59: Online tools, webinars & virtual guidance",
  "Day 60: Practice",
  "Day 61: Mini Project – Online Counseling Session Draft",
  "Day 62: Revision",

  "Day 63: Group counseling & workshops",
  "Day 64: Planning & executing sessions",
  "Day 65: Practice",
  "Day 66: Mini Project – Workshop Plan",
  "Day 67: Revision",

  "Day 68: Career trends & labor market overview",
  "Day 69: Guiding students on emerging careers",
  "Day 70: Practice",
  "Day 71: Mini Project – Career Trend Report",
  "Day 72: Revision",

  "Day 73: Counseling ethics & confidentiality",
  "Day 74: Handling sensitive student information",
  "Day 75: Practice",
  "Day 76: Mini Project – Ethics Case Study",
  "Day 77: Revision",

  "Day 78: Parent & teacher communication",
  "Day 79: Collaborative planning & guidance",
  "Day 80: Practice",
  "Day 81: Mini Project – Parent Meeting Notes",
  "Day 82: Revision",

  "Day 83: College & career fairs guidance",
  "Day 84: Planning and organizing events",
  "Day 85: Practice",
  "Day 86: Mini Project – Event Plan Draft",
  "Day 87: Revision",

  "Day 88: Leadership & team management in counseling",
  "Day 89: Mentoring junior counselors",
  "Day 90: Practice",
  "Day 91: Mini Project – Team Management Plan",
  "Day 92: Revision",

  "Day 93: Documentation & reporting",
  "Day 94: Maintaining student records & reports",
  "Day 95: Practice",
  "Day 96: Mini Project – Record Keeping Draft",
  "Day 97: Revision",

  "Day 98: Evaluation & feedback techniques",
  "Day 99: Continuous improvement in counseling practices",
  "Day 100: Practice",
  "Day 101: Mini Project – Feedback Analysis Report",
  "Day 102: Revision",

  "Day 103: Portfolio planning",
  "Day 104: Collecting assessment reports, guidance plans & session notes",
  "Day 105: Formatting & presentation",
  "Day 106: Practice",
  "Day 107: Portfolio Draft",
  "Day 108: Revision",

  "Day 109: Resume & LinkedIn setup",
  "Day 110: Apply for internships or counseling assistant positions",
  "Day 111: Networking & mentorship",
  "Day 112: Practice",
  "Day 113: Final portfolio preparation",
  "Day 114: Mock interviews",
  "Day 115: Revision",

  "Day 116: Specialization planning (School, College, Career, Vocational, Special Needs)",
  "Day 117: Certification & course planning",
  "Day 118: Continuing education overview",
  "Day 119: Final review of all topics",
  "Day 120: Next-step roadmap for Education Counselor career progression"
],
"School Administrator": [

  "Day 1: Understand School Administrator role & career paths",
  "Day 2: Basics of school management & organizational structure",
  "Day 3: Legal and regulatory frameworks for schools",
  "Day 4: Tools setup (School management software, databases, spreadsheets)",
  "Day 5: Introduction to ethics & professional conduct",
  "Day 6: Communication skills fundamentals",
  "Day 7: Revision",

  "Day 8: Academic planning & curriculum management",
  "Day 9: Scheduling classes, exams, and events",
  "Day 10: Practice",
  "Day 11: Mini Project – Academic Calendar Draft",
  "Day 12: Revision",

  "Day 13: Teacher recruitment & staff management",
  "Day 14: Hiring procedures, contracts & performance evaluation",
  "Day 15: Practice",
  "Day 16: Mini Project – Staff Management Plan",
  "Day 17: Revision",

  "Day 18: Student enrollment & admissions process",
  "Day 19: Admission criteria, interviews & documentation",
  "Day 20: Practice",
  "Day 21: Mini Project – Admission Plan Draft",
  "Day 22: Revision",

  "Day 23: Financial management basics",
  "Day 24: Budgeting, fee management & reporting",
  "Day 25: Practice",
  "Day 26: Mini Project – School Budget Draft",
  "Day 27: Revision",

  "Day 28: School policies & procedures",
  "Day 29: Developing, communicating, and enforcing policies",
  "Day 30: Practice",
  "Day 31: Mini Project – Policy Draft",
  "Day 32: Revision",

  "Day 33: Facility & resource management",
  "Day 34: Classroom, library, laboratory & IT management",
  "Day 35: Practice",
  "Day 36: Mini Project – Resource Management Plan",
  "Day 37: Revision",

  "Day 38: Student support services",
  "Day 39: Counseling, health & extracurricular activities management",
  "Day 40: Practice",
  "Day 41: Mini Project – Student Support Plan",
  "Day 42: Revision",

  "Day 43: Academic assessment & reporting",
  "Day 44: Exams, grading, performance tracking & reports",
  "Day 45: Practice",
  "Day 46: Mini Project – Performance Report Draft",
  "Day 47: Revision",

  "Day 48: Parent & community communication",
  "Day 49: Parent-teacher meetings, newsletters & events",
  "Day 50: Practice",
  "Day 51: Mini Project – Communication Plan Draft",
  "Day 52: Revision",

  "Day 53: Leadership & team management",
  "Day 54: Motivating staff, conflict resolution & delegation",
  "Day 55: Practice",
  "Day 56: Mini Project – Team Management Draft",
  "Day 57: Revision",

  "Day 58: Technology in school administration",
  "Day 59: School management software, online platforms & virtual classrooms",
  "Day 60: Practice",
  "Day 61: Mini Project – Technology Integration Plan",
  "Day 62: Revision",

  "Day 63: Legal compliance & safety regulations",
  "Day 64: Child safety, labor laws & statutory compliance",
  "Day 65: Practice",
  "Day 66: Mini Project – Compliance Checklist",
  "Day 67: Revision",

  "Day 68: Strategic planning & school improvement",
  "Day 69: Long-term vision, goals & monitoring progress",
  "Day 70: Practice",
  "Day 71: Mini Project – Strategic Plan Draft",
  "Day 72: Revision",

  "Day 73: Event management & coordination",
  "Day 74: Annual functions, workshops & seminars",
  "Day 75: Practice",
  "Day 76: Mini Project – Event Plan Draft",
  "Day 77: Revision",

  "Day 78: Quality assurance & accreditation",
  "Day 79: Preparing for inspections, audits & accreditation processes",
  "Day 80: Practice",
  "Day 81: Mini Project – QA Checklist",
  "Day 82: Revision",

  "Day 83: Marketing & admissions strategy",
  "Day 84: Promoting school programs & brand building",
  "Day 85: Practice",
  "Day 86: Mini Project – Marketing Plan Draft",
  "Day 87: Revision",

  "Day 88: Financial audits & reporting",
  "Day 89: Tracking expenses, income & compliance reports",
  "Day 90: Practice",
  "Day 91: Mini Project – Audit Report Draft",
  "Day 92: Revision",

  "Day 93: Mentorship & professional development",
  "Day 94: Staff training, workshops & leadership programs",
  "Day 95: Practice",
  "Day 96: Mini Project – Professional Development Plan",
  "Day 97: Revision",

  "Day 98: Crisis management & problem solving",
  "Day 99: Handling emergencies, complaints & disputes",
  "Day 100: Practice",
  "Day 101: Mini Project – Crisis Management Plan",
  "Day 102: Revision",

  "Day 103: Portfolio planning",
  "Day 104: Collecting reports, plans & administrative documents",
  "Day 105: Formatting & presentation",
  "Day 106: Practice",
  "Day 107: Portfolio Draft",
  "Day 108: Revision",

  "Day 109: Resume & LinkedIn setup",
  "Day 110: Apply for internships or assistant administrator positions",
  "Day 111: Networking & mentorship",
  "Day 112: Practice",
  "Day 113: Final portfolio preparation",
  "Day 114: Mock interviews",
  "Day 115: Revision",

  "Day 116: Specialization planning (Academic, Financial, HR, Operations, Technology)",
  "Day 117: Certification & course planning",
  "Day 118: Continuing education overview",
  "Day 119: Final review of all topics",
  "Day 120: School Administrator career progression"
],
"Academic Coordinator": [

  "Day 1: Understand Academic Coordinator role & career paths",
  "Day 2: Basics of educational systems & academic administration",
  "Day 3: Legal and regulatory frameworks for education",
  "Day 4: Tools setup (Student databases, curriculum planning software, spreadsheets)",
  "Day 5: Introduction to ethics & professional conduct",
  "Day 6: Communication skills fundamentals",
  "Day 7: Revision",

  "Day 8: Academic calendar planning",
  "Day 9: Scheduling classes, exams, and academic events",
  "Day 10: Practice",
  "Day 11: Mini Project – Academic Calendar Draft",
  "Day 12: Revision",

  "Day 13: Curriculum management",
  "Day 14: Designing course structures and learning outcomes",
  "Day 15: Practice",
  "Day 16: Mini Project – Curriculum Plan Draft",
  "Day 17: Revision",

  "Day 18: Faculty coordination",
  "Day 19: Scheduling, workload management & communication",
  "Day 20: Practice",
  "Day 21: Mini Project – Faculty Coordination Plan",
  "Day 22: Revision",

  "Day 23: Student enrollment & admissions",
  "Day 24: Managing admission records & documentation",
  "Day 25: Practice",
  "Day 26: Mini Project – Enrollment Management Draft",
  "Day 27: Revision",

  "Day 28: Academic progress monitoring",
  "Day 29: Grading, assessments & performance tracking",
  "Day 30: Practice",
  "Day 31: Mini Project – Student Progress Report",
  "Day 32: Revision",

  "Day 33: Academic support & mentoring",
  "Day 34: Counseling, remedial sessions & learning assistance",
  "Day 35: Practice",
  "Day 36: Mini Project – Academic Support Plan",
  "Day 37: Revision",

  "Day 38: Event & seminar coordination",
  "Day 39: Workshops, guest lectures & academic programs",
  "Day 40: Practice",
  "Day 41: Mini Project – Event Plan Draft",
  "Day 42: Revision",

  "Day 43: Quality assurance & accreditation",
  "Day 44: Preparing for inspections & audits",
  "Day 45: Practice",
  "Day 46: Mini Project – QA Checklist Draft",
  "Day 47: Revision",

  "Day 48: Technology in academic administration",
  "Day 49: LMS, online assessments & virtual classrooms",
  "Day 50: Practice",
  "Day 51: Mini Project – Technology Integration Plan",
  "Day 52: Revision",

  "Day 53: Policies & procedures management",
  "Day 54: Academic guidelines, code of conduct & compliance",
  "Day 55: Practice",
  "Day 56: Mini Project – Policy Draft",
  "Day 57: Revision",

  "Day 58: Communication & collaboration",
  "Day 59: Parent, student & faculty interaction",
  "Day 60: Practice",
  "Day 61: Mini Project – Communication Plan Draft",
  "Day 62: Revision",

  "Day 63: Research & academic projects",
  "Day 64: Facilitating student & faculty research activities",
  "Day 65: Practice",
  "Day 66: Mini Project – Research Coordination Draft",
  "Day 67: Revision",

  "Day 68: Examination management",
  "Day 69: Setting exams, schedules & evaluation criteria",
  "Day 70: Practice",
  "Day 71: Mini Project – Exam Management Plan",
  "Day 72: Revision",

  "Day 73: Data analysis & reporting",
  "Day 74: Analyzing student performance & faculty feedback",
  "Day 75: Practice",
  "Day 76: Mini Project – Data Analysis Report",
  "Day 77: Revision",

  "Day 78: Leadership & team management",
  "Day 79: Coordinating academic teams & resolving conflicts",
  "Day 80: Practice",
  "Day 81: Mini Project – Team Management Plan",
  "Day 82: Revision",

  "Day 83: Resource & budget management",
  "Day 84: Allocating resources, managing academic budget",
  "Day 85: Practice",
  "Day 86: Mini Project – Resource Allocation Plan",
  "Day 87: Revision",

  "Day 88: Crisis management & problem solving",
  "Day 89: Handling academic disputes & emergencies",
  "Day 90: Practice",
  "Day 91: Mini Project – Crisis Management Plan",
  "Day 92: Revision",

  "Day 93: Professional development & training",
  "Day 94: Workshops, seminars & certifications for staff",
  "Day 95: Practice",
  "Day 96: Mini Project – Professional Development Plan",
  "Day 97: Revision",

  "Day 98: Portfolio planning",
  "Day 99: Collecting curriculum plans, reports & event documentation",
  "Day 100: Formatting & presentation",
  "Day 101: Practice",
  "Day 102: Portfolio Draft",
  "Day 103: Revision",

  "Day 104: Resume & LinkedIn setup",
  "Day 105: Apply for internships or assistant coordinator positions",
  "Day 106: Networking & mentorship",
  "Day 107: Practice",
  "Day 108: Final portfolio preparation",
  "Day 109: Mock interviews",
  "Day 110: Revision",

  "Day 111: Specialization planning (Curriculum, Assessment, Faculty, Student Affairs, Events)",
  "Day 112: Certification & course planning",
  "Day 113: Continuing education overview",
  "Day 114: Advanced academic planning exercises",
  "Day 115: Mock coordination sessions",
  "Day 116: Review all reports & plans",
  "Day 117: Advanced case simulations",
  "Day 118: Final review of all topics",
  "Day 119: Career planning & roadmap preparation",
  "Day 120:  Academic Coordinator career progression"
]



 # You can add more careers slowly
}


if __name__ == "__main__":
    app.run(debug=True)