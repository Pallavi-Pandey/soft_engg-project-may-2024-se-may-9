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
      }
    },
    methods: {
      selectOption(optionId) {
        // Emit the selected option ID to the parent component
        this.$emit('answer-selected', {
          question_id: this.question.question_id,
          option_id: optionId
        });
      }
    },
    template: `
    <div class="question-container">
        <h4 class="question-title">Question {{ index + 1 }}:</h4>
        <p class="question-text">{{ question.question_text }}</p>
        <div v-for="option in question.options" :key="option.option_id" class="option">
            <input 
            type="radio" 
            :id="option.option_id" 
            :name="'question-' + question.question_id" 
            :value="option.option_id" 
            @change="selectOption(option.option_id)"
            class="option-input"
            />
            <label :for="option.option_id" class="option-label">{{ option.option_text }}</label>
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
  