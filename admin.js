// DOM Elements
const sidebar = document.getElementById('sidebar');
const menuToggle = document.getElementById('menuToggle');
const closeSidebar = document.getElementById('closeSidebar');
const mainContent = document.querySelector('.main-content');
const profileTrigger = document.getElementById('profileTrigger');
const profileDropdown = document.getElementById('profileDropdown');
const navLinks = document.querySelectorAll('.nav-link');
const pages = document.querySelectorAll('.page');

// Dummy Data
let teachers = [
    { id: 1, name: 'John Smith', email: 'john.smith@school.edu', subject: 'Mathematics', status: 'Active' },
    { id: 2, name: 'Sarah Johnson', email: 'sarah.johnson@school.edu', subject: 'English', status: 'Active' },
    { id: 3, name: 'Michael Brown', email: 'michael.brown@school.edu', subject: 'Science', status: 'Inactive' },
    { id: 4, name: 'Emily Davis', email: 'emily.davis@school.edu', subject: 'History', status: 'Active' },
    { id: 5, name: 'Robert Wilson', email: 'robert.wilson@school.edu', subject: 'Art', status: 'Active' }
];

let students = [
    { id: 1, name: 'Alex Thompson', email: 'alex.thompson@student.edu', grade: '10', status: 'Active' },
    { id: 2, name: 'Emma Garcia', email: 'emma.garcia@student.edu', grade: '11', status: 'Active' },
    { id: 3, name: 'James Martinez', email: 'james.martinez@student.edu', grade: '9', status: 'Active' },
    { id: 4, name: 'Sophie Anderson', email: 'sophie.anderson@student.edu', grade: '12', status: 'Inactive' },
    { id: 5, name: 'Daniel Lee', email: 'daniel.lee@student.edu', grade: '10', status: 'Active' },
    { id: 6, name: 'Olivia Taylor', email: 'olivia.taylor@student.edu', grade: '11', status: 'Active' }
];

// Global state
let editingTeacherId = null;
let editingStudentId = null;

// Initialize Application
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    populateTeachersTable();
    populateStudentsTable();
    setupEventListeners();
    showPage('dashboard');
});

// Event Listeners Setup
function setupEventListeners() {
    // Sidebar toggle
    menuToggle.addEventListener('click', toggleSidebar);
    closeSidebar.addEventListener('click', toggleSidebar);

    // Profile dropdown
    profileTrigger.addEventListener('click', toggleProfileDropdown);
    document.addEventListener('click', function(e) {
        if (!profileTrigger.contains(e.target)) {
            profileDropdown.classList.remove('show');
        }
    });

    // Navigation
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            if (link.classList.contains('logout')) {
                handleLogout();
                return;
            }
            
            const page = link.dataset.page;
            if (page) {
                showPage(page);
                setActiveNav(link);
            }
        });
    });

    // Teacher Management
    document.getElementById('addTeacherBtn').addEventListener('click', () => openTeacherModal());
    document.getElementById('teacherForm').addEventListener('submit', handleTeacherSubmit);
    document.getElementById('cancelTeacherBtn').addEventListener('click', closeTeacherModal);

    // Student Management
    document.getElementById('addStudentBtn').addEventListener('click', () => openStudentModal());
    document.getElementById('studentForm').addEventListener('submit', handleStudentSubmit);
    document.getElementById('cancelStudentBtn').addEventListener('click', closeStudentModal);

    // Student Search
    document.getElementById('studentSearch').addEventListener('input', handleStudentSearch);

    // System Maintenance
    document.getElementById('backupBtn').addEventListener('click', handleBackup);
    document.getElementById('updateBtn').addEventListener('click', handleUpdate);

    // Gamification Forms
    document.getElementById('tokenForm').addEventListener('submit', handleTokenSubmit);
    document.getElementById('levelForm').addEventListener('submit', handleLevelSubmit);

    // Sync & Notes
    document.getElementById('autosaveToggle').addEventListener('change', handleAutosaveToggle);
    document.getElementById('forceSyncBtn').addEventListener('click', handleForceSync);
    document.getElementById('saveNotesBtn').addEventListener('click', handleSaveNotes);

    // Modal close buttons
    document.querySelectorAll('.close').forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            this.closest('.modal').classList.remove('show');
        });
    });

    // Close modals when clicking outside
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.remove('show');
            }
        });
    });

    // Window resize handler
    window.addEventListener('resize', handleWindowResize);
}

