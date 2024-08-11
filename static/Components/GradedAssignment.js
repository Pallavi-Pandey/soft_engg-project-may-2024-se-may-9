import GradedAssignmentQuestions from './GradedAssignmentQuestions.js';

export default {
  components: {
    GradedAssignmentQuestions
  },
  props: {
    courseId: {
      type: Number,
      required: true
    },
    weekId: {
      type: Number,
      required: true
    },
    assignmentId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      assignmentTitle: '',
      questions: [],
      deadline: null,
      answers: [],
      errorMessage: ''
    };
  },
  methods: {
    async fetchAssignmentData() {
      try {
        const response = await fetch(`/course_assignment/${this.courseId}/${this.weekId}/${this.assignmentId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch assignment data');
        }
        const data = await response.json();
        this.assignmentTitle = Object.keys(data)[0];
        this.questions = data[this.assignmentTitle];
        if (this.questions.length > 0 && this.questions[0].deadline) {
          this.deadline = new Date(this.questions[0].deadline);
        }
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
    updateAnswer(answer) {
        const index = this.answers.findIndex(a => a.question_id === answer.question_id);
        if (index !== -1) {
            this.answers[index] = answer;
        } else {
            this.answers.push(answer);
        }
    },
    async submitAssignment() {
        try {
            const response = await fetch(`/course_assignment/${this.courseId}/${this.weekId}/${this.assignmentId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.answers)
            });
            if (!response.ok) {
                throw new Error('Failed to submit assignment');
            }
            const result = await response.json();
            alert(result.message);
        } catch (error) {
            this.errorMessage = error.message;
        }
    }
  },
  mounted() {
    this.fetchAssignmentData();
  },
  template: `
    <div class="graded-assignment">
      <h2>{{ assignmentTitle }}</h2>
      <p v-if="deadline">Due date: {{ deadline.toLocaleString() }}</p>
      <p>You may submit any number of times before the due date. The final submission will be considered for grading.</p>
      
      <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
      
      <div v-for="(question, index) in questions" :key="question.question_id">
        <GradedAssignmentQuestions 
          :question="question" 
          :index="index"
          @answer-selected="updateAnswer"
        />
      </div>
      
      <button @click="submitAssignment" class="btn btn-primary mt-3">Submit Assignment</button>
    </div>
  `
};