const video = document.getElementById('video');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const snapshotBtn = document.getElementById('snapshotBtn');
const clearBtn = document.getElementById('clearBtn');
const darkModeBtn = document.getElementById('darkModeBtn');
const status = document.getElementById('status');
const output = document.getElementById('output');

let stream = null;
let captureInterval = null;
let darkMode = false;

async function startWebcam() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        video.srcObject = stream;
        startBtn.disabled = true;
        stopBtn.disabled = false;
        status.textContent = '🟢 Running...';
        startCaptureLoop();
    } catch (err) {
        console.error('Failed to start webcam:', err);
        status.textContent = '❌ Error: ' + err.message;
    }
}

function stopWebcam() {
    if (stream) {
        stream.getTracks().forEach(t => t.stop());
        stream = null;
    }
    if (captureInterval) {
        clearInterval(captureInterval);
        captureInterval = null;
    }
    startBtn.disabled = false;
    stopBtn.disabled = true;
    status.textContent = '⏹️ Stopped';
}

function startCaptureLoop() {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 640;
    canvas.height = 480;

    captureInterval = setInterval(async () => {
        if (!stream) return;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
        status.textContent = '📤 Sending frame...';
        try {
            const resp = await fetch('/detect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: dataUrl })
            });
            const json = await resp.json();
            if (json.image) {
                output.src = json.image;
                status.textContent = '✅ Frame processed';
            } else if (json.error) {
                status.textContent = '⚠️ Server error: ' + json.error;
            }
        } catch (err) {
            console.error('Error sending frame:', err);
            status.textContent = '❌ Network error: ' + err.message;
        }
    }, 700); // every 700ms
}

// 📸 Snapshot
snapshotBtn.addEventListener('click', () => {
    if (!output.src) {
        alert("No detection output yet!");
        return;
    }
    const a = document.createElement('a');
    a.href = output.src;
    a.download = 'snapshot.jpg';
    a.click();
});

// 🗑️ Clear Output
clearBtn.addEventListener('click', () => {
    output.src = '';
    status.textContent = '🧹 Output cleared';
});

// 🌙 Dark Mode
darkModeBtn.addEventListener('click', () => {
    darkMode = !darkMode;
    document.body.style.background = darkMode ? "#1f2937" : "#f4f6f9";
    document.body.style.color = darkMode ? "#f9fafb" : "#333";
    darkModeBtn.textContent = darkMode ? "☀️ Light Mode" : "🌙 Dark Mode";
});

startBtn.addEventListener('click', startWebcam);
stopBtn.addEventListener('click', stopWebcam);
