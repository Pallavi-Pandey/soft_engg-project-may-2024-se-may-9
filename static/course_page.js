import ContentSidebar from "./Components/ContentSidebar.js";
import FixedSidebar from "./Components/FixedSidebar.js";
import Navbar from "./Components/Navbar.js";
import MainContent from "./Components/MainContent.js";

export default {
    components: {
        ContentSidebar,
        FixedSidebar,
        Navbar,
        MainContent
    },
    data() {
        return {
            selectedComponent: 'AboutCourse' // Default component
        };
    },
    methods: {
        updateContent(componentName) {
            this.selectedComponent = componentName;
        }
    },
    template: `
    <div class="course-container">
        <Navbar />
        <div class="content-wrapper" style="display: flex;">
            <FixedSidebar />
            <ContentSidebar @update-content="updateContent" />
            <MainContent :currentComponent="selectedComponent" />
        </div>
    </div>
    `
};
