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
      errorMessage: '',
      answers:[]
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
      this.answers.push({question_id, option_id})
    },
    async submitAssignmentAnswers() {
      try {
        console.log(this.answers); // Log the payload for debugging
    
        const response = await fetch(`/api/course_assignment/${this.courseId}/${this.weekId}/${this.assignmentId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('authToken') // Ensure the token is included
          },
          body: JSON.stringify(this.answers) // Sending the array of answers directly
        });
    
        // Check if the response is not ok
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
    
        // Parse the success response
        const result = await response.json();
        this.successMessage = result.message || 'Assignment submitted successfully!'; // Capture success message
        console.log('Assignment submitted:', result);
    
        // Optionally clear the answers or redirect the user after submission
        this.answers = [];
      } catch (error) {
        this.errorMessage = error.message; // Handle and display error message
        console.error('Error submitting assignment:', error); // Log the full error for debugging
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
