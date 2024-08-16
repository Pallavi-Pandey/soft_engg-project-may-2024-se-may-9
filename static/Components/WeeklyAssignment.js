// ParentComponent.js
import QuestionComponent from './QuestionComponent.js';

export default {
  components: {
    QuestionComponent
  },
  props: {
    courseId: {
      type: Number,
      default: 1
    },
    weekId: {
      type: Number,
      default: 2
    },
    content: {
      type: Object
    },
  },
  data() {
    return {
      questions: [],
      errorMessage: '',
<<<<<<< HEAD
      answers:[]
=======
      answers: {},
      checkFlag: false,
      marksObtained: 0,
      totalMarks:0
>>>>>>> 53bcc9e509dbf7ddb71ea0d500b41cccb87ad122
    };
  },
  methods: {
    async fetchAssignmentData() {
      try {
        const response = await fetch(`/api/course_assignment/1/${this.weekId}/${this.content.id}`, {
          method: 'GET',
          headers: {
            'Authentication-Token': localStorage.getItem('authToken')
          }
        });
        if (!response.ok) {
          throw new Error('Failed to fetch assignment data');
        }
        const data = await response.json();
        console.log(data);
        this.questions = data[this.content.title]; // Adjust based on the actual response structure.
        this.answers = {}
        for (let question of this.questions) {
          let questionId = question.question_id
          this.answers[questionId] = 0;
        }
      } catch (error) {
        console.log(error)
        this.errorMessage = error.message;
      }
    },
    async fetchAssignmentAnswersData() {
      try {
        const response = await fetch(`/api/answers/1/${this.weekId}/${this.content.id}`, {
          method: 'GET',
          headers: {
            'Authentication-Token': localStorage.getItem('authToken')
          }
        });
        if (!response.ok) {
          console.log('Failed to fetch assignment data');
        }
        const data = await response.json();
        console.log(data);
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
    handleAnswerSelected({ question_id, option_id, option_text }) {
      // Handle the selected answer here (e.g., store it or send it to the server)
      console.log(`Question ID: ${question_id}, Selected Option ID: ${option_id}`);
<<<<<<< HEAD
      this.answers.push({question_id, option_id})
    },
    async submitAssignmentAnswers() {
      try {
        console.log(this.answers); // Log the payload for debugging
    
        const response = await fetch(`/api/course_assignment/${this.courseId}/${this.weekId}/${this.assignmentId}`, {
=======
      this.answers[question_id] = {
        option_id: option_id,
        option_text: option_text
      }
    },
    checkAnswers() {
      this.checkFlag = false
      this.checkFlag = true
      this.marksObtained = 0
      this.totalMarks = 0
      for( let question of this.questions) {
        if (question.answer == this.answers[question.question_id].option_text) {
          this.marksObtained += question.question_score
        }
        this.totalMarks += question.question_score
      }
    },
    async submitAssignmentAnswers() {
      try {
        // Prepare the payload
        console.log(this.answers, "answers")
        const answersArray = Object.keys(this.answers).map(question_id => ({
          question_id,
          option_id: this.answers[question_id].option_id
        }));
        console.log(answersArray, "answersArray")

        const response = await fetch(`/api/course_assignment/${this.weekId}/${this.content.id}`, {
>>>>>>> 53bcc9e509dbf7ddb71ea0d500b41cccb87ad122
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('authToken') // Ensure the token is included
          },
          body: JSON.stringify(this.answers) // Sending the array of answers directly
        });
<<<<<<< HEAD
    
        // Check if the response is not ok
=======

>>>>>>> 53bcc9e509dbf7ddb71ea0d500b41cccb87ad122
        if (!response.ok) {
          // Attempt to parse error response as JSON
          let errorMessage = 'Unknown error';
          try {
            const errorData = await response.json();
            errorMessage = errorData.ErrorMsg || 'Failed to submit assignment answers';
          } catch (jsonError) {
            // If JSON parsing fails, read raw response text
            errorMessage = await response.text();
          }
          throw new Error(errorMessage);
        }
<<<<<<< HEAD
    
        // Parse the success response
=======

>>>>>>> 53bcc9e509dbf7ddb71ea0d500b41cccb87ad122
        const result = await response.json();
        this.successMessage = result.message || 'Assignment submitted successfully!'; // Capture success message
        console.log('Assignment submitted:', result);
<<<<<<< HEAD
    
        // Optionally clear the answers or redirect the user after submission
        this.answers = [];
=======

        // Optionally clear the answers or redirect the user
        this.answers = {};
>>>>>>> 53bcc9e509dbf7ddb71ea0d500b41cccb87ad122
      } catch (error) {
        this.errorMessage = error.message; // Handle and display error message
        console.error('Error submitting assignment:', error); // Log the full error for debugging
      }
    }
    
    
    

  },
  created() {
    this.fetchAssignmentData();
    this.fetchAssignmentAnswersData();
  },
  template: `
    <div>
      <h3>{{ this.content.title }}</h3>
      <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
      <div v-for="(question, index) in questions" :key="question.question_id">
        <QuestionComponent 
          :question="question" 
          :index="index" 
          :checkFlag="checkFlag"
          @answer-selected="handleAnswerSelected" 
        />
        <div v-if="checkFlag">
          <span v-if="question.answer != answers[question.question_id].option_text" style="color: red;">Answer: {{question.answer}}</span>
          <span v-if="question.answer == answers[question.question_id].option_text" style="color: green;">Answer: {{question.answer}}</span>
        </div>
        </br>
      </div>
<<<<<<< HEAD
      <button @click="submitAssignmentAnswers" class="btn btn-primary mt-3">Submit Answers</button>
      <br>
=======
      <div v-if="checkFlag">
      <span> Score: {{ marksObtained }} / {{ totalMarks }} </span>
      </div>
      <button v-if="this.content.type == 'graded_assignment_content_type'" @click="submitAssignmentAnswers()" class="btn btn-primary mt-3">Submit Answers</button>
      <button v-if="this.content.type == 'assignment_content_type'" @click="checkAnswers()" class="btn btn-primary mt-3">Check Answers</button>
      </br>
>>>>>>> 53bcc9e509dbf7ddb71ea0d500b41cccb87ad122
    </div>
  `
};
