from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# --- SECURE QUESTION BANK ---
QUESTIONS = {
    "easy": [
        {
            "id": 1,
            "question": "x = 10\ny = 3\nprint(x // y)\nprint(x % y)",
            "options": ["3, 1", "3.33, 1", "3, 0", "4, 1"],
            "answer": "3, 1",
            "marks": 5
        }
    ],
    "moderate": [
        {
            "id": 11,
            "question": "What is the output?\nx = 5\nfor i in range(1, 4):\n    x = x + i\nprint(x)",
            "options": ["8", "11", "14", "15"],
            "answer": "11",
            "marks": 10
        }
    ],
    "difficult": [
        {
            "id": 21,
            "question": "Given [3, 4, -1, 1, 2, 6], find the subarray with sum 9.",
            "options": ["[3, 4, 2]", "[4, -1, 1, 2, 3]", "[3, 6]", "[4, -1, 1, 2, 3] and [3, 6]"],
            "answer": "[3, 6]",
            "marks": 15
        }
    ]
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz Arena - Vybe 2K26</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Neo-Brutalist Color Palette & Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');
        
        :root {
            --bg-color: #f4f4f0;
            --main-black: #0f0f0f;
            --brand-yellow: #facc15;
            --brand-cyan: #22d3ee;
            --brand-pink: #f472b6;
        }

        body { 
            background-color: var(--bg-color); 
            color: var(--main-black); 
            font-family: 'Space Grotesk', sans-serif;
            overflow-x: hidden;
            /* Animated Grid Pattern */
            background-image: 
                linear-gradient(to right, #00000015 2px, transparent 2px),
                linear-gradient(to bottom, #00000015 2px, transparent 2px);
            background-size: 40px 40px;
            background-position: center;
        }

        /* Scrolling Marquee */
        .marquee-container {
            width: 100vw;
            background: var(--main-black);
            color: white;
            white-space: nowrap;
            overflow: hidden;
            border-bottom: 4px solid var(--main-black);
            position: fixed;
            top: 0;
            left: 0;
            z-index: 50;
            padding: 8px 0;
            box-shadow: 0 4px 0px var(--brand-pink);
        }
        .marquee-content {
            display: inline-block;
            font-weight: 900;
            text-transform: uppercase;
            font-size: 1.2rem;
            animation: scroll 15s linear infinite;
        }
        @keyframes scroll {
            0% { transform: translateX(100vw); }
            100% { transform: translateX(-100%); }
        }

        /* Floating CSS Graphics */
        .shape {
            position: fixed;
            z-index: -1;
            border: 4px solid var(--main-black);
            box-shadow: 4px 4px 0px var(--main-black);
        }
        .shape-circle {
            width: 100px; height: 100px;
            border-radius: 50%;
            background: var(--brand-cyan);
            top: 15%; left: 10%;
            animation: float 6s ease-in-out infinite;
        }
        .shape-square {
            width: 80px; height: 80px;
            background: var(--brand-pink);
            bottom: 20%; right: 10%;
            animation: spin 10s linear infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        @keyframes spin {
            100% { transform: rotate(360deg); }
        }

        /* UI Components */
        .brutalist-card {
            border: 4px solid var(--main-black);
            box-shadow: 12px 12px 0px var(--main-black);
            background: white;
            transition: transform 0.2s;
            position: relative;
            z-index: 10;
        }
        
        .brutalist-btn { 
            border: 4px solid var(--main-black); 
            box-shadow: 6px 6px 0px var(--main-black); 
            background-color: var(--brand-yellow); 
            font-weight: 900; 
            text-transform: uppercase;
            transition: all 0.15s ease; 
            cursor: pointer;
            font-family: 'Space Grotesk', sans-serif;
        }
        .brutalist-btn:hover {
            background-color: var(--brand-cyan);
            transform: translate(-2px, -2px);
            box-shadow: 8px 8px 0px var(--main-black);
        }
        .brutalist-btn:active { 
            box-shadow: 0px 0px 0px var(--main-black); 
            transform: translate(6px, 6px); 
        }

        .option-label {
            border: 4px solid var(--main-black);
            transition: all 0.2s;
        }
        .option-label:hover {
            background-color: var(--brand-pink);
            color: white;
            transform: translateX(10px);
            box-shadow: -4px 4px 0px var(--main-black);
        }
        input[type="radio"]:checked + span {
            background-color: var(--brand-yellow);
            color: black;
            display: inline-block;
            width: 100%;
        }

        .code-block {
            font-family: 'Space Mono', monospace;
            background: #e5e5e5;
            border: 4px solid var(--main-black);
            box-shadow: inset 4px 4px 0px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body class="p-8 flex flex-col items-center justify-center min-h-screen pt-24">

    <!-- Marquee Banner -->
    <div class="marquee-container">
        <div class="marquee-content">
            🔥 VYBE 2K26 INTER-COLLEGIATE FEST 🔥 KLE SOCIETY'S DEGREE COLLEGE NAGARBHAVI 🔥 QUIZ ARENA 🔥
        </div>
    </div>

    <!-- Floating Background Shapes -->
    <div class="shape shape-circle"></div>
    <div class="shape shape-square"></div>

    <div id="app" class="w-full max-w-2xl relative z-10"></div>

    <script>
        let currentStep = 'team_entry';
        let difficulty = '';
        let questions = [];
        let currentQIndex = 0;
        let score = 0;

        const appDiv = document.getElementById('app');

        function render() {
            if (currentStep === 'team_entry') {
                appDiv.innerHTML = `
                    <div class="brutalist-card p-8 mb-8 text-center">
                        <div class="flex flex-col sm:flex-row justify-center items-center gap-8 mb-8 border-b-4 border-black pb-8">
                            <img src="https://raw.githubusercontent.com/yuvanshankerk-jpg/quiz-arena-vercel/main/kle_logo.png" alt="KLE Logo" class="h-20 object-contain hover:scale-110 transition-transform">
                            <h1 class="text-4xl font-black">X</h1>
                            <img src="https://raw.githubusercontent.com/yuvanshankerk-jpg/quiz-arena-vercel/main/vybe_logo.png" alt="Vybe Logo" class="h-16 object-contain hover:scale-110 transition-transform">
                        </div>
                        <h2 class="text-5xl font-black uppercase mb-2 tracking-tighter" style="text-shadow: 2px 2px 0px var(--brand-cyan);">Quiz Arena</h2>
                        <p class="mb-8 font-bold text-gray-600 uppercase">Offline Kiosk Console</p>
                        
                        <div class="relative mb-6">
                            <input type="text" id="teamName" placeholder="ENTER TEAM NAME" class="w-full border-4 border-black p-4 text-2xl outline-none focus:bg-yellow-50 font-bold uppercase transition-colors">
                        </div>
                        
                        <button onclick="startQuiz()" class="brutalist-btn w-full p-4 text-2xl">Start // Register</button>
                    </div>
                `;
            } else if (currentStep === 'choose_difficulty') {
                appDiv.innerHTML = `
                    <div class="brutalist-card p-8 mb-8">
                        <h2 class="text-3xl font-black uppercase mb-8 text-center" style="text-shadow: 2px 2px 0px var(--brand-pink);">Select Difficulty</h2>
                        <div class="grid grid-cols-1 gap-6">
                            <button onclick="fetchQuestions('easy')" class="brutalist-btn p-6 text-2xl bg-green-400 hover:!bg-green-300">Level 1: Easy (5 Pts)</button>
                            <button onclick="fetchQuestions('moderate')" class="brutalist-btn p-6 text-2xl bg-yellow-400 hover:!bg-yellow-300">Level 2: Moderate (10 Pts)</button>
                            <button onclick="fetchQuestions('difficult')" class="brutalist-btn p-6 text-2xl bg-red-400 hover:!bg-red-300 text-white hover:!text-black">Level 3: Difficult (15 Pts)</button>
                        </div>
                    </div>
                `;
            } else if (currentStep === 'quiz') {
                const q = questions[currentQIndex];
                let optionsHtml = q.options.map((opt, index) => `
                    <label class="option-label block p-4 mb-4 cursor-pointer font-bold text-lg bg-white relative overflow-hidden group">
                        <input type="radio" name="answer" value="${opt}" class="absolute opacity-0">
                        <span class="block relative z-10 transition-colors group-hover:text-white p-2">
                           <span class="border-2 border-black rounded-full px-2 py-1 mr-2 text-sm">${String.fromCharCode(65 + index)}</span> ${opt}
                        </span>
                    </label>
                `).join('');

                appDiv.innerHTML = `
                    <div class="brutalist-card p-8 mb-8">
                        <div class="flex justify-between items-center border-b-4 border-black pb-4 mb-6">
                            <h2 class="text-2xl font-black">Q${currentQIndex + 1} <span class="text-gray-400 text-lg">/ ${questions.length}</span></h2>
                            <span class="text-xl font-black border-4 border-black px-3 py-1 bg-brand-cyan shadow-[2px_2px_0px_#000]">${q.marks} PTS</span>
                        </div>
                        <pre class="code-block p-6 mb-8 text-lg whitespace-pre-wrap">${q.question}</pre>
                        
                        <div class="space-y-4 mb-8">
                            ${optionsHtml}
                        </div>
                        
                        <button onclick="submitAnswer()" class="brutalist-btn w-full p-5 text-2xl">Lock In Answer</button>
                    </div>
                `;
            } else if (currentStep === 'game_over') {
                appDiv.innerHTML = `
                    <div class="brutalist-card p-10 text-center">
                        <h1 class="text-6xl font-black uppercase mb-2 text-red-500" style="text-shadow: 4px 4px 0px #000;">Run Over</h1>
                        <p class="font-bold text-xl mb-8 uppercase">Session Terminated</p>
                        
                        <div class="border-4 border-black p-8 mb-8 bg-black text-white transform rotate-2">
                            <p class="text-2xl font-bold mb-2">FINAL SCORE</p>
                            <div class="text-7xl font-black text-brand-yellow">${score}</div>
                        </div>
                        
                        <button onclick="location.reload()" class="brutalist-btn w-full p-5 text-2xl">New Team // Reset Kiosk</button>
                    </div>
                `;
            }
        }

        function startQuiz() {
            if(document.getElementById('teamName').value.trim() !== '') {
                currentStep = 'choose_difficulty';
                render();
            } else {
                alert('Enter a team name!');
            }
        }

        async function fetchQuestions(level) {
            const response = await fetch('/api/questions/' + level);
            questions = await response.json();
            currentStep = 'quiz';
            render();
        }

        function submitAnswer() {
            const selected = document.querySelector('input[name="answer"]:checked');
            if (!selected) return alert("Select an answer before locking in!");
            
            if (selected.value === questions[currentQIndex].answer) {
                score += questions[currentQIndex].marks;
                currentQIndex++;
                if (currentQIndex >= questions.length) currentStep = 'game_over';
            } else {
                currentStep = 'game_over'; 
            }
            render();
        }

        // Add highlight effect when clicking radio buttons
        document.addEventListener('change', function(e) {
            if(e.target.name === 'answer') {
                document.querySelectorAll('.option-label').forEach(el => {
                    el.style.backgroundColor = 'white';
                    el.style.color = 'black';
                });
                const parent = e.target.closest('.option-label');
                parent.style.backgroundColor = 'var(--brand-yellow)';
                parent.style.color = 'black';
            }
        });

        render();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/questions/<level>')
def get_questions(level):
    return jsonify(QUESTIONS.get(level, []))

if __name__ == '__main__':
    app.run(debug=True)
