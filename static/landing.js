import Navbar from "./Components/Navbar.js"
export default {
    components:{
        Navbar
    },
    data(){
        return{
            token:""
        }
    },
    methods:{
        async getToken(){
            try{
                this.token = localStorage.getItem('AuthToken')
            }
            catch{
                console.log('Error')
                this.token="!";
            }
        }
    },
    template: `
    <div>
      <Navbar />
      <div class="main-content">
        <div class="content-wrapper text-center">
          <h1 class="display-3 mb-5">IIT Madras
          <br> Online Degree</h1>
          <div class="button-group">
            <button class="btn btn-primary me-2" @click="$router.push('/login')">Log In</button>
            <button class="btn btn-primary" @click="$router.push('/signup')">Sign Up</button>
          </div>
        </div>
      </div>
    </div>
    `
}