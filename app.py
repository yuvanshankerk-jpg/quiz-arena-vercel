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
        body { background-color: #ffffff; color: #000000; font-family: 'Courier New', Courier, monospace; }
        .brutalist-border { border: 4px solid #000; box-shadow: 8px 8px 0px #000; }
        .brutalist-btn { 
            border: 4px solid #000; box-shadow: 4px 4px 0px #000; 
            background-color: #facc15; font-weight: 900; text-transform: uppercase;
            transition: all 0.1s ease; cursor: pointer;
        }
        .brutalist-btn:active { box-shadow: 0px 0px 0px #000; transform: translate(4px, 4px); }
    </style>
</head>
<body class="p-8 flex flex-col items-center justify-center min-h-screen">
    <div id="app" class="w-full max-w-2xl"></div>

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
                    <div class="brutalist-border p-8 bg-white mb-8">
                        <h1 class="text-4xl font-black uppercase tracking-tighter mb-2">Vybe 2K26</h1>
                        <h2 class="text-2xl font-bold uppercase border-b-4 border-black pb-4 mb-4">Quiz Arena</h2>
                        <input type="text" id="teamName" placeholder="ENTER TEAM NAME" class="w-full border-4 border-black p-4 mb-4 text-xl outline-none focus:bg-gray-100">
                        <button onclick="startQuiz()" class="brutalist-btn w-full p-4 text-xl">Start // Register Team</button>
                    </div>
                `;
            } else if (currentStep === 'choose_difficulty') {
                appDiv.innerHTML = `
                    <div class="brutalist-border p-8 bg-white mb-8">
                        <h2 class="text-2xl font-black uppercase mb-6">Select Difficulty</h2>
                        <div class="grid grid-cols-1 gap-4">
                            <button onclick="fetchQuestions('easy')" class="brutalist-btn p-4 text-lg bg-green-400">Easy (5 Pts)</button>
                            <button onclick="fetchQuestions('moderate')" class="brutalist-btn p-4 text-lg bg-yellow-400">Moderate (10 Pts)</button>
                            <button onclick="fetchQuestions('difficult')" class="brutalist-btn p-4 text-lg bg-red-400">Difficult (15 Pts)</button>
                        </div>
                    </div>
                `;
            } else if (currentStep === 'quiz') {
                const q = questions[currentQIndex];
                let optionsHtml = q.options.map(opt => `
                    <label class="block border-4 border-black p-4 mb-4 cursor-pointer hover:bg-gray-100 font-bold">
                        <input type="radio" name="answer" value="${opt}" class="mr-2"> ${opt}
                    </label>
                `).join('');

                appDiv.innerHTML = `
                    <div class="brutalist-border p-8 bg-white mb-8">
                        <div class="flex justify-between items-center border-b-4 border-black pb-4 mb-4">
                            <h2 class="text-xl font-black">QUESTION ${currentQIndex + 1}/${questions.length}</h2>
                            <span class="text-xl font-black bg-black text-white px-2 py-1">PTS: ${q.marks}</span>
                        </div>
                        <pre class="bg-gray-100 border-4 border-black p-4 mb-6 font-mono font-bold text-lg whitespace-pre-wrap">${q.question}</pre>
                        ${optionsHtml}
                        <button onclick="submitAnswer()" class="brutalist-btn w-full p-4 text-xl mt-4">Submit // Lock In</button>
                    </div>
                `;
            } else if (currentStep === 'game_over') {
                appDiv.innerHTML = `
                    <div class="brutalist-border p-8 bg-white text-center">
                        <h1 class="text-5xl font-black uppercase mb-4">Run Over</h1>
                        <div class="text-3xl font-bold border-4 border-black p-4 mb-6 bg-black text-white">FINAL SCORE: ${score}</div>
                        <button onclick="location.reload()" class="brutalist-btn w-full p-4 text-xl">New Team // Reset</button>
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
            if (!selected) return alert("Select an answer!");
            
            if (selected.value === questions[currentQIndex].answer) {
                score += questions[currentQIndex].marks;
                currentQIndex++;
                if (currentQIndex >= questions.length) currentStep = 'game_over';
            } else {
                currentStep = 'game_over'; 
            }
            render();
        }

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

# Only run this locally; Vercel handles serving differently
if __name__ == '__main__':
    app.run(debug=True)
