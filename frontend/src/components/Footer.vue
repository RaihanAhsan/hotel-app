<template>
  <footer id="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <h4 style="font-size:1.8rem;">The Grand<span style="color:var(--gold);">Jakarta</span></h4>
          <p>A landmark of elegance in the heart of Indonesia's capital. Where timeless luxury meets modern sophistication.</p>
          <div style="margin-top:16px;display:flex;gap:16px;flex-wrap:wrap;">
            <span><i class="fas fa-map-pin" style="color:var(--gold);"></i> SCBD, South Jakarta 12190</span>
            <span><i class="fas fa-phone" style="color:var(--gold);"></i> +62 21 555 1234</span>
          </div>
        </div>
        <div>
          <h4>Quick Links</h4>
          <ul>
            <li><router-link to="/">Home</router-link></li>
            <li><a href="#" @click.prevent="scrollTo('rooms')">Suites</a></li>
            <li><a href="#" @click.prevent="scrollTo('amenities')">Amenities</a></li>
            <li><a href="#" @click.prevent="scrollTo('footer')">Contact</a></li>
          </ul>
        </div>
        <div>
          <h4>Support</h4>
          <ul>
            <li><a href="#">FAQ</a></li>
            <li><a href="#">Cancellation Policy</a></li>
            <li><a href="#">Privacy Policy</a></li>
            <li><a href="#">Contact Us</a></li>
          </ul>
        </div>
        <div>
          <h4>Connect</h4>
          <div class="socials" style="margin-bottom:16px;">
            <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
            <a href="#" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
            <a href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
            <a href="#" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
          </div>
          <p style="font-size:0.85rem;">&copy; 2026 The Grand Jakarta. All rights reserved.</p>
        </div>
      </div>
      <div class="footer-bottom">
        <span>Designed with <i class="fas fa-heart" style="color:var(--gold);"></i> in Jakarta</span>
        <span><i class="fas fa-globe-asia"></i> Indonesia · English</span>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const scrollTo = (id) => {
  if (router.currentRoute.value.path !== '/') {
    router.push('/')
    setTimeout(() => {
      const el = document.getElementById(id)
      if (el) el.scrollIntoView({ behavior: 'smooth' })
    }, 300)
  } else {
    const el = document.getElementById(id)
    if (el) el.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<style scoped>
footer {
  background: var(--dark-soft);
  color: rgba(255, 255, 255, 0.7);
  padding: 60px 0 30px;
  border-top: 1px solid rgba(255, 255, 255, 0.04);
}
.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 40px;
  margin-bottom: 40px;
}
.footer-grid h4 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.2rem;
  color: var(--white);
  margin-bottom: 16px;
}
.footer-grid p {
  font-size: 0.9rem;
  max-width: 320px;
  line-height: 1.8;
}
.footer-grid ul li { margin-bottom: 10px; }
.footer-grid ul a {
  font-size: 0.9rem;
  transition: var(--transition);
  cursor: pointer;
}
.footer-grid ul a:hover { color: var(--gold); }
.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  padding-top: 24px;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 0.85rem;
}
.socials {
  display: flex;
  gap: 18px;
}
.socials a {
  font-size: 1.2rem;
  transition: var(--transition);
  color: rgba(255, 255, 255, 0.5);
}
.socials a:hover {
  color: var(--gold);
  transform: translateY(-3px);
}
@media (max-width:1024px) {
  .footer-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width:768px) {
  .footer-grid { grid-template-columns: 1fr; gap: 30px; }
  .footer-bottom { flex-direction: column; align-items: center; text-align: center; }
}
</style>