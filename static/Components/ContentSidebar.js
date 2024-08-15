export default {
    template: `
    <div class="content-sidebar">
      <ul class="nav flex-column mt-3">
        <!-- Headline Sections -->
        <li class="nav-item">
          <a class="nav-link" href="#course-introduction">Course Introduction</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#about-course">About the Course</a>
        </li>

        <!-- Dropdown for Week 1 -->
        <li class="nav-item">
          <a class="nav-link dropdown-toggle" href="#" id="week1Dropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">Week 1</a>
          <ul class="dropdown-menu" aria-labelledby="week1Dropdown">
            <li><a class="dropdown-item" href="#" @click="selectItem('LectureContent')">Lecture1</a></li>
            <li><a class="dropdown-item" href="#" @click="selectItem('WeeklyAssignment')">Graded Assignment</a></li>
            <li><a class="dropdown-item" href="#" @click="selectItem('ProgrammingAssignment')">Programming Assignment</a></li>
          </ul>
        </li>

        <!-- Dropdown for Week 2 and onwards -->
        <li class="nav-item">
          <a class="nav-link dropdown-toggle" href="#" id="week2Dropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">Week 2</a>
          <ul class="dropdown-menu" aria-labelledby="week2Dropdown">
            <!-- Add items for Week 2 if needed -->
          </ul>
        </li>

        <!-- Repeat for other weeks as needed -->
        <li class="nav-item">
          <a class="nav-link dropdown-toggle" href="#" id="week3Dropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">Week 3</a>
          <ul class="dropdown-menu" aria-labelledby="week3Dropdown">
            <!-- Add items for Week 3 if needed -->
          </ul>
        </li>

        <li class="nav-item">
          <a class="nav-link dropdown-toggle" href="#" id="week4Dropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">Week 4</a>
          <ul class="dropdown-menu" aria-labelledby="week4Dropdown">
            <!-- Add items for Week 4 if needed -->
          </ul>
        </li>

        <li class="nav-item">
          <a class="nav-link dropdown-toggle" href="#" id="week5Dropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">Week 5</a>
          <ul class="dropdown-menu" aria-labelledby="week5Dropdown">
            <!-- Add items for Week 5 if needed -->
          </ul>
        </li>

        <li class="nav-item">
          <a class="nav-link dropdown-toggle" href="#" id="week7Dropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">Week 7</a>
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