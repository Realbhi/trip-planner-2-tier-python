const express = require("express");
const { createProxyMiddleware } = require("http-proxy-middleware");
const path = require("path");

const app = express();
const PORT = 3000;

const BACKEND_URL = process.env.BACKEND_URL || "http://trip-backend-service:5000";
console.log(`[frontend] proxying /api and /health to ${BACKEND_URL}`);

// Proxy /api and /health straight to backend pod
app.use(
  ["/api", "/health"],
  createProxyMiddleware({
    target: BACKEND_URL,
    changeOrigin: true,
    on: {
      error: (err, req, res) => {
        res.status(502).json({ error: "Backend unreachable", detail: err.message });
      },
    },
  })
);

// Static UI
app.use(express.static(path.join(__dirname, "../public")));

// Friendly aliases  GET /locations?location=Goa  →  backend /api/locations/Goa
const aliases = [
  { alias: "/locations", api: "/api/locations" },
  { alias: "/mustvisit", api: "/api/mustvisit" },
  { alias: "/weather",   api: "/api/weather"   },
  { alias: "/itinerary", api: "/api/itinerary" },
];

aliases.forEach(({ alias, api }) => {
  app.get(alias, async (req, res) => {
    const loc = req.query.location;
    const url = loc
      ? `${BACKEND_URL}${api}/${encodeURIComponent(loc)}`
      : `${BACKEND_URL}${api}`;
    try {
      const r = await fetch(url);
      const data = await r.json();
      res.status(r.status).json(data);
    } catch (err) {
      res.status(502).json({ error: "Backend unreachable", detail: err.message });
    }
  });
});

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "../public/index.html"));
});

app.listen(PORT, () =>
  console.log(`[trip-planner frontend] http://0.0.0.0:${PORT}`)
);
