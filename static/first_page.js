export default {
    template: `
        <div class="text-center" style="padding-top:150px">
            <h1 class="display-3 mb-5"> Placeholder Welcome Page </h1>
            <div style="justify-content: center">
              <button class="btn btn-primary me-2" @click="$router.push('/login')">Log In</button>
              <button class="btn btn-primary me-2" @click="$router.push('/signup')">Sign Up</button>
            </div>
        </div>
    `
}