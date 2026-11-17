from flask import Flask, render_template, request
from resume_parser import extract_text_from_pdf
from ai_matcher import match_resume_to_job, get_missing_skills

app = Flask(__name__)

JOB_CATEGORIES = {
    "Computer Science": [
        "Web Developer", "Data Analyst", "Software Engineer",
        "Machine Learning Engineer", "Cyber Security Analyst", "Cloud Engineer"
    ],
    "Medical": [
        "Doctor", "Nurse", "Pharmacist", "Lab Technician"
    ],
    "Robotics": [
        "Robotics Engineer", "Automation Engineer", "Embedded Systems Engineer"
    ],
    "Business": [
        "Marketing Manager", "HR Manager", "Business Analyst"
    ],
    "Design": [
        "UI UX Designer", "Graphic Designer"
    ]
}

JOB_DESCRIPTIONS = {
    "Web Developer": "HTML CSS JavaScript React",
    "Data Analyst": "Python SQL Excel PowerBI",
    "Software Engineer": "Java DSA System Design",
    "Machine Learning Engineer": "Python ML AI NLP",
    "Cyber Security Analyst": "Networking Security Ethical Hacking",
    "Cloud Engineer": "AWS Azure DevOps",

    "Doctor": "Medical Diagnosis Treatment",
    "Nurse": "Patient Care Medical Support",
    "Pharmacist": "Medicines Pharmacy",
    "Lab Technician": "Lab Testing Equipment",

    "Robotics Engineer": "Robotics Sensors Automation",
    "Automation Engineer": "PLC SCADA Automation",
    "Embedded Systems Engineer": "C C++ Microcontrollers",

    "Marketing Manager": "SEO Marketing Strategy",
    "HR Manager": "Recruitment Communication",
    "Business Analyst": "Data Analysis Excel SQL",

    "UI UX Designer": "Figma Design User Experience",
    "Graphic Designer": "Photoshop Illustrator Creativity"
}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/categories")
def categories():
    return render_template("categories.html", categories=JOB_CATEGORIES)

@app.route("/subcategories/<category>")
def subcategories(category):
    subcats = JOB_CATEGORIES.get(category, [])
    return render_template("subcategories.html", category=category, subcategories=subcats)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["resume"]
    role = request.form.get("role")

    if file:
        text = extract_text_from_pdf(file)
        job_desc = JOB_DESCRIPTIONS.get(role, "")

        score = match_resume_to_job(text, job_desc)
        missing_skills = get_missing_skills(text, job_desc)

        return render_template("result.html",
                               score=score,
                               missing_skills=missing_skills,
                               role=role)

    return "Error uploading file"

if __name__ == "__main__":
    app.run(debug=True)