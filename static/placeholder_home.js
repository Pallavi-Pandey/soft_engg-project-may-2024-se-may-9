export default {
    template: `
      <div v-if="user_found">
        <div class="text-center" style="padding-top:150px">
          <h1 class="mb-5 display-4">Welcome, {{ name }}!</h1>
          <div style="justify-content: center">
            <button class="btn btn-primary" @click="$router.push('/course_info')">Test Course Info Retrieval</button>
            <button @click="log_out" class="btn btn-danger me-2">Log Out</button>
          </div>
        </div>
      </div>
      
      <div v-else class="text-center mt-5">
        <h1 class="display-3 mb-5">Unable to retrieve user details.</h1>
        <h2>Please try again!</h2>
        <div class="d-flex justify-content-center">
          <button class="btn btn-primary" @click="$router.push('/login')">Log In</button>
          <button class="btn btn-primary" @click="$router.push('/signup')">Sign Up</button>
        </div>
      </div>
    `,
    data() {
      return {
        user_found: true, // Whether logged-in user could be retrieved
        name: '', // Name of currently logged-in user
        userId: 0, // ID of currently logged-in user
        token: localStorage.getItem('authToken') // Authentication token
      };
    },
    methods: {
      async fetchUserData() {
        // Retrieve details of currently logged-in user
        const response = await fetch('/get_user', {
          headers: {
            'Authentication-Token': this.token,
            "Content-Type": "application/json"
          }
        }); 
        if (response.ok) {
          const userData = await response.json();
          this.name = userData.name;
          this.userId = userData.student_id;
        } else {
          user_found = false; // User couldn't be retrieved
          console.error('Failed to fetch user data');
        }
      },
      // Log out the user
      async log_out() {
        const response = await fetch("/log_out", {
            method: "POST",
            headers: {
              'Authentication-Token': this.token,
            },
        });

        if (response.ok) {
            localStorage.removeItem('authToken');
            console.log('Logout successful');

            // Redirect to the login page
            this.$router.push('/login');
        } else {
            const responseData = await response.json();
            console.error('Logout failed:', responseData.error_message);
        }
      }
    },
    created() {
      // Fetch user data when the component is created
      this.fetchUserData();
    }
};