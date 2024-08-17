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
      answers: {},
      checkFlag: false,
      marksObtained: 0,
      totalMarks:0,
      successMessage: "",
      isSubmitted: false,
      loading: false, // To track if questions are being generated
      questionsGenerated: false, // To check if questions have been generated
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
        console.log("This datsa",data);
        this.questions = data[this.content.title].map(question => {
          const matchedOption = question.options.find(option => option.option_text === question.answer);
          return {
            ...question,
            answer_id: matchedOption ? matchedOption.option_id : null // Handle cases where no match is found
          };
        });
        this.answers = {}
        for (let question of this.questions) {
          let questionId = question.question_id
          this.answers[questionId] = {
            option_id: null
          };
        }
        this.marksObtained =  data.assingment_score;
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
        else{
          this.isSubmitted = true;
          const data = await response.json();
          console.log("Fetched Data:", data); // Log the fetched data to verify
      
          // Store the score if available
          if (data.assingment_score) {
            console.log("Assignment Score:", data.assingment_score); // Log the score
            this.marksObtained = data.assingment_score;
          }
      
          this.answers = {};
          data?.["Student Marked Answers"].forEach((answer) => {
            let dataObj = {
              question_id: answer.question_id,
              option_id: answer.marked_option_id,
            };
            this.handleAnswerSelected(dataObj);
          });
          console.log(this.answers, "answers");
        }
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
    
    handleAnswerSelected({ question_id, option_id }) {
      // Handle the selected answer here (e.g., store it or send it to the server)
      console.log(`Question ID: ${question_id}, Selected Option ID: ${option_id}`);
      this.answers[question_id] = {
        option_id: option_id,
      }
      console.log(this.answers)
    },
    checkAnswers() {
      this.checkFlag = true
      this.marksObtained = 0
      this.totalMarks = 0
      for( let question of this.questions) {
        if (question.answer_id == this.answers[question.question_id]?.option_id) {
          this.marksObtained += question.question_score
        }
        this.totalMarks += question.question_score
      }
      
    },
    async submitAssignmentAnswers() {
      try {
        // Prepare the payload as an array of objects
        const answersArray = Object.keys(this.answers).map(question_id => ({
          question_id: parseInt(question_id), // Convert question_id to an integer
          option_id: this.answers[question_id].option_id
        }));
    
        console.log(answersArray, "answersArray");
    
        const response = await fetch(`/api/course_assignment/1/${this.weekId}/${this.content.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('authToken') // Ensure the token is included
          },
          body: JSON.stringify(answersArray) // Sending the array of answers
        });
    
        if (!response.ok) {
          // Attempt to parse error response as JSON
          let errorMessage = 'Unknown error';
          try {
            const errorData = await response.json();
            errorMessage = errorData.message || 'Failed to submit assignment answers';
          } catch (jsonError) {
            // If JSON parsing fails, read raw response text
            errorMessage = await response.text();
          }
          throw new Error(errorMessage);
        }
    
        const result = await response.json();
        this.successMessage = result.message || 'Assignment submitted successfully!'; // Capture success message
        console.log('Assignment submitted:', result);
    
        // Optionally clear the answers or redirect the user
        this.answers = {};
      } catch (error) {
        this.errorMessage = error.message; // Handle and display error message
        console.error('Error submitting assignment:', error); // Log the full error for debugging
      }
    },
    async generateMockAssignmentQuestions(courseId, weekId, assignmentType) {
      this.loading = true;
      this.questionsGenerated = false;
      try {
        const response = await fetch(`/mock_assignment/${courseId}/${weekId}/${assignmentType}`, {
          method: 'GET',
          headers: {
            'Authentication-Token': localStorage.getItem('authToken')
          }
        });

        if (!response.ok) {
          throw new Error('Failed to generate mock assignment questions');
        }

        const mockQuestions = await response.json();
        console.log('Generated Mock Questions:', mockQuestions);

        // Process the mock questions to be used in your QuestionComponent
        this.questions = mockQuestions.map((question, index) => ({
          question_id: index + 1, // Assign a unique question ID
          question_text: question.question_text,
          options: question.options.map((option, idx) => ({
            option_id: idx + 1, // Assign a unique option ID
            option_text: option
          })),
          answer_id: null // Placeholder for the correct answer, if needed
        }));

        // Initialize answers object
        this.answers = {};
        this.questions.forEach(question => {
          this.answers[question.question_id] = {
            option_id: null
          };
        });

        console.log('Questions processed for display:', this.questions);

        this.questionsGenerated = true; // Questions have been generated
      } catch (error) {
        this.errorMessage = error.message;
        console.error('Error generating mock assignment questions:', error);
      } finally {
        this.loading = false;
      }
    }
    ,
    async onLoadData() {
      await this.fetchAssignmentData();
      await this.fetchAssignmentAnswersData();
    },
  },
  created() {
    this.onLoadData()
  },
  template:`
  <div>
    <h3>{{ content.title }}</h3>
    <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
    <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

    <!-- Display the assignment score only if it is submitted -->
    <div v-if="isSubmitted" class="alert alert-success">
      Assignment Score: {{ marksObtained }}
    </div>

    <div v-for="(question, index) in questions" :key="question.question_id">
      <QuestionComponent 
        :question="question" 
        :index="index" 
        :selectedOptionId="answers[question.question_id]?.option_id"
        @answer-selected="handleAnswerSelected" 
      />
      
      <br />
    </div>

    <div v-if="checkFlag">
      <span> Score: {{ marksObtained }} / {{ totalMarks }} </span>
    </div>

    <button 
      v-if="content.type == 'graded_assignment_content_type'" 
      @click="submitAssignmentAnswers()" 
      class="btn btn-primary mt-3">
      Submit Answers
    </button>
    <button 
      v-if="content.type == 'assignment_content_type'" 
      @click="() => { checkAnswers(); submitAssignmentAnswers(); }" 
      class="btn btn-primary mt-3">
      Check Answers
    </button>
    <br />
    <button 
      v-if="!questionsGenerated && !loading" 
      @click="generateMockAssignmentQuestions(courseId, weekId, content.type)" 
      class="btn btn-primary mt-3">
      Generate Questions
    </button>

    <!-- Display loading message while questions are being generated -->
    <div v-if="loading" class="alert alert-info">
      Generating Questions...
    </div>

    <!-- Display the questions once they are generated -->
    <div v-if="questionsGenerated">
      <div v-for="(question, index) in questions" :key="question.question_id">
        <QuestionComponent 
          :question="question" 
          :index="index" 
          :selectedOptionId="answers[question.question_id]?.option_id"
          @answer-selected="handleAnswerSelected" 
        />
      </div>
    </div>
  </div>

`
};
