// app.js - Logica interactiva para el Sistema de Priorizacion de Inspecciones - GAMLP

const tabs = ['general', 'estructural', 'humedad', 'terreno', 'entorno'];
let currentTab = 0;
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const btnPrev = document.getElementById('btn-prev');
const btnNext = document.getElementById('btn-next');
const btnSubmit = document.getElementById('btn-submit');

function switchTab(index) {
    if (index < 0 || index >= tabs.length) return;
    currentTab = index;
    tabBtns.forEach((btn, i) => {
        if (i === index) btn.classList.add('active');
        else btn.classList.remove('active');
    });
    tabContents.forEach((content, i) => {
        if (i === index) content.classList.add('active');
        else content.classList.remove('active');
    });
    
    btnPrev.disabled = index === 0;
    
    if (index === tabs.length - 1) {
        btnNext.classList.add('hidden');
        btnSubmit.classList.remove('hidden');
    } else {
        btnNext.classList.remove('hidden');
        btnSubmit.classList.add('hidden');
    }
}

tabBtns.forEach((btn, i) => btn.addEventListener('click', () => switchTab(i)));
btnPrev.addEventListener('click', () => switchTab(currentTab - 1));
btnNext.addEventListener('click', () => switchTab(currentTab + 1));

// DRAG AND DROP
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const previewContainer = document.getElementById('preview-container');
const previewImg = document.getElementById('image-preview');
const previewFilename = document.getElementById('preview-filename');
const btnRemoveImg = document.getElementById('btn-remove-img');
const iaLoading = document.getElementById('ia-loading');
const iaSuccess = document.getElementById('ia-success');

dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', e => {
    e.preventDefault(); dropZone.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) handleImageFile(file);
    else showToast('Suba una imagen valida (JPG, PNG, WEBP).', 'error');
});
fileInput.addEventListener('change', () => { if (fileInput.files[0]) handleImageFile(fileInput.files[0]); });
btnRemoveImg.addEventListener('click', () => {
    fileInput.value = '';
    dropZone.classList.remove('hidden');
    previewContainer.classList.add('hidden');
    iaSuccess.classList.add('hidden');
    iaLoading.classList.add('hidden');
});

async function handleImageFile(file) {
    const reader = new FileReader();
    reader.onload = e => {
        previewImg.src = e.target.result;
        previewFilename.textContent = file.name;
        dropZone.classList.add('hidden');
        previewContainer.classList.remove('hidden');
    };
    reader.readAsDataURL(file);
    const fd = new FormData();
    fd.append('image', file);
    iaLoading.classList.remove('hidden');
    iaSuccess.classList.add('hidden');
    
    try {
        const res = await fetch('/upload-image', { method: 'POST', body: fd });
        const data = await res.json();
        if (!res.ok) { 
            showToast(data.error || 'Error al analizar imagen.', 'error'); 
            iaLoading.classList.add('hidden'); 
            return; 
        }
        
        if (data.RN26_grietas_IA !== undefined) document.getElementById('RN26_grietas_IA').value = data.RN26_grietas_IA;
        if (data.RN27_humedad_IA !== undefined) document.getElementById('RN27_humedad_IA').value = data.RN27_humedad_IA;
        if (data.RN28_deformacion_IA !== undefined) document.getElementById('RN28_deformacion_IA').value = data.RN28_deformacion_IA;
        
        iaLoading.classList.add('hidden');
        iaSuccess.classList.remove('hidden');
        showToast('Imagen procesada por IA exitosamente.', 'success');
        
        // Mover automáticamente a la última pestaña donde están los resultados de IA
        switchTab(tabs.length - 1);
        
        ['RN26_grietas_IA','RN27_humedad_IA','RN28_deformacion_IA'].forEach(id => {
            const el = document.getElementById(id);
            if (el) { 
                el.style.boxShadow = '0 0 0 3px rgba(255, 102, 0, 0.4)'; 
                setTimeout(() => el.style.boxShadow = '', 2000); 
            }
        });
    } catch { 
        iaLoading.classList.add('hidden'); 
        showToast('Error de conexion con servidor.', 'error'); 
    }
}

// FORM SUBMIT
const evaluationForm = document.getElementById('evaluation-form');
const resultsEmpty = document.getElementById('results-empty');
const resultsContent = document.getElementById('results-content');

evaluationForm.addEventListener('submit', async e => {
    e.preventDefault();
    const btnText = btnSubmit.querySelector('.btn-text');
    const btnLoad = btnSubmit.querySelector('.btn-loading');
    btnText.textContent = 'Procesando...';
    btnLoad.classList.remove('hidden');
    btnSubmit.disabled = true;
    
    const formData = {};
    document.querySelectorAll('[name]').forEach(el => { 
        if (el.name && el.value !== '') formData[el.name] = el.value; 
    });
    
    try {
        const res = await fetch('/predict', { 
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' }, 
            body: JSON.stringify(formData) 
        });
        const result = await res.json();
        if (!res.ok) { 
            showToast(result.error || 'Error al predecir.', 'error'); 
            return; 
        }
        displayResults(result);
    } catch { 
        showToast('Error de conexion. Verifique que app.py este corriendo.', 'error'); 
    } finally {
        btnText.textContent = 'Calcular Riesgo y Prioridad';
        btnLoad.classList.add('hidden');
        btnSubmit.disabled = false;
    }
});

