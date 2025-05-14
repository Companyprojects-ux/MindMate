import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, SmilePlus } from 'lucide-react';
import { moodService } from '../../services/moodService';
import { MoodStatistics, MoodEntry } from '../../types';
import Button from '../../components/ui/Button';
import Card from '../../components/ui/Card';
import { Bar, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const MoodStats = () => {
  const [statistics, setStatistics] = useState<MoodStatistics | null>(null);
  const [moodEntries, setMoodEntries] = useState<MoodEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const [statsData, entriesData] = await Promise.all([
          moodService.getMoodStatistics(),
          moodService.getMoodEntries()
        ]);
        setStatistics(statsData);
        setMoodEntries(entriesData);
      } catch (err) {
        setError('Failed to load mood statistics');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  // Prepare trend data for the line chart
  const trendData = {
    labels: statistics?.mood_trend.map(item => item.date) || [],
    datasets: [
      {
        label: 'Average Mood',
        data: statistics?.mood_trend.map(item => item.average_rating) || [],
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
        tension: 0.3,
      },
    ],
  };

  // Prepare tag data for the bar chart
  const tagData = {
    labels: statistics?.most_common_tags.map(item => item.tag) || [],
    datasets: [
      {
        label: 'Frequency',
        data: statistics?.most_common_tags.map(item => item.count) || [],
        backgroundColor: 'rgba(6, 182, 212, 0.7)',
        borderColor: 'rgb(6, 182, 212)',
        borderWidth: 1,
      },
    ],
  };

  // Chart options
  const lineOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Mood Trend Over Time',
      },
    },
    scales: {
      y: {
        min: 0,
        max: 10,
        title: {
          display: true,
          text: 'Mood Rating',
        },
      },
    },
  };

  const barOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Most Common Mood Tags',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Count',
        },
      },
    },
  };

  const getMoodEmoji = (rating: number) => {
    const moodEmojis = ['😞', '😟', '😐', '🙂', '😊', '😄', '😃', '😁', '🤩', '😍'];
    return moodEmojis[Math.min(Math.floor(rating) - 1, 9)];
  };

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
        <Link to="/mood" className="inline-flex items-center text-primary-600 hover:text-primary-700">
          <ArrowLeft size={16} className="mr-1" /> Back to mood tracker
        </Link>
        
        <Link to="/mood">
          <Button leftIcon={<SmilePlus size={16} />}>
            Record Mood
          </Button>
        </Link>
      </div>

      <h1 className="text-2xl font-bold mb-6">Mood Statistics</h1>

      {error && (
        <div className="bg-error-50 border border-error-200 text-error-700 px-4 py-3 rounded-md mb-6">
          <p>{error}</p>
        </div>
      )}

      {isLoading ? (
        <div className="grid gap-6 grid-cols-1 md:grid-cols-2 lg:grid-cols-4 mb-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="animate-pulse bg-white rounded-lg shadow-card p-6">
              <div className="h-4 bg-gray-200 rounded w-1/3 mb-2"></div>
              <div className="h-6 bg-gray-200 rounded w-1/2"></div>
            </div>
          ))}
          <div className="md:col-span-2 animate-pulse bg-white rounded-lg shadow-card p-6">
            <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
            <div className="h-40 bg-gray-200 rounded"></div>
          </div>
          <div className="md:col-span-2 animate-pulse bg-white rounded-lg shadow-card p-6">
            <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
            <div className="h-40 bg-gray-200 rounded"></div>
          </div>
        </div>
      ) : (
        <>
          {statistics && (
            <>
              <div className="grid gap-6 grid-cols-1 md:grid-cols-2 lg:grid-cols-4 mb-6">
                <Card className="animate-fadeIn">
                  <h2 className="text-sm font-medium text-gray-500 mb-1">Average Mood</h2>
                  <div className="flex items-center">
                    <span className="text-3xl font-bold text-primary-700">{statistics.average_rating.toFixed(1)}</span>
                    <span className="text-3xl ml-2">{getMoodEmoji(statistics.average_rating)}</span>
                  </div>
                </Card>
                
                <Card className="animate-fadeIn" style={{ animationDelay: '100ms' }}>
                  <h2 className="text-sm font-medium text-gray-500 mb-1">Highest Mood</h2>
                  <div className="flex items-center">
                    <span className="text-3xl font-bold text-success-600">{statistics.highest_rating}</span>
                    <span className="text-3xl ml-2">{getMoodEmoji(statistics.highest_rating)}</span>
                  </div>
                </Card>
                
                <Card className="animate-fadeIn" style={{ animationDelay: '200ms' }}>
                  <h2 className="text-sm font-medium text-gray-500 mb-1">Lowest Mood</h2>
                  <div className="flex items-center">
                    <span className="text-3xl font-bold text-error-600">{statistics.lowest_rating}</span>
                    <span className="text-3xl ml-2">{getMoodEmoji(statistics.lowest_rating)}</span>
                  </div>
                </Card>
                
                <Card className="animate-fadeIn" style={{ animationDelay: '300ms' }}>
                  <h2 className="text-sm font-medium text-gray-500 mb-1">Total Entries</h2>
                  <div className="flex items-center">
                    <span className="text-3xl font-bold text-secondary-700">{statistics.total_entries}</span>
                  </div>
                </Card>
              </div>
              
              <div className="grid gap-6 grid-cols-1 md:grid-cols-2 mb-6">
                <Card className="animate-fadeIn" style={{ animationDelay: '400ms' }}>
                  <h2 className="text-lg font-semibold mb-4">Mood Over Time</h2>
                  <div className="h-64">
                    <Line data={trendData} options={lineOptions} />
                  </div>
                </Card>
                
                <Card className="animate-fadeIn" style={{ animationDelay: '500ms' }}>
                  <h2 className="text-lg font-semibold mb-4">Common Tags</h2>
                  <div className="h-64">
                    <Bar data={tagData} options={barOptions} />
                  </div>
                </Card>
              </div>
            </>
          )}
          
          <Card className="animate-fadeIn" style={{ animationDelay: '600ms' }}>
            <h2 className="text-lg font-semibold mb-4">Recent Mood Entries</h2>
            
            {moodEntries.length === 0 ? (
              <p className="text-gray-500 text-center py-4">No mood entries found</p>
            ) : (
              <div className="space-y-4">
                {moodEntries.slice(0, 5).map((entry) => (
                  <div 
                    key={entry.entry_id} 
                    className="p-4 border border-gray-100 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center">
                        <div className="w-10 h-10 rounded-full bg-primary-100 flex items-center justify-center text-xl">
                          {getMoodEmoji(entry.mood_rating)}
                        </div>
                        <div className="ml-3">
                          <div className="text-lg font-medium">{entry.mood_rating}/10</div>
                          <div className="text-sm text-gray-500">
                            {new Date(entry.timestamp).toLocaleDateString()} at{' '}
                            {new Date(entry.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    {entry.tags.length > 0 && (
                      <div className="flex flex-wrap gap-1 mb-2">
                        {entry.tags.map((tag, i) => (
                          <span key={i} className="px-2 py-0.5 bg-gray-100 text-gray-700 text-xs rounded-full">
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                    
                    {entry.notes && <p className="text-gray-700 text-sm">{entry.notes}</p>}
                  </div>
                ))}
              </div>
            )}
          </Card>
        </>
      )}
    </div>
  );
};

export default MoodStats;