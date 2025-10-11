"""Game Templates for different interactive learning experiences"""

# Quick Quiz Template (MCQ)
QUICK_QUIZ_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{GAME_TITLE}} - {{TOPIC}}</title>
    <script src="https://cdn.tailwindcss.com/3.4.0"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <link rel="stylesheet" href="../../styles/theme.css">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#7c3aed',
                        'primary-dark': '#5b21b6',
                        'primary-light': '#a855f7'
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-gradient-to-br from-purple-50 to-indigo-100 min-h-screen">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-purple-100">
        <div class="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
            <div>
                <h1 class="text-xl font-bold text-gray-900">{{GAME_TITLE}}</h1>
                <p class="text-sm text-gray-600">{{TOPIC}}</p>
            </div>
            <div class="flex items-center gap-4">
                <div class="bg-primary text-white px-3 py-1 rounded-full text-sm font-medium">
                    Score: <span id="score">0</span>/{{MAX_SCORE}}
                </div>
                <a href="../" class="text-primary hover:text-primary-dark font-medium">← Back to Topic</a>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-3xl mx-auto px-4 py-8">
        <div class="bg-white rounded-xl shadow-lg p-6">
            <!-- Progress Bar -->
            <div class="mb-6">
                <div class="flex justify-between text-sm text-gray-600 mb-2">
                    <span>Question <span id="current-question">1</span> of <span id="total-questions">{{TOTAL_QUESTIONS}}</span></span>
                    <span><span id="progress-percentage">0</span>% Complete</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                    <div id="progress-bar" class="bg-primary h-2 rounded-full transition-all duration-300" style="width: 0%"></div>
                </div>
            </div>

            <!-- Question Container -->
            <div id="question-container" class="mb-8">
                <h2 id="question-text" class="text-lg font-medium text-gray-900 mb-4"></h2>
                <div id="options-container" class="space-y-3">
                    <!-- Options will be inserted here -->
                </div>
            </div>

            <!-- Controls -->
            <div class="flex justify-between items-center">
                <button id="prev-btn" class="px-4 py-2 text-primary border border-primary rounded-lg hover:bg-primary hover:text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed" disabled>
                    Previous
                </button>
                <button id="next-btn" class="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed" disabled>
                    Next Question
                </button>
            </div>

            <!-- Results Screen (Hidden) -->
            <div id="results-screen" class="hidden text-center">
                <div class="mb-6">
                    <div class="w-24 h-24 mx-auto mb-4 rounded-full bg-primary flex items-center justify-center">
                        <i data-lucide="trophy" class="w-12 h-12 text-white"></i>
                    </div>
                    <h2 class="text-2xl font-bold text-gray-900 mb-2">Quiz Complete!</h2>
                    <p class="text-gray-600">You scored <span id="final-score">0</span> out of {{MAX_SCORE}} points</p>
                    <div id="score-message" class="mt-2 text-sm"></div>
                </div>
                <div class="flex gap-4 justify-center">
                    <button id="retry-btn" class="px-6 py-2 border border-primary text-primary rounded-lg hover:bg-primary hover:text-white transition-colors">
                        Try Again
                    </button>
                    <a href="../" class="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors">
                        Back to Topic
                    </a>
                </div>
            </div>
        </div>
    </main>

    <script src="../../scripts/common.js"></script>
    <script>
        // Game Data - Replace with actual content
        const gameData = {{GAME_DATA}};
        
        // Game State
        let currentQuestion = 0;
        let score = 0;
        let answers = [];
        let gameStarted = false;

        // DOM Elements
        const elements = {
            currentQuestion: document.getElementById('current-question'),
            totalQuestions: document.getElementById('total-questions'),
            progressPercentage: document.getElementById('progress-percentage'),
            progressBar: document.getElementById('progress-bar'),
            questionText: document.getElementById('question-text'),
            optionsContainer: document.getElementById('options-container'),
            prevBtn: document.getElementById('prev-btn'),
            nextBtn: document.getElementById('next-btn'),
            scoreDisplay: document.getElementById('score'),
            questionContainer: document.getElementById('question-container'),
            resultsScreen: document.getElementById('results-screen'),
            finalScore: document.getElementById('final-score'),
            scoreMessage: document.getElementById('score-message'),
            retryBtn: document.getElementById('retry-btn')
        };

        // Initialize Game
        function initGame() {
            elements.totalQuestions.textContent = gameData.questions.length;
            showQuestion(0);
            setupEventListeners();
            gameStarted = true;
            window.__GAME_OK__ = true;
        }

        function setupEventListeners() {
            elements.prevBtn.addEventListener('click', () => navigateQuestion(-1));
            elements.nextBtn.addEventListener('click', () => navigateQuestion(1));
            elements.retryBtn.addEventListener('click', resetGame);
        }

        function showQuestion(index) {
            const question = gameData.questions[index];
            currentQuestion = index;
            
            // Update UI
            elements.currentQuestion.textContent = index + 1;
            elements.questionText.textContent = question.question;
            
            // Update progress
            const progress = ((index + 1) / gameData.questions.length) * 100;
            elements.progressPercentage.textContent = Math.round(progress);
            elements.progressBar.style.width = progress + '%';
            
            // Render options
            renderOptions(question.options, index);
            
            // Update navigation
            elements.prevBtn.disabled = index === 0;
            elements.nextBtn.textContent = index === gameData.questions.length - 1 ? 'Finish Quiz' : 'Next Question';
            elements.nextBtn.disabled = !answers[index];
        }

        function renderOptions(options, questionIndex) {
            elements.optionsContainer.innerHTML = '';
            
            options.forEach((option, optionIndex) => {
                const button = document.createElement('button');
                button.className = `w-full text-left p-4 border-2 rounded-lg transition-colors hover:border-primary focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 ${
                    answers[questionIndex] === optionIndex ? 'border-primary bg-primary/5' : 'border-gray-200'
                }`;
                button.textContent = option;
                button.addEventListener('click', () => selectOption(questionIndex, optionIndex));
                
                elements.optionsContainer.appendChild(button);
            });
        }

        function selectOption(questionIndex, optionIndex) {
            answers[questionIndex] = optionIndex;
            renderOptions(gameData.questions[questionIndex].options, questionIndex);
            elements.nextBtn.disabled = false;
        }

        function navigateQuestion(direction) {
            const newIndex = currentQuestion + direction;
            
            if (newIndex >= 0 && newIndex < gameData.questions.length) {
                showQuestion(newIndex);
            } else if (newIndex >= gameData.questions.length) {
                finishQuiz();
            }
        }

        function finishQuiz() {
            // Calculate score
            score = 0;
            gameData.questions.forEach((question, index) => {
                if (answers[index] === question.correct) {
                    score += question.points;
                }
            });
            
            showResults();
        }

        function showResults() {
            elements.questionContainer.classList.add('hidden');
            elements.resultsScreen.classList.remove('hidden');
            elements.finalScore.textContent = score;
            elements.scoreDisplay.textContent = score;
            
            // Score message
            const percentage = (score / {{MAX_SCORE}}) * 100;
            let message = '';
            if (percentage >= 90) message = 'Excellent work! 🎉';
            else if (percentage >= 70) message = 'Great job! 👏';
            else if (percentage >= 50) message = 'Good effort! 👍';
            else message = 'Keep practicing! 💪';
            
            elements.scoreMessage.textContent = message;
            elements.scoreMessage.className = `mt-2 text-sm ${percentage >= 70 ? 'text-green-600' : 'text-orange-600'}`;
        }

        function resetGame() {
            currentQuestion = 0;
            score = 0;
            answers = [];
            elements.scoreDisplay.textContent = '0';
            elements.questionContainer.classList.remove('hidden');
            elements.resultsScreen.classList.add('hidden');
            showQuestion(0);
        }

        // Initialize Lucide icons and start game
        document.addEventListener('DOMContentLoaded', () => {
            lucide.createIcons();
            initGame();
        });
    </script>
