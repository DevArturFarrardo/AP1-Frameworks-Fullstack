import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Configuração do Vite (servidor de desenvolvimento do React).
// O proxy abaixo redireciona qualquer chamada que comece com "/api"
// para o servidor Flask em http://localhost:5000.
// Assim, no React, você só precisa chamar fetch("/api/products"),
// sem se preocupar com CORS nem com URL absoluta.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
      // Faz com que `<img src="/uploads/products/xyz.png">` no React
      // seja servido pelo Flask, que tem os arquivos no disco.
      "/uploads": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
    },
  },
});
