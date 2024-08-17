export default {
    props: {
        courseId: {
            type: Number,
            required: true,
            default: 1
        }
    },
    data(){
        return {
            courseTitle:"CourseName"
        }
    },
    methods: {
        async fetchCourseData(courseId) {
        try {
            const response = await fetch(`/api/courses/${courseId}`, {
            method: 'GET',
            headers: {
                'Authentication-Token': localStorage.getItem('authToken')
            }
            });

            if (!response.ok) {
            throw new Error('Failed to fetch course data');
            }
            
            const data = await response.json();
            console.log(data)
            this.courseTitle = data.Course; // Update the course title
        } catch (error) {
            console.error('Error fetching course data:', error);
        }
    }
    },
    created() {
      this.fetchCourseData(this.courseId); // Fetch course data when the component is created
    },
    template: `
    <router-link :to="'/course_page/3' ">
        <div class="card" style="margin: 0.4em .4em; width: calc(100/3);">
            <div class="image-wrapper" style="max-width:100%; height:19em">
            <img src="https://static.vecteezy.com/system/resources/thumbnails/008/962/785/small/abstract-red-circle-dots-wave-pattern-on-black-design-modern-technology-background-vector.jpg" class="card-img-top" alt="Product Image" style="max-width:100%; max-height:100%">
        </div>
        <div class="card-body" style="text-align: left;">
            <h5 class="card-title">{{ courseTitle }}</h5>
            <div class="weekly-asignment-scores">Week 1 Assignment- 89.00</div>
            <div class="weekly-asignment-scores">Week 2 Assignment- 76.00</div>
            <div class="weekly-asignment-scores">Week 3 Assignment- 88.00</div>
            <div class="weekly-asignment-scores">Week 4 Assignment- 95.00</div>
        </div>
        </div>
    </router-link>
    `
};