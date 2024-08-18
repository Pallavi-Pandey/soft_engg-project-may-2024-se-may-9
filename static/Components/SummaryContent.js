export default {
    props: {
        content: {
            required: true,
            type: Object
        },
        weekId: {
            required: true,
            type: Number
        },
        courseId: {
            required: true,
            type: Number
        },
    },
    data() {
        return {
            summary: '',
            errorMessage: '',
            isLoading: false
        };
    },
    template: `
    <div>
        <h2 v-if="content.type=='weekly_summary'">
            Week Summary
        </h2>
        <h2 v-if="content.type=='course_summary'">
            Course Summary
        </h2>
        <button @click="generateSummary" class="btn btn-primary me-2">Generate Summary</button>
        <div v-if="isLoading" style="margin-left: 20px; margin-top: 20px; font-style: italic; color: darkorange;">
          Generating your summary...<div class="spinner"></div>
        </div>
        <div v-if="summary" class="mt-3 summary-container">  
            <div v-html="renderedContent"></div>
        </div>
        <div v-if="errorMessage" class="alert alert-danger mt-3">
            {{ errorMessage }}
        </div>
    </div>
    `,
    computed: {
        renderedContent() {
          return this.renderMarkdown(this.summary);
        }
      },
    methods: {
        renderMarkdown(content) {
            const md = window.markdownit();
            return md.render(content);
          },

        async generateSummary() {
            this.isLoading = true
            try {
                let response;
                if(this.content.type == "weekly_summary") {
                    response = await fetch(`/api/summary/week/${this.weekId}`, {
                        method: 'GET',
                        headers: {
                            'Authentication-Token': localStorage.getItem('authToken'), // Replace with your actual authentication token
                        },
                    });
                } else if (this.content.type == "course_summary") {
                    response = await fetch(`/api/summary/course/${this.courseId}`, {
                        method: 'GET',
                        headers: {
                            'Authentication-Token': localStorage.getItem('authToken'), // Replace with your actual authentication token
                        },
                    });
                }
                
                if (!response.ok) {
                    throw new Error(`Error: ${response.status}`);
                }

                const data = await response.json();
                this.summary = data.summary;
            } catch (error) {
                this.errorMessage = error.message || 'Failed to generate summary.';
            } finally {
                this.isLoading = false
            }
        },
    },
};
