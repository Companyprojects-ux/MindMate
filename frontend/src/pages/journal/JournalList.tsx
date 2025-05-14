import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, BookHeart, Search, X } from 'lucide-react';
import { journalService } from '../../services/journalService';
import { JournalEntry } from '../../types';
import Button from '../../components/ui/Button';
import Card from '../../components/ui/Card';
import FormInput from '../../components/ui/FormInput';

const JournalList = () => {
  const [entries, setEntries] = useState<JournalEntry[]>([]);
  const [filteredEntries, setFilteredEntries] = useState<JournalEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    const fetchEntries = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await journalService.getJournalEntries();
        setEntries(data);
        setFilteredEntries(data);
      } catch (err) {
        setError('Failed to load journal entries');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchEntries();
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!searchQuery.trim()) {
      setFilteredEntries(entries);
      return;
    }
    
    setIsSearching(true);
    try {
      const results = await journalService.searchJournalEntries(searchQuery);
      setFilteredEntries(results);
    } catch (err) {
      setError('Failed to search journal entries');
      console.error(err);
    } finally {
      setIsSearching(false);
    }
  };

  const clearSearch = () => {
    setSearchQuery('');
    setFilteredEntries(entries);
  };

  const formatDate = (timestamp: string) => {
    return new Date(timestamp).toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Journal</h1>
        <Link to="/journal/new">
          <Button leftIcon={<Plus size={16} />}>New Entry</Button>
        </Link>
      </div>

      <Card className="mb-6">
        <form onSubmit={handleSearch} className="flex items-center">
          <div className="relative flex-1">
            <input
              type="text"
              className="form-input pl-10 pr-10"
              placeholder="Search journal entries..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <Search size={18} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            {searchQuery && (
              <button
                type="button"
                onClick={clearSearch}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <X size={18} />
              </button>
            )}
          </div>
          <Button
            type="submit"
            className="ml-2"
            isLoading={isSearching}
          >
            Search
          </Button>
        </form>
      </Card>

      {error && (
        <div className="bg-error-50 border border-error-200 text-error-700 px-4 py-3 rounded-md mb-6">
          <p>{error}</p>
        </div>
      )}

      {isLoading ? (
        <div className="space-y-6">
          {[...Array(3)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <div className="h-6 bg-gray-200 rounded w-1/3 mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
              <div className="space-y-2">
                <div className="h-4 bg-gray-200 rounded w-full"></div>
                <div className="h-4 bg-gray-200 rounded w-full"></div>
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
              </div>
            </Card>
          ))}
        </div>
      ) : filteredEntries.length === 0 ? (
        <Card className="text-center py-8">
          <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <BookHeart size={24} className="text-gray-400" />
          </div>
          <h2 className="text-xl font-medium text-gray-700 mb-2">
            {searchQuery ? 'No entries match your search' : 'No journal entries found'}
          </h2>
          <p className="text-gray-500 mb-6">
            {searchQuery 
              ? 'Try a different search term or clear your search' 
              : 'Start writing today to track your thoughts and feelings'}
          </p>
          {searchQuery ? (
            <Button onClick={clearSearch}>Clear Search</Button>
          ) : (
            <Link to="/journal/new">
              <Button leftIcon={<Plus size={16} />}>Create First Entry</Button>
            </Link>
          )}
        </Card>
      ) : (
        <div className="space-y-6">
          {filteredEntries.map((entry) => (
            <Link key={entry.entry_id} to={`/journal/edit/${entry.entry_id}`}>
              <Card className="hover:shadow-lg transition-shadow animate-fadeIn">
                <h2 className="text-xl font-semibold mb-1">{entry.title}</h2>
                <p className="text-gray-500 text-sm mb-3">{formatDate(entry.timestamp)}</p>
                
                {entry.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1 mb-3">
                    {entry.tags.map((tag, i) => (
                      <span key={i} className="px-2 py-0.5 bg-gray-100 text-gray-700 text-xs rounded-full">
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
                
                <p className="text-gray-700 line-clamp-3">{entry.content}</p>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export default JournalList;