// RESULTADOS
const riskColorMap = {
    BAJO:    { bg: 'rgba(16,185,129,0.12)', border: 'rgba(16,185,129,0.3)', text: '#34d399', stroke: '#10b981' },
    MEDIO:   { bg: 'rgba(245,158,11,0.12)', border: 'rgba(245,158,11,0.3)', text: '#fbbf24', stroke: '#f59e0b' },
    ALTO:    { bg: 'rgba(249,115,22,0.12)', border: 'rgba(249,115,22,0.3)', text: '#fb923c', stroke: '#f97316' },
    CRITICO: { bg: 'rgba(239,68,68,0.12)',  border: 'rgba(239,68,68,0.3)',  text: '#f87171', stroke: '#ef4444' },
};

function displayResults(result) {
    resultsEmpty.classList.add('hidden');
    resultsContent.classList.remove('hidden');
    
    const now = new Date();
    document.getElementById('result-timestamp').textContent = now.toLocaleString('es-BO', { dateStyle: 'medium', timeStyle: 'short' });
    
    const score = parseFloat(result.indice_riesgo);
    const gaugeEl = document.getElementById('gauge-fill');
    const circumference = 314.16;
    animateValue(document.getElementById('risk-score'), 0, score, 1500, v => v.toFixed(1));
    setTimeout(() => { gaugeEl.style.strokeDashoffset = circumference - (score / 100) * circumference; }, 100);
    
    const nivel = result.nivel_riesgo;
    const colors = riskColorMap[nivel] || riskColorMap.CRITICO;
    const riskBadge = document.getElementById('risk-badge-card');
    riskBadge.style.backgroundColor = colors.bg;
    riskBadge.style.borderColor = colors.border;
    const riskTitle = document.getElementById('risk-level');
    riskTitle.style.color = colors.text;
    riskTitle.textContent = nivel;
    gaugeEl.style.stroke = colors.stroke;
    
    document.getElementById('action-title').textContent = result.accion;
    document.getElementById('action-desc').textContent = result.detalle;
    
    const prioridad = parseFloat(result.prioridad);
    const priorityBar = document.getElementById('priority-bar');
    animateValue(document.getElementById('priority-value'), 0, prioridad, 1200, v => v.toFixed(1));
    setTimeout(() => { priorityBar.style.width = ((prioridad / 10) * 100) + '%'; }, 100);
    priorityBar.style.backgroundColor = colors.stroke;
    
    const confianza = parseFloat(result.confianza);
    const confBar = document.getElementById('confidence-bar');
    animateValue(document.getElementById('confidence-value'), 0, confianza, 1200, v => v.toFixed(1) + '%');
    setTimeout(() => { confBar.style.width = confianza + '%'; }, 100);
    
    if (window.innerWidth < 1024) document.getElementById('results-panel').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

document.getElementById('btn-reset-eval').addEventListener('click', () => {
    resultsContent.classList.add('hidden');
    resultsEmpty.classList.remove('hidden');
    evaluationForm.reset();
    btnRemoveImg.click();
    document.getElementById('gauge-fill').style.strokeDashoffset = '314.16';
    document.getElementById('priority-bar').style.width = '0%';
    document.getElementById('confidence-bar').style.width = '0%';
    switchTab(0);
});

function animateValue(el, start, end, duration, formatter) {
    const t0 = performance.now();
    function upd(ts) {
        const p = Math.min((ts - t0) / duration, 1);
        const e = 1 - Math.pow(1 - p, 3);
        el.textContent = formatter(start + (end - start) * e);
        if (p < 1) requestAnimationFrame(upd);
    }
    requestAnimationFrame(upd);
}

function showToast(message, type) {
    const existing = document.querySelector('.toast-notification');
    if (existing) existing.remove();
    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.textContent = message;
    const c = { 
        success: { bg:'rgba(16,185,129,0.15)',border:'rgba(16,185,129,0.3)',text:'#34d399' }, 
        error: { bg:'rgba(239,68,68,0.15)',border:'rgba(239,68,68,0.3)',text:'#f87171' }, 
        info: { bg:'rgba(255,102,0,0.15)',border:'rgba(255,102,0,0.3)',text:'#ff6600' } 
    }[type || 'info'];
    toast.style.cssText = 'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:' + c.bg + ';border:1px solid ' + c.border + ';color:' + c.text + ';padding:12px 20px;border-radius:10px;font-size:0.85rem;font-weight:500;z-index:9999;max-width:480px;text-align:center;backdrop-filter:blur(12px);';
    document.body.appendChild(toast);
    setTimeout(() => { 
        toast.style.opacity='0'; 
        toast.style.transition='opacity 0.3s'; 
        setTimeout(() => toast.remove(), 300); 
    }, 4000);
}

// Theme toggle
const themeToggle = document.getElementById('theme-toggle');
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark');
        const isDark = document.body.classList.contains('dark');
        themeToggle.textContent = isDark ? '☀️ Claro' : '🌙 Oscuro';
    });
}

switchTab(0);
