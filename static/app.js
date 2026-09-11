// VeriProfile AI - Core Frontend Controller
document.addEventListener('DOMContentLoaded', () => {
  // Initialize Lucide Icons
  lucide.createIcons();

  // State
  let currentResult = null;
  let radarChartInstance = null;
  let uploadedImageFile = null;

  // DOM Elements
  const profileForm = document.getElementById('profileForm');
  const analyzeBtn = document.getElementById('analyzeBtn');
  const resetBtn = document.getElementById('resetBtn');
  const presetsContainer = document.getElementById('presetsContainer');
  const imageInput = document.getElementById('imageInput');
  const imageDropzone = document.getElementById('imageDropzone');
  const dropzoneContent = document.getElementById('dropzoneContent');
  const dropzonePreview = document.getElementById('dropzonePreview');
  const previewImg = document.getElementById('previewImg');
  const removeImgBtn = document.getElementById('removeImgBtn');
  const exportDossierBtn = document.getElementById('exportDossierBtn');
  const copyJsonBtn = document.getElementById('copyJsonBtn');
  const toast = document.getElementById('toast');

  // Gauge & HUD Elements
  const meterFill = document.getElementById('meterFill');
  const fakeProbVal = document.getElementById('fakeProbVal');
  const threatClassification = document.getElementById('threatClassification');
  const dossierBadge = document.getElementById('dossierBadge');
  const hudAnnotatedImage = document.getElementById('hudAnnotatedImage');
  const hudPlaceholder = document.getElementById('hudPlaceholder');
  const hudScanline = document.getElementById('hudScanline');
  const cvStatusBadge = document.getElementById('cvStatusBadge');
  const statFaces = document.getElementById('statFaces');
  const statRatio = document.getElementById('statRatio');
  const statSharpness = document.getElementById('statSharpness');

  // Metrics
  const metricFFRatio = document.getElementById('metricFFRatio');
  const metricDensity = document.getElementById('metricDensity');
  const metricDigits = document.getElementById('metricDigits');
  const metricAuth = document.getElementById('metricAuth');
  const flaggedList = document.getElementById('flaggedList');
  const positiveList = document.getElementById('positiveList');

  // Tabs
  const navBtns = document.querySelectorAll('.nav-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');

  // Batch
  const batchDropzone = document.getElementById('batchDropzone');
  const batchFilesInput = document.getElementById('batchFilesInput');
  const batchProgress = document.getElementById('batchProgress');
  const batchProgressBar = document.getElementById('batchProgressBar');
  const batchProgressPct = document.getElementById('batchProgressPct');
  const batchTableWrapper = document.getElementById('batchTableWrapper');
  const batchTableBody = document.getElementById('batchTableBody');

  // ==================== 1. CYBER BACKGROUND PARTICLES ====================
  const canvas = document.getElementById('cyberCanvas');
  const ctx = canvas.getContext('2d');
  let particles = [];

  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resizeCanvas);
  resizeCanvas();

  for (let i = 0; i < 45; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      size: Math.random() * 2 + 1
    });
  }

  function drawParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'rgba(0, 242, 254, 0.4)';
    ctx.strokeStyle = 'rgba(0, 242, 254, 0.05)';

    for (let i = 0; i < particles.length; i++) {
      let p = particles[i];
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0) p.x = canvas.width;
      if (p.x > canvas.width) p.x = 0;
      if (p.y < 0) p.y = canvas.height;
      if (p.y > canvas.height) p.y = 0;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();

      for (let j = i + 1; j < particles.length; j++) {
        let p2 = particles[j];
        let dx = p.x - p2.x;
        let dy = p.y - p2.y;
        let dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 130) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(drawParticles);
  }
  drawParticles();

  // ==================== 2. TABS CONTROLLER ====================
  navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      navBtns.forEach(b => b.classList.remove('active'));
      tabPanes.forEach(t => t.classList.remove('active'));

      btn.classList.add('active');
      const targetTab = btn.getAttribute('data-tab');
      const targetPane = document.getElementById(`${targetTab}Tab`);
      if (targetPane) targetPane.classList.add('active');
    });
  });

  // ==================== 3. RADAR CHART INIT ====================
  function initRadarChart(dataScores = null) {
    const defaultData = dataScores ? Object.values(dataScores) : [20, 20, 20, 20, 20];
    const labels = dataScores ? Object.keys(dataScores) : [
      'Audience Health', 'Visual Authenticity', 'Handle Credibility', 'Activity Density', 'Metadata Integrity'
    ];

    const ctxRadar = document.getElementById('radarChart').getContext('2d');

    if (radarChartInstance) {
      radarChartInstance.destroy();
    }

    radarChartInstance = new Chart(ctxRadar, {
      type: 'radar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Health Dimension Score',
          data: defaultData,
          backgroundColor: 'rgba(0, 242, 254, 0.18)',
          borderColor: '#00f2fe',
          borderWidth: 2,
          pointBackgroundColor: '#00f2fe',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: '#00f2fe',
          pointRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            angleLines: { color: 'rgba(255, 255, 255, 0.08)' },
            grid: { color: 'rgba(255, 255, 255, 0.08)' },
            pointLabels: {
              color: '#94a3b8',
              font: { size: 10, family: "'Plus Jakarta Sans', sans-serif" }
            },
            suggestedMin: 0,
            suggestedMax: 100,
            ticks: { display: false, stepSize: 25 }
          }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }
  initRadarChart();

  // ==================== 4. LOAD PRESETS ====================
  async function loadPresets() {
    try {
      const res = await fetch('/api/presets');
      const data = await res.json();
      presetsContainer.innerHTML = '';

      if (data.presets && data.presets.length > 0) {
        data.presets.forEach(p => {
          const chip = document.createElement('button');
          chip.className = 'preset-chip';
          chip.textContent = p.name;
          chip.title = p.description;
          chip.addEventListener('click', () => {
            applyPreset(p);
          });
          presetsContainer.appendChild(chip);
        });
      }
    } catch (e) {
      presetsContainer.innerHTML = '<span style="font-size:0.75rem; color:#ef4444;">Could not load presets</span>';
    }
  }
  loadPresets();

  function applyPreset(p) {
    document.getElementById('username').value = p.username;
    document.getElementById('followers').value = p.followers;
    document.getElementById('following').value = p.following;
    document.getElementById('posts').value = p.posts;
    document.getElementById('bio').value = p.bio;
    document.getElementById('is_private').value = p.is_private ? '1' : '0';

    clearImage();
    showToast(`Loaded preset: ${p.name}`);
  }

  // ==================== 5. IMAGE DROPZONE HANDLING ====================
  imageDropzone.addEventListener('click', () => imageInput.click());

  ['dragenter', 'dragover'].forEach(eventName => {
    imageDropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      imageDropzone.style.borderColor = '#00f2fe';
    });
  });

  ['dragleave', 'drop'].forEach(eventName => {
    imageDropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      imageDropzone.style.borderColor = '';
    });
  });

  imageDropzone.addEventListener('drop', (e) => {
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleImageSelection(e.dataTransfer.files[0]);
    }
  });

  imageInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files[0]) {
      handleImageSelection(e.target.files[0]);
    }
  });

  function handleImageSelection(file) {
    uploadedImageFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImg.src = e.target.result;
      dropzoneContent.classList.add('hidden');
      dropzonePreview.classList.remove('hidden');
    };
    reader.readAsDataURL(file);
  }

  removeImgBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    clearImage();
  });

  function clearImage() {
    uploadedImageFile = null;
    imageInput.value = '';
    previewImg.src = '';
    dropzoneContent.classList.remove('hidden');
    dropzonePreview.classList.add('hidden');
  }

  // ==================== 6. SUBMIT PROFILE ANALYSIS ====================
  profileForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    await runProfileScan();
  });

  async function runProfileScan() {
    analyzeBtn.disabled = true;
    hudScanline.classList.add('active');

    const formData = new FormData();
    formData.append('username', document.getElementById('username').value);
    formData.append('followers', document.getElementById('followers').value);
    formData.append('following', document.getElementById('following').value);
    formData.append('posts', document.getElementById('posts').value);
    formData.append('bio', document.getElementById('bio').value);
    formData.append('is_private', document.getElementById('is_private').value);

    if (uploadedImageFile) {
      formData.append('image', uploadedImageFile);
    }

    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();

      if (data.success && data.result) {
        currentResult = data.result;
        renderResult(data.result);
        showToast('Scan complete. Telemetry updated.');
      } else {
        showToast('Analysis error: ' + (data.error || 'Server rejected request'));
      }
    } catch (err) {
      showToast('Network error: ' + err.message);
    } finally {
      analyzeBtn.disabled = false;
      hudScanline.classList.remove('active');
    }
  }

  function renderResult(res) {
    // 1. Dossier & Threat Classification
    dossierBadge.textContent = `#${res.dossier_id}`;
    threatClassification.textContent = res.classification;
    threatClassification.style.color = res.theme_color;
    threatClassification.style.borderColor = res.theme_color;
    threatClassification.style.background = `${res.theme_color}18`;

    // 2. Animate Circular Speedometer Gauge (Circumference ~ 502)
    const prob = res.fake_probability;
    const circumference = 2 * Math.PI * 80; // ~502.65
    const offset = circumference - (prob / 100) * circumference;

    meterFill.style.stroke = res.theme_color;
    meterFill.style.strokeDashoffset = offset;

    // Counter animation
    let currentVal = 0;
    const step = prob / 20;
    const interval = setInterval(() => {
      currentVal += step;
      if (currentVal >= prob) {
        currentVal = prob;
        clearInterval(interval);
      }
      fakeProbVal.textContent = `${currentVal.toFixed(1)}%`;
      fakeProbVal.style.color = res.theme_color;
    }, 25);

    // 3. Biometric HUD Viewport
    if (res.cv_analysis && res.cv_analysis.annotated_image_base64) {
      hudAnnotatedImage.src = res.cv_analysis.annotated_image_base64;
      hudAnnotatedImage.style.display = 'block';
      hudPlaceholder.style.display = 'none';

      cvStatusBadge.textContent = res.cv_analysis.forensic_badge;
      cvStatusBadge.style.color = res.theme_color;
      cvStatusBadge.style.borderColor = res.theme_color;

      statFaces.textContent = res.cv_analysis.face_count;
      statRatio.textContent = `${(res.cv_analysis.face_ratio * 100).toFixed(1)}%`;
      statSharpness.textContent = res.cv_analysis.sharpness;
    } else {
      hudAnnotatedImage.style.display = 'none';
      hudPlaceholder.style.display = 'block';
      cvStatusBadge.textContent = 'NO AVATAR';
      statFaces.textContent = '0';
      statRatio.textContent = '0%';
      statSharpness.textContent = '0';
    }

    // 4. Metric summary tiles
    metricFFRatio.textContent = res.metrics.ff_ratio;
    metricDensity.textContent = res.metrics.activity_density;
    metricDigits.textContent = `${res.metrics.digit_ratio}%`;
    metricAuth.textContent = `${res.authenticity_score}%`;
    metricAuth.style.color = res.authenticity_score > 60 ? '#10b981' : '#ef4444';

    // 5. Radar chart
    initRadarChart(res.radar_scores);

    // 6. Reasons breakdown
    flaggedList.innerHTML = '';
    res.reasons_flagged.forEach(reason => {
      const li = document.createElement('li');
      li.textContent = reason;
      flaggedList.appendChild(li);
    });

    positiveList.innerHTML = '';
    res.positive_factors.forEach(indicator => {
      const li = document.createElement('li');
      li.textContent = indicator;
      positiveList.appendChild(li);
    });

    // 7. Enable action buttons
    exportDossierBtn.disabled = false;
    copyJsonBtn.disabled = false;
  }

  // ==================== 7. EXPORT & COPY ====================
  exportDossierBtn.addEventListener('click', async () => {
    if (!currentResult) return;
    try {
      const res = await fetch('/api/export-dossier', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ result: currentResult })
      });
      const html = await res.text();
      const printWindow = window.open('', '_blank');
      printWindow.document.write(html);
      printWindow.document.close();
    } catch (e) {
      showToast('Export failed: ' + e.message);
    }
  });

  copyJsonBtn.addEventListener('click', () => {
    if (!currentResult) return;
    navigator.clipboard.writeText(JSON.stringify(currentResult, null, 2));
    showToast('Copied JSON forensic telemetry to clipboard!');
  });

  resetBtn.addEventListener('click', () => {
    profileForm.reset();
    clearImage();
    fakeProbVal.textContent = '--%';
    fakeProbVal.style.color = '#f8fafc';
    meterFill.style.strokeDashoffset = 502;
    threatClassification.textContent = 'AWAITING TARGET TELEMETRY';
    threatClassification.style.color = '';
    threatClassification.style.borderColor = '';
    threatClassification.style.background = '';
    hudAnnotatedImage.style.display = 'none';
    hudPlaceholder.style.display = 'block';
    flaggedList.innerHTML = '<li class="empty-state">No profile scanned yet.</li>';
    positiveList.innerHTML = '<li class="empty-state">No profile scanned yet.</li>';
    initRadarChart();
    exportDossierBtn.disabled = true;
    copyJsonBtn.disabled = true;
  });

  // ==================== 8. BATCH SCANNER ====================
  batchDropzone.addEventListener('click', () => batchFilesInput.click());

  batchFilesInput.addEventListener('change', async (e) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    batchProgress.classList.remove('hidden');
    batchTableWrapper.style.display = 'block';
    batchTableBody.innerHTML = '';

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append(`file_${i}`, files[i]);
    }

    try {
      batchProgressBar.style.width = '40%';
      batchProgressPct.textContent = '40%';

      const res = await fetch('/api/batch', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();

      batchProgressBar.style.width = '100%';
      batchProgressPct.textContent = '100%';

      if (data.success && data.results) {
        data.results.forEach(item => {
          const tr = document.createElement('tr');
          const cv = item.cv_analysis || {};

          tr.innerHTML = `
            <td>
              <img src="${cv.annotated_image_base64 || '/static/placeholder.png'}" class="batch-avatar" alt="Avatar" />
            </td>
            <td><strong>@${item.username}</strong></td>
            <td><span class="badge-cyan">${cv.forensic_badge || 'N/A'}</span></td>
            <td>${cv.sharpness || 0}</td>
            <td style="color:${item.theme_color}; font-family:var(--font-mono); font-weight:700;">
              ${item.fake_probability}%
            </td>
            <td>
              <span style="color:${item.theme_color}; font-weight:700; font-size:0.75rem;">
                ${item.threat_level}
              </span>
            </td>
          `;
          batchTableBody.appendChild(tr);
        });
        showToast(`Batch completed: ${data.results.length} accounts analyzed.`);
      }
    } catch (err) {
      showToast('Batch processing error: ' + err.message);
    }
  });

  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 3200);
  }

  // Automatically run initial scan on default profile for instant demonstration
  setTimeout(() => {
    runProfileScan();
  }, 400);
});
