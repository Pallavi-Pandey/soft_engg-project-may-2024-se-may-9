import Navbar from "./Components/Navbar.js";
import FixedSidebar from "./Components/FixedSidebar.js";
import ContentSidebar from "./Components/ContentSidebar.js";
import MainContent from "./Components/MainContent.js";

export default {
    components: {
        Navbar,
        FixedSidebar,
        ContentSidebar,
        MainContent
    },
    data() {
        return {
            selectedComponent: 'AboutCourse',  // Default component
            courseTitle: '',  // Store the course title
            userEmail: '',  // Store the user email
            id: null
        };
    },
    methods: {
        async fetchUserEmail() {
            try {
                const response = await fetch('/get_user', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': localStorage.getItem('authToken')
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    this.userEmail = data.email;  // Set the user email from the response
                } else {
                    console.error('Failed to fetch user email');
                }
            } catch (error) {
                console.error('Error fetching user email:', error);
            }
        },
        async fetchCourseTitle() {
            try {
                const response = await fetch(`/api/courses/${this.courseId}`, {
                    headers: {
                        'Authentication-Token': localStorage.getItem('authToken')
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    this.courseTitle = data.course_title;  // Set the course title from the response
                } else {
                    console.error('Failed to fetch course title');
                }
            } catch (error) {
                console.error('Error fetching course title:', error);
            }
        },
        updateContent(payload) {
            this.selectedComponent = payload.componentName
            this.id = payload.id
        }
    },
    created() {
        this.fetchUserEmail();  // Fetch user email when component is created
        this.fetchCourseTitle();  // Fetch course title when component is created
    },
    template: `
    <div class="course-container">
        <!-- Pass the fetched userEmail and courseTitle to the Navbar component -->
        <Navbar :userEmail="userEmail" :courseTitle="courseTitle" />
        <div class="content-wrapper" style="display: flex;">
            <FixedSidebar />
            <ContentSidebar @update-content="updateContent" />
            <MainContent :currentComponent="selectedComponent" :id="id" />
        </div>
    </div>
    `
};
