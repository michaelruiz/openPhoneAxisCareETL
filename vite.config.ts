export default defineConfig({
  server: {
    proxy: {
      '/logs': 'http://localhost:8000',
      '/mock': 'http://localhost:8000',
      '/webhook': 'http://localhost:8000'
    }
  }
})