// Sidebar Functions
function toggleSidebar() {
    const isMobile = window.innerWidth <= 768;
    
    if (isMobile) {
        sidebar.classList.toggle('open');
    } else {
        sidebar.classList.toggle('closed');
        mainContent.classList.toggle('full-width');
    }
}

function handleWindowResize() {
    const isMobile = window.innerWidth <= 768;
    
    if (isMobile) {
        sidebar.classList.remove('closed');
        mainContent.classList.remove('full-width');
        if (!sidebar.classList.contains('open')) {
            sidebar.classList.remove('open');
        }
    } else {
        sidebar.classList.remove('open');
    }
}

// Profile Dropdown
function toggleProfileDropdown() {
    profileDropdown.classList.toggle('show');
}

// Navigation Functions
function showPage(pageId) {
    pages.forEach(page => {
        page.style.display = 'none';
    });
    
    const targetPage = document.getElementById(`${pageId}-page`);
    if (targetPage) {
        targetPage.style.display = 'block';
    }

    // Update page title
    const titles = {
        dashboard: 'Admin Dashboard',
        teachers: 'Manage Teachers',
        students: 'Manage Students',
        maintenance: 'System Maintenance',
        analytics: 'Platform Analytics',
        gamification: 'Gamification Rules',
        sync: 'Sync & Notes',
        settings: 'Settings'
    };

    const pageTitle = document.querySelector('.page-title');
    if (titles[pageId]) {
        pageTitle.textContent = titles[pageId];
    }

    // Load page-specific content
    if (pageId === 'analytics') {
        setTimeout(initializeAnalyticsCharts, 100);
    }
}

function setActiveNav(activeLink) {
    navLinks.forEach(link => link.classList.remove('active'));
    activeLink.classList.add('active');
}

