# AI-Powered Course Generator

An intelligent system that automatically generates interactive educational mini-games for any topic using AI agents.

## 🎯 Overview

The Course Generator takes any educational topic (e.g., "trigonometry", "photosynthesis", "world history") and automatically:

1. **Plans** the learning content by breaking it into subtopics and objectives
2. **Generates** 2-3 interactive mini-games (5-10 points each) as standalone HTML files
3. **Validates** and fixes any issues in the generated games
4. **Serves** them through a modern, purple-themed web interface

## 🏗️ System Architecture

### Agent-Based Architecture (Google ADK)

- **Course Generator Agent** (Main Coordinator)
  - **Topic Planner Agent** - Creates structured learning plans
  - **Game Generator Agent** - Generates HTML/CSS/JS game files
  - **Validator Agent** - Checks and fixes generated games

### Game Templates

- **Quick Quiz** - Multiple choice questions (10 points)
- **Drag & Match** - Match terms to definitions (8 points)
- **Fill-in** - Complete the blanks (8 points)
- **Target Number** - Numeric problem solving (10 points)
- **Ordering** - Arrange items in sequence (10 points)
- **Flash Round** - Timed true/false (10 points)

### Tech Stack

- **Backend**: Node.js + Express (API & static server)
- **Frontend**: Plain HTML/CSS/JS with Tailwind CDN
- **AI**: Google ADK (Agent Development Kit)
- **Styling**: Purple theme with accessibility features
- **Icons**: Lucide icons
- **Storage**: File-based (no database required)

## 🚀 Quick Start

### Prerequisites

- Node.js (v16+)
- Python 3.8+
- Google ADK access

### Installation

1. **Install Node.js dependencies:**
   ```bash
   cd course-generator
   npm install
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the web server:**
   ```bash
   npm start
   # or
   node server.js
   ```

4. **Access the application:**
   - Open http://localhost:3000
   - Browse existing topics or generate new ones

### Generate a New Topic

**Via Web Interface:**
1. Go to http://localhost:3000
2. Enter a topic in the input field
3. Click "Generate"
4. Wait 1-2 minutes for AI generation
5. Play the generated games!

**Via Python Script:**
```bash
cd course-generator
python main.py "your topic here"
```

## 📁 Project Structure

```
course-generator/
├── server.js                 # Express server
├── package.json              # Node dependencies
├── requirements.txt          # Python dependencies
├── main.py                   # Python CLI entry point
│
├── course_generator_agent/   # AI Agents
│   ├── agent.py             # Main coordinator agent
│   ├── prompts.py           # System prompts
│   └── sub_agents/
│       ├── topic_planner.py    # Learning plan generation
│       ├── game_generator.py   # Game file creation
│       └── validator.py        # Quality assurance
│
├── game_templates/           # Reusable game templates
│   └── templates.py         # HTML/CSS/JS templates
│
└── public/                  # Web assets
    ├── index.html          # Topic browser
    ├── topic.html          # Individual topic page
    ├── styles/theme.css    # Purple theme + utilities
    ├── scripts/common.js   # Shared game utilities
    └── topics/             # Generated content
        └── {topic-name}/
            ├── metadata.json
            ├── game-{slug}.html
            └── assets/ (optional)
