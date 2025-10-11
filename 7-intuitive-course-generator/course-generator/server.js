const express = require("express");
const path = require("path");
const fs = require("fs").promises;
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

// Routes

// Home page - serve the topic browser
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// API: Get all available topics
app.get("/api/topics", async (req, res) => {
  try {
    res.set("Cache-Control", "no-store");
    const topicsDir = path.join(__dirname, "public", "topics");

    // Check if topics directory exists
    try {
      await fs.access(topicsDir);
    } catch {
      return res.json([]);
    }

    const entries = await fs.readdir(topicsDir, { withFileTypes: true });
    const topics = [];

    for (const entry of entries) {
      if (entry.isDirectory()) {
        const topicPath = path.join(topicsDir, entry.name);
        const metadataPath = path.join(topicPath, "metadata.json");

        try {
          const metadataContent = await fs.readFile(metadataPath, "utf-8");
          const metadata = JSON.parse(metadataContent);
          topics.push({
            slug: entry.name,
            ...metadata,
          });
        } catch (error) {
          // If no metadata, create basic info
          topics.push({
            slug: entry.name,
            topic: entry.name.replace(/-/g, " "),
            description: `Learning games for ${entry.name.replace(/-/g, " ")}`,
            games: [],
            createdAt: new Date().toISOString(),
          });
        }
      }
    }

    res.json(topics);
  } catch (error) {
    console.error("Error fetching topics:", error);
    res.status(500).json({ error: "Failed to fetch topics" });
  }
});

// API: Get specific topic metadata
app.get("/api/topics/:topic", async (req, res) => {
  try {
    res.set("Cache-Control", "no-store");
    const topicSlug = req.params.topic;
    const metadataPath = path.join(
      __dirname,
      "public",
      "topics",
      topicSlug,
      "metadata.json"
    );

    const metadataContent = await fs.readFile(metadataPath, "utf-8");
    const metadata = JSON.parse(metadataContent);

    res.json({
      slug: topicSlug,
      ...metadata,
    });
  } catch (error) {
    console.error(`Error fetching topic ${req.params.topic}:`, error);
    res.status(404).json({ error: "Topic not found" });
  }
});

// Serve topic pages
app.get("/topics", (req, res) => {
  // Redirect to home where topic list is shown
  res.redirect(302, "/");
});

app.get("/topics/:topic", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "topic.html"));
});

// Serve individual games
app.get("/topics/:topic/:game", async (req, res) => {
  try {
    const { topic, game } = req.params;
    const gamePath = path.join(
      __dirname,
      "public",
      "topics",
      topic,
      `game-${game}.html`
    );

    // Check if file exists
    await fs.access(gamePath);
    res.sendFile(gamePath);
  } catch (error) {
    res.status(404).send(`
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Game Not Found</title>
        <script src="https://cdn.tailwindcss.com/3.4.0"></script>
      </head>
      <body class="bg-gradient-to-br from-purple-50 to-indigo-100 min-h-screen flex items-center justify-center">
        <div class="bg-white rounded-xl shadow-lg p-8 text-center max-w-md">
          <h1 class="text-2xl font-bold text-gray-900 mb-4">Game Not Found</h1>
          <p class="text-gray-600 mb-6">The requested game could not be found.</p>
          <a href="/topics/${req.params.topic}" class="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
            Back to Topic
          </a>
        </div>
      </body>
      </html>
    `);
  }
});

// API: Generate new topic (for development/testing)
app.post("/api/generate/:topic", async (req, res) => {
  try {
    const topic = req.params.topic;

    // This would integrate with the Python agent system
    // For now, return a placeholder response
    res.json({
      success: true,
      message: `Course generation for "${topic}" initiated`,
      topic: topic,
      status: "generating",
    });
  } catch (error) {
    console.error("Error generating topic:", error);
    res.status(500).json({ error: "Failed to generate topic" });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error("Server error:", err);
  res.status(500).json({ error: "Internal server error" });
});

// 404 handler
app.use((req, res) => {
  res.status(404).send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Page Not Found</title>
      <script src="https://cdn.tailwindcss.com/3.4.0"></script>
    </head>
    <body class="bg-gradient-to-br from-purple-50 to-indigo-100 min-h-screen flex items-center justify-center">
      <div class="bg-white rounded-xl shadow-lg p-8 text-center max-w-md">
        <h1 class="text-2xl font-bold text-gray-900 mb-4">Page Not Found</h1>
        <p class="text-gray-600 mb-6">The requested page could not be found.</p>
        <a href="/" class="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
          Go Home
        </a>
      </div>
    </body>
    </html>
  `);
});

// Start server
app.listen(PORT, () => {
  console.log(`🎮 Course Generator running on http://localhost:${PORT}`);
  console.log(`📚 Topics available at http://localhost:${PORT}/topics`);
  console.log(`🔧 API endpoints at http://localhost:${PORT}/api/topics`);
});
