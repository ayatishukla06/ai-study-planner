// --- POMODORO LOGIC ---
let timeLeft = 25 * 60; 
let timerId = null;
let isBreak = false;

function updateDisplay() {
    const display = document.getElementById('timer-display');
    if (!display) return;
    
    let mins = Math.floor(timeLeft / 60);
    let secs = timeLeft % 60;
    display.innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function toggleTimer() {
    const controlBtn = document.getElementById('timer-control');
    const statusText = document.getElementById('timer-status');

    if (timerId) {
        clearInterval(timerId);
        timerId = null;
        if (controlBtn) controlBtn.innerText = "Resume Quest";
        if (statusText) statusText.innerText = "Paused...";
    } else {
        if (controlBtn) controlBtn.innerText = "Pause";
        if (statusText) statusText.innerText = isBreak ? "⚡ Recovery Mode..." : "🔥 Grinding...";
        
        timerId = setInterval(() => {
            if (timeLeft > 0) {
                timeLeft--;
                updateDisplay();
            } else {
                handleTimerEnd();
            }
        }, 1000);
    }
}

function handleTimerEnd() {
    clearInterval(timerId);
    timerId = null;
    const statusText = document.getElementById('timer-status');
    const controlBtn = document.getElementById('timer-control');

    if (!isBreak) {
        alert("Focus Session Complete! Level Up!");
        isBreak = true;
        timeLeft = 5 * 60;
        if (statusText) statusText.innerText = "Break Time!";
    } else {
        alert("Break Over! Back to the Grind!");
        isBreak = false;
        timeLeft = 25 * 60;
        if (statusText) statusText.innerText = "Ready to grind?";
    }
    
    updateDisplay();
    if (controlBtn) controlBtn.innerText = "Start Next Quest";
}

function resetTimer() {
    clearInterval(timerId);
    timerId = null;
    isBreak = false;
    timeLeft = 25 * 60;
    updateDisplay();
    
    const controlBtn = document.getElementById('timer-control');
    const statusText = document.getElementById('timer-status');
    if (controlBtn) controlBtn.innerText = "Start Quest";
    if (statusText) statusText.innerText = "Ready to grind?";
}

// Ensure display is correct on page load
document.addEventListener('DOMContentLoaded', updateDisplay);