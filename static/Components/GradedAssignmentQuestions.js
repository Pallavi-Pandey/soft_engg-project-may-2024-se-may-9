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
    data() {
        return {
            selectedOption: null
        };
    },
    template: `
        <div class="card mb-3">
            <div class="card-body">
            <h5 class="card-title">Question {{ index + 1 }}</h5>
            <p class="card-text">{{ question.question_text }}</p>
            <div v-for="option in question.options" :key="option.option_id">
                <div class="form-check">
                <input class="form-check-input" type="radio" 
                    :id="'option-' + option.option_id" 
                    :value="option.option_id" 
                    v-model="selectedOption"
                    @change="$emit('answer-selected', { question_id: question.question_id, option_id: selectedOption })">
                <label class="form-check-label" :for="'option-' + option.option_id">
                    {{ option.option_text }}
                </label>
                </div>
            </div>
            </div>
        </div>
    `
};