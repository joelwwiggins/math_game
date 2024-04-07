function startGame() {
    const playerName = document.getElementById('playerName').value;
    if (playerName.trim() === '') {
        alert('Please enter your name to start the game.');
        return;
    }
    document.getElementById('gameArea').style.display = 'block';
    generateQuestion();
}

let correctAnswer;

function generateQuestion() {
    const num1 = Math.floor(Math.random() * 10) + 1;
    const num2 = Math.floor(Math.random() * 10) + 1;
    correctAnswer = num1 + num2;
    document.getElementById('question').textContent = `${num1} + ${num2}`;
}

function submitAnswer() {
    const userAnswer = parseInt(document.getElementById('answer').value);
    if (userAnswer === correctAnswer) {
        document.getElementById('feedback').textContent = 'Correct! Here comes the next question.';
        generateQuestion();
    } else {
        document.getElementById('feedback').textContent = 'Wrong answer. Try again!';
    }
    document.getElementById('answer').value = ''; // Clear the input field for the next answer
}
