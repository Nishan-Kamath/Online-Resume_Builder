from flask import Flask, render_template, request, redirect, url_for
from fpdf import FPDF

app = Flask(__name__)

# Function to generate basic suggestions for resume improvement
def generate_suggestions(resume_data):
    suggestions = []

    # Example rule-based suggestions
    if 'python' not in resume_data['skills']:
        suggestions.append("Consider adding Python as a skill.")
    
    if len(resume_data['summary'].split()) < 50:
        suggestions.append("Your professional summary is too short. Aim for at least 50 words.")
    
    if len(resume_data['experience']) < 3:
        suggestions.append("You might want to add more details to your work experience section.")

    return suggestions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_resume():
    # Get form data
    resume_data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "phone": request.form['phone'],
        "summary": request.form['summary'],
        "skills": request.form.getlist('skills[]'),
        "experience": request.form['experience'],
    }

    # Generate suggestions
    suggestions = generate_suggestions(resume_data)

    return render_template('suggestions.html', resume_data=resume_data, suggestions=suggestions)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Resume', ln=True, align='C')

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    # Get resume data from the form
    resume_data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "phone": request.form['phone'],
        "summary": request.form['summary'],
        "skills": request.form.getlist('skills[]'),
        "experience": request.form['experience'],
    }

    # Create PDF
    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    # Add content and handle encoding issues
    pdf.cell(200, 10, txt=resume_data['name'].encode('utf-8', 'replace').decode('utf-8'), ln=True, align='L')
    pdf.cell(200, 10, txt=resume_data['email'], ln=True, align='L')
    pdf.cell(200, 10, txt=resume_data['phone'], ln=True, align='L')
    pdf.ln(10)
    
    pdf.cell(200, 10, txt="Professional Summary:", ln=True)
    pdf.multi_cell(200, 10, txt=resume_data['summary'].encode('utf-8', 'replace').decode('utf-8'))
    pdf.ln(10)
    
    pdf.cell(200, 10, txt="Skills:", ln=True)
    pdf.multi_cell(200, 10, txt=', '.join(resume_data['skills']).encode('utf-8', 'replace').decode('utf-8'))
    pdf.ln(10)
    
    pdf.cell(200, 10, txt="Experience:", ln=True)
    pdf.multi_cell(200, 10, txt=resume_data['experience'].encode('utf-8', 'replace').decode('utf-8'))
    
    # Output the PDF to a file
    pdf_file = "resume.pdf"
    pdf.output(pdf_file)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
