# MindMate+ | Mental Health Companion

A comprehensive mental health tracking and support application built with React, TypeScript, and Tailwind CSS. This frontend application works with the MindMate backend to provide a complete mental health support solution.

## Features

- 🔒 **Secure Authentication**: User registration, login, and profile management
- 💊 **Medication Management**: Track medications, dosages, and schedules
- ⏰ **Reminder System**: Get notified when it's time to take medications
- 😊 **Mood Tracking**: Monitor mood patterns over time with visual statistics
- 📝 **Journal**: Record thoughts and feelings with searchable entries
- 🧠 **Mental Health Assessments**: Take standardized assessments like PHQ-9 and GAD-7
- 🤖 **AI-powered Support**: Get personalized coping strategies and mental health support
- 📚 **Resources**: Access educational content and helpful resources
- 📊 **Comprehensive Dashboard**: View all your health data in one place
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices

## Prerequisites

- Node.js (v18 or higher)
- npm (v9 or higher)
- Backend API running on http://localhost:8001

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/Abhigyan-Truce/MindMate.git
cd MindMate
```

2. Navigate to the frontend directory:
```bash
cd frontend
```

3. Install dependencies:
```bash
npm install
```

4. Create a `.env` file in the frontend directory with the following variables:
```env
VITE_API_URL=http://localhost:8001
```

5. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173` (or another port if 3000 is in use)

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── layout/       # Layout components (header, footer, etc.)
│   │   └── ui/           # UI components (buttons, inputs, etc.)
│   ├── pages/            # Page components organized by feature
│   │   ├── ai/           # AI support features
│   │   ├── auth/         # Authentication pages
│   │   ├── journal/      # Journal feature
│   │   ├── medications/  # Medication management
│   │   ├── mood/         # Mood tracking
│   │   └── reminders/    # Reminder system
│   ├── services/         # API service functions
│   ├── store/            # Global state management with Zustand
│   └── types/            # TypeScript type definitions
├── public/               # Static assets
└── index.html            # Entry HTML file
```

## Key Components

- **Authentication**: Secure login, registration, and profile management
- **Dashboard**: Overview of medications, mood, reminders, and journal entries
- **Medication Management**: Add, edit, and delete medications with details
- **Reminder System**: Schedule and manage medication reminders
- **Mood Tracking**: Record daily mood with notes and view trends
- **Journal**: Write and manage journal entries with mood association
- **AI Support**: Chat with AI assistant for mental health support
- **Settings**: Manage user preferences and notification settings

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Tech Stack

- **Framework**: React 18
- **Build Tool**: Vite
- **Language**: TypeScript
- **Styling**: Tailwind CSS with custom design system
- **State Management**: Zustand
- **Routing**: React Router v6
- **Form Handling**: React Hook Form
- **HTTP Client**: Axios
- **Data Visualization**: Chart.js with react-chartjs-2
- **Date Handling**: date-fns
- **Icons**: Lucide React
- **Markdown Rendering**: React Markdown

## API Integration

The application integrates with a RESTful backend API running on `http://localhost:8001`. The API provides endpoints for:

- User authentication and profile management
- Medication management
- Reminder scheduling and notifications
- Mood tracking and statistics
- Journal entries
- AI-powered mental health support

Ensure the backend server is running before starting the frontend application. See the main README for backend setup instructions.

## Browser Support

The application is optimized for modern browsers:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

MIT License - feel free to use this project for personal or commercial purposes.