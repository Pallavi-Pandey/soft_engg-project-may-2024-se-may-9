export default {
    data() {
        return {
            contentId: 2, // Replace with the actual content ID
            summary: '',
            errorMessage: ''
        };
    },
    template: `
    <div>
        <h2>
            1.1 Deconstructing the Software Development Process - Introduction
        </h2>
        <span class="stars">★★★☆☆</span> /5 (19 reviews)
        <br>
        <iframe width="746" height="420" 
            src="https://www.youtube.com/embed/hKm_rh1RTJQ?si=o20ZOZkqiv1heEVy" 
            title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
            clipboard-write; encrypted-media; gyroscope; picture-in-picture; 
            web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
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
        renderVideo() {
            const iframe = this.$refs.videoIframe;
            if (iframe) {
                iframe.src = iframe.src; 
            }
        },

        async generateSummary() {
            try {
                const response = await fetch(`/api/summary/module/${this.contentId}`, {
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
        }
    },
    mounted() {
        this.renderVideo();
    },
};
