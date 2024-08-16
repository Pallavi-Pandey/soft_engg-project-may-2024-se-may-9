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
    },
    data() {
        return {
            contentId: 2, // Replace with the actual content ID
            summary: '',
            errorMessage: '',
            src: ""
        };
    },
    template: `
    <div>
        <h2>
            {{content.title}}
        </h2>
        <span class="stars">★★★☆☆</span> /5 (19 reviews)
        <br>
        <iframe width="746" height="420" 
            :src="src" 
            title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
            clipboard-write; encrypted-media; gyroscope; picture-in-picture; 
            web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen
            ref="videoIframe">
        </iframe>
        <br>
        <button @click="generateSummary" class="btn btn-primary me-2">Generate Summary</button>
        <div v-if="summary" class="mt-3">
            <h3>Lecture Summary</h3>
            <p>{{ summary }}</p>
        </div>
        <div v-if="errorMessage" class="alert alert-danger mt-3">
            {{ errorMessage }}
        </div>
    </div>
    `,
    methods: {

        async fetchVideoLectureURL() {
            try {
                const response = await fetch(`/api/course_video/${this.content.id}`, {
                    method: 'GET',
                    headers: {
                        'Authentication-Token': localStorage.getItem('authToken'), // Replace with your actual authentication token
                    },
                });

                if (!response.ok) {
                    throw new Error(`Error: ${response.status}`);
                }

                const data = await response.json();

                this.src = "https://www.youtube.com/embed/" + data.ID
                console.log(this.src, 'data')
            } catch (error) {
                this.errorMessage = error.message || 'Failed to generate summary.';
            }
        },
        renderVideo() {
            const iframe = this.$refs.videoIframe;
            if (iframe) {
                iframe.src = iframe.src;
            }
        },

        async generateSummary() {
            try {
                const response = await fetch(`/api/summary/module/${this.content.id}`, {
                    method: 'GET',
                    headers: {
                        'Authentication-Token': localStorage.getItem('authToken'), // Replace with your actual authentication token
                    },
                });

                if (!response.ok) {
                    throw new Error(`Error: ${response.status}`);
                }

                const data = await response.json();
                this.summary = data.summary;
            } catch (error) {
                this.errorMessage = error.message || 'Failed to generate summary.';
            }
        },
        async onLoadData() {
            await this.fetchVideoLectureURL();
            this.renderVideo();
        }
    },
    mounted() {
        this.onLoadData();
    },
};
