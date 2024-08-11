import AboutCourse from "./AboutCourse.js";
import LectureContent from "./LectureContent.js";
import GradedAssignment from "./GradedAssignment.js";

export default {
    props: {
        currentComponent: {
            type: String,
            required: true
        }
    },
    components: {
        AboutCourse,
        LectureContent,
        GradedAssignment
    },
    computed: {
        componentToShow() {
            return {
                AboutCourse,
                LectureContent,
                GradedAssignment
            }[this.currentComponent] || AboutCourse; // Fallback to AboutCourse
        }
    },
    template: `
        <component :is="componentToShow" />
    `
};
