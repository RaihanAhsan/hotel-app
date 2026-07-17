<template>
  <div class="page active" id="page-home">
    <!-- HERO -->
    <section class="hero-home">
      <div class="container hero-content">
        <div class="badge"><i class="fas fa-crown"></i> 5-Star · Jakarta's Finest</div>
        <h1>Where <span>Legacy</span> Meets <span>Skyline</span></h1>
        <p>An iconic sanctuary in the heart of Jakarta. Experience timeless elegance, world-class service, and panoramic city views that redefine luxury.</p>
        <div class="hero-actions">
          <button class="btn btn-primary" @click="handleBookNow">
            <i class="fas fa-calendar-check" style="margin-right:10px;"></i>Book Your Stay
          </button>
          <a href="#experiences" class="btn btn-outline-light">Discover More</a>
        </div>
      </div>
    </section>

    <!-- SIGNATURE EXPERIENCES -->
    <section class="experiences section-padding" id="experiences">
      <div class="container">
        <div class="reveal" v-intersect="onReveal">
          <span class="section-label">The Grand Experience</span>
          <h2 class="section-title">Signature <span>Moments</span></h2>
          <p class="section-subtitle">Every stay is crafted to be unforgettable — from sunrise views to Michelin-starred dining.</p>
        </div>
        <div class="exp-grid">
          <div v-for="(exp, idx) in experiences" :key="idx" class="exp-card reveal" v-intersect="onReveal">
            <div class="icon"><i :class="exp.icon"></i></div>
            <h3>{{ exp.title }}</h3>
            <p>{{ exp.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- OUR SIGNATURE ROOMS -->
    <section class="rooms-preview section-padding" id="rooms">
      <div class="container">
        <div class="reveal" v-intersect="onReveal">
          <span class="section-label">Luxury Suites</span>
          <h2 class="section-title">Our <span>Signature</span> Rooms</h2>
          <p class="section-subtitle">Each room is a masterpiece of design, offering breathtaking views and uncompromising comfort.</p>
        </div>
        <div class="room-grid">
          <div v-for="room in store.rooms" :key="room.id" class="room-card reveal" v-intersect="onReveal">
            <div class="img-wrap">
              <img :src="room.image" :alt="room.name" loading="lazy" />
              <span class="badge-room">{{ room.id === 'penthouse' ? 'Penthouse' : room.id === 'executive' ? 'Executive' : 'Popular' }}</span>
            </div>
            <div class="body">
              <h3>{{ room.name }}</h3>
              <div class="price">${{ room.price }} <small>/ night</small></div>
              <p>{{ room.description }}</p>
              <button class="btn btn-primary" @click="selectRoom(room.id)">Book Now</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- WORLD-CLASS AMENITIES -->
    <section class="amenities-home section-padding" id="amenities">
      <div class="container">
        <div class="reveal" v-intersect="onReveal">
          <span class="section-label" style="color:var(--gold-light);">World-Class Amenities</span>
          <h2 class="section-title">Every <span>Detail</span> Matters</h2>
          <p class="section-subtitle">Designed for the discerning traveler — where luxury meets functionality.</p>
        </div>
        <div class="amenity-grid">
          <div v-for="(item, idx) in amenities" :key="idx" class="amenity-item reveal" v-intersect="onReveal">
            <i :class="item.icon"></i>
            <h4>{{ item.title }}</h4>
            <p>{{ item.desc }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMainStore } from '../store'

const router = useRouter()
const store = useMainStore()

const experiences = [
  { icon: 'fas fa-utensils', title: 'Fine Dining', desc: 'Three restaurants, including a Michelin-starred establishment with panoramic city views.' },
  { icon: 'fas fa-spa', title: 'Sky Spa', desc: 'Rejuvenate in our glass-walled spa with treatments inspired by ancient Indonesian rituals.' },
  { icon: 'fas fa-swimming-pool', title: 'Infinity Pool', desc: 'An iconic rooftop pool that seems to merge with the Jakarta skyline — day and night.' },
  { icon: 'fas fa-concierge-bell', title: 'Personal Butler', desc: 'Dedicated 24/7 butler service for every suite, anticipating your every need.' }
]

const amenities = [
  { icon: 'fas fa-dumbbell', title: 'Fitness Center', desc: '24/7 gym with personal trainers' },
  { icon: 'fas fa-wifi', title: 'High-Speed WiFi', desc: '1 Gbps fiber throughout' },
  { icon: 'fas fa-car', title: 'Valet Parking', desc: 'Complimentary for guests' },
  { icon: 'fas fa-child', title: 'Kids\' Club', desc: 'Supervised activities for young guests' },
  { icon: 'fas fa-business-time', title: 'Business Lounge', desc: 'Private meeting rooms & workstations' },
  { icon: 'fas fa-shuttle-van', title: 'Airport Transfer', desc: 'Luxury car service available' }
]

const handleBookNow = () => {
  if (!store.isLoggedIn) {
    store.openAuthModal('login')
  } else {
    router.push('/rooms')
  }
}

const selectRoom = (roomId) => {
  if (!store.isLoggedIn) {
    store.pendingRoomId = roomId
    store.openAuthModal('login')
    return
  }
  store.selectedRoomId = roomId
  router.push('/booking')
}

// Intersection Observer for reveal
const onReveal = (el) => {
  if (el) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible')
        }
      })
    }, { threshold: 0.15, rootMargin: '0px 0px -30px 0px' })
    observer.observe(el)
  }
}

