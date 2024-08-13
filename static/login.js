export default {
    template: `
    <div class="container" style="margin: 0 auto; padding-top: 150px">
      <div class="row justify-content-center">
        <div class="col-lg-4">

          <div class="card shadow-sm">
            <div class="card-body">
              <h2 class="mb-3" style="font-size: 28px; font-weight: bold; color: #007bff; text-align: center; padding-top:15px">Login</h2>
              <form @submit.prevent="submitForm">
                <div class="mb-3">
                  <label for="email" class="form-label">Email:</label>
                  <input type="email" v-model="email" class="form-control" id="email" required />
                </div>
                <div class="mb-4">
                  <label for="password" class="form-label">Password:</label>
                  <input type="password" v-model="password" class="form-control" id="password" required />
                </div>
                <div style="text-align: center">
                  <button type="submit" class="btn btn-primary">Log In</button>
                </div>
              </form>
              <div v-if="errorMessage" class="alert alert-danger mt-2 text-center">{{ errorMessage }}</div>
              <div class="text-center mt-3">
                Haven't made an account yet?
                <router-link to="/signup" class="link-primary">Sign up here.</router-link>
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </div>
    `,
    data() {
      return {
        email: "",
        password: "",
        errorMessage: "",
      };
    },
    methods: {
      async submitForm() {
        // Make POST request to the login endpoint for validation
        const response = await fetch("/log_in", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            // Send email and password as request body
            body: JSON.stringify({
                email: this.email,
                password: this.password,
            }),
        });

        const responseData = await response.json();

        if (response.ok) {
            localStorage.setItem("authToken", responseData.token);
            this.$router.push("/home");
        } else {
        this.errorMessage = responseData.error_message;
        }
      } 
    },
};