import Navbar from "./Components/Navbar.js";
export default {
    template:`
    <div>
    <Navbar />
      <div class="main-content">
      <div class="container align-items-center">
        <div class="row justify-content-center">
          <div class="col-md-6 col-lg-4">
            <div class="card shadow-sm">
              <div class="card-body">
                <h2 class="mb-3" style="font-size: 28px; font-weight: bold; color: #007bff; text-align: center; padding-top: 15px">Sign Up</h2>
                
                <form @submit.prevent="submitForm">
                  <div class="mb-3">
                    <label for="name" class="form-label">Name:</label>
                    <input type="text" v-model="name" class="form-control" id="name" required />
                  </div>
                  <div class="mb-3">
                    <label for="email" class="form-label">Email:</label>
                    <input type="email" v-model="email" class="form-control" id="email" required />
                  </div>
                  <div class="mb-3">
                    <label for="password" class="form-label">Password:</label>
                    <input type="password" v-model="password" class="form-control" id="password" required />
                  </div>
                  <div class="mb-3">
                    <label for="confirmPassword" class="form-label">Confirm Password:</label>
                    <input type="password" v-model="confirmPassword" class="form-control" id="confirmPassword" required />
                  </div>
                  <div style="text-align: center">
                    <button type="submit" class="btn btn-primary">Sign Up</button>
                  </div>  
                </form>

                <div v-if="successMessage" class="alert alert-success mt-3">
                  {{ successMessage }}
                  <button @click="$router.push('/login')" class="ms-2 btn btn-outline-success">Log In</button>
                </div>

                <div v-if="errorMessages.length > 0" class="alert alert-danger mt-3">
                  <ul>
                    <li v-for="errorMessage in errorMessages" :key="errorMessage">{{ errorMessage }}</li>
                  </ul>
                </div>
                
                <div class="text-center mt-3">
                  Already have an account?
                  <router-link to="/log_in" class="mt-3 link-primary">Log in here.</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
    `,
    components:{
      Navbar
    },
    data() {
      return {
        name: "", // Name of new user
        email: "", // Email of new user
        password: "", // Password of new user
        confirmPassword: "", // Re-entering password
        successMessage: "", // Text for successful login
        errorMessages: [], // Any and all errors in user input
      };
    },
    methods: {
      async submitForm() {
          // Make POST request to signup endpoint for validation
          const response = await fetch("/signup", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              name: this.name,
              email: this.email,
              password: this.password,
              confirm_password: this.confirmPassword
            }),
          });
  
          const responseData = await response.json();
  
          if (response.ok) {
            // Registration successful
            this.successMessage = "Account created successfully! ";
            this.errorMessages = [];
          } else {
            // Registration failed, set error messages
            this.successMessage = "";
            this.errorMessages = responseData.error_messages;
          }
      } 
    },
};