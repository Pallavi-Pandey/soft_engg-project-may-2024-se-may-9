import course_info from './course_info.js'
import landing from './landing.js'
import login from './login.js'
import signup from './signup.js'
import home from './home.js'
import weekly_content from './weekly_content.js'
import course_page from './course_page.js'

const routes = [
    { path: '/', component: landing },
    { path: '/login', component: login },
    { path: '/signup', component: signup },
    { path: '/course_info', component: course_info },
    { path: '/home', component: home },
    { path: '/weekly_content', component: weekly_content },
    { path: '/course_page/:course_id?', component: course_page, props:true }
]

export default new VueRouter({
    routes
})