```

## 🎮 Game Features

### Consistent Experience
- **Purple Theme** - Modern, professional appearance
- **Accessibility** - ARIA labels, keyboard navigation, focus management
- **Responsive Design** - Works on desktop and mobile
- **Progress Tracking** - Local storage for user progress
- **Score System** - 5-10 points per game with feedback

### Game Types

1. **Quick Quiz** (MCQ)
   - 5 questions, 2 points each
   - Immediate feedback
   - Progress tracking

2. **Drag & Match**
   - Match terms to definitions
   - Visual feedback for correct/incorrect
   - Partial credit scoring

3. **Fill-in** (Planned)
   - Short answer completion
   - Auto-grading with tolerance

4. **Target Number** (Planned)
   - Numeric problem solving
   - Math expression evaluation

5. **Ordering** (Planned)
   - Sequence arrangement
   - Drag-and-drop interface

6. **Flash Round** (Planned)
   - Timed true/false questions
   - Rapid-fire gameplay

## 🔧 API Endpoints

### Web API
- `GET /` - Topic browser homepage
- `GET /topics` - List all available topics
- `GET /topics/{topic}` - Individual topic page
- `GET /topics/{topic}/{game}` - Play specific game

### REST API
- `GET /api/topics` - Get all topics metadata (JSON)
- `GET /api/topics/{topic}` - Get specific topic metadata (JSON)
- `POST /api/generate/{topic}` - Generate new topic (triggers AI agents)

## 🧪 Example Usage

### Sample Topics
The system can generate games for any educational topic:

- **Mathematics**: "trigonometry", "algebra", "calculus"
- **Science**: "photosynthesis", "atomic structure", "genetics"
- **History**: "world war 2", "ancient rome", "industrial revolution"
- **Language**: "grammar basics", "vocabulary building", "pronunciation"
- **Technology**: "computer networks", "databases", "web development"

### Generated Content Structure
```json
{
  "topic": "Trigonometry",
  "description": "Basic trigonometry concepts...",
  "games": [
    {
      "slug": "angle-basics",
      "title": "Angle Basics Quiz",
      "type": "quiz",
      "maxScore": 10
    },
    {
      "slug": "trig-ratios", 
      "title": "Match Trig Ratios",
      "type": "drag-match",
      "maxScore": 8
    }
  ],
  "createdAt": "2025-10-08T00:00:00Z"
}
```

## 🎨 Design System

### Purple Theme
- **Primary**: `#7c3aed` (Violet 600)
- **Primary Dark**: `#5b21b6` (Violet 800)
- **Primary Light**: `#a855f7` (Violet 500)

### Components
- **Cards**: Rounded, shadowed containers
- **Buttons**: Consistent hover/focus states
- **Progress Bars**: Visual feedback
- **Badges**: Score/status indicators
- **Toast Notifications**: User feedback

### Accessibility
- **WCAG 2.1 AA** compliance target
- **Keyboard Navigation** throughout
- **Screen Reader** support
- **High Contrast** mode support
- **Reduced Motion** preferences

## 🔍 Quality Assurance

### Automated Validation
The Validator Agent checks each generated game for:

- **Technical**: Valid HTML, required imports, JavaScript functionality
- **Accessibility**: ARIA labels, keyboard support, focus management  
- **Scoring**: Proper point values (5-10), completion detection
- **Design**: Theme consistency, responsive layout
- **User Experience**: Clear instructions, error handling

### Manual Testing Checklist
- [ ] Game loads without errors
- [ ] All interactive elements work
- [ ] Scoring calculates correctly
- [ ] Progress saves/loads properly
- [ ] Responsive on mobile devices
- [ ] Keyboard navigation works
- [ ] Screen reader compatibility

## 🚧 Development Status

### ✅ Completed (MVP)
- [x] Agent-based architecture with Google ADK
- [x] Topic Planner Agent (learning plan generation)
- [x] Game Generator Agent (HTML file creation)  
- [x] Validator Agent (quality assurance)
- [x] Express server with API endpoints
- [x] Purple-themed design system
- [x] Topic browser interface
- [x] Quick Quiz game template
- [x] Drag & Match game template
- [x] Sample trigonometry topic

### 🔄 In Progress
- [ ] More game templates (Fill-in, Target Number, etc.)
- [ ] Python-agent integration testing
- [ ] Automated topic generation pipeline

### 📋 Future Enhancements
- [ ] User accounts and progress sync
- [ ] Topic sharing and export
- [ ] Advanced game mechanics
- [ ] Multiple difficulty levels
- [ ] Collaborative learning features
- [ ] Analytics and insights
- [ ] Content moderation system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly (see checklist above)
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ using AI Agents • Powered by Interactive Learning**