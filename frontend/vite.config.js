import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [
    vue({
      devTools: true
    })
  ],

  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url))
    }
  },

  server: {
    host: true,
    port: 5173,

    // required for ngrok + HTTPS
    hmr: {
      clientPort: 443
    },

    allowedHosts: [
      "whale-stunning-brightly.ngrok-free.app"
    ]
  }
});
