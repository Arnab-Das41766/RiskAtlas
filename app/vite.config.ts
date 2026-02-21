import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

// https://vite.dev/config/
export default defineConfig({
  base: './',
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },

  // ── Dev server settings (Cloudflare tunnel support) ─────────────────────
  server: {
    // Bind to all network interfaces so Cloudflared can forward traffic
    host: true,

    // Allow any *.trycloudflare.com subdomain (leading dot = wildcard match)
    allowedHosts: ['.trycloudflare.com'],

    // Proxy /api/* → localhost:8000 (server-side, so phones/tunnels work)
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
});
