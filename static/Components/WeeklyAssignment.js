import QuestionComponent from './QuestionComponent.js';

export default {
  components: {
    QuestionComponent,
  },
  props: {
    courseId: {
      type: Number,
      default: 1, // Default value for courseId
    },
    weekId: {
      type: Number,
      default: 2, // Default value for weekId
    },
    assignmentId: {
      type: Number,
      default: 16, // Default value for assignmentId
    },
  },
  data() {
    return {
      questions: [],
      errorMessage: '',
    };
  },
  methods: {
    async fetchAssignmentData() {
      try {
        const response = await fetch(`/course_assignment/${this.courseId}/${this.weekId}/${this.assignmentId}`,{
          method: 'GET',
          headers: {
            'Authentication-Token' : localStorage.getItem('authToken')
          }
        });
        if (!response.ok) {
          throw new Error('Failed to fetch assignment data');
        }
        const data = await response.json();
        this.questions = data;
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
    handleAnswerSelected({ question_id, option_id }) {
      // Handle the selected answer here (e.g., store it or send it to the server)
      console.log(`Question ID: ${question_id}, Selected Option ID: ${option_id}`);
    },
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
    </div>
  `,
};
