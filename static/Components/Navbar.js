export default {
    template: `
    <nav class="navbar navbar-expand-lg navbar-light bg-light" style="box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">
                <img src="https://upload.wikimedia.org/wikipedia/en/6/69/IIT_Madras_Logo.svg" alt="IIT Madras" height="40">
                IIT Madras
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="#">Course Name</a>
                    </li>
                </ul>
                <div class="d-flex">
                    <button @click="log_out" class="btn btn-danger me-2">Log Out</button>
                </div>
                <div class="d-flex">
                    dummy_email@email.com
                </div>
            </div>
        </div>
    </nav>
    `,

    methods:{
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
    }
}
