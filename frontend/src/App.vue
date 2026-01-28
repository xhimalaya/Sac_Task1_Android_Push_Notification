<!-- App.vue -->
<template>
  <div class="app">
    <header class="header">
      <h1>PushNotify</h1>

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
    </main>
  </div>
</template>

<script>
export default {
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

    // Add one-time listener for first click to trigger notification permission
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
      // Optionally keep this for manual trigger or retry
      this.requestNotificationPermission();
    },
    async requestNotificationPermission() {
      if (!('Notification' in window) || !('serviceWorker' in navigator)) {
        alert('Notifications are not supported in this browser.');
        return;
      }

      // Check current permission status to avoid redundant prompts
      if (Notification.permission === 'granted') {
        await this.subscribeToPush();
        return;
      } else if (Notification.permission === 'denied') {
        alert('Notifications are blocked. Please enable them in browser settings.');
        return;
      }

      // Request permission
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
        await fetch("http://localhost:8001/api/subscribe", {
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