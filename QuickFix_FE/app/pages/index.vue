<script setup>
import { ref } from 'vue'

useHead({
  title: 'QuickFix - Your Trusted Online Pharmacy'
})

definePageMeta({
  layout: 'default' // Or use 'back' if you want it wrapped in your core layout framework
})

const api = useApi()

// --- UI STATES & CAROUSEL DRIVERS ---
const searchInput = ref('')
const selectedCategory = ref(null)

// Static Medical Banners
const promoBanners = ref([
  { title: '24/7 Professional Pharmacy Access', desc: 'Consult and fulfill your prescription drug profiles safely online.', color: 'bg-emerald-800' },
  { title: 'Fast App-Based Counter Pickup', desc: 'Skip the long waiting lines. Scan your verified prescription QR code and leave.', color: 'bg-cyan-800' }
])

// Featured Categories Grid Mapping
const mainCategories = ref([
  { id: 5, name: 'Obat Bebas', icon: 'mdi-pill', desc: 'Over-the-counter medicine' },
  { id: 6, name: 'Obat Keras', icon: 'mdi-alert-circle-outline', desc: 'Prescription required' },
  { id: 7, name: 'Suplemen', icon: 'mdi-bottle-tonic-plus-outline', desc: 'Vitamins & wellness' },
  { id: 8, name: 'Alat Kesehatan', icon: 'mdi-thermometer', desc: 'Medical equipment tools' }
])

// Featured Drugs Grid Showcase Products (Fallback Mock)
const featuredProducts = ref([
  { id: '1', name: 'Cetirizine 10mg', generic_name: 'Cetirizine HCl', price: 4334, dosage_form: 'Syrupy', category_name: 'Obat Bebas', requires_prescription: false, image: null },
  { id: '2', name: 'Amoxicillin 500mg', generic_name: 'Amoxicillin', price: 14500, dosage_form: 'Capsule', category_name: 'Obat Keras', requires_prescription: true, image: null },
  { id: '3', name: 'Antangin Habbatussauda', generic_name: 'Herbal Blend', price: 33144, dosage_form: 'Sachet', category_name: 'Alat Kesehatan', requires_prescription: false, image: null }
])

const handleQuickSearch = () => {
  if (searchInput.value.trim()) {
    // Navigate straight to your shop interface listing matching parameters
    navigateTo(`/shop?query=${searchInput.value.trim()}`)
  }
}
</script>

