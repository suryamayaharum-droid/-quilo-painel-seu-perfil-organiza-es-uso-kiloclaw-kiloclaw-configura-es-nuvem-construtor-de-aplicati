/**
 * HoloOS JavaScript SDK
 * =====================
 */

class HoloOSClient {
  constructor(baseUrl = "http://localhost:8000") {
    this.baseUrl = baseUrl;
  }

  async chat(message, model = null) {
    const response = await fetch(`${this.baseUrl}/api/ai/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, model }),
    });
    return response.json();
  }

  async listModels() {
    const response = await fetch(`${this.baseUrl}/api/ai/models`);
    const data = await response.json();
    return data.models || [];
  }

  async storeMemory(content, tags = []) {
    const response = await fetch(`${this.baseUrl}/api/memory/store`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content, tags }),
    });
    return response.json();
  }

  async retrieveMemory(query, limit = 5) {
    const response = await fetch(
      `${this.baseUrl}/api/memory/retrieve?query=${encodeURIComponent(query)}&limit=${limit}`
    );
    const data = await response.json();
    return data.results || [];
  }

  async executeTool(tool, params = {}) {
    const response = await fetch(`${this.baseUrl}/api/tools/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tool, params }),
    });
    return response.json();
  }

  async createGoal(description, strategy = "chain_of_thought") {
    const response = await fetch(`${this.baseUrl}/api/planning/goal`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description, strategy }),
    });
    return response.json();
  }

  async getMetrics() {
    const response = await fetch(`${this.baseUrl}/api/monitoring/metrics`);
    return response.json();
  }

  async securityStatus() {
    const response = await fetch(`${this.baseUrl}/api/security/status`);
    return response.json();
  }

  async listModules() {
    const response = await fetch(`${this.baseUrl}/api/modules`);
    const data = await response.json();
    return data.modules || [];
  }

  // WebSocket for real-time
  connectWebSocket(callback) {
    this.ws = new WebSocket(`${this.baseUrl.replace("http", "ws")}/ws`);
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      callback(data);
    };
  }

  disconnectWebSocket() {
    if (this.ws) this.ws.close();
  }
}

// Export for different module systems
if (typeof module !== "undefined" && module.exports) {
  module.exports = HoloOSClient;
}
if (typeof window !== "undefined") {
  window.HoloOSClient = HoloOSClient;
}

export default HoloOSClient;