// Register directive manually
const vIntersect = {
  mounted(el, binding) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          if (typeof binding.value === 'function') {
            binding.value(el)
          } else {
            el.classList.add('visible')
          }
        }
      })
    }, { threshold: 0.15, rootMargin: '0px 0px -30px 0px' })
    observer.observe(el)
    el._observer = observer
  },
  unmounted(el) {
    if (el._observer) {
      el._observer.disconnect()
    }
  }
}

// For backwards compatibility
onMounted(() => {
  setTimeout(() => {
    document.querySelectorAll('.reveal').forEach(el => {
      if (el.getBoundingClientRect().top < window.innerHeight + 100) {
        el.classList.add('visible')
      }
    })
  }, 300)
})
</script>

<style scoped>
.page {
  display: block;
  animation: fadePage 0.6s ease forwards;
}
@keyframes fadePage {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

.hero-home {
  min-height: 100vh;
  display: flex;
  align-items: center;
  position: relative;
  background: linear-gradient(135deg, rgba(10, 10, 10, 0.7) 0%, rgba(10, 10, 10, 0.2) 80%),
    url('https://images.pexels.com/photos/2694036/pexels-photo-2694036.jpeg?auto=compress&cs=tinysrgb&w=1600') center/cover no-repeat;
  background-attachment: fixed;
  padding: 140px 0 80px;
}
.hero-home::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 30% 50%, rgba(200, 161, 101, 0.08) 0%, transparent 70%);
  z-index: 1;
}
.hero-home>* { position: relative; z-index: 2; }
.hero-content { max-width: 760px; }
.hero-content .badge {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: rgba(200, 161, 101, 0.15);
  backdrop-filter: blur(8px);
  padding: 8px 24px;
  border-radius: 50px;
  font-size: 0.75rem;
  letter-spacing: 1.5px;
  color: var(--gold-light);
  border: 1px solid rgba(200, 161, 101, 0.25);
  margin-bottom: 24px;
  font-weight: 500;
}
.hero-content .badge i { color: var(--gold); }
.hero-content h1 {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(3.2rem, 8vw, 5.6rem);
  font-weight: 700;
  line-height: 1.05;
  color: var(--white);
  letter-spacing: -1px;
}
.hero-content h1 span { color: var(--gold); }
.hero-content p {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 20px 0 40px;
  max-width: 520px;
  font-weight: 300;
  line-height: 1.8;
}
.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.experiences { background: var(--white); }
.exp-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 32px;
  margin-top: 48px;
}
.exp-card {
  background: var(--cream);
  border-radius: var(--radius);
  padding: 36px 28px;
  text-align: center;
  transition: var(--transition);
  border: 1px solid transparent;
}
.exp-card:hover {
  transform: translateY(-8px);
  border-color: var(--gold);
  box-shadow: var(--shadow-gold);
  background: var(--white);
}
.exp-card .icon {
  font-size: 2.8rem;
  color: var(--gold);
  margin-bottom: 16px;
  display: inline-block;
}
.exp-card h3 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--dark);
}
.exp-card p { color: #666; font-size: 0.95rem; margin-top: 8px; }

.rooms-preview { background: var(--cream); }
.room-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
  margin-top: 48px;
}
.room-card {
  background: var(--white);
  border-radius: var(--radius);
  overflow: hidden;
  transition: var(--transition);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}
.room-card:hover {
  transform: translateY(-12px);
  box-shadow: var(--shadow-dark);
}
.room-card .img-wrap {
  height: 260px;
  overflow: hidden;
  position: relative;
}
.room-card .img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: var(--transition);
}
.room-card:hover .img-wrap img { transform: scale(1.05); }
.room-card .img-wrap .badge-room {
  position: absolute;
  top: 16px;
  right: 16px;
  background: var(--gold);
  color: var(--white);
  padding: 4px 16px;
  border-radius: 50px;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}
.room-card .body { padding: 28px 28px 32px; }
.room-card .body h3 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--dark);
}
.room-card .body .price {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--gold);
  margin: 4px 0 8px;
}
.room-card .body .price small {
  font-size: 0.9rem;
  font-weight: 400;
  color: #888;
}
.room-card .body p {
  color: #666;
  font-size: 0.95rem;
  margin: 8px 0 20px;
}
.room-card .body .btn { width: 100%; padding: 14px; font-size: 0.85rem; }

.amenities-home {
  background: var(--dark);
  color: rgba(255, 255, 255, 0.85);
}
.amenities-home .section-title { color: var(--white); }
.amenities-home .section-subtitle { color: rgba(255, 255, 255, 0.6); }
.amenity-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 40px;
  margin-top: 48px;
  text-align: center;
}
.amenity-item {
  padding: 20px;
  border-radius: var(--radius);
  border: 1px solid rgba(255, 255, 255, 0.06);
  transition: var(--transition);
}
.amenity-item:hover {
  border-color: var(--gold);
  background: rgba(200, 161, 101, 0.06);
}
.amenity-item i {
  font-size: 2.6rem;
  color: var(--gold);
  margin-bottom: 12px;
}
.amenity-item h4 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--white);
}
.amenity-item p {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 4px;
}

@media (max-width:768px) {
  .hero-home { background-attachment: scroll; padding: 120px 0 60px; }
  .room-grid { grid-template-columns: 1fr; }
  .exp-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width:480px) {
  .exp-grid { grid-template-columns: 1fr; }
  .hero-content h1 { font-size: 2.4rem; }
  .hero-content p { font-size: 1rem; }
}
</style>