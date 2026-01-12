
let currentLanguage = 'english';
let currentState = '';
let allStates = [];
let allCrops = [];


document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});


async function initializeApp() {
    await loadStates();
    await loadCrops();
    await loadLanguages();
    
    
    document.getElementById('languageSelect').value = currentLanguage;
}


async function loadStates() {
    try {
        const response = await fetch('/api/states');
        const data = await response.json();
        allStates = data.states;
        
        
        ['stateSelect', 'stateSelect2'].forEach(id => {
            const select = document.getElementById(id);
            select.innerHTML = '<option value="">Select Your State</option>';
            allStates.forEach(state => {
                const option = document.createElement('option');
                option.value = state;
                option.textContent = state;
                select.appendChild(option);
            });
        });
    } catch (error) {
        console.error('Error loading states:', error);
    }
}


async function loadCrops() {
    try {
        const response = await fetch('/api/crops');
        const data = response.json();
        allCrops = (await data).crops;
        
        
        ['cropSelect1', 'cropSelect2', 'cropSelect3'].forEach(id => {
            const select = document.getElementById(id);
            select.innerHTML = '<option value="">Choose a crop</option>';
            allCrops.forEach(crop => {
                const option = document.createElement('option');
                option.value = crop;
                option.textContent = crop;
                select.appendChild(option);
            });
        });
    } catch (error) {
        console.error('Error loading crops:', error);
    }
}


async function loadLanguages() {
    try {
        const response = await fetch('/api/languages');
        const data = await response.json();
        
        const languageSelect = document.getElementById('languageSelect');
        languageSelect.innerHTML = '';
        
        for (const [code, label] of Object.entries(data.languages)) {
            const option = document.createElement('option');
            option.value = code;
            option.textContent = label;
            languageSelect.appendChild(option);
        }
    } catch (error) {
        console.error('Error loading languages:', error);
    }
}

function updateLanguage() {
    const select = document.getElementById('languageSelect');
    currentLanguage = select.value;
    console.log('Language changed to:', currentLanguage);
}

function updateState() {
    const select = document.getElementById('stateSelect');
    currentState = select.value;
    console.log('State changed to:', currentState);
}

function showSection(sectionId) {

    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.add('active');
    }
    
    const navLink = document.querySelector(`[onclick="showSection('${sectionId}')"]`);
    if (navLink) {
        navLink.classList.add('active');
    }
    
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}


async function getAdvisory() {
    const crop = document.getElementById('cropSelect1').value;
    const problem = document.getElementById('problemText').value;
    const language = currentLanguage;
    
    if (!crop || !problem) {
        alert('Please select a crop and describe the problem');
        return;
    }
    
    showLoading(true);
    document.getElementById('spinner1').style.display = 'inline-block';
    
    try {
        const response = await fetch('/api/crop-advisory', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                crop: crop,
                problem: problem,
                language: language
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayAdvisoryResult(data);
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error getting advisory:', error);
        alert('Error getting advisory. Please try again.');
    } finally {
        showLoading(false);
        document.getElementById('spinner1').style.display = 'none';
    }
}

function displayAdvisoryResult(data) {
    const resultDiv = document.getElementById('advisoryResult');
    const contentDiv = document.getElementById('advisoryContent');
    
    contentDiv.innerHTML = `
        <div class="result-text">
            ${data.advisory.replace(/\n/g, '<br>')}
        </div>
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 2px solid #ecf0f1; font-size: 0.9rem; color: #7f8c8d;">
            <strong>⚠️ Disclaimer:</strong> ${data.disclaimer}
        </div>
    `;
    
    resultDiv.style.display = 'block';
    resultDiv.scrollIntoView({ behavior: 'smooth' });
}


function handleImageSelect() {
    const input = document.getElementById('imageInput');
    const file = input.files[0];
    
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = document.getElementById('previewImg');
            img.src = e.target.result;
            document.getElementById('imagePreview').style.display = 'block';
            document.getElementById('analyzeBtn').style.display = 'flex';
        };
        reader.readAsDataURL(file);
    }
}

function clearImage() {
    document.getElementById('imageInput').value = '';
    document.getElementById('imagePreview').style.display = 'none';
    document.getElementById('analyzeBtn').style.display = 'none';
    document.getElementById('imageResult').style.display = 'none';
}

