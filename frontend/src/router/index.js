import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Rooms from '../views/Rooms.vue'
import Booking from '../views/Booking.vue'
import MyBookings from '../views/MyBookings.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/rooms', name: 'Rooms', component: Rooms },
  { path: '/booking', name: 'Booking', component: Booking },
  { path: '/my-bookings', name: 'MyBookings', component: MyBookings },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0 }
  }
})

export default router