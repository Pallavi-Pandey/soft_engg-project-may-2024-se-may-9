import GradedAssignmentQuestions from './GradedAssignmentQuestions.js';

export default {
  components: {
    GradedAssignmentQuestions,
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
      question: `Question

Accept three positive intergers as input from the user and check if they form the sides of a right triangle.Print YES if they form one, and NO if they do not.

Input-Output

Specification

The input will have three lines, with one integer on each line.
THe output will be a single line containing one of these two strings: YES or NO.

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
      code: '', // This will hold the content of the Ace Editor
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
    },
    createDeadLineMidnightIST(year, month, day) {
      if (this.deadline) {
        let dateList = this.deadline.split("-")
        const date = new Date(dateList[0], dateList[1] - 1, dateList[2], 0, 0, 0);
        date.setHours(date.getHours() + 5);
        date.setMinutes(date.getMinutes() + 30);
        return date;
      }
    },
    createAceEditor() {
      let editor = ace.edit("editor");
      editor.setTheme("ace/theme/monokai")
      editor.session.setMode("ace/mode/javascript")

    }

  },
  mounted() {
    // this.fetchAssignmentData();
    // this.createAceEditor();
  },
  template: `
    <div class="graded-assignment" style="width: 80%; margin-left: 10px;">
    </br>
      <div style="background-color: maroon; color: white;">
        <div style="margin-left: 20px; margin-top: 10px;" v-if="createDeadLineMidnightIST() < new Date()">The due date for submitting this assignment has passed.</div>
        <div style="margin-left: 20px; margin-bottom: 20px;" v-if="deadline">Due date: {{ deadline.toLocaleString() }}</div>
      </div>
      <div style="margin-left: 20px;">{{ question }}</div>
      </br>
      <div style="color: red; margin-left: 20px;">This assignment has public test cases. Please click on "Test Run" button to see the status of public test cases. Assignment will be evaluated only after submitting using "Submit" button below. If you only test run the program, your assignment will not be graded and you will not see your score after the deadline.</div>
      </br>
      <div style="margin-left: 20px;">
      Choose Language:<select v-model="selectedLanguage" id="language" style="margin-left: 20px;" class="mb-3">
      <option disabled value="">Select a language</option>
      <option v-for="option in options" :key="option" :value="option">
        {{ option }}
      </option>
    </select>
    </div>

    <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
    <div>
    <button @click="submitAssignment" class="btn btn-primary mt-3">Submit Assignment</button>
    </div>
    </div>
  `
};