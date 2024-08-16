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

        <li class="nav-item" v-for="(week, index) in weekList" :key="index">
          <span class="nav-link dropdown-toggle" 
            :id="'week' + index + 'Dropdown'" 
            role="button" 
            data-bs-toggle="dropdown" 
            aria-expanded="false">
            {{ week.title }}
          </span>
          <ul class="dropdown-menu" :aria-labelledby="'week' + index + 'Dropdown'">
            <li v-for="(content, index) in week.weekContent" :key="index">
              <span class="dropdown-item" @click="selectItem(content.id, 'LectureContent')"
              v-if="content.type == 'html_page_content_type'">{{ content.title }}</span>
              <span class="dropdown-item" @click="selectItem(content.id, 'LectureContent')"
              v-if="content.type == 'module_content_type'">{{ content.title }}</span>
              <span class="dropdown-item" @click="selectItem(content.id, 'WeeklyAssignment')"
              v-if="content.type == 'assignment_content_type'">{{ content.title }}</span>
              <span class="dropdown-item" @click="selectItem(content.id, 'WeeklyAssignment')"
              v-if="content.type == 'graded_assignment_content_type'">{{ content.title }}</span>
              <span class="dropdown-item" @click="selectItem(content.id, 'ProgrammingAssignment')"
              v-if="content.type == 'programming_content_type'">{{ content.title }}</span>
            </li>
          </ul>
        </li>
      </ul>
    </div>
    `,
  data() {
    return {
      courseId: 1,
      weekList: [],
    };
  },
  mounted() {
    this.onLoadData();
  },
  methods: {
    selectItem(id, componentName) {
      let data = {
        id: id,
        componentName: componentName
      }
      this.$emit('update-content', data);
    },
    async onLoadData() {
      await this.fetchCourseDetails();
      await this.fetchWeekDetails();
    },
    async fetchCourseDetails() {
      try {
        const response = await fetch(`/api/courses/${this.courseId}`, {
          headers: {
            'Authentication-Token': localStorage.getItem('authToken')
          }
        });

        if (response.ok) {
          const data = await response.json();
          this.weekList = data.Weeks
        } else {
          console.error('Failed to fetch course details');
        }
      } catch (error) {
        console.error('Error fetching course details:', error);
      }
    },
    async fetchWeekDetails() {
      try {
        let i = 0
        for (let week of this.weekList) {
          const response = await fetch(`/api/courses/${this.courseId}/${week.id}`, {
            headers: {
              'Authentication-Token': localStorage.getItem('authToken')
            }
          });

          if (response.ok) {
            const data = await response.json();
            let weekData = {
              ...week,
              weekContent: data.Contents
            }
            this.weekList.splice(i,1,weekData)
            i++
          } else {
            console.error('Failed to fetch course details');
          }
        }
      } catch (error) {
        console.error('Error fetching course details:', error);
      }
    }
  },
};