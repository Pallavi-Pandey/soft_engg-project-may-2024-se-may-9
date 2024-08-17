// QuestionComponent.js
export default {
    props: {
      question: {
        type: Object,
        required: true
      },
      index: {
        type: Number,
        required: true
      },
      selectedOptionId: {
        type: Number,
      }
    },
    data() {
      return {
        selectedOption: this.selectedOptionId
      }
    },
    watch: {
      selectedOptionId(newVal) {
        this.selectedOption = newVal;
      }
    },
    methods: {
      selectOption(optionId) {
        this.selectedOption = optionId;
        // Emit the selected option ID to the parent component
        this.$emit('answer-selected', {
          question_id: this.question.question_id,
          option_id: optionId,
        });
      }
    },
    template: `
      <div class="question-container">
        <h4>Question {{ index + 1 }}:</h4>
        <p>{{ question.question_text }} ({{question.question_score }} points)</p>
        <div v-for="option in question.options" :key="option.option_id" class="option">
            <input 
            type="radio" 
            :id="option.option_id" 
            :name="'question-' + question.question_id" 
            :value="option.option_id" 
            v-model="selectedOption"
            @change="selectOption(option.option_id)"
          />
          <label :for="option.option_id">{{ option.option_text }}</label>
        </div>
    </div>
    `,
    style: `
      .question-container {
        margin-bottom: 20px;
      }
      .option {
        margin-bottom: 10px;
      }
    `
  };
  