<template>
  <div class="w-full min-h-screen bg-[#faf7f2] text-slate-800 flex flex-col pt-14">
    
    <header class="w-full bg-white border-b border-slate-200 py-12 md:py-20 px-6 md:px-12 grid grid-cols-12 gap-8 items-center">
      <div class="col-span-12 md:col-span-7 flex flex-col gap-4">
        <v-chip class="w-fit font-bold" color="primary" size="small" variant="tonal">
          🚀 MODERN HEALTHCARE DISPENSARY
        </v-chip>
        <h1 class="text-4xl md:text-6xl font-black text-slate-900 tracking-tight leading-tight">
          Your Health, Secured. <br />
          <span class="text-[#1b5a5a]">Your Pharmacy, Simplified.</span>
        </h1>
        <p class="text-base md:text-lg text-slate-500 max-w-xl leading-relaxed">
          Access over 2,000 certified medical compounds, upload prescription profiles securely, and enjoy contactless counter checkout processing in seconds.
        </p>

        <div class="w-full max-w-2xl bg-slate-50 p-2 rounded-xl border border-slate-200 flex flex-col sm:flex-row gap-3 mt-4 items-center">
          <v-text-field
            v-model="searchInput"
            prepend-inner-icon="mdi-magnify"
            placeholder="Search by generic name, symptom, or barcode SKU..."
            variant="solo"
            flat
            hide-details
            density="comfortable"
            class="w-full bg-transparent border-0"
            @keyup.enter="handleQuickSearch"
          ></v-text-field>
          <v-btn color="#1b5a5a" class="text-white font-bold px-8 h-12" flat rounded="lg" @click="handleQuickSearch">
            Search Shop
          </v-btn>
        </div>
      </div>

      <div class="col-span-12 md:col-span-5 hidden md:flex justify-center relative">
        <div class="w-72 h-72 rounded-3xl bg-[#eedec9] absolute transform -rotate-6 scale-105 opacity-40"></div>
        <v-card class="w-80 p-6 rounded-3xl border border-slate-200 text-center relative bg-white" elevation="6">
          <div class="w-20 h-20 bg-[#1b5a5a] text-white rounded-2xl mx-auto flex items-center justify-center mb-4 shadow">
            <v-icon size="x-large">mdi-qrcode-scan</v-icon>
          </div>
          <h3 class="text-xl font-bold text-slate-800">Scan & Handoff</h3>
          <p class="text-xs text-slate-400 mt-2 px-4">
            Show your unified application checkout QR token directly to our cashiers for zero-line order pickups.
          </p>
          <div class="mt-6 p-3 bg-slate-50 border rounded-xl border-dashed font-mono text-sm text-slate-600 font-bold">
            # QF-2026-ACTIVE
          </div>
        </v-card>
      </div>
    </header>

    <section class="w-full py-12 px-6 md:px-12 max-w-7xl mx-auto flex flex-col gap-6">
      <div>
        <h2 class="text-2xl font-bold text-slate-900">Browse Medical Categories</h2>
        <p class="text-xs text-slate-400">Select specific product divisions to filter target treatments</p>
      </div>

      <div class="grid grid-cols-12 gap-4 w-full">
        <v-card
          v-for="cat in mainCategories"
          :key="cat.id"
          class="col-span-12 sm:col-span-6 md:col-span-3 pa-5 rounded-xl border border-slate-200/60 hover:border-cyan-700 hover:shadow-md transition-all cursor-pointer bg-white group flex items-start gap-4"
          elevation="0"
          @click="navigateTo(`/shop?category=${cat.id}`)"
        >
          <div class="p-3 rounded-xl bg-slate-50 text-slate-500 group-hover:bg-[#1b5a5a] group-hover:text-white transition-colors">
            <v-icon size="large">{{ cat.icon }}</v-icon>
          </div>
          <div class="flex flex-col">
            <h4 class="font-bold text-slate-800 group-hover:text-[#1b5a5a] transition-colors">{{ cat.name }}</h4>
            <p class="text-xs text-slate-400 mt-0.5 leading-tight">{{ cat.desc }}</p>
          </div>
        </v-card>
      </div>
    </section>


    <footer class="w-full mt-auto bg-slate-900 text-slate-400 py-12 px-6 md:px-12 border-t border-slate-800">
      <div class="max-w-7xl mx-auto grid grid-cols-12 gap-8 text-sm">
        <div class="col-span-12 md:col-span-5 flex flex-col gap-3">
          <div class="flex items-center gap-2 text-white font-black text-xl">
            <v-icon color="cyan-400">mdi-shield-plus-outline</v-icon>
            <span>QuickFix E-Pharmacy</span>
          </div>
          <p class="text-xs text-slate-500 max-w-sm leading-relaxed">
            Integrated digital apothecary workspace environment engineered for Klinik Makmur Jaya. Licensed distribution under Indonesian National Pharmaceutical Regulatory Guidelines (BNSP 2026).
          </p>
        </div>

        <div class="col-span-6 md:col-span-3 flex flex-col gap-2">
          <h5 class="text-white font-bold text-xs uppercase tracking-wider mb-2">Operational Bounds</h5>
          <p class="text-xs">🏪 Online Dispensation: 24/7 Hours</p>
          <p class="text-xs">🏥 Physical Counter Pickup: 08:00 - 21:00 WIB</p>
        </div>

        <div class="col-span-6 md:col-span-4 flex flex-col gap-2">
          <h5 class="text-white font-bold text-xs uppercase tracking-wider mb-2">Security Infrastructure Assurance</h5>
          <div class="flex items-center gap-1.5 text-emerald-400 text-xs font-mono">
            <v-icon size="small">mdi-lock-check-outline</v-icon> JWT HttpOnly Secured Sessions
          </div>
          <div class="flex items-center gap-1.5 text-emerald-400 text-xs font-mono mt-1">
            <v-icon size="small">mdi-database-check-outline</v-icon> Atomic Transaction Architecture
          </div>
        </div>
      </div>

      <div class="max-w-7xl mx-auto border-t border-slate-800/80 mt-10 pt-4 text-center text-xs text-slate-600">
        © 2026 QuickFix System Core Architecture. All Rights Reserved.
      </div>
    </footer>

  </div>
</template>