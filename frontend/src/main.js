// main.js
import { createApp } from "vue";
import App from "./App.vue";
import "./styles/main.css";

// Register service worker (required for PWA context)
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/service-worker.js");
}

createApp(App).mount("#app");