import AboutCourse from "./AboutCourse.js";
import LectureContent from "./LectureContent.js";
import WeeklyAssignment from "./WeeklyAssignment.js";
import ProgrammingAssignment from "./ProgrammingAssignment.js";

export default {
    props: {
        currentComponent: {
            type: String,
            required: true
        },
        content : {
            required: true,
            type: Object
        },
        weekId : {
            required: true,
            type: Number
        },
    },
    components: {
        AboutCourse,
        LectureContent,
        WeeklyAssignment,
        ProgrammingAssignment
    },
    computed: {
        componentToShow() {
            return {
                AboutCourse,
                LectureContent,
                WeeklyAssignment,
                ProgrammingAssignment
            }[this.currentComponent] || AboutCourse; // Fallback to AboutCourse
        }
    },
    template: `
        <component :is="componentToShow" :weekId="weekId" :content="content" />
    `
};
