from flask import Flask, request, render_template, send_from_directory
import pandas as pd
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORT_FOLDER'] = 'report_cards'

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)

def calculate_grade(score):
    if score >= 90:
        return "A", "Excellent"
    elif score >= 80:
        return "B", "Very Good"
    elif score >= 70:
        return "C", "Good"
    elif score >= 60:
        return "D", "Fair"
    else:
        return "F", "Needs Improvement"

def generate_comment(context, average, name, subjects):
    if average >= 90:
        return f"{name} has demonstrated outstanding performance across all subjects."
    elif average >= 70:
        return f"{name} has performed well but still has room for improvement in some subjects."
    else:
        return f"{name} needs to put in more effort to improve academic performance."

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.xlsx'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            df = pd.read_excel(filepath)
            df.columns = df.columns.str.strip()

            required_cols = ['Name']
            optional_cols = ['Student ID', 'Class', 'Address']
            metadata_cols = [col for col in df.columns if col in required_cols + optional_cols]
            subject_cols = [col for col in df.columns if col not in metadata_cols]

            report_files = []

            for _, row in df.iterrows():
                student = {
                    "name": row.get("Name"),
                    "student_id": row.get("Student ID", ""),
                    "class": row.get("Class", ""),
                    "address": row.get("Address", ""),
                    "subjects": {},
                    "summary": {}
                }

                total = 0
                count = 0
                for subject in subject_cols:
                    score = pd.to_numeric(row[subject], errors='coerce')
                    if pd.notnull(score):
                        grade_letter, performance = calculate_grade(score)
                        student["subjects"][subject] = {
                            "score": score,
                            "grade": grade_letter,
                            "performance": performance
                        }
                        total += score
                        count += 1

                if count > 0:
                    avg = total / count
                    grade_letter, performance = calculate_grade(avg)
                    student["summary"] = {
                        "average": round(avg, 2),
                        "grade": grade_letter,
                        "performance": performance,
                        "comment": generate_comment("overall", avg, student["name"], student["subjects"]),
                        "total": total,
                        "subjects_count": count
                    }

                env = Environment(loader=FileSystemLoader('templates'))
                template = env.get_template('report_card.html')
                html_out = template.render(student=student)
                safe_name = student['name'].replace(' ', '_')
                pdf_path = os.path.join(app.config['REPORT_FOLDER'], f"{safe_name}.pdf")
                HTML(string=html_out).write_pdf(pdf_path)

                report_files.append(f"{safe_name}.pdf")

            return render_template('results.html', reports=report_files)

    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['REPORT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