async function analyzeImage() {
    const input = document.getElementById('imageInput');
    const file = input.files[0];
    
    if (!file) {
        alert('Please select an image');
        return;
    }
    
    const formData = new FormData();
    formData.append('image', file);
    formData.append('language', currentLanguage);
    
    showLoading(true);
    document.getElementById('spinner2').style.display = 'inline-block';
    
    try {
        const response = await fetch('/api/analyze-image', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayImageResult(data);
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error analyzing image:', error);
        alert('Error analyzing image. Please try again.');
    } finally {
        showLoading(false);
        document.getElementById('spinner2').style.display = 'none';
    }
}

function displayImageResult(data) {
    const resultDiv = document.getElementById('imageResult');
    const contentDiv = document.getElementById('imageContent');
    
    contentDiv.innerHTML = `
        <div class="result-text">
            ${data.analysis.replace(/\n/g, '<br>')}
        </div>
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 2px solid #ecf0f1; font-size: 0.9rem; color: #7f8c8d;">
            <strong>⚠️ Disclaimer:</strong> ${data.disclaimer}
        </div>
    `;
    
    resultDiv.style.display = 'block';
    resultDiv.scrollIntoView({ behavior: 'smooth' });
}


async function getPlanningAdvisory() {
    const crop = document.getElementById('cropSelect2').value;
    const planningType = document.querySelector('input[name="planning_type"]:checked').value;
    const language = currentLanguage;
    
    if (!crop) {
        alert('Please select a crop');
        return;
    }
    
    showLoading(true);
    document.getElementById('spinner3').style.display = 'inline-block';
    
    try {
        const response = await fetch('/api/planning-advisory', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                crop: crop,
                planning_type: planningType,
                language: language
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayPlanningResult(data);
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error getting planning advisory:', error);
        alert('Error getting planning advice. Please try again.');
    } finally {
        showLoading(false);
        document.getElementById('spinner3').style.display = 'none';
    }
}

function displayPlanningResult(data) {
    const resultDiv = document.getElementById('planningResult');
    const contentDiv = document.getElementById('planningContent');
    
    const planningTypeLabel = data.planning_type === 'weather' ? 'Weather Planning' : 'Market Planning';
    
    contentDiv.innerHTML = `
        <div style="margin-bottom: 1rem; padding: 0.5rem; background: rgba(47, 196, 109, 0.1); border-radius: 8px;">
            <strong>Type: ${planningTypeLabel}</strong>
        </div>
        <div class="result-text">
            ${data.advisory.replace(/\n/g, '<br>')}
        </div>
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 2px solid #ecf0f1; font-size: 0.9rem; color: #7f8c8d;">
            <strong>ℹ️ Note:</strong> ${data.disclaimer}
        </div>
    `;
    
    resultDiv.style.display = 'block';
    resultDiv.scrollIntoView({ behavior: 'smooth' });
}


async function getSchemes() {
    const state = document.getElementById('stateSelect2').value;
    const crop = document.getElementById('cropSelect3').value;
    const language = currentLanguage;
    
    if (!state || !crop) {
        alert('Please select both state and crop');
        return;
    }
    
    showLoading(true);
    document.getElementById('spinner4').style.display = 'inline-block';
    
    try {
        const response = await fetch('/api/schemes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                state: state,
                crop: crop,
                language: language
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displaySchemesResult(data);
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error getting schemes:', error);
        alert('Error getting schemes. Please try again.');
    } finally {
        showLoading(false);
        document.getElementById('spinner4').style.display = 'none';
    }
}

function displaySchemesResult(data) {
    const resultDiv = document.getElementById('schemesResult');
    const contentDiv = document.getElementById('schemesContent');
    
    if (data.schemes.length === 0) {
        contentDiv.innerHTML = `
            <div style="padding: 2rem; text-align: center; background: #f5f7fa; border-radius: 12px;">
                <p style="color: #7f8c8d; font-size: 1.1rem;">
                    ${data.message || 'No schemes found for this combination.'}
                </p>
            </div>
        `;
    } else {
        let html = '';
        data.schemes.forEach((scheme, index) => {
            html += `
                <div class="scheme-item">
                    <h4>${index + 1}. ${scheme.scheme_name}</h4>
                    <div class="result-text" style="margin-top: 1rem;">
                        ${scheme.explanation.replace(/\n/g, '<br>')}
                    </div>
                </div>
            `;
        });
        contentDiv.innerHTML = html;
    }
    
    resultDiv.style.display = 'block';
    resultDiv.scrollIntoView({ behavior: 'smooth' });
}

function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (show) {
        overlay.style.display = 'flex';
    } else {
        overlay.style.display = 'none';
    }
}


function formatText(text) {
    return text.replace(/\n/g, '<br>').replace(/\n\n/g, '<br><br>');
}


function handleError(error) {
    console.error('Error:', error);
    showLoading(false);
    alert('An error occurred. Please try again.');
}
window.addEventListener("scroll", () => {
    const btn = document.getElementById("backToTop");
    if (window.scrollY > 300) {
        btn.style.display = "block";
    } else {
        btn.style.display = "none";
    }
});

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


console.log('%cAnnadata Saathi v1.0', 'color: #093d1fff; font-size: 16px; font-weight: bold;');
console.log('AI Agricultural Assistant for Indian Farmers');
