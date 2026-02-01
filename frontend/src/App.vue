<!-- App.vue -->
<template>
  <div class="app">
    <header class="header">
      <h1>Push Notification</h1>

      <button class="bell" @click="onBellClick">
        🔔
      </button>
    </header>

    <main class="content">
      <p class="placeholder">
        No notifications yet
      </p>

      <button
        v-if="showInstallButton"
        class="install-btn"
        @click="installApp"
      >
        Install App
      </button>

      <!-- Survey Upload Section -->
      <div class="survey-section">
        <h2>Survey Data Upload</h2>
        <SurveyForm />
      </div>
    </main>
  </div>
</template>

<script>
import SurveyForm from './surveydataupload/SurveyForm.vue'

export default {
  components: {
    SurveyForm
  },
  data() {
    return {
      deferredPrompt: null,
      showInstallButton: false
    };
  },
  mounted() {
    window.addEventListener("beforeinstallprompt", (e) => {
      e.preventDefault();
      this.deferredPrompt = e;
      this.showInstallButton = true;
    });
    document.addEventListener('click', this.requestNotificationPermission, { once: true });
  },
  methods: {
    async installApp() {
      if (!this.deferredPrompt) return;
      this.deferredPrompt.prompt();
      await this.deferredPrompt.userChoice;
      this.deferredPrompt = null;
      this.showInstallButton = false;
    },
    onBellClick() {
      this.requestNotificationPermission();
    },
    async requestNotificationPermission() {
      if (!('Notification' in window) || !('serviceWorker' in navigator)) {
        alert('Notifications are not supported in this browser.');
        return;
      }

      if (Notification.permission === 'granted') {
        await this.subscribeToPush();
        return;
      } else if (Notification.permission === 'denied') {
        alert('Notifications are blocked. Please enable them in browser settings.');
        return;
      }

      const permission = await Notification.requestPermission();
      if (permission === 'granted') {
        await this.subscribeToPush();
      } else if (permission === 'denied') {
        alert('Notifications permission denied.');
      } else {
        alert('Notifications permission dismissed.');
      }
    },
    async subscribeToPush() {
        const registration = await navigator.serviceWorker.ready;

        const subscription = await registration.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: 'BIYwN-nVU1e9pp3B0gh_1Allx9--XdzkkGbjFSUyWX3LBtunOjMXD3-08cHPyDK5QhQi4yfBOJDoiPDfOq7BhBc'
        });

        console.log("Push subscription:", subscription);
        await fetch("https://whale-stunning-brightly.ngrok-free.app/api/subscribe", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            device_id: crypto.randomUUID(),
            endpoint: subscription.endpoint,
            keys: subscription.toJSON().keys,
            user_agent: navigator.userAgent
          })
        });

        alert("Notifications enabled!");
    }
  }
};
</script>

<style scoped>
/* Optional: Add some spacing for the new section */
.survey-section {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #ddd;
}

.survey-section h2 {
  margin-bottom: 1rem;
  color: #0d6efd;
}
</style>