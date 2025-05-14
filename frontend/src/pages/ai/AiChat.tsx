import { useEffect, useState, useRef } from 'react';
import { SendHorizontal, Bot, User, ThumbsUp, ThumbsDown, BarChart3, Brain } from 'lucide-react';
import { aiService } from '../../services/aiService';
import { ChatMessage, AiSuggestions, AiRecommendations, WeeklyReport } from '../../types';
import Button from '../../components/ui/Button';
import Card from '../../components/ui/Card';
import ReactMarkdown from 'react-markdown';

const AiChat = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [suggestions, setSuggestions] = useState<AiSuggestions | null>(null);
  const [recommendations, setRecommendations] = useState<AiRecommendations | null>(null);
  const [weeklyReport, setWeeklyReport] = useState<WeeklyReport | null>(null);
  const [activeTab, setActiveTab] = useState<'chat' | 'suggestions' | 'recommendations' | 'report'>('chat');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchData = async () => {
      setIsFetching(true);
      setError(null);
      try {
        const [chatHistory, suggestionsData, recommendationsData, reportData] = await Promise.all([
          aiService.getChatHistory(),
          aiService.getAiSuggestions(),
          aiService.getRecommendations(),
          aiService.getWeeklyReport()
        ]);
        setMessages(chatHistory);
        setSuggestions(suggestionsData);
        setRecommendations(recommendationsData);
        setWeeklyReport(reportData);
      } catch (err) {
        setError('Failed to load AI data');
        console.error(err);
      } finally {
        setIsFetching(false);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim()) return;
    
    const userMessage: ChatMessage = {
      message_id: `temp-${Date.now()}`,
      message: input,
      is_user: true,
      timestamp: new Date().toISOString(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    
    try {
      const response = await aiService.sendMessage(input);
      
      const aiMessage: ChatMessage = {
        message_id: `temp-response-${Date.now()}`,
        message: response.response,
        is_user: false,
        timestamp: new Date().toISOString(),
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      setError('Failed to send message');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
  };

  const handleFeedback = async (feedback: string) => {
    try {
      await aiService.submitFeedback(feedback);
      console.log('Feedback submitted:', feedback);
      // Optionally show a confirmation
    } catch (err) {
      console.error('Error submitting feedback:', err);
    }
  };

  if (isFetching) {
    return (
      <div className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/3 mb-6"></div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="md:col-span-3 h-96 bg-gray-200 rounded"></div>
          <div className="h-96 bg-gray-200 rounded"></div>
        </div>
        <div className="h-12 bg-gray-200 rounded"></div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">AI Support</h1>

      {error && (
        <div className="bg-error-50 border border-error-200 text-error-700 px-4 py-3 rounded-md mb-6">
          <p>{error}</p>
        </div>
      )}

      <div className="mb-6 border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('chat')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'chat'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <div className="flex items-center">
              <Bot size={16} className="mr-2" />
              Chat
            </div>
          </button>
          <button
            onClick={() => setActiveTab('suggestions')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'suggestions'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <div className="flex items-center">
              <Brain size={16} className="mr-2" />
              Daily Suggestions
            </div>
          </button>
          <button
            onClick={() => setActiveTab('recommendations')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'recommendations'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <div className="flex items-center">
              <BarChart3 size={16} className="mr-2" />
              Personalized Recommendations
            </div>
          </button>
          <button
            onClick={() => setActiveTab('report')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'report'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <div className="flex items-center">
              <BarChart3 size={16} className="mr-2" />
              Weekly Report
            </div>
          </button>
        </nav>
      </div>

      {activeTab === 'chat' && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="md:col-span-3">
            <Card className="mb-4">
              <div className="h-96 overflow-y-auto mb-4 p-2">
                {messages.length === 0 ? (
                  <div className="flex items-center justify-center h-full">
                    <div className="text-center">
                      <Bot size={36} className="mx-auto text-gray-400 mb-3" />
                      <p className="text-gray-500">No messages yet. Start a conversation!</p>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {messages.map((msg, index) => (
                      <div
                        key={msg.message_id || index}
                        className={`flex ${msg.is_user ? 'justify-end' : 'justify-start'}`}
                      >
                        <div
                          className={`max-w-3/4 rounded-lg px-4 py-2 ${
                            msg.is_user
                              ? 'bg-primary-600 text-white'
                              : 'bg-gray-100 text-gray-800'
                          }`}
                        >
                          <div className="flex items-center mb-1">
                            {msg.is_user ? (
                              <User size={16} className="mr-1" />
                            ) : (
                              <Bot size={16} className="mr-1" />
                            )}
                            <span className="text-xs opacity-75">
                              {new Date(msg.timestamp).toLocaleTimeString([], {
                                hour: '2-digit',
                                minute: '2-digit',
                              })}
                            </span>
                            {!msg.is_user && (
                              <div className="ml-2 flex space-x-1">
                                <button
                                  onClick={() => handleFeedback('helpful')}
                                  className="text-gray-500 hover:text-success-500"
                                  title="Helpful"
                                >
                                  <ThumbsUp size={12} />
                                </button>
                                <button
                                  onClick={() => handleFeedback('not helpful')}
                                  className="text-gray-500 hover:text-error-500"
                                  title="Not Helpful"
                                >
                                  <ThumbsDown size={12} />
                                </button>
                              </div>
                            )}
                          </div>
                          <div className="whitespace-pre-wrap">{msg.message}</div>
                        </div>
                      </div>
                    ))}
                    <div ref={messagesEndRef} />
                  </div>
                )}
              </div>
              
              <form onSubmit={handleSubmit} className="flex items-center space-x-2">
                <input
                  type="text"
                  className="form-input flex-1"
                  placeholder="Ask me anything about mental health, medications, coping strategies..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  disabled={isLoading}
                />
                <Button
                  type="submit"
                  isLoading={isLoading}
                  rightIcon={<SendHorizontal size={16} />}
                >
                  Send
                </Button>
              </form>
            </Card>
          </div>
          
          <div>
            <Card>
              <h2 className="text-lg font-semibold mb-4">Suggested Questions</h2>
              <div className="space-y-2">
                <button
                  className="w-full text-left p-2 rounded-md hover:bg-gray-100 text-sm transition-colors"
                  onClick={() => handleSuggestionClick('How can I manage my anxiety?')}
                >
                  How can I manage my anxiety?
                </button>
                <button
                  className="w-full text-left p-2 rounded-md hover:bg-gray-100 text-sm transition-colors"
                  onClick={() => handleSuggestionClick('What are some good sleep habits?')}
                >
                  What are some good sleep habits?
                </button>
                <button
                  className="w-full text-left p-2 rounded-md hover:bg-gray-100 text-sm transition-colors"
                  onClick={() => handleSuggestionClick('How can I remember to take my medications?')}
                >
                  How can I remember to take my medications?
                </button>
                <button
                  className="w-full text-left p-2 rounded-md hover:bg-gray-100 text-sm transition-colors"
                  onClick={() => handleSuggestionClick('What are some positive coping strategies?')}
                >
                  What are some positive coping strategies?
                </button>
              </div>
            </Card>
          </div>
        </div>
      )}

      {activeTab === 'suggestions' && suggestions && (
        <div className="grid gap-6 grid-cols-1 md:grid-cols-2">
          <Card className="animate-fadeIn">
            <h2 className="text-lg font-semibold mb-4 text-primary-700">Journal Prompt</h2>
            <p className="text-gray-700 mb-3">{suggestions.journal_prompt}</p>
            <div className="mt-4 flex justify-end">
              <Button
                size="sm"
                variant="outline"
                leftIcon={<ThumbsUp size={14} />}
                onClick={() => handleFeedback('Journal prompt was helpful')}
                className="mr-2"
              >
                Helpful
              </Button>
              <Button
                size="sm"
                variant="outline"
                leftIcon={<ThumbsDown size={14} />}
                onClick={() => handleFeedback('Journal prompt was not helpful')}
              >
                Not Helpful
              </Button>
            </div>
          </Card>
          
          <Card className="animate-fadeIn" style={{ animationDelay: '100ms' }}>
            <h2 className="text-lg font-semibold mb-4 text-secondary-700">Coping Tip</h2>
            <p className="text-gray-700 mb-3">{suggestions.coping_tip}</p>
            <div className="mt-4 flex justify-end">
              <Button
                size="sm"
                variant="outline"
                leftIcon={<ThumbsUp size={14} />}
                onClick={() => handleFeedback('Coping tip was helpful')}
                className="mr-2"
              >
                Helpful
              </Button>
              <Button
                size="sm"
                variant="outline"
                leftIcon={<ThumbsDown size={14} />}
                onClick={() => handleFeedback('Coping tip was not helpful')}
              >
                Not Helpful
              </Button>
            </div>
          </Card>
          
          <Card className="animate-fadeIn" style={{ animationDelay: '200ms' }}>
            <h2 className="text-lg font-semibold mb-4 text-accent-700">Motivational Content</h2>
            <p className="text-gray-700 mb-3">{suggestions.motivational_content}</p>
            <div className="mt-4 flex justify-end">
              <Button
                size="sm"
                variant="outline"
                leftIcon={<ThumbsUp size={14} />}
                onClick={() => handleFeedback('Motivational content was helpful')}
                className="mr-2"
              >
                Helpful
              </Button>
              <Button
                size="sm"
                variant="outline"
                leftIcon={<ThumbsDown size={14} />}
                onClick={() => handleFeedback('Motivational content was not helpful')}
              >
                Not Helpful
              </Button>
            </div>
          </Card>
          
          <Card className="animate-fadeIn" style={{ animationDelay: '300ms' }}>
            <h2 className="text-lg font-semibold mb-4 text-primary-700">Medication Tip</h2>
            <p className="text-gray-700 mb-3">{suggestions.medication_tip}</p>
            <div className="mt-4 flex justify-end">
              <Button
                size="sm"
                variant="outline"
                leftIcon={<ThumbsUp size={14} />}
                onClick={() => handleFeedback('Medication tip was helpful')}
                className="mr-2"
              >
                Helpful
              </Button>
              <Button
                size="sm"
                variant="outline"
                leftIcon={<ThumbsDown size={14} />}
                onClick={() => handleFeedback('Medication tip was not helpful')}
              >
                Not Helpful
              </Button>
            </div>
          </Card>
        </div>
      )}

      {activeTab === 'recommendations' && recommendations && (
        <div className="grid gap-6 grid-cols-1 md:grid-cols-2">
          <Card className="md:col-span-2 animate-fadeIn">
            <h2 className="text-lg font-semibold mb-4">Personalized Recommendations</h2>
            <p className="text-gray-500 mb-6">
              Based on your data, MindMate+ has generated these recommendations to support your mental health journey.
            </p>
          </Card>
          
          <Card className="animate-fadeIn" style={{ animationDelay: '100ms' }}>
            <h2 className="text-lg font-semibold mb-4 text-primary-700">Journal Prompts</h2>
            <div className="space-y-4">
              {recommendations.journal_prompts.map((prompt, index) => (
                <div key={index} className="p-3 bg-gray-50 rounded-md">
                  <h3 className="font-medium mb-1">{prompt.title}</h3>
                  <p className="text-gray-700 text-sm">{prompt.prompt}</p>
                </div>
              ))}
            </div>
          </Card>
          
          <Card className="animate-fadeIn" style={{ animationDelay: '200ms' }}>
            <h2 className="text-lg font-semibold mb-4 text-secondary-700">Coping Strategies</h2>
            <div className="space-y-4">
              {recommendations.coping_strategies.map((strategy, index) => (
                <div key={index} className="p-3 bg-gray-50 rounded-md">
                  <h3 className="font-medium mb-1">{strategy.title}</h3>
                  <p className="text-gray-700 text-sm">{strategy.description}</p>
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}

      {activeTab === 'report' && weeklyReport && (
        <Card className="animate-fadeIn">
          <h2 className="text-lg font-semibold mb-4">Weekly Progress Report</h2>
          <div className="prose max-w-none">
            <ReactMarkdown>{weeklyReport.report}</ReactMarkdown>
          </div>
        </Card>
      )}
    </div>
  );
};

export default AiChat;