export default {
    template: `
        <div class="content-sidebar">
            <ul class="nav flex-column mt-3">
                <li class="nav-item" ><a class="nav-link" href="#">Course Introduction</a></li>
                <li class="nav-item" @click="selectItem('AboutCourse')">About the Course</li>
                <li class="nav-item"><a class="nav-link" href="#">General Instructions</a></li>
                <li class="nav-item" @click="selectItem('LectureContent')">Week 1</li>
                <li class="nav-item" @click="selectItem('GradedAssignment')"><a>Graded Assignment</a></li>
                <li class="nav-item" @click="selectItem('ProgrammingAssignment')"><a>Programming Assignment</a></li>
                <li class="nav-item"><a class="nav-link" href="#">Week 2</a></li>
                <li class="nav-item"><a class="nav-link" href="#">Week 3</a></li>
                <li class="nav-item"><a class="nav-link" href="#">Week 4</a></li>
                <li class="nav-item"><a class="nav-link" href="#">Week 5</a></li>
                <li class="nav-item"><a class="nav-link" href="#">Week 7</a></li>
            </ul>
        </div>
    `,
    data() {
      return {
        // Add any necessary data properties here
      };
    },
    methods: {
      selectItem(componentName) {
        this.$emit('update-content', componentName);
      }
    },
  };