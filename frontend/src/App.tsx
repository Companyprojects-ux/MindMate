import { useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';

// Pages
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import Dashboard from './pages/Dashboard';
import MedicationList from './pages/medications/MedicationList';
import MedicationDetail from './pages/medications/MedicationDetail';
import MedicationForm from './pages/medications/MedicationForm';
import ReminderList from './pages/reminders/ReminderList';
import MoodTracker from './pages/mood/MoodTracker';
import MoodStats from './pages/mood/MoodStats';
import JournalList from './pages/journal/JournalList';
import JournalForm from './pages/journal/JournalForm';
import AiChat from './pages/ai/AiChat';

// Components
import Layout from './components/layout/Layout';
import { useAuthStore } from './store/authStore';
import NotFound from './pages/NotFound';

function App() {
  const { isAuthenticated, checkAuth } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  // Protected route wrapper
  const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
    if (!isAuthenticated) {
      // Save the location they were trying to access
      return <Navigate to="/login" state={{ from: location }} replace />;
    }
    return <>{children}</>;
  };

  // Public route wrapper (redirects if already authenticated)
  const PublicRoute = ({ children }: { children: React.ReactNode }) => {
    if (isAuthenticated) {
      return <Navigate to="/dashboard" replace />;
    }
    return <>{children}</>;
  };

  return (
    <Routes>
      {/* Public routes */}
      <Route
        path="/login"
        element={
          <PublicRoute>
            <Login />
          </PublicRoute>
        }
      />
      <Route
        path="/register"
        element={
          <PublicRoute>
            <Register />
          </PublicRoute>
        }
      />

      {/* Protected routes */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        
        {/* Medication routes */}
        <Route path="medications" element={<MedicationList />} />
        <Route path="medications/:id" element={<MedicationDetail />} />
        <Route path="medications/new" element={<MedicationForm />} />
        <Route path="medications/edit/:id" element={<MedicationForm />} />
        
        {/* Reminder routes */}
        <Route path="reminders" element={<ReminderList />} />
        
        {/* Mood routes */}
        <Route path="mood" element={<MoodTracker />} />
        <Route path="mood/stats" element={<MoodStats />} />
        
        {/* Journal routes */}
        <Route path="journal" element={<JournalList />} />
        <Route path="journal/new" element={<JournalForm />} />
        <Route path="journal/edit/:id" element={<JournalForm />} />
        
        {/* AI routes */}
        <Route path="ai-chat" element={<AiChat />} />
      </Route>

      {/* Fallback route */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default App;