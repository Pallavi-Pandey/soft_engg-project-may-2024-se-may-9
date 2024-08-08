export default {
    template: `
        <div class="container mt-4 text-center">
            <h1 class="mb-5 display-4">{{ week_name }}</h1>

            <table class="table table-bordered table-hover">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Type</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="content in contents" :key="content.order">
                        <td>{{ content.title }}</td>
                        <td>{{ content.type }}</td>
                    </tr>
                </tbody>
            </table>

            <button @click="log_out" class="btn btn-danger me-2">Log Out</button>
        </div>
    `,
    data() {
        return {
            contents: [],
            week_name: "",
            token: localStorage.getItem('authToken')
        };
    },
    methods: {
        async fetchWeeklyContents() {
            const response = await fetch('/api/courses/1/1', {
                headers: {
                    'Authentication-Token': this.token,
                    "Content-Type": "application/json"
                }
            });

            if (response.ok) {
                const response_data = await response.json()
                this.week_name = response_data.Week
                this.contents = response_data.Contents
            } else {
                const response_data = await response.json()
                console.log(response_data.message)
            }
        },
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
        },
    },
    created() {
        this.fetchWeeklyContents();
    }
};