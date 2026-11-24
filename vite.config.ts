/// <reference types="vitest" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    rollupOptions: {
      // SINGLE_FILE=1 : version en un seul fichier (scripts/build-single.mjs)
      output: process.env.SINGLE_FILE === '1' ? { inlineDynamicImports: true } : {
        manualChunks: {
          react: ['react', 'react-dom', 'react-router-dom', 'zustand'],
          recharts: ['recharts'],
          candles: ['lightweight-charts'],
        },
      },
    },
  },
  test: { environment: 'node', include: ['src/**/*.test.ts'] },
});
