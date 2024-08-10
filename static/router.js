import course_info from './course_info.js'
import first_page from './first_page.js'
import login from './login.js'
import signup from './signup.js'
import placeholder_home from './placeholder_home.js'
import weekly_content from './weekly_content.js'

const routes = [
    { path: '/', component: first_page },
    { path: '/login', component: login },
    { path: '/signup', component: signup },
    { path: '/course_info', component: course_info },
    { path: '/placeholder_home', component: placeholder_home },
    { path: '/weekly_content', component: weekly_content }
]

export default new VueRouter({
    routes
})