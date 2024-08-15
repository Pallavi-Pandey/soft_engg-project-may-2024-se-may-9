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
    assignmentId: {
      type: Number,
      default: 16
    }
  },
  data() {
    return {
      questions: [],
      errorMessage: ''
    };
  },
  methods: {
    async fetchAssignmentData() {
      try {
        const response = await fetch(`/api/course_assignment/${this.courseId}/${this.weekId}/${this.assignmentId}`, {
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
        this.questions = data['Graded Assignment 1']; // Adjust based on the actual response structure
      } catch (error) {
        console.log(error)
        this.errorMessage = error.message;
      }
    },
    handleAnswerSelected({ question_id, option_id }) {
      // Handle the selected answer here (e.g., store it or send it to the server)
      console.log(`Question ID: ${question_id}, Selected Option ID: ${option_id}`);
    },
    async submitAssignmentAnswers() {
      try {
        // Prepare the payload
        const answersArray = Object.keys(this.answers).map(question_id => ({
          question_id,
          option_id: this.answers[question_id]
        }));
        console.log(answersArray)
        const response = await fetch(`/api/course_assignment/${this.weekId}/${this.assignmentId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('authToken')
          },
          body: JSON.stringify({ answers: answersArray })
        });
        
        if (!response.ok) {
          throw new Error('Failed to submit assignment answers');
        }
        
        const result = await response.json();
        this.successMessage = result; // Success message from the API
        console.log('Assignment submitted:', result);
        
        // Optionally clear the answers or redirect the user
        this.answers = {};
      } catch (error) {
        this.errorMessage = error.message;
      }
    }

  },
  mounted() {
    this.fetchAssignmentData();
  },
  template: `
    <div>
      <h3>Weekly Assignment</h3>
      <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
      <div v-for="(question, index) in questions" :key="question.question_id">
        <QuestionComponent 
          :question="question" 
          :index="index" 
          @answer-selected="handleAnswerSelected" 
        />
      </div>
      <button @click="submitAssignmentAnswers" class="btn btn-primary mt-3">Submit Answers</button>
      <br>
    </div>
  `
};
