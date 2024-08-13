export default {
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
        <button @click="generate_summmary" class="btn btn-primary me-2">Generate Summary</button>
    </div>
    `,
    mounted() {
        this.renderVideo();
    },
    methods: {
        renderVideo() {
            const iframe = this.$refs.videoIframe;
            if (iframe) {
                iframe.src = iframe.src; 
            }
        },

        generate_summary(){
            //Function that generates summary
        }
    }
};
