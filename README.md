# IsoLo - Loop Architect

An AI-Aware React/TypeScript audio processing application built with **Spec-Driven Development** principles.

## Overview

Loop Architect is a modern audio processing tool that combines a React frontend with a Python backend to provide powerful stem separation and sound isolation capabilities. The project demonstrates AI-assisted development with clear specifications, strict type safety, and modular architecture.

### Key Features

- 🎵 **Audio Stem Separation** - Separate audio into vocals, drums, bass, guitar, piano, and other
- 🤖 **SAM Audio Integration** - Isolate ANY sound by name using AI (e.g., "saxophone solo", "crowd applause")
- 🎼 **Musical Analysis** - Automatic BPM and key detection with harmonic recommendations
- ✂️ **Loop Generation** - Slice audio into loops with customizable settings
- 🎨 **Modern UI** - React/TypeScript frontend with Tailwind CSS
- 🔒 **Strict TypeScript** - No `any` types, full type safety
- 🧩 **Modular Architecture** - Clean separation between frontend and backend

## Project Structure

```
IsoLo/
├── .github/
│   ├── instructions/          # Agent-specific instructions
│   └── copilot-instructions.md # Strict coding standards
├── backend/                   # Python backend
│   ├── app.py                # Gradio application
│   ├── sam_audio_integration.py # SAM Audio integration
│   ├── SAM_AUDIO_INTEGRATION.md # SAM Audio documentation
│   └── README.md             # Backend documentation
├── huggingface/              # Hugging Face Spaces deployment
│   ├── app.py                # Gradio app for HF Spaces
│   ├── requirements.txt      # Python dependencies
│   ├── README.md             # Space card & documentation
│   └── DEPLOYMENT.md         # Deployment guide
├── docs/
│   ├── specs/                 # Feature specifications (SOURCE OF TRUTH)
│   └── context/               # Project context & decisions
├── src/                       # React frontend
│   ├── components/
│   │   └── dynamic/           # Modular, reusable components
│   ├── App.tsx                # Root component
│   └── main.tsx               # Application entry point
├── AGENTS.md                  # AI agent coordination guide
├── GEMINI.md                  # Vision & architectural guidelines
└── package.json               # Frontend dependencies & scripts
```

## Getting Started

### Prerequisites

- **Node.js 18+** and npm (for frontend)
- **Python 3.8+** (for backend)

### Frontend Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Type check
npm run type-check

# Lint code
npm run lint
```

### Backend Installation

```bash
# Install Python dependencies
pip install numpy scipy soundfile librosa gradio matplotlib

# Optional: Install SAM Audio for named sound isolation
pip install sam-audio-infer

# Run the Gradio backend
python backend/app.py
```

See [backend/README.md](./backend/README.md) for detailed backend documentation.

### Hugging Face Spaces Deployment

Deploy Loop Architect to Hugging Face Spaces for public access:

```bash
# All deployment files are in the huggingface/ folder
cd huggingface/

# Validate the package
python validate.py

# See DEPLOYMENT.md for complete instructions
# Option 1: Upload files directly to HF Spaces
# Option 2: Clone and push via git
```

The `huggingface/` folder contains everything needed:
- 🚀 Ready-to-deploy Gradio app
- 📦 Complete Python dependencies
- 📖 Comprehensive deployment guide
- ✅ Pre-deployment validation script

See [huggingface/DEPLOYMENT.md](./huggingface/DEPLOYMENT.md) for step-by-step deployment instructions.

### Development Workflow

1. **Check Specifications** - Review `/docs/specs/` for feature requirements
2. **Read Context** - Understand patterns in `/docs/context/`
3. **Implement** - Follow strict TypeScript and Tailwind CSS standards (frontend) or type hints (backend)
4. **Test** - Verify changes work as expected
5. **Document** - Update specs and context as needed

## AI Agent Collaboration

This repository is optimized for AI-assisted development:

### For Gemini
- See `GEMINI.md` for vision and architectural guidelines
- Focus on specifications, architecture, and code reviews
- Create specs in `/docs/specs/` before implementation

### For GitHub Copilot
- See `.github/copilot-instructions.md` for strict standards
- Implement features based on specifications
- Follow TypeScript strict mode (no `any` types)
- Use Tailwind CSS exclusively for styling

### For All AI Agents
- See `AGENTS.md` for coordination protocol
- Specifications in `/docs/specs/` are the source of truth
- Follow Spec-Driven Development workflow
- Maintain modular, clean architecture

## Core Principles

### 1. Spec-Driven Development
Every feature begins with a specification in `/docs/specs/`. No implementation without a spec.

### 2. Type Safety First
TypeScript strict mode with zero `any` types. Let the compiler catch errors.

### 3. Modular Architecture
Components in `/src/components/dynamic/` are self-contained and composable.

### 4. Utility-First Styling
Tailwind CSS only - no separate CSS files, no inline styles (except dynamic values).

### 5. Accessibility
ARIA labels, semantic HTML, keyboard navigation - built-in from the start.

## Technology Stack

### Frontend
- **React 18** - UI library
- **TypeScript 5** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **ESLint** - Code linting with strict rules

### Backend
- **Python 3.8+** - Backend runtime
- **Gradio** - Web interface for audio processing
- **Librosa** - Audio analysis and processing
- **NumPy/SciPy** - Numerical computing
- **SAM Audio** (optional) - AI-powered sound isolation
- **PyTorch** - Deep learning framework (for SAM Audio)

## Documentation

- **[backend/README.md](./backend/README.md)** - Python backend documentation
- **[backend/SAM_AUDIO_INTEGRATION.md](./backend/SAM_AUDIO_INTEGRATION.md)** - SAM Audio integration guide
- **[huggingface/DEPLOYMENT.md](./huggingface/DEPLOYMENT.md)** - Hugging Face Spaces deployment guide
- **[huggingface/PACKAGE_INFO.md](./huggingface/PACKAGE_INFO.md)** - HF deployment package overview
- **[AGENTS.md](./AGENTS.md)** - AI agent coordination guide
- **[GEMINI.md](./GEMINI.md)** - Vision and architectural guidelines
- **[.github/copilot-instructions.md](./.github/copilot-instructions.md)** - Strict coding standards
- **[/docs/specs/](./docs/specs/)** - Feature specifications (source of truth)
- **[/docs/context/](./docs/context/)** - Project context and decisions

## Contributing

This project follows Spec-Driven Development:

1. Create or update specification in `/docs/specs/`
2. Implement according to the spec
3. Follow standards in `.github/copilot-instructions.md`
4. Update context documentation if new patterns emerge

## License

[Add your license here]

---

**Built with AI-Native Development principles** 🤖✨ 
