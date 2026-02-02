// File: /workspaces/upgraded-WinkyTalk/agent-starter-react/components/SuperSearchDashboard.tsx

/**
 * 🚀 SUPER SEARCH DASHBOARD - Advanced AI Navigation Interface
 * Real-time visualization of AI web navigation and search
 */

//
import { 
  Card, Progress, List, Tag, Timeline, Image, 
  Button, Input, Alert, Row, Col, Statistic, Typography,
  Space, Collapse, Badge, Tooltip, Modal, Empty
} from 'antd';
import { 
  GlobalOutlined, SearchOutlined, EyeOutlined, 
  RocketOutlined, CheckCircleOutlined, ClockCircleOutlined,
  SafetyOutlined, FilterOutlined, DollarOutlined,
  EnvironmentOutlined, LinkOutlined, LoadingOutlined,
  QuestionCircleOutlined, ThunderboltOutlined
} from '@ant-design/icons';
import './SuperSearchDashboard.css';

const { Title, Text, Paragraph } = Typography;
const { Panel } = Collapse;

// Type Definitions
interface SearchResult {
  title: string;
  snippet: string;
  link: string;
  source: string;
  price?: string;
  location?: string;
  image_url?: string;
  relevance?: number;
  extracted_at: string;
  condition?: string;
  authenticity_score?: number;
  site_visited?: string;
}

interface AIAnalysis {
  best_option?: {
    index: number;
    reason: string;
    confidence: number;
  };
  price_range?: {
    min: number;
    max: number;
    average: number;
  };
  recommendations?: string[];
  summary?: string;
  risks?: string[];
  opportunities?: string[];
}

interface TaskProgress {
  task_id: string;
  status: 'idle' | 'planning' | 'searching' | 'analyzing' | 'complete' | 'error';
  current_step: number;
  total_steps: number;
  visited_sites: string[];
  found_items: SearchResult[];
  ai_analysis: AIAnalysis;
  last_update: string;
  current_action?: string;
  error_message?: string;
  estimated_time_remaining?: number;
}

interface WebSocketMessage {
  type: 'progress' | 'error' | 'complete' | 'item_found' | 'site_visited';
  data: TaskProgress | SearchResult | string;
  timestamp: string;
}

