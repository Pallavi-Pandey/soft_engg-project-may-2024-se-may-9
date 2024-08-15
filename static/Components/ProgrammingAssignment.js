import GradedAssignmentQuestions from './QuestionComponent.js';

export default {
  components: {
    GradedAssignmentQuestions,
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
      default: 17
    }
  },
  data() {
    return {
      assignmentTitle: '',
      question: `Question

Accept three positive integers as input from the user and check if they form the sides of a right triangle. Print YES if they form one, and NO if they do not.

Input-Output

Specification

The input will have three lines, with one integer on each line.
The output will be a single line containing one of these two strings: YES or NO.

Examples

Input-1
1
2
3

Output-1
NO

Input-2
3
4
5

Output-2
YES`,
      deadline: "2024-08-11",
      answers: [],
      errorMessage: '',
      options: ["Python3"],
      selectedLanguage: '', // Define selectedLanguage in the data object
      code: '', // This will hold the content of the Ace Editor
      hint: '', // This will store the hint from the API
      editorOptions: {
        mode: 'python', // Specify the mode, e.g., 'python'
        theme: 'monokai', // Specify the theme, e.g., 'monokai'
        tabSize: 2, // Customize other options
        fontSize: 14 // Customize font size
      }
    };
  },
  methods: {
    async fetchAssignmentData() {
      
      try {
        const token = localStorage.getItem('authToken'); // Replace with your actual key for the token
        if (!token) {
          throw new Error('No authentication token found');
        }
        const response = await fetch(`/api/course_assignment/${this.courseId}/${this.weekId}/${this.assignmentId}`,{
          method: 'GET',
          headers: {
            'Authentication-Token': token
          }
        });
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
    async fetchHint() {
      try {
        const token = localStorage.getItem('authToken'); // Replace with your actual key for the token
        if (!token) {
          throw new Error('No authentication token found');
        }

        const response = await fetch(`/api/program_hint/${this.assignmentId}`, {
          method: 'GET',
          headers: {
            'Authentication-Token': token // Use the token from localStorage
          }
        });

        if (!response.ok) {
          throw new Error('Failed to fetch hint');
        }

        const data = await response.json();
        this.hint = data.hint;
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
      console.log(this.code);
      try {
        const response = await fetch(`/api/course_assignment/${this.courseId}/${this.weekId}/${this.assignmentId}`, {
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
    },
    createDeadLineMidnightIST() {
      if (this.deadline) {
        let dateList = this.deadline.split("-");
        const date = new Date(dateList[0], dateList[1] - 1, dateList[2], 0, 0, 0);
        date.setHours(date.getHours() + 5);
        date.setMinutes(date.getMinutes() + 30);
        return date;
      }
    },
    createAceEditor() {
      if (window.ace) {
        let editor = ace.edit("editor");
        editor.setTheme("ace/theme/" + this.editorOptions.theme);
        editor.session.setMode("ace/mode/" + this.editorOptions.mode); // Set mode based on selected language
        editor.setValue(this.code); // Load the initial code into the editor

        // Listen for changes in the editor and update the `code` data property
        editor.session.on('change', () => {
          this.code = editor.getValue();
        });
      } else {
        console.error("Ace editor is not loaded");
      }
    }
  },
  mounted() {
    // Fetch assignment data and hint when component is mounted
    this.fetchAssignmentData();
    this.fetchHint();
    
    // Initialize Ace Editor when component is mounted
    this.$nextTick(() => {
      this.createAceEditor();
    });
  },
  template: `
    <div class="graded-assignment" style="width: 80%; margin-left: 10px;">
      <div style="background-color: maroon; color: white;">
        <div style="margin-left: 20px; margin-top: 10px;" v-if="createDeadLineMidnightIST() < new Date()">The due date for submitting this assignment has passed.</div>
        <div style="margin-left: 20px; margin-bottom: 20px;" v-if="deadline">Due date: {{ deadline.toLocaleString() }}</div>
      </div>
      <div style="margin-left: 20px;">{{ question }}</div>
      <div style="color: red; margin-left: 20px;">This assignment has public test cases. Please click on "Test Run" button to see the status of public test cases. Assignment will be evaluated only after submitting using "Submit" button below. If you only test run the program, your assignment will not be graded and you will not see your score after the deadline.</div>
      <div style="margin-left: 20px;">
        Choose Language:
        <select v-model="selectedLanguage" id="language" style="margin-left: 20px;" class="mb-3">
          <option disabled value="">Select a language</option>
          <option v-for="option in options" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </div>
      
      <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

      <!-- Ace Editor HTML -->
      <div id="editor" style="height: 400px; width: 100%;">{{ code }}</div>

      <!-- Display Hint -->
      <div v-if="hint" style="margin-left: 20px; margin-top: 20px; font-style: italic; color: darkgreen;">
        Hint: {{ hint }}
      </div>

      <!-- Submit button -->
      <div>
        <button @click="submitAssignment" class="btn btn-primary mt-3">Submit Assignment</button>
      </div>
    </div>
  `
};
