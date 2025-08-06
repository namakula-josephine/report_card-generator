from flask import render_template
from weasyprint import HTML

def render_report_to_pdf(student, pdf_path):
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report_card.html')

    html_content = template.render(student=student, school_name="Your School Name")
    HTML(string=html_content).write_pdf(pdf_path)
