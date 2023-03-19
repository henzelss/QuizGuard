const startButton = document.getElementById('start-btn')
const nextButton = document.getElementById('next-btn')
const questionContainerElement = document.getElementById('question-container')
const questionElement = document.getElementById('question')
const answerButtonsElement = document.getElementById('answer-buttons')

let shuffledQuestions, currentQuestionIndex

startButton.addEventListener('click', startGame)
nextButton.addEventListener('click', () => {
  currentQuestionIndex++
  setNextQuestion()
})

function startGame() {
  startButton.classList.add('hide')
  shuffledQuestions = questions.sort(() => Math.random() - .5)
  currentQuestionIndex = 0
  questionContainerElement.classList.remove('hide')
  setNextQuestion()
}

function setNextQuestion() {
  resetState()
  showQuestion(shuffledQuestions[currentQuestionIndex])
}

function showQuestion(question) {
  questionElement.innerText = question.question
  question.answers.forEach(answer => {
    const button = document.createElement('button')
    button.innerText = answer.text
    button.classList.add('btn')
    if (answer.correct) {
      button.dataset.correct = answer.correct
    }
    button.addEventListener('click', selectAnswer)
    answerButtonsElement.appendChild(button)
  })
}

function resetState() {
  clearStatusClass(document.body)
  nextButton.classList.add('hide')
  while (answerButtonsElement.firstChild) {
    answerButtonsElement.removeChild(answerButtonsElement.firstChild)
  }
}

function selectAnswer(e) {
  const selectedButton = e.target
  const correct = selectedButton.dataset.correct
  setStatusClass(document.body, correct)
  Array.from(answerButtonsElement.children).forEach(button => {
    setStatusClass(button, button.dataset.correct)
  })
  if (shuffledQuestions.length > currentQuestionIndex + 1) {
    nextButton.classList.remove('hide')
  } else {
    startButton.innerText = 'Restart'
    startButton.classList.remove('hide')
  }
}

function setStatusClass(element, correct) {
  clearStatusClass(element)
  if (correct) {
    element.classList.add('correct')
  } else {
    element.classList.add('wrong')
  }
}

function clearStatusClass(element) {
  element.classList.remove('correct')
  element.classList.remove('wrong')
}

const questions = [
  {
    question: 'What year did the Titanic sink in the Atlantic Ocean on 15 April, on its maiden voyage from Southampton?',
    answers: [
      { text: '1913', correct: false },
      { text: '1914', correct: false },
      { text: '1915', correct: false },
      { text: '1912', correct: true }
    ]
  },
  {
    question: 'What is the title of the first ever Carry On film made and released in 1958?',
    answers: [
      { text: 'Carry on Commander', correct: false },
      { text: 'Carry on Lieutinenant', correct: false },
      { text: 'Carry on Private', correct: false },
      { text: 'Carry on Sergeant', correct: true }
    ]
  },
  {
    question: 'What year did the Titanic sink in the Atlantic Ocean on 15 April, on its maiden voyage from Southampton?',
    answers: [
      { text: '1913', correct: false },
      { text: '1914', correct: false },
      { text: '1915', correct: false },
      { text: '1912', correct: true }
    ]
  },
  {
    question: 'What is the name of the biggest technology company in South Korea?',
    answers: [
      { text: 'Toshiba', correct: false },
      { text: 'Sony', correct: false },
      { text: 'Samsung', correct: true },
      { text: 'Huawei', correct: false }
    ]
  },
  {
    question: 'What is the capital of Portugal?',
    answers: [
      { text: 'Lisbon', correct: true },
      { text: 'Belfast ', correct: false },
      { text: 'Belgrade', correct: false },
      { text: 'Barcelona', correct: false }
    ]
  },
  {
    question: 'What is the chemical symbol for silver?',
    answers: [
      { text: 'Si', correct: false },
      { text: 'Ag', correct: true },
      { text: 'Sr', correct: false },
      { text: 'Au', correct: false }
    ]
  },
  {
    question: 'What is the world’s smallest bird?',
    answers: [
      { text: 'House Sparrow', correct: false },
      { text: 'Bee Hummingbird', correct: true },
      { text: 'House Finch', correct: false },
      { text: 'Chipping Sparrow', correct: false }
    ]
  }
]