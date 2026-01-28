const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
const VAPID_PUBLIC_KEY = import.meta.env.VITE_VAPID_PUBLIC_KEY;
console.log(">>>>>>>>>>>>>>>>>  ", BACKEND_URL)
console.log(">>>>>>>>>>>>>>>>>  ", VAPID_PUBLIC_KEY)

/* Convert base64 VAPID key */
function urlBase64ToUint8Array(base64String) {
  const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding)
    .replace(/-/g, "+")
    .replace(/_/g, "/");

  const rawData = window.atob(base64);
  return Uint8Array.from([...rawData].map(char => char.charCodeAt(0)));
}

/* Main entry: register + subscribe + send to backend */
export async function registerPushService() {
  if (!("serviceWorker" in navigator)) {
    throw new Error("Service Worker not supported");
  }

  /* 1️⃣ Register service worker */
  const registration = await navigator.serviceWorker.register(
    "/service-worker.js"
  );

  /* 2️⃣ Ask notification permission */
  const permission = await Notification.requestPermission();
  if (permission !== "granted") {
    throw new Error("Notification permission denied");
  }

  /* 3️⃣ Reuse existing subscription if present */
  let subscription = await registration.pushManager.getSubscription();

  if (!subscription) {
    subscription = await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY)
    });
  }

  /* 4️⃣ Send subscription to backend */
  await fetch(`${BACKEND_URL}/api/subscribe`, {
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

  return subscription;
}
