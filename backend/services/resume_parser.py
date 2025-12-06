import PyPDF2
import docx
import re
from datetime import datetime

class ResumeParser:
    """AI-powered resume parser to extract skills, education, and experience"""
    
    def __init__(self):
        self.skill_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'sql', 'mongodb', 'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'machine learning', 'data analysis', 'git', 'agile', 'scrum',
            'html', 'css', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go',
            'flask', 'django', 'spring boot', 'rest api', 'graphql',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy'
        ]
    
    def parse(self, file):
        """Parse resume file and extract information"""
        filename = file.filename.lower()
        
        if filename.endswith('.pdf'):
            text = self._extract_text_from_pdf(file)
        elif filename.endswith('.docx'):
            text = self._extract_text_from_docx(file)
        else:
            text = file.read().decode('utf-8', errors='ignore')
        
        profile_data = {
            'skills': self._extract_skills(text),
            'education': self._extract_education(text),
            'experience': self._extract_experience(text),
            'certifications': self._extract_certifications(text),
            'email': self._extract_email(text),
            'phone': self._extract_phone(text)
        }
        
        return profile_data
    
    def _extract_text_from_pdf(self, file):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            return ""
    
    def _extract_text_from_docx(self, file):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            return ""
    
    def _extract_skills(self, text):
        """Extract skills from resume text"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.skill_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill.title())
        
        # Remove duplicates
        return list(set(found_skills))
    
    def _extract_education(self, text):
        """Extract education information"""
        education = []
        
        # Look for degree patterns
        degree_patterns = [
            r'(bachelor|master|phd|b\.tech|m\.tech|bca|mca|b\.sc|m\.sc).*?(?:in|of)\s+([a-zA-Z\s]+)',
            r'(bachelor|master|phd)\'?s?\s+(?:degree\s+)?(?:in|of)\s+([a-zA-Z\s]+)'
        ]
        
        for pattern in degree_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                education.append({
                    'degree': match.group(0).strip(),
                    'field': match.group(2).strip() if len(match.groups()) > 1 else 'Not specified'
                })
        
        return education[:3]  # Limit to 3 most relevant
    
    def _extract_experience(self, text):
        """Extract work experience"""
        experience = []
        
        # Look for common experience patterns
        exp_pattern = r'(\d+)\s*(?:\+)?\s*(?:years?|yrs?)\s+(?:of\s+)?experience'
        matches = re.findall(exp_pattern, text, re.IGNORECASE)
        
        if matches:
            total_years = max([int(m) for m in matches])
            experience.append({
                'total_years': total_years,
                'level': self._categorize_experience_level(total_years)
            })
        
        return experience
    
    def _extract_certifications(self, text):
        """Extract certifications"""
        certifications = []
        
        cert_keywords = [
            'aws certified', 'azure certified', 'google cloud certified',
            'scrum master', 'pmp', 'cissp', 'comptia', 'oracle certified'
        ]
        
        text_lower = text.lower()
        for cert in cert_keywords:
            if cert in text_lower:
                certifications.append(cert.title())
        
        return list(set(certifications))
    
    def _extract_email(self, text):
        """Extract email address"""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else None
    
    def _extract_phone(self, text):
        """Extract phone number"""
        phone_pattern = r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,5}[-\s\.]?[0-9]{1,5}'
        matches = re.findall(phone_pattern, text)
        return matches[0] if matches else None
    
    def _categorize_experience_level(self, years):
        """Categorize experience level"""
        if years < 1:
            return 'Entry Level'
        elif years < 3:
            return 'Junior'
        elif years < 6:
            return 'Mid-Level'
        else:
            return 'Senior'
