import first_page from './first_page.js'
import login from './login.js'
import signup from './signup.js'
import placeholder_home from './placeholder_home.js'

const routes = [
    { path: '/', component: first_page },
    { path: '/login', component: login },
    { path: '/signup', component: signup },
    { path: '/placeholder_home', component: placeholder_home }
]

export default new VueRouter({
    routes
})