export default {
    template: `
    <div class="content-sidebar">
      <ul class="nav flex-column mt-3">
        <!-- Headline Sections -->
        <li class="nav-item">
          <span class="nav-link" @click="selectItem('AboutCourse')">Course Introduction</span>
        </li>
        <li class="nav-item">
          <span class="nav-link" @click="selectItem('AboutCourse')">About the Course</span>
        </li>

        <!-- Dropdown for Week 1 -->
        <li class="nav-item">
          <span class="nav-link dropdown-toggle" id="week1Dropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">Week 1</span>
          <ul class="dropdown-menu" aria-labelledby="week1Dropdown">
            <li><span class="dropdown-item" @click="selectItem('LectureContent')">Lecture1</span></li>
            <li><span class="dropdown-item" @click="selectItem('WeeklyAssignment')">Graded Assignment</span></li>
            <li><span class="dropdown-item" @click="selectItem('ProgrammingAssignment')">Programming Assignment</span></li>
          </ul>
        </li>

        <!-- Dropdown for Week 2 and onwards -->
        <li class="nav-item">
          <span class="nav-link dropdown-toggle" id="week2Dropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">Week 2</span>
          <ul class="dropdown-menu" aria-labelledby="week2Dropdown">
            <!-- Add items for Week 2 if needed -->
          </ul>
        </li>

        <!-- Repeat for other weeks as needed -->
        <li class="nav-item">
          <span class="nav-link dropdown-toggle" id="week3Dropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">Week 3</span>
          <ul class="dropdown-menu" aria-labelledby="week3Dropdown">
            <!-- Add items for Week 3 if needed -->
          </ul>
        </li>

        <li class="nav-item">
          <span class="nav-link dropdown-toggle" id="week4Dropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">Week 4</span>
          <ul class="dropdown-menu" aria-labelledby="week4Dropdown">
            <!-- Add items for Week 4 if needed -->
          </ul>
        </li>

        <li class="nav-item">
          <span class="nav-link dropdown-toggle" id="week5Dropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">Week 5</span>
          <ul class="dropdown-menu" aria-labelledby="week5Dropdown">
            <!-- Add items for Week 5 if needed -->
          </ul>
        </li>

        <li class="nav-item">
          <span class="nav-link dropdown-toggle" id="week7Dropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">Week 7</span>
          <ul class="dropdown-menu" aria-labelledby="week7Dropdown">
            <!-- Add items for Week 7 if needed -->
          </ul>
        </li>
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