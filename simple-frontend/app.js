// API Base URL
const API_URL = 'http://localhost:5000/api';
const USER_ID = 'user_123'; // Mock user ID

// Global state
let quizQuestions = [];
let currentQuestionIndex = 0;
let quizAnswers = [];
let selectedRole = '';
let currentSession = null;

// Navigation
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show selected section
    document.getElementById(sectionId).classList.add('active');
    
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    event.target?.classList.add('active');
    
    // Load data for specific sections
    if (sectionId === 'jobs') {
        loadJobMatches();
    } else if (sectionId === 'admin') {
        loadAdminDashboard();
    } else if (sectionId === 'shadowing') {
        loadJobRoles();
    }
}

// Tab switching
function switchTab(tabName) {
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    event.target.classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

// Profile - Resume Upload
document.getElementById('resume-file')?.addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name || 'Choose File';
    document.getElementById('file-label').textContent = fileName;
});

async function uploadResume(event) {
    event.preventDefault();
    
    const fileInput = document.getElementById('resume-file');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', USER_ID);
    
    try {
        showLoading(true);
        const response = await fetch(`${API_URL}/profile/upload-resume`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        if (response.ok) {
            displayProfile(data.profile);
            alert('Resume parsed successfully!');
        } else {
            alert('Error: ' + (data.error || 'Failed to parse resume'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error uploading resume. Make sure the backend server is running.');
    } finally {
        showLoading(false);
    }
}

// Profile - Manual Entry
async function createProfile(event) {
    event.preventDefault();
    
    const skills = document.getElementById('skills').value.split(',').map(s => s.trim());
    const education = document.getElementById('education').value;
    const interests = document.getElementById('interests').value.split(',').map(i => i.trim());
    
    const profileData = {
        user_id: USER_ID,
        skills: skills,
        education: [{ degree: education }],
        interests: interests
    };
    
    try {
        showLoading(true);
        const response = await fetch(`${API_URL}/profile/manual-entry`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(profileData)
        });
        
        const data = await response.json();
        if (response.ok) {
            displayProfile(data.profile);
            alert('Profile created successfully!');
        } else {
            alert('Error: ' + (data.error || 'Failed to create profile'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error creating profile. Make sure the backend server is running.');
    } finally {
        showLoading(false);
    }
}

function displayProfile(profile) {
    const display = document.getElementById('profile-display');
    const content = document.getElementById('profile-content');
    
    let html = '';
    
    if (profile.skills && profile.skills.length > 0) {
        html += '<div class="profile-section"><h3>Skills</h3><div>';
        profile.skills.forEach(skill => {
            html += `<span class="tag">${skill}</span>`;
        });
        html += '</div></div>';
    }
    
    if (profile.education && profile.education.length > 0) {
        html += '<div class="profile-section"><h3>Education</h3>';
        profile.education.forEach(edu => {
            html += `<p>${edu.degree || edu}</p>`;
        });
        html += '</div>';
    }
    
    if (profile.interests && profile.interests.length > 0) {
        html += '<div class="profile-section"><h3>Interests</h3><div>';
        profile.interests.forEach(interest => {
            html += `<span class="tag">${interest}</span>`;
        });
        html += '</div></div>';
    }
    
    content.innerHTML = html;
    display.style.display = 'block';
}

// Quiz
async function startQuiz() {
    try {
        showLoading(true);
        const response = await fetch(`${API_URL}/quiz/start`);
        const data = await response.json();
        
        if (response.ok) {
            quizQuestions = data.questions;
            currentQuestionIndex = 0;
            quizAnswers = [];
            
            document.getElementById('quiz-intro').style.display = 'none';
            document.getElementById('quiz-content').style.display = 'block';
            
            displayQuestion();
        } else {
            alert('Error loading quiz');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error starting quiz. Make sure the backend server is running.');
    } finally {
        showLoading(false);
    }
}

function displayQuestion() {
    const question = quizQuestions[currentQuestionIndex];
    const progress = ((currentQuestionIndex + 1) / quizQuestions.length) * 100;
    
    document.getElementById('quiz-progress').style.width = progress + '%';
    document.getElementById('progress-text').textContent = 
        `Question ${currentQuestionIndex + 1} of ${quizQuestions.length}`;
    document.getElementById('question-text').textContent = question.question;
    
    const container = document.getElementById('options-container');
    container.innerHTML = '';
    
    question.options.forEach(option => {
        const button = document.createElement('button');
        button.className = 'option-button';
        button.textContent = option;
        button.onclick = () => selectOption(question.id, option, button);
        
        // Check if already answered
        const existing = quizAnswers.find(a => a.question_id === question.id);
        if (existing && existing.response === option) {
            button.classList.add('selected');
        }
        
        container.appendChild(button);
    });
    
    // Update navigation buttons
    document.getElementById('prev-btn').disabled = currentQuestionIndex === 0;
    const nextBtn = document.getElementById('next-btn');
    if (currentQuestionIndex === quizQuestions.length - 1) {
        nextBtn.textContent = 'Submit Quiz';
        nextBtn.onclick = submitQuiz;
    } else {
        nextBtn.textContent = 'Next';
        nextBtn.onclick = nextQuestion;
    }
}

function selectOption(questionId, response, button) {
    // Remove previous selection
    document.querySelectorAll('.option-button').forEach(btn => {
        btn.classList.remove('selected');
    });
    button.classList.add('selected');
    
    // Save answer
    const existingIndex = quizAnswers.findIndex(a => a.question_id === questionId);
    if (existingIndex >= 0) {
        quizAnswers[existingIndex] = { question_id: questionId, response };
    } else {
        quizAnswers.push({ question_id: questionId, response });
    }
}

function nextQuestion() {
    if (currentQuestionIndex < quizQuestions.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
    }
}

function previousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
    }
}

async function submitQuiz() {
    if (quizAnswers.length !== quizQuestions.length) {
        alert('Please answer all questions');
        return;
    }
    
    try {
        showLoading(true);
        const response = await fetch(`${API_URL}/quiz/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: USER_ID, answers: quizAnswers })
        });
        
        const data = await response.json();
        if (response.ok) {
            displayQuizResults(data.results);
        } else {
            alert('Error submitting quiz');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error submitting quiz');
    } finally {
        showLoading(false);
    }
}

function displayQuizResults(results) {
    document.getElementById('quiz-content').style.display = 'none';
    const resultsDiv = document.getElementById('quiz-results');
    resultsDiv.style.display = 'block';
    
    let html = '<div class="card"><h2>Top Personality Traits</h2><div class="traits-container">';
    results.top_traits.forEach(trait => {
        html += `<div class="trait-badge">${trait.replace('_', ' ').toUpperCase()}</div>`;
    });
    html += '</div></div>';
    
    html += '<div class="card"><h2>Recommended Careers</h2><div class="careers-grid">';
    results.recommended_careers.slice(0, 6).forEach(career => {
        html += `
            <div class="career-card card">
                <h3>${career.title}</h3>
                <div class="match-score">
                    <div class="score-circle">${career.match_score}%</div>
                    <span>Match Score</span>
                </div>
                <p style="color: #666; font-size: 14px; font-style: italic;">
                    Based on: ${career.trait.replace('_', ' ')}
                </p>
            </div>
        `;
    });
    html += '</div></div>';
    
    resultsDiv.innerHTML = html;
}

// Job Matching
async function loadJobMatches() {
    try {
        showLoading(true);
        const response = await fetch(`${API_URL}/jobs/match/${USER_ID}`);
        const data = await response.json();
        
        if (response.ok) {
            displayJobMatches(data.matches);
        } else {
            alert('Error loading job matches');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error loading jobs. Make sure the backend server is running.');
    } finally {
        showLoading(false);
    }
}

function displayJobMatches(matches) {
    const container = document.getElementById('job-matches');
    
    if (matches.length === 0) {
        container.innerHTML = '<p>No job matches found. Create a profile first!</p>';
        return;
    }
    
    container.innerHTML = matches.map(match => {
        const color = match.match_percentage >= 80 ? '#10b981' : 
                     match.match_percentage >= 60 ? '#f59e0b' : '#ef4444';
        
        return `
            <div class="job-match-card card">
                <h3>${match.job.title}</h3>
                <p style="color: #667eea; font-weight: 600;">${match.job.company}</p>
                <p style="color: #666; font-size: 14px;">📍 ${match.job.location}</p>
                
                <div class="match-percentage">
                    <div class="percentage-circle" style="border-color: ${color}; color: ${color};">
                        ${match.match_percentage}%
                    </div>
                    <p>Match</p>
                </div>
                
                <div>
                    <strong>✓ Matching Skills:</strong>
                    <div>${match.matching_skills.slice(0, 3).map(s => 
                        `<span class="tag tag-success">${s}</span>`
                    ).join('')}</div>
                </div>
                
                ${match.missing_skills.length > 0 ? `
                    <div style="margin-top: 1rem;">
                        <strong>⚠ Missing Skills:</strong>
                        <div>${match.missing_skills.slice(0, 3).map(s => 
                            `<span class="tag tag-warning">${s}</span>`
                        ).join('')}</div>
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');
}

async function searchJobs() {
    const query = document.getElementById('job-search').value;
    
    try {
        showLoading(true);
        const response = await fetch(`${API_URL}/jobs/search?query=${query}`);
        const data = await response.json();
        
        if (response.ok && data.jobs) {
            // Display search results
            console.log('Search results:', data.jobs);
        }
    } catch (error) {
        console.error('Error:', error);
    } finally {
        showLoading(false);
    }
}

// Roadmap
async function generateRoadmap() {
    const targetJob = document.getElementById('target-job').value;
    
    if (!targetJob) {
        alert('Please enter a job ID');
        return;
    }
    
    try {
        showLoading(true);
        const response = await fetch(`${API_URL}/roadmap/generate/${USER_ID}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target_job_id: targetJob })
        });
        
        const data = await response.json();
        if (response.ok) {
            displayRoadmap(data.roadmap);
        } else {
            alert('Error: ' + (data.error || 'Failed to generate roadmap'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error generating roadmap');
    } finally {
        showLoading(false);
    }
}

function displayRoadmap(roadmap) {
    document.getElementById('roadmap-generate').style.display = 'none';
    const content = document.getElementById('roadmap-content');
    content.style.display = 'block';
    
    let html = `
        <div class="card">
            <h2>Path to: ${roadmap.target_job_title}</h2>
            <div style="display: flex; justify-content: space-around; margin: 2rem 0;">
                <div><p style="color: #666;">Current Match</p>
                    <h3 style="color: #667eea;">${roadmap.current_match_percentage}%</h3></div>
                <div><p style="color: #666;">Duration</p>
                    <h3 style="color: #667eea;">${roadmap.total_duration}</h3></div>
                <div><p style="color: #666;">Progress</p>
                    <h3 style="color: #667eea;">${roadmap.progress}%</h3></div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${roadmap.progress}%"></div>
            </div>
        </div>
        
        <h3>Your Learning Path</h3>
    `;
    
    roadmap.learning_path.forEach(item => {
        const priorityClass = item.priority.toLowerCase();
        html += `
            <div class="card" style="border-left: 4px solid #667eea;">
                <h4>${item.skill}</h4>
                <span class="tag">${item.priority} Priority</span>
                <p>Duration: ${item.estimated_duration}</p>
                
                <div style="margin-top: 1rem;">
                    <strong>Recommended Courses:</strong>
                    ${item.courses.map(course => `
                        <div style="padding: 0.5rem; background: #f9fafb; margin: 0.5rem 0; border-radius: 8px;">
                            <strong>${course.name}</strong> - ${course.provider}
                            <span class="tag ${course.type.toLowerCase() === 'free' ? 'tag-success' : ''}">${course.type}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    });
    
    content.innerHTML = html;
}

// Portfolio
async function generateProjectIdeas() {
    try {
        showLoading(true);
        const response = await fetch(`${API_URL}/portfolio/generate-ideas/${USER_ID}?count=5`);
        const data = await response.json();
        
        if (response.ok) {
            displayProjectIdeas(data.project_ideas);
        } else {
            alert('Error generating project ideas');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error generating ideas');
    } finally {
        showLoading(false);
    }
}

function displayProjectIdeas(ideas) {
    const container = document.getElementById('project-ideas');
    container.style.display = 'block';
    
    let html = '<h2>Your Personalized Project Ideas</h2><div class="features-grid">';
    
    ideas.forEach(idea => {
        const diffColor = idea.difficulty === 'Beginner' ? '#10b981' : 
                         idea.difficulty === 'Intermediate' ? '#f59e0b' : '#ef4444';
        
        html += `
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                    <h3>${idea.title}</h3>
                    <span class="tag" style="background: ${diffColor}; color: white;">${idea.difficulty}</span>
                </div>
                <p>${idea.description}</p>
                <p style="color: #666; margin: 0.5rem 0;">⏱️ ${idea.estimated_time}</p>
                <div style="margin: 1rem 0;">
                    <strong>Skills:</strong>
                    ${idea.skills_needed.map(s => `<span class="tag">${s}</span>`).join('')}
                </div>
                <p style="color: #667eea; font-size: 14px; font-style: italic;">${idea.why_recommended}</p>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

// Virtual Shadowing
function loadJobRoles() {
    const roles = [
        'Data Scientist',
        'Software Engineer',
        'Product Manager',
        'UX Designer',
        'DevOps Engineer',
        'Machine Learning Engineer'
    ];
    
    const grid = document.getElementById('roles-grid');
    grid.innerHTML = roles.map(role => `
        <button class="role-button" onclick="selectRole('${role}', event)">${role}</button>
    `).join('');
}

function selectRole(role, event) {
    selectedRole = role;
    document.querySelectorAll('.role-button').forEach(btn => {
        btn.classList.remove('selected');
    });
    event.target.classList.add('selected');
    document.getElementById('start-shadow-btn').disabled = false;
}

async function startShadowing() {
    if (!selectedRole) return;
    
    try {
        showLoading(true);
        const response = await fetch(`${API_URL}/shadowing/start-session`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: USER_ID, job_role: selectedRole })
        });
        
        const data = await response.json();
        if (response.ok) {
            currentSession = data.session;
            document.getElementById('role-selection').style.display = 'none';
            document.getElementById('chat-section').style.display = 'block';
            document.getElementById('shadow-role-title').textContent = `Shadowing: ${selectedRole}`;
            
            displayMessages(data.session.conversation_history);
        } else {
            alert('Error starting session');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error starting shadowing session');
    } finally {
        showLoading(false);
    }
}

function displayMessages(messages) {
    const container = document.getElementById('messages-container');
    container.innerHTML = messages.map(msg => `
        <div class="message ${msg.role === 'user' ? 'user-message' : ''}">
            <div class="message-avatar">${msg.role === 'user' ? '👤' : '🤖'}</div>
            <div class="message-content"><p>${msg.message}</p></div>
        </div>
    `).join('');
    container.scrollTop = container.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message || !currentSession) return;
    
    input.value = '';
    
    // Add user message to UI
    const container = document.getElementById('messages-container');
    container.innerHTML += `
        <div class="message user-message">
            <div class="message-avatar">👤</div>
            <div class="message-content"><p>${message}</p></div>
        </div>
    `;
    
    try {
        const response = await fetch(`${API_URL}/shadowing/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                session_id: currentSession.session_id, 
                message: message 
            })
        });
        
        const data = await response.json();
        if (response.ok) {
            container.innerHTML += `
                <div class="message">
                    <div class="message-avatar">🤖</div>
                    <div class="message-content"><p>${data.response}</p></div>
                </div>
            `;
            container.scrollTop = container.scrollHeight;
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error sending message');
    }
}

document.getElementById('chat-input')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

function endShadowing() {
    currentSession = null;
    selectedRole = '';
    document.getElementById('chat-section').style.display = 'none';
    document.getElementById('role-selection').style.display = 'block';
    document.getElementById('messages-container').innerHTML = '';
    loadJobRoles();
}

// Admin Dashboard
async function loadAdminDashboard() {
    try {
        showLoading(true);
        const response = await fetch(`${API_URL}/admin/analytics?university_id=univ_001`);
        const data = await response.json();
        
        if (response.ok) {
            displayAdminDashboard(data);
        } else {
            alert('Error loading analytics');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error loading admin dashboard');
    } finally {
        showLoading(false);
    }
}

function displayAdminDashboard(analytics) {
    const container = document.getElementById('admin-content');
    
    let html = `
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
            <div class="card">
                <div style="font-size: 48px;">👥</div>
                <h3 style="color: #667eea; font-size: 32px;">${analytics.total_students.toLocaleString()}</h3>
                <p style="color: #666;">Total Students</p>
            </div>
            <div class="card">
                <div style="font-size: 48px;">✅</div>
                <h3 style="color: #667eea; font-size: 32px;">${analytics.active_users.toLocaleString()}</h3>
                <p style="color: #666;">Active Users</p>
            </div>
            <div class="card">
                <div style="font-size: 48px;">📊</div>
                <h3 style="color: #667eea; font-size: 32px;">${analytics.avg_match_percentage}%</h3>
                <p style="color: #666;">Avg Match Rate</p>
            </div>
            <div class="card">
                <div style="font-size: 48px;">✏️</div>
                <h3 style="color: #667eea; font-size: 32px;">${analytics.completed_quizzes}</h3>
                <p style="color: #666;">Completed Quizzes</p>
            </div>
        </div>
        
        <div class="card">
            <h2>Top Career Interests</h2>
            ${analytics.top_career_interests.map(career => {
                const maxCount = analytics.top_career_interests[0].count;
                const width = (career.count / maxCount) * 100;
                return `
                    <div style="margin-bottom: 1rem;">
                        <div style="font-weight: 600; margin-bottom: 0.5rem;">${career.career}</div>
                        <div style="position: relative; height: 32px; background: #f0f0f0; border-radius: 8px; overflow: hidden;">
                            <div style="height: 100%; width: ${width}%; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);"></div>
                            <span style="position: absolute; right: 12px; top: 50%; transform: translateY(-50%); font-weight: 600; color: white;">${career.count}</span>
                        </div>
                    </div>
                `;
            }).join('')}
        </div>
    `;
    
    container.innerHTML = html;
}

// Utility Functions
function showLoading(show) {
    // You can implement a loading spinner here
    if (show) {
        console.log('Loading...');
    }
}

// Initialize navigation on page load
document.addEventListener('DOMContentLoaded', () => {
    // Set up nav link click handlers
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const sectionId = link.getAttribute('href').substring(1);
            showSection(sectionId);
        });
    });
    
    // Show home section by default
    showSection('home');
});