// Chart Initialization
function initializeCharts() {
    // Usage Chart
    const usageCtx = document.getElementById('usageChart').getContext('2d');
    new Chart(usageCtx, {
        type: 'doughnut',
        data: {
            labels: ['Teachers', 'Students', 'Administrators'],
            datasets: [{
                data: [247, 1423, 12],
                backgroundColor: ['#3b82f6', '#10b981', '#f59e0b'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // Activity Chart
    const activityCtx = document.getElementById('activityChart').getContext('2d');
    new Chart(activityCtx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Active Users',
                data: [120, 190, 170, 220, 180, 90, 60],
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function initializeAnalyticsCharts() {
    // Engagement Chart
    const engagementCtx = document.getElementById('engagementChart').getContext('2d');
    new Chart(engagementCtx, {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Engagement Score',
                data: [85, 92, 88, 95, 90, 97],
                backgroundColor: '#3b82f6',
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });

    // Quiz Chart
    const quizCtx = document.getElementById('quizChart').getContext('2d');
    new Chart(quizCtx, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                label: 'Quizzes Completed',
                data: [45, 62, 58, 71],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // Growth Chart
    const growthCtx = document.getElementById('growthChart').getContext('2d');
    new Chart(growthCtx, {
        type: 'bar',
        data: {
            labels: ['Q1', 'Q2', 'Q3', 'Q4'],
            datasets: [{
                label: 'New Users',
                data: [120, 150, 180, 200],
                backgroundColor: '#f59e0b'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // Device Chart
    const deviceCtx = document.getElementById('deviceChart').getContext('2d');
    new Chart(deviceCtx, {
        type: 'doughnut',
        data: {
            labels: ['Desktop', 'Mobile', 'Tablet'],
            datasets: [{
                data: [45, 35, 20],
                backgroundColor: ['#3b82f6', '#10b981', '#f59e0b']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Teacher Management
function populateTeachersTable() {
    const tbody = document.getElementById('teachersTableBody');
    tbody.innerHTML = '';

    teachers.forEach(teacher => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${teacher.id}</td>
            <td>${teacher.name}</td>
            <td>${teacher.email}</td>
            <td>${teacher.subject}</td>
            <td><span class="status-badge ${teacher.status.toLowerCase()}">${teacher.status}</span></td>
            <td class="table-actions">
                <button class="btn btn-sm btn-secondary" onclick="editTeacher(${teacher.id})">
                    <i class="fas fa-edit"></i> Edit
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteTeacher(${teacher.id})">
                    <i class="fas fa-trash"></i> Delete
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function openTeacherModal(teacher = null) {
    const modal = document.getElementById('teacherModal');
    const title = document.getElementById('teacherModalTitle');
    const form = document.getElementById('teacherForm');

    if (teacher) {
        title.textContent = 'Edit Teacher';
        document.getElementById('teacherName').value = teacher.name;
        document.getElementById('teacherEmail').value = teacher.email;
        document.getElementById('teacherSubject').value = teacher.subject;
        document.getElementById('teacherStatus').value = teacher.status;
        editingTeacherId = teacher.id;
    } else {
        title.textContent = 'Add Teacher';
        form.reset();
        editingTeacherId = null;
    }

    modal.classList.add('show');
}

function closeTeacherModal() {
    document.getElementById('teacherModal').classList.remove('show');
}

function handleTeacherSubmit(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('teacherName').value,
        email: document.getElementById('teacherEmail').value,
        subject: document.getElementById('teacherSubject').value,
        status: document.getElementById('teacherStatus').value
    };

    if (editingTeacherId) {
        // Update existing teacher
        const index = teachers.findIndex(t => t.id === editingTeacherId);
        if (index !== -1) {
            teachers[index] = { ...teachers[index], ...formData };
        }
    } else {
        // Add new teacher
        const newTeacher = {
            id: Math.max(...teachers.map(t => t.id)) + 1,
            ...formData
        };
        teachers.push(newTeacher);
    }

    populateTeachersTable();
    closeTeacherModal();
    showNotification(editingTeacherId ? 'Teacher updated successfully!' : 'Teacher added successfully!');
}

function editTeacher(id) {
    const teacher = teachers.find(t => t.id === id);
    if (teacher) {
        openTeacherModal(teacher);
    }
}

function deleteTeacher(id) {
    if (confirm('Are you sure you want to delete this teacher?')) {
        teachers = teachers.filter(t => t.id !== id);
        populateTeachersTable();
        showNotification('Teacher deleted successfully!');
    }
}

// Student Management
function populateStudentsTable(filteredStudents = null) {
    const tbody = document.getElementById('studentsTableBody');
    tbody.innerHTML = '';

    const studentsToShow = filteredStudents || students;

    studentsToShow.forEach(student => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${student.id}</td>
            <td>${student.name}</td>
            <td>${student.email}</td>
            <td>Grade ${student.grade}</td>
            <td><span class="status-badge ${student.status.toLowerCase()}">${student.status}</span></td>
            <td class="table-actions">
                <button class="btn btn-sm btn-secondary" onclick="editStudent(${student.id})">
                    <i class="fas fa-edit"></i> Edit
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteStudent(${student.id})">
                    <i class="fas fa-trash"></i> Delete
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function openStudentModal(student = null) {
    const modal = document.getElementById('studentModal');
    const title = document.getElementById('studentModalTitle');
    const form = document.getElementById('studentForm');

    if (student) {
        title.textContent = 'Edit Student';
        document.getElementById('studentName').value = student.name;
        document.getElementById('studentEmail').value = student.email;
        document.getElementById('studentGrade').value = student.grade;
        document.getElementById('studentStatus').value = student.status;
        editingStudentId = student.id;
    } else {
        title.textContent = 'Add Student';
        form.reset();
        editingStudentId = null;
    }

    modal.classList.add('show');
}

function closeStudentModal() {
    document.getElementById('studentModal').classList.remove('show');
}

function handleStudentSubmit(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('studentName').value,
        email: document.getElementById('studentEmail').value,
        grade: document.getElementById('studentGrade').value,
        status: document.getElementById('studentStatus').value
    };

    if (editingStudentId) {
        // Update existing student
        const index = students.findIndex(s => s.id === editingStudentId);
        if (index !== -1) {
            students[index] = { ...students[index], ...formData };
        }
    } else {
        // Add new student
        const newStudent = {
            id: Math.max(...students.map(s => s.id)) + 1,
            ...formData
        };
        students.push(newStudent);
    }

    populateStudentsTable();
    closeStudentModal();
    showNotification(editingStudentId ? 'Student updated successfully!' : 'Student added successfully!');
}

function editStudent(id) {
    const student = students.find(s => s.id === id);
    if (student) {
        openStudentModal(student);
    }
}

function deleteStudent(id) {
    if (confirm('Are you sure you want to delete this student?')) {
        students = students.filter(s => s.id !== id);
        populateStudentsTable();
        showNotification('Student deleted successfully!');
    }
}

function handleStudentSearch(e) {
    const searchTerm = e.target.value.toLowerCase();
    const filteredStudents = students.filter(student => 
        student.name.toLowerCase().includes(searchTerm) ||
        student.email.toLowerCase().includes(searchTerm) ||
        student.grade.toLowerCase().includes(searchTerm)
    );
    populateStudentsTable(filteredStudents);
}

// System Maintenance
function handleBackup() {
    const backupBtn = document.getElementById('backupBtn');
    const originalText = backupBtn.innerHTML;
    
    backupBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Backing up...';
    backupBtn.disabled = true;
    
    setTimeout(() => {
        backupBtn.innerHTML = originalText;
        backupBtn.disabled = false;
        showNotification('Backup completed successfully!');
    }, 3000);
}

function handleUpdate() {
    const updateBtn = document.getElementById('updateBtn');
    const originalText = updateBtn.innerHTML;
    
    updateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Checking...';
    updateBtn.disabled = true;
    
    setTimeout(() => {
        updateBtn.innerHTML = originalText;
        updateBtn.disabled = false;
        showNotification('System is up to date!');
    }, 2000);
}

// Gamification
function handleTokenSubmit(e) {
    e.preventDefault();
    showNotification('Token rules saved successfully!');
}

function handleLevelSubmit(e) {
    e.preventDefault();
    showNotification('Level rules saved successfully!');
}

// Sync & Notes
function handleAutosaveToggle(e) {
    const isEnabled = e.target.checked;
    showNotification(`Autosave ${isEnabled ? 'enabled' : 'disabled'}!`);
}

function handleForceSync() {
    const syncBtn = document.getElementById('forceSyncBtn');
    const originalText = syncBtn.innerHTML;
    
    syncBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Syncing...';
    syncBtn.disabled = true;
    
    setTimeout(() => {
        syncBtn.innerHTML = originalText;
        syncBtn.disabled = false;
        showNotification('Sync completed successfully!');
    }, 2000);
}

function handleSaveNotes() {
    const saveBtn = document.getElementById('saveNotesBtn');
    const originalText = saveBtn.innerHTML;
    
    saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
    saveBtn.disabled = true;
    
    setTimeout(() => {
        saveBtn.innerHTML = originalText;
        saveBtn.disabled = false;
        document.querySelector('.autosave-status').textContent = 'Last saved: Just now';
        showNotification('Notes saved successfully!');
    }, 1000);
}

// Utility Functions
function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        showNotification('Logged out successfully!');
        // In a real application, you would redirect to the login page
    }
}

function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>${message}</span>
    `;
    
    // Add notification styles
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        background: '#10b981',
        color: 'white',
        padding: '1rem 1.5rem',
        borderRadius: '0.5rem',
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
        zIndex: '9999',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease'
    });
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}