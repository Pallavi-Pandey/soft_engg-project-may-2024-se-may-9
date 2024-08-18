export default {
    data() {
      return {
        courseId: 2, // Default course ID, modify as needed
        weakConcepts: '', // String to store the weak concepts
        loading: false, // Loading state to manage API call
        errorMessage: '', // Error message in case of API failure
      };
    },
    methods: {
      async fetchWeakConcepts() {
        this.loading = true;
        this.errorMessage = '';
    
        try {
          const response = await fetch(`/api/weak_concepts/${this.courseId}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authentication-Token': localStorage.getItem('authToken'), // Ensure the token is included if needed
            },
          });
    
          if (response.ok) {
            const data = await response.json();
            this.weakConcepts = data.weak_concepts;
            console.log('Weak Concepts:', data);
          } else {
            throw new Error('Failed to fetch weak concepts');
          }
        } catch (error) {
          this.errorMessage = error.message;
          console.error('Error:', error);
        } finally {
          this.loading = false;
        }
      },
      renderMarkdown(content) {
        const md = window.markdownit();
        return md.render(content);
      },
    },
    computed: {
      renderWeakConcepts() {
        return this.renderMarkdown(this.weakConcepts); // Use `this.renderMarkdown` to reference the method
      },
    },
    template: `
      <div class="weak-concepts-container">
        <button @click="fetchWeakConcepts" class="btn btn-primary">
          Fetch Weak Concepts
        </button>
  
        <div v-if="loading" class="mt-3">
          <p>Loading weak concepts...</p>
        </div>
  
        <div v-if="errorMessage" class="mt-3 text-danger">
          <p>{{ errorMessage }}</p>
        </div>
  
        <div v-if="weakConcepts && !loading" class="mt-3">
          <h3>Weak Concepts:</h3>
          <div v-html="renderWeakConcepts"></div>
        </div>
      </div>
    `,
  };
  