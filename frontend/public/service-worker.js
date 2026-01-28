/* ===============================
   Service Worker Lifecycle
================================ */

self.addEventListener("install", () => {
  // Activate immediately
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  // Take control of all open clients
  event.waitUntil(self.clients.claim());
});

/* ===============================
   Push Event Handler
================================ */

self.addEventListener("push", event => {
  let payload = {
    title: "Notification",
    message: "You have a new message",
    data: {}
  };

  if (event.data) {
    try {
      payload = event.data.json();
    } catch (err) {
      console.error("Failed to parse push payload", err);
    }
  }

  const title = payload.title || "Notification";

  const options = {
    body: payload.message || "",
    icon: "/icon-192.png",
    badge: "/icon-192.png",
    vibrate: [100, 50, 100],
    data: payload.data || {},
    tag: "push-notification",
    renotify: true
  };

  event.waitUntil(
    Promise.all([
      // Show system notification
      self.registration.showNotification(title, options),

      // Send message to open app (for UI update)
      self.clients.matchAll({ includeUncontrolled: true, type: "window" })
        .then(clients => {
          for (const client of clients) {
            client.postMessage({
              type: "PUSH_RECEIVED",
              message: payload.message || ""
            });
          }
        })
    ])
  );
});

/* ===============================
   Notification Click Handler
================================ */

self.addEventListener("notificationclick", event => {
  event.notification.close();

  const targetUrl = event.notification.data?.url || "/";

  event.waitUntil(
    self.clients.matchAll({ type: "window", includeUncontrolled: true })
      .then(clientList => {
        // Focus existing tab if open
        for (const client of clientList) {
          if (client.url.includes(targetUrl) && "focus" in client) {
            return client.focus();
          }
        }
        // Otherwise open a new tab
        if (self.clients.openWindow) {
          return self.clients.openWindow(targetUrl);
        }
      })
  );
});
