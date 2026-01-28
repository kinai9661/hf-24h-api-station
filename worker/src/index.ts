export default {
  async fetch(request, env, ctx) {
    return new Response('Keep-alive worker is running.');
  },

  async scheduled(event, env, ctx) {
    // Replace with your actual HF Space URL
    // e.g., 'https://kinai9661-hf-24h-api-station.hf.space'
    const spaceUrl = 'https://huggingface.co/spaces/kines9661/loess'; 
    
    try {
      const response = await fetch(spaceUrl);
      console.log(`Pinged ${spaceUrl}: ${response.status}`);
    } catch (error) {
      console.error(`Failed to ping ${spaceUrl}:`, error);
    }
  }
};