const SuperSearchDashboard: React.FC = () => {
  // State Management
  const [searchTask, setSearchTask] = useState<string>('');
  const [currentTask, setCurrentTask] = useState<string>('');
  const [progress, setProgress] = useState<TaskProgress>({
    task_id: '',
    status: 'idle',
    current_step: 0,
    total_steps: 0,
    visited_sites: [],
    found_items: [],
    ai_analysis: {},
    last_update: new Date().toISOString()
  });
  
  const [websocket, setWebsocket] = useState<WebSocket | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<'disconnected' | 'connecting' | 'connected' | 'error'>('disconnected');
  const [error, setError] = useState<string>('');
  const [showExamples, setShowExamples] = useState<boolean>(true);
  const [selectedItem, setSelectedItem] = useState<SearchResult | null>(null);
  const [showDetailsModal, setShowDetailsModal] = useState<boolean>(false);
  
  const taskIdRef = useRef<string>('');
  const reconnectAttempts = useRef<number>(0);
  const maxReconnectAttempts = 5;

  // Example tasks with categories
  const exampleTasks = [
    {
      category: 'Marketplace',
      tasks: [
        "Find best gaming laptop under $500 on Facebook Marketplace in San Jose",
        "Look for iPhone 15 deals on Craigslist Los Angeles",
        "Find used car under $8000 on Facebook Marketplace near me"
      ]
    },
    {
      category: 'Shopping',
      tasks: [
        "Compare MacBook Pro M3 prices on Amazon vs Best Buy",
        "Find cheapest AirPods Pro 2 with warranty",
        "Search for 4K monitors under $300 with good reviews"
      ]
    },
    {
      category: 'Real Estate',
      tasks: [
        "Find apartments for rent in NYC under $2000/month",
        "Search for houses for sale in Austin TX under $400k",
        "Look for studio apartments in San Francisco"
      ]
    },
    {
      category: 'Information',
      tasks: [
        "Latest AI news and breakthroughs 2024",
        "Current stock market trends and analysis",
        "Weather forecast for next week in Chicago"
      ]
    }
  ];

  // WebSocket Connection Management
  const connectWebSocket = useCallback((taskId: string) => {
    if (websocket) {
      websocket.close();
    }

    const wsUrl = `ws://${window.location.hostname}:8000/ws/${taskId}`;
    const ws = new WebSocket(wsUrl);
    
    setConnectionStatus('connecting');
    taskIdRef.current = taskId;

    ws.onopen = () => {
      console.log('🔗 WebSocket connected to:', wsUrl);
      setConnectionStatus('connected');
      reconnectAttempts.current = 0;
      setError('');
    };

    ws.onmessage = (event: MessageEvent) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data);
        handleWebSocketMessage(message);
      } catch (err) {
        console.error('Failed to parse WebSocket message:', err);
      }
    };

    ws.onerror = (error: Event) => {
      console.error('WebSocket error:', error);
      setConnectionStatus('error');
      setError('Connection error. Retrying...');
    };

    ws.onclose = (event: CloseEvent) => {
      console.log('WebSocket disconnected:', event.code, event.reason);
      setConnectionStatus('disconnected');
      
      // Auto-reconnect logic
      if (reconnectAttempts.current < maxReconnectAttempts && taskIdRef.current) {
        setTimeout(() => {
          reconnectAttempts.current++;
          console.log(`Reconnecting attempt ${reconnectAttempts.current}...`);
          connectWebSocket(taskIdRef.current);
        }, 2000 * reconnectAttempts.current); // Exponential backoff
      }
    };

    setWebsocket(ws);
  }, [websocket]);

  const handleWebSocketMessage = (message: WebSocketMessage) => {
    switch (message.type) {
      case 'progress':
        setProgress(message.data as TaskProgress);
        break;
      case 'item_found':
        const newItem = message.data as SearchResult;
        setProgress(prev => ({
          ...prev,
          found_items: [...prev.found_items, newItem]
        }));
        break;
      case 'site_visited':
        const site = message.data as string;
        setProgress(prev => ({
          ...prev,
          visited_sites: [...prev.visited_sites, site]
        }));
        break;
      case 'error':
        setError(message.data as string);
        setProgress(prev => ({ ...prev, status: 'error' }));
        break;
      case 'complete':
        setProgress(prev => ({ ...prev, status: 'complete' }));
        break;
    }
  };

  // Start a new search task
  const startSearch = async () => {
    if (!searchTask.trim()) {
      setError('Please enter a search task');
      return;
    }

    setCurrentTask(searchTask);
    setError('');
    setShowExamples(false);

    try {
      const response = await fetch('http://localhost:8000/search', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ 
          task: searchTask,
          max_results: 20,
          use_ai_analysis: true
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      
      if (data.task_id) {
        connectWebSocket(data.task_id);
      } else {
        throw new Error('No task ID received');
      }

    } catch (err: any) {
      setError(`Failed to start search: ${err.message}`);
      setProgress(prev => ({ ...prev, status: 'error' }));
    }
  };

  // Cancel current search
  const cancelSearch = () => {
    if (websocket) {
      websocket.close();
      setWebsocket(null);
    }
    setProgress({
      task_id: '',
      status: 'idle',
      current_step: 0,
      total_steps: 0,
      visited_sites: [],
      found_items: [],
      ai_analysis: {},
      last_update: new Date().toISOString()
    });
    setCurrentTask('');
    setError('');
  };

  // Format price for display
  const formatPrice = (price: string | undefined): string => {
    if (!price) return 'N/A';
    
    // Extract numbers from price string
    const matches = price.match(/\$?(\d+(?:\.\d+)?)/);
    if (matches && matches[1]) {
      const amount = parseFloat(matches[1]);
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(amount);
    }
    
    return price;
  };

  // Calculate progress percentage
  const calculateProgress = (): number => {
    if (progress.total_steps === 0) return 0;
    return Math.round((progress.current_step / progress.total_steps) * 100);
  };

  // Format time remaining
  const formatTimeRemaining = (seconds: number | undefined): string => {
    if (!seconds) return 'Calculating...';
    
    if (seconds < 60) return `${seconds} seconds`;
    if (seconds < 3600) return `${Math.ceil(seconds / 60)} minutes`;
    return `${Math.ceil(seconds / 3600)} hours`;
  };

  // Get status color
  const getStatusColor = (status: TaskProgress['status']): string => {
    switch (status) {
      case 'idle': return 'default';
      case 'planning': return 'blue';
      case 'searching': return 'orange';
      case 'analyzing': return 'purple';
      case 'complete': return 'green';
      case 'error': return 'red';
      default: return 'default';
    }
  };

  // Get status icon
  const getStatusIcon = (status: TaskProgress['status']) => {
    switch (status) {
      case 'idle': return <RocketOutlined />;
      case 'planning': return <ClockCircleOutlined />;
      case 'searching': return <SearchOutlined spin />;
      case 'analyzing': return <ThunderboltOutlined spin />;
      case 'complete': return <CheckCircleOutlined />;
      case 'error': return <SafetyOutlined />;
      default: return <RocketOutlined />;
    }
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (websocket) {
        websocket.close();
      }
    };
  }, [websocket]);

  return (
    <div className="super-search-dashboard">
      {/* Connection Status Badge */}
      <div style={{ position: 'fixed', top: 20, right: 20, zIndex: 1000 }}>
        <Badge 
          status={
            connectionStatus === 'connected' ? 'success' :
            connectionStatus === 'connecting' ? 'processing' :
            connectionStatus === 'error' ? 'error' : 'default'
          }
          text={
            connectionStatus === 'connected' ? 'Live Connected' :
            connectionStatus === 'connecting' ? 'Connecting...' :
            connectionStatus === 'error' ? 'Connection Error' : 'Disconnected'
          }
        />
      </div>

      {/* Main Header */}
      <Card 
        className="dashboard-header"
        bordered={false}
        style={{ 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          marginBottom: 24
        }}
      >
        <Row align="middle" gutter={[16, 16]}>
          <Col xs={24} md={16}>
            <Title level={2} style={{ color: 'white', margin: 0 }}>
              <RocketOutlined /> Winky Super Search
            </Title>
            <Paragraph style={{ color: 'rgba(255, 255, 255, 0.85)', marginBottom: 0 }}>
              Advanced AI-powered web navigation that browses, analyzes, and finds exactly what you need.
            </Paragraph>
          </Col>
          <Col xs={24} md={8}>
            <Statistic
              title="Active Searches"
              value={progress.status !== 'idle' ? 1 : 0}
              prefix={<EyeOutlined />}
              valueStyle={{ color: 'white' }}
            />
          </Col>
        </Row>
      </Card>

      {/* Search Input Section */}
      <Card title="🔍 Start AI Search" bordered={false} style={{ marginBottom: 24 }}>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <Input.TextArea
            size="large"
            placeholder="Describe what you want to find in detail...
Example: 'Find the best gaming laptop under $500 on Facebook Marketplace in San Jose, should have at least 16GB RAM and SSD storage'
            "
            value={searchTask}
            onChange={(e) => setSearchTask(e.target.value)}
            autoSize={{ minRows: 2, maxRows: 4 }}
            disabled={progress.status === 'searching' || progress.status === 'analyzing'}
          />
          
          <Row gutter={16}>
            <Col flex="auto">
              <Button 
                type="primary" 
                size="large" 
                icon={<SearchOutlined />}
                onClick={startSearch}
                loading={progress.status === 'searching' || progress.status === 'analyzing'}
                block
              >
                {progress.status === 'idle' ? 'Start AI Search' : 'Searching...'}
              </Button>
            </Col>
            <Col>
              <Button 
                size="large"
                onClick={cancelSearch}
                disabled={progress.status === 'idle'}
                danger
              >
                Cancel
              </Button>
            </Col>
          </Row>

          {error && (
            <Alert 
              message="Error" 
              description={error}
              type="error" 
              showIcon
              closable
              onClose={() => setError('')}
            />
          )}

          {/* Example Tasks */}
          <Collapse 
            ghost 
            size="small"
            activeKey={showExamples ? ['examples'] : []}
            onChange={(keys: string[]) => setShowExamples(keys.includes('examples'))}
          >
            <Panel header="💡 Example Search Tasks" key="examples">
              {exampleTasks.map((category, catIndex) => (
                <div key={catIndex} style={{ marginBottom: 16 }}>
                  <Text strong style={{ display: 'block', marginBottom: 8 }}>
                    {category.category}:
                  </Text>
                  <Space wrap>
                    {category.tasks.map((task, taskIndex) => (
                      <Tag
                        key={taskIndex}
                        color="blue"
                        style={{ cursor: 'pointer', marginBottom: 4 }}
                        onClick={() => setSearchTask(task)}
                      >
                        {task.length > 60 ? task.substring(0, 60) + '...' : task}
                      </Tag>
                    ))}
                  </Space>
                </div>
              ))}
            </Panel>
          </Collapse>
        </Space>
      </Card>

      {/* Progress Tracking - Only show when active */}
      {(progress.status !== 'idle') && (
        <Card title="🚀 AI Navigation Progress" bordered={false} style={{ marginBottom: 24 }}>
          <Space direction="vertical" size="large" style={{ width: '100%' }}>
            {/* Progress Bar */}
            <div>
              <Row justify="space-between" style={{ marginBottom: 8 }}>
                <Col>
                  <Tag icon={getStatusIcon(progress.status)} color={getStatusColor(progress.status)}>
                    {progress.status.toUpperCase()}
                  </Tag>
                  {progress.current_action && (
                    <Text type="secondary" style={{ marginLeft: 8 }}>
                      {progress.current_action}
                    </Text>
                  )}
                </Col>
                <Col>
                  <Text strong>{calculateProgress()}% Complete</Text>
                </Col>
              </Row>
              <Progress 
                percent={calculateProgress()} 
                status={progress.status === 'error' ? 'exception' : 'active'}
                strokeColor={{
                  '0%': '#1890ff',
                  '100%': '#52c41a',
                }}
              />
            </div>

            {/* Stats Row */}
            <Row gutter={16}>
              <Col xs={12} sm={6}>
                <Statistic 
                  title="Step" 
                  value={`${progress.current_step}/${progress.total_steps}`}
                  prefix={<ClockCircleOutlined />}
                />
              </Col>
              <Col xs={12} sm={6}>
                <Statistic 
                  title="Sites" 
                  value={progress.visited_sites.length}
                  prefix={<GlobalOutlined />}
                />
              </Col>
              <Col xs={12} sm={6}>
                <Statistic 
                  title="Items" 
                  value={progress.found_items.length}
                  prefix={<EyeOutlined />}
                />
              </Col>
              <Col xs={12} sm={6}>
                <Statistic 
                  title="Time Left" 
                  value={formatTimeRemaining(progress.estimated_time_remaining)}
                  prefix={<ClockCircleOutlined />}
                />
              </Col>
            </Row>

            {/* Navigation Timeline */}
            {progress.visited_sites.length > 0 && (
              <Card size="small" title="📍 Navigation Path">
                <Timeline mode="left">
                  {progress.visited_sites.map((site, index) => (
                    <Timeline.Item 
                      key={index}
                      dot={
                        <Badge 
                          count={index + 1}
                          style={{ 
                            backgroundColor: index === progress.current_step - 1 ? '#52c41a' : '#1890ff'
                          }}
                        />
                      }
                      color={index === progress.current_step - 1 ? 'green' : 'blue'}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Tooltip title={site}>
                          <a 
                            href={site} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            style={{ 
                              color: index === progress.current_step - 1 ? '#52c41a' : '#1890ff',
                              textDecoration: 'none'
                            }}
                          >
                            <LinkOutlined /> {new URL(site).hostname}
                          </a>
                        </Tooltip>
                        {index === progress.current_step - 1 && (
                          <Tag color="green" icon={<LoadingOutlined spin />}>
                            Current
                          </Tag>
                        )}
                      </div>
                    </Timeline.Item>
                  ))}
                </Timeline>
              </Card>
            )}
          </Space>
        </Card>
      )}

      {/* Results Section */}
      {progress.found_items.length > 0 && (
        <Card 
          title={`📦 Found Items (${progress.found_items.length})`}
          extra={
            <Tag color="blue" icon={<FilterOutlined />}>
              Sorted by Relevance
            </Tag>
          }
          bordered={false}
          style={{ marginBottom: 24 }}
        >
          <List
            grid={{
              gutter: 16,
              xs: 1,
              sm: 2,
              md: 3,
              lg: 3,
              xl: 4,
              xxl: 4,
            }}
            dataSource={progress.found_items}
            renderItem={(item, index) => (
              <List.Item>
                <Card
                  hoverable
                  onClick={() => {
                    setSelectedItem(item);
                    setShowDetailsModal(true);
                  }}
                  cover={
                    item.image_url ? (
                      <div style={{ height: 180, overflow: 'hidden' }}>
                        <Image
                          alt={item.title}
                          src={item.image_url}
                          height={180}
                          width="100%"
                          style={{ objectFit: 'cover' }}
                          preview={false}
                          fallback="/fallback-image.png"
                        />
                      </div>
                    ) : (
                      <div style={{
                        height: 180,
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'white'
                      }}>
                        <EyeOutlined style={{ fontSize: 48 }} />
                      </div>
                    )
                  }
                  actions={[
                    <Tooltip title="View Details">
                      <EyeOutlined key="view" />
                    </Tooltip>,
                    <Tooltip title="Visit Link">
                      <a href={item.link} target="_blank" rel="noopener noreferrer" onClick={(e) => e.stopPropagation()}>
                        <LinkOutlined />
                      </a>
                    </Tooltip>,
                    item.price && (
                      <Tooltip title="Price">
                        <DollarOutlined key="price" />
                      </Tooltip>
                    )
                  ]}
                >
                  <Card.Meta
                    title={
                      <Text ellipsis={{ tooltip: item.title }}>
                        {item.title || 'Untitled Item'}
                      </Text>
                    }
                    description={
                      <Space direction="vertical" size={2} style={{ width: '100%' }}>
                        {item.snippet && (
                          <Text type="secondary" ellipsis>
                            {item.snippet}
                          </Text>
                        )}
                        
                        <div style={{ marginTop: 8 }}>
                          {item.price && (
                            <Tag color="green" icon={<DollarOutlined />}>
                              {formatPrice(item.price)}
                            </Tag>
                          )}
                          
                          {item.location && (
                            <Tag color="blue" icon={<EnvironmentOutlined />}>
                              {item.location}
                            </Tag>
                          )}
                          
                          {item.condition && (
                            <Tag color="orange">
                              {item.condition}
                            </Tag>
                          )}
                        </div>
                        
                        {item.relevance && (
                          <Progress 
                            percent={Math.round(item.relevance * 100)} 
                            size="small" 
                            showInfo={false}
                            strokeColor="#52c41a"
                          />
                        )}
                      </Space>
                    }
                  />
                </Card>
              </List.Item>
            )}
            locale={{ emptyText: <Empty description="No items found yet" /> }}
          />
        </Card>
      )}

      {/* AI Analysis Section */}
      {progress.status === 'complete' && progress.ai_analysis && Object.keys(progress.ai_analysis).length > 0 && (
        <Card 
          title="🤖 AI Analysis & Recommendations"
          bordered={false}
          style={{ 
            marginBottom: 24,
            background: 'linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%)'
          }}
        >
          <Space direction="vertical" size="large" style={{ width: '100%' }}>
            {/* Best Option */}
            {progress.ai_analysis.best_option && (
              <Alert
                message={
                  <Space direction="vertical" size={2}>
                    <Text strong>🎯 Best Option (Item #{progress.ai_analysis.best_option.index})</Text>
                    <Text type="secondary">{progress.ai_analysis.best_option.reason}</Text>
                    <Progress 
                      percent={Math.round((progress.ai_analysis.best_option.confidence || 0) * 100)} 
                      status="active"
                      strokeColor="#52c41a"
                    />
                  </Space>
                }
                type="success"
                showIcon
              />
            )}

            {/* Price Analysis */}
            {progress.ai_analysis.price_range && (
              <Card size="small" title="💰 Price Analysis">
                <Row gutter={16}>
                  <Col span={8}>
                    <Statistic 
                      title="Lowest" 
                      value={formatPrice(`$${progress.ai_analysis.price_range.min}`)}
                      prefix={<DollarOutlined />}
                    />
                  </Col>
                  <Col span={8}>
                    <Statistic 
                      title="Average" 
                      value={formatPrice(`$${progress.ai_analysis.price_range.average}`)}
                      prefix={<DollarOutlined />}
                    />
                  </Col>
                  <Col span={8}>
                    <Statistic 
                      title="Highest" 
                      value={formatPrice(`$${progress.ai_analysis.price_range.max}`)}
                      prefix={<DollarOutlined />}
                    />
                  </Col>
                </Row>
              </Card>
            )}

            {/* Recommendations */}
            {progress.ai_analysis.recommendations && progress.ai_analysis.recommendations.length > 0 && (
              <Card size="small" title="💡 Recommendations">
                <List
                  size="small"
                  dataSource={progress.ai_analysis.recommendations}
                  renderItem={(rec, index) => (
                    <List.Item>
                      <List.Item.Meta
                        avatar={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
                        title={`Suggestion ${index + 1}`}
                        description={rec}
                      />
                    </List.Item>
                  )}
                />
              </Card>
            )}

            {/* Summary */}
            {progress.ai_analysis.summary && (
              <Card size="small" title="📊 Summary">
                <Paragraph>{progress.ai_analysis.summary}</Paragraph>
              </Card>
            )}
          </Space>
        </Card>
      )}

      {/* Details Modal */}
      <Modal
        title="Item Details"
        open={showDetailsModal && selectedItem !== null}
        onCancel={() => setShowDetailsModal(false)}
        footer={[
          <Button key="close" onClick={() => setShowDetailsModal(false)}>
            Close
          </Button>,
          <Button 
            key="visit" 
            type="primary" 
            href={selectedItem?.link} 
            target="_blank"
            icon={<LinkOutlined />}
          >
            Visit Website
          </Button>
        ]}
        width={800}
      >
        {selectedItem && (
          <Space direction="vertical" size="large" style={{ width: '100%' }}>
            {selectedItem.image_url && (
              <div style={{ textAlign: 'center' }}>
                <Image
                  src={selectedItem.image_url}
                  alt={selectedItem.title}
                  style={{ maxWidth: '100%', maxHeight: 300 }}
                />
              </div>
            )}
            
            <Title level={4}>{selectedItem.title}</Title>
            
            {selectedItem.snippet && (
              <Paragraph>{selectedItem.snippet}</Paragraph>
            )}
            
            <Row gutter={16}>
              {selectedItem.price && (
                <Col>
                  <Tag color="green" icon={<DollarOutlined />}>
                    Price: {formatPrice(selectedItem.price)}
                  </Tag>
                </Col>
              )}
              
              {selectedItem.location && (
                <Col>
                  <Tag color="blue" icon={<EnvironmentOutlined />}>
                    Location: {selectedItem.location}
                  </Tag>
                </Col>
              )}
              
              {selectedItem.condition && (
                <Col>
                  <Tag color="orange">
                    Condition: {selectedItem.condition}
                  </Tag>
                </Col>
              )}
              
              {selectedItem.authenticity_score && (
                <Col>
                  <Tag color={selectedItem.authenticity_score > 0.7 ? 'success' : 'warning'}>
                    Authenticity: {Math.round(selectedItem.authenticity_score * 100)}%
                  </Tag>
                </Col>
              )}
            </Row>
            
            <div>
              <Text strong>Source: </Text>
              <a href={selectedItem.source} target="_blank" rel="noopener noreferrer">
                {selectedItem.source}
              </a>
            </div>
            
            <div>
              <Text strong>Found At: </Text>
              <Text type="secondary">
                {new Date(selectedItem.extracted_at).toLocaleString()}
              </Text>
            </div>
            
            {selectedItem.relevance && (
              <div>
                <Text strong>Relevance Score: </Text>
                <Progress 
                  percent={Math.round(selectedItem.relevance * 100)} 
                  status="active"
                  strokeColor="#52c41a"
                  style={{ width: 200 }}
                />
              </div>
            )}
          </Space>
        )}
      </Modal>
    </div>
  );
};

export default SuperSearchDashboard;