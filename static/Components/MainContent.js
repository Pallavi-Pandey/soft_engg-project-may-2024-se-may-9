import AboutCourse from "./AboutCourse.js";
import LectureContent from "./LectureContent.js";
import GradedAssignment from "./GradedAssignment.js";
import ProgrammingAssignment from "./ProgrammingAssignment.js";

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
        GradedAssignment,
        ProgrammingAssignment
    },
    computed: {
        componentToShow() {
            return {
                AboutCourse,
                LectureContent,
                GradedAssignment,
                ProgrammingAssignment
            }[this.currentComponent] || AboutCourse; // Fallback to AboutCourse
        }
    },
    template: `
        <component :is="componentToShow" />
    `
};