</body>
</html>"""

# Drag and Match Template
DRAG_MATCH_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{GAME_TITLE}} - {{TOPIC}}</title>
    <script src="https://cdn.tailwindcss.com/3.4.0"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <link rel="stylesheet" href="../../styles/theme.css">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#7c3aed',
                        'primary-dark': '#5b21b6',
                        'primary-light': '#a855f7'
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-gradient-to-br from-purple-50 to-indigo-100 min-h-screen">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-purple-100">
        <div class="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
            <div>
                <h1 class="text-xl font-bold text-gray-900">{{GAME_TITLE}}</h1>
                <p class="text-sm text-gray-600">{{TOPIC}}</p>
            </div>
            <div class="flex items-center gap-4">
                <div class="bg-primary text-white px-3 py-1 rounded-full text-sm font-medium">
                    Score: <span id="score">0</span>/{{MAX_SCORE}}
                </div>
                <a href="../" class="text-primary hover:text-primary-dark font-medium">← Back to Topic</a>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-5xl mx-auto px-4 py-8">
        <div class="bg-white rounded-xl shadow-lg p-6">
            <!-- Instructions -->
            <div class="mb-6">
                <h2 class="text-lg font-medium text-gray-900 mb-2">Match the Terms</h2>
                <p class="text-gray-600">Drag items from the left column to match them with the correct definitions on the right.</p>
            </div>

            <!-- Game Area -->
            <div id="game-area" class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <!-- Terms Column -->
                <div class="space-y-3">
                    <h3 class="font-medium text-gray-900 mb-4">Terms</h3>
                    <div id="terms-container" class="space-y-3">
                        <!-- Terms will be inserted here -->
                    </div>
                </div>

                <!-- Definitions Column -->
                <div class="space-y-3">
                    <h3 class="font-medium text-gray-900 mb-4">Definitions</h3>
                    <div id="definitions-container" class="space-y-3">
                        <!-- Definitions will be inserted here -->
                    </div>
                </div>
            </div>

            <!-- Controls -->
            <div class="flex justify-between items-center mt-8">
                <button id="reset-btn" class="px-4 py-2 text-primary border border-primary rounded-lg hover:bg-primary hover:text-white transition-colors">
                    Reset
                </button>
                <button id="check-btn" class="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors">
                    Check Answers
                </button>
            </div>

            <!-- Results Screen (Hidden) -->
            <div id="results-screen" class="hidden text-center mt-8">
                <div class="mb-6">
                    <div class="w-24 h-24 mx-auto mb-4 rounded-full bg-primary flex items-center justify-center">
                        <i data-lucide="target" class="w-12 h-12 text-white"></i>
                    </div>
                    <h2 class="text-2xl font-bold text-gray-900 mb-2">Matching Complete!</h2>
                    <p class="text-gray-600">You scored <span id="final-score">0</span> out of {{MAX_SCORE}} points</p>
                    <div id="score-message" class="mt-2 text-sm"></div>
                </div>
                <div class="flex gap-4 justify-center">
                    <button id="retry-btn" class="px-6 py-2 border border-primary text-primary rounded-lg hover:bg-primary hover:text-white transition-colors">
                        Try Again
                    </button>
                    <a href="../" class="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors">
                        Back to Topic
                    </a>
                </div>
            </div>
        </div>
    </main>

    <script src="../../scripts/common.js"></script>
    <script>
        // Game Data
        const gameData = {{GAME_DATA}};
        
        // Game State
        let matches = {};
        let score = 0;
        let gameCompleted = false;

        // Initialize Game
        function initGame() {
            renderTerms();
            renderDefinitions();
            setupDragAndDrop();
            setupEventListeners();
            window.__GAME_OK__ = true;
        }

        function setupEventListeners() {
            document.getElementById('reset-btn').addEventListener('click', resetGame);
            document.getElementById('check-btn').addEventListener('click', checkAnswers);
            document.getElementById('retry-btn')?.addEventListener('click', resetGame);
        }

        function renderTerms() {
            const container = document.getElementById('terms-container');
            container.innerHTML = '';
            
            gameData.terms.forEach((term, index) => {
                const div = document.createElement('div');
                div.className = 'term-item p-4 bg-purple-50 border-2 border-purple-200 rounded-lg cursor-move hover:bg-purple-100 transition-colors';
                div.draggable = true;
                div.dataset.termId = index;
                div.textContent = term;
                container.appendChild(div);
            });
        }

        function renderDefinitions() {
            const container = document.getElementById('definitions-container');
            container.innerHTML = '';
            
            gameData.definitions.forEach((definition, index) => {
                const div = document.createElement('div');
                div.className = 'definition-item min-h-[60px] p-4 bg-gray-50 border-2 border-gray-200 rounded-lg border-dashed hover:border-primary transition-colors';
                div.dataset.definitionId = index;
                div.innerHTML = `<span class="text-gray-700">${definition}</span><div class="drop-zone mt-2 hidden"></div>`;
                container.appendChild(div);
            });
        }

        function setupDragAndDrop() {
            // Drag start
            document.addEventListener('dragstart', (e) => {
                if (e.target.classList.contains('term-item')) {
                    e.dataTransfer.setData('text/plain', e.target.dataset.termId);
                    e.target.style.opacity = '0.5';
                }
            });

            // Drag end
            document.addEventListener('dragend', (e) => {
                if (e.target.classList.contains('term-item')) {
                    e.target.style.opacity = '1';
                }
            });

            // Drag over
            document.addEventListener('dragover', (e) => {
                e.preventDefault();
                if (e.target.closest('.definition-item')) {
                    e.target.closest('.definition-item').classList.add('border-primary', 'bg-purple-50');
                }
            });

            // Drag leave
            document.addEventListener('dragleave', (e) => {
                if (e.target.closest('.definition-item')) {
                    e.target.closest('.definition-item').classList.remove('border-primary', 'bg-purple-50');
                }
            });

            // Drop
            document.addEventListener('drop', (e) => {
                e.preventDefault();
                const definitionItem = e.target.closest('.definition-item');
                if (definitionItem) {
                    const termId = e.dataTransfer.getData('text/plain');
                    const definitionId = definitionItem.dataset.definitionId;
                    
                    // Remove previous match for this definition
                    Object.keys(matches).forEach(key => {
                        if (matches[key] === parseInt(definitionId)) {
                            delete matches[key];
                        }
                    });
                    
                    // Add new match
                    matches[termId] = parseInt(definitionId);
                    
                    // Update visuals
                    updateMatchVisuals();
                    definitionItem.classList.remove('border-primary', 'bg-purple-50');
                }
            });
        }

        function updateMatchVisuals() {
            // Reset all items
            document.querySelectorAll('.term-item').forEach(item => {
                item.classList.remove('bg-green-100', 'border-green-300');
                item.classList.add('bg-purple-50', 'border-purple-200');
            });
            
            document.querySelectorAll('.definition-item').forEach(item => {
                item.classList.remove('bg-green-100', 'border-green-300');
                item.classList.add('bg-gray-50', 'border-gray-200');
            });

            // Highlight matched pairs
            Object.entries(matches).forEach(([termId, definitionId]) => {
                const termItem = document.querySelector(`[data-term-id="${termId}"]`);
                const definitionItem = document.querySelector(`[data-definition-id="${definitionId}"]`);
                
                if (termItem && definitionItem) {
                    termItem.classList.remove('bg-purple-50', 'border-purple-200');
                    termItem.classList.add('bg-green-100', 'border-green-300');
                    
                    definitionItem.classList.remove('bg-gray-50', 'border-gray-200');
                    definitionItem.classList.add('bg-green-100', 'border-green-300');
                }
            });
        }

        function checkAnswers() {
            if (gameCompleted) return;
            
            score = 0;
            const maxScore = {{MAX_SCORE}};
            const pointsPerMatch = maxScore / gameData.correctMatches.length;
            
            // Check each match
            Object.entries(matches).forEach(([termId, definitionId]) => {
                const correctDefinitionId = gameData.correctMatches[parseInt(termId)];
                if (definitionId === correctDefinitionId) {
                    score += pointsPerMatch;
                }
            });
            
            score = Math.round(score);
            document.getElementById('score').textContent = score;
            
            showResults();
            gameCompleted = true;
        }

        function showResults() {
            document.getElementById('game-area').style.display = 'none';
            document.querySelector('.flex.justify-between').style.display = 'none';
            document.getElementById('results-screen').classList.remove('hidden');
            document.getElementById('final-score').textContent = score;
            
            // Score message
            const percentage = (score / {{MAX_SCORE}}) * 100;
            let message = '';
            if (percentage >= 90) message = 'Perfect matching! 🎯';
            else if (percentage >= 70) message = 'Great matching! 👍';
            else if (percentage >= 50) message = 'Good effort! 🎪';
            else message = 'Keep practicing! 💪';
            
            const messageEl = document.getElementById('score-message');
            messageEl.textContent = message;
            messageEl.className = `mt-2 text-sm ${percentage >= 70 ? 'text-green-600' : 'text-orange-600'}`;
        }

        function resetGame() {
            matches = {};
            score = 0;
            gameCompleted = false;
            document.getElementById('score').textContent = '0';
            document.getElementById('game-area').style.display = 'grid';
            document.querySelector('.flex.justify-between').style.display = 'flex';
            document.getElementById('results-screen').classList.add('hidden');
            renderTerms();
            renderDefinitions();
        }

        // Initialize game on load
        document.addEventListener('DOMContentLoaded', () => {
            lucide.createIcons();
            initGame();
        });
    </script>
</body>
</html>"""

# Template Registry
GAME_TEMPLATES = {
    'quiz': QUICK_QUIZ_TEMPLATE,
    'drag-match': DRAG_MATCH_TEMPLATE,
    # Add more templates as needed
}

def get_template(template_type: str) -> str:
    """Get a game template by type"""
    return GAME_TEMPLATES.get(template_type, QUICK_QUIZ_TEMPLATE)