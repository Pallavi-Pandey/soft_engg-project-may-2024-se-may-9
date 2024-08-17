import landing from './landing.js'
import login from './login.js'
import signup from './signup.js'
import home from './home.js'
import course_page from './course_page.js'

const routes = [
    { path: '/', component: landing },
    { path: '/login', component: login },
    { path: '/signup', component: signup },
    { path: '/home', component: home },
    { path: '/course_page/:course_id?', component: course_page, props:true }
    
]

export default new VueRouter({
    routes
})