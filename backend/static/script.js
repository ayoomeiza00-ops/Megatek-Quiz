let questions = [];
let currentIndex = 0;
let timer = null;
let timeLeft = 0;
let selectedOption = null;
let resultId = null;
let score = 0;

const startScreen = document.getElementById('start-screen');
const quizScreen = document.getElementById('quiz-screen');
const resultScreen = document.getElementById('result-screen');
const startBtn = document.getElementById('start-btn');
const questionText = document.getElementById('question-text');
const optionsContainer = document.getElementById('options-container');
const nextBtn = document.getElementById('next-btn');
const timerDisplay = document.getElementById('timer-display');
const questionCounter = document.getElementById('question-counter');
const roundInfo = document.getElementById('round-info');
const finalScore = document.getElementById('final-score');
const resultLink = document.getElementById('result-link');
const copyBtn = document.getElementById('copy-btn');

// Fetch questions and start
startBtn.addEventListener('click', async () => {
    // Call /api/start to create a session
    const resp = await fetch('/api/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_name: 'Student' })
    });
    const data = await resp.json();
    resultId = data.result_id;
    
    // Load questions
    const qResp = await fetch('/api/questions');
    questions = await qResp.json();
    
    startScreen.style.display = 'none';
    quizScreen.style.display = 'block';
    showQuestion(0);
});

function showQuestion(index) {
    if (index >= questions.length) {
        finishQuiz();
        return;
    }
    const q = questions[index];
    currentIndex = index;
    selectedOption = null;
    nextBtn.disabled = true;
    
    // Update header
    const round = q.round;
    roundInfo.textContent = `Round ${round}`;
    questionCounter.textContent = `${index+1} / ${questions.length}`;
    
    // Set timer
    timeLeft = q.time_limit;
    timerDisplay.textContent = `⏱ ${timeLeft}s`;
    
    // Show question
    questionText.textContent = `${index+1}. ${q.question}`;
    optionsContainer.innerHTML = '';
    q.options.forEach((opt, i) => {
        const label = document.createElement('label');
        label.innerHTML = `<input type="radio" name="option" value="${i}"> ${opt}`;
        optionsContainer.appendChild(label);
    });
    
    // Radio change
    document.querySelectorAll('input[name="option"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
            selectedOption = parseInt(e.target.value);
            nextBtn.disabled = false;
            // Highlight selected
            document.querySelectorAll('#options-container label').forEach((l, idx) => {
                l.classList.toggle('selected', idx === selectedOption);
            });
        });
    });
    
    // Start timer
    clearInterval(timer);
    timer = setInterval(() => {
        timeLeft--;
        timerDisplay.textContent = `⏱ ${timeLeft}s`;
        if (timeLeft <= 0) {
            clearInterval(timer);
            // Timeout: auto advance with no selection
            submitAnswer(null);
        }
    }, 1000);
}

// Next button click
nextBtn.addEventListener('click', () => {
    clearInterval(timer);
    submitAnswer(selectedOption);
});

function submitAnswer(selected) {
    // Send answer to backend
    fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            q_index: currentIndex,
            selected: selected !== undefined ? selected : null
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // Move to next question
            showQuestion(currentIndex + 1);
        }
    });
}

function finishQuiz() {
    clearInterval(timer);
    // Call finish endpoint to get final score
    fetch('/api/finish', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            quizScreen.style.display = 'none';
            resultScreen.style.display = 'block';
            finalScore.textContent = data.score;
            const link = `${window.location.origin}/result/${data.result_id}`;
            resultLink.value = link;
        });
}

// Copy link
copyBtn.addEventListener('click', () => {
    resultLink.select();
    document.execCommand('copy');
    alert('Link copied!');
});