// filepath: d:\项目\占卜网站\占卜\frontend\src\components\DivinationWorkbench.tsx
import React, { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Badge } from './ui/badge';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { ToastContainer, useToast } from './ui/toast';
import { EnhancedLoadingSpinner } from './ui/enhanced-loading-spinner';
import { AnimatedHexagram } from './ui/animated-hexagram';
import DivinationMethodSelector from './DivinationMethodSelector';
import type { DivinationMethod, DivinationInputResult } from './DivinationMethodSelector';
import { 
  Download, 
  RefreshCw, 
  Coins, 
  Eye, 
  Calendar,
  FileText,
  Sparkles,
  Lightbulb,
  ArrowLeft,
  Settings,
  History,
  Copy,
  Share2,
  Command,
  Zap
} from 'lucide-react';

// 类型定义
interface TextExplanation {
  text: string;
  explanation: string;
}

interface LineInterpretations {
  traditional?: TextExplanation;
  shaoYong?: any;
  fuPeiRong?: any;
  zhangMingRen?: any;
}

interface HexagramInterpretations {
  traditional?: { description: string };
  shaoYong?: any;
  fuPeiRong?: any;
  zhangMingRen?: any;
}

interface Line {
  position: number;
  type: 'yang' | 'yin';
  changing: boolean;
  text?: string;
  explanation?: string;
  image?: TextExplanation;
  interpretations?: LineInterpretations;
}

interface Hexagram {
  number: number;
  name: string;
  chineseName: string;
  symbol: string;
  upperTrigram: string;
  lowerTrigram: string;
  kingWen?: TextExplanation;
  image?: TextExplanation;
  interpretations?: HexagramInterpretations;
  lines?: Line[];
}

interface ChangeInfo {
  hasChanges: boolean;
  changingLines: number[];
  changedHexagram?: Hexagram;
}

interface DivinationResult {
  question: string;
  originalHexagram: Hexagram;
  changedHexagram?: Hexagram;
  mutualHexagram?: Hexagram;
  lines: Line[];
  timestamp: string;
  interpretation: string;
  divinerName?: string;
  notes?: string;
  changeInfo?: ChangeInfo;
}

interface DivinationWorkbenchProps {
  onNavigateToLanding?: () => void;
  onNavigateToHistory?: () => void;
  onNavigateToSettings?: () => void;
  viewingRecord?: DivinationRecord | null;
  onClearViewingRecord?: () => void;
}

interface DivinationRecord {
  id: string;
  question: string;
  originalHexagram: {
    number: number;
    name: string;
    chineseName: string;
    symbol: string;
  };
  changedHexagram?: {
    number: number;
    name: string;
    chineseName: string;
    symbol: string;
  };
  divinerName?: string;
  timestamp: string;
  notes?: string;
  changingLinesCount: number;
}

const DivinationWorkbench: React.FC<DivinationWorkbenchProps> = ({ 
  onNavigateToLanding,
  onNavigateToHistory,
  onNavigateToSettings,
  viewingRecord,
  onClearViewingRecord
}) => {
  const [question, setQuestion] = useState('');
  const [divinerName, setDivinerName] = useState('');
  const [result, setResult] = useState<DivinationResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [notes, setNotes] = useState('');
  const [selectedView, setSelectedView] = useState<'original' | 'changed' | 'mutual'>('original');
  const [animatedResult, setAnimatedResult] = useState(false);
  
  // 起卦方法相关状态
  const [selectedMethod, setSelectedMethod] = useState<DivinationMethod>('coins');
  const [divinationInput, setDivinationInput] = useState<DivinationInputResult | null>(null);

  // Refs
  const questionTextareaRef = useRef<HTMLTextAreaElement>(null);
  // Toast 功能
  const { showSuccess, showError, showInfo } = useToast();

  // 键盘快捷键处理
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ctrl/Cmd + Enter 执行占卜
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        if (!isLoading && question.trim()) {
          performDivination();
        }
      }
      
      // Ctrl/Cmd + K 聚焦到问题输入框
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        questionTextareaRef.current?.focus();
      }
      
      // Ctrl/Cmd + R 重置占卜
      if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault();
        resetDivination();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [question, isLoading]);

  // 动画处理
  useEffect(() => {
    if (result && !animatedResult) {
      setAnimatedResult(true);
      showSuccess('占卜完成', '您的卦象已生成，请查看结果');
      // 重置动画状态
      const timer = setTimeout(() => setAnimatedResult(false), 1000);
      return () => clearTimeout(timer);
    }
  }, [result]);

  // 复制到剪贴板
  const copyToClipboard = async (text: string, successMessage: string) => {
    try {
      await navigator.clipboard.writeText(text);
      showSuccess('复制成功', successMessage);
    } catch (error) {
      console.error('复制失败:', error);
      // 如果现代API不可用，使用传统方法
      const textArea = document.createElement('textarea');
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      try {
        document.execCommand('copy');
        showSuccess('复制成功', successMessage);
      } catch (fallbackError) {
        showError('复制失败', '无法复制到剪贴板');
      }
      document.body.removeChild(textArea);
    }
  };

  // 处理查看历史记录的情况
  useEffect(() => {
    if (viewingRecord && onClearViewingRecord) {
      // 根据历史记录模拟结果显示
      const mockResult: DivinationResult = {
        question: viewingRecord.question,
        originalHexagram: {
          number: viewingRecord.originalHexagram.number,
          name: viewingRecord.originalHexagram.name,
          chineseName: viewingRecord.originalHexagram.chineseName,
          symbol: viewingRecord.originalHexagram.symbol,
          upperTrigram: '',
          lowerTrigram: '',
        },
        lines: [],
        timestamp: viewingRecord.timestamp,
        interpretation: '这是历史记录查看，详细解释请查看原始占卜结果。',
        divinerName: viewingRecord.divinerName,
        notes: viewingRecord.notes,
      };
      
      if (viewingRecord.changedHexagram) {
        mockResult.changedHexagram = {
          ...viewingRecord.changedHexagram,
          upperTrigram: '',
          lowerTrigram: '',
        };
      }
      
      setResult(mockResult);
      setQuestion(viewingRecord.question);
      setDivinerName(viewingRecord.divinerName || '');
      setNotes(viewingRecord.notes || '');
    }
  }, [viewingRecord, onClearViewingRecord]);

  // 处理起卦输入结果
  const handleDivinationInput = (inputResult: DivinationInputResult) => {
    setDivinationInput(inputResult);
  };  // 执行占卜 - 增强版本
  const performDivination = async () => {
    console.log('执行占卜函数被调用');
    
    if (!question.trim()) {
      // 聚焦到问题输入框
      questionTextareaRef.current?.focus();
      return;
    }

    setIsLoading(true);
    setAnimatedResult(false);
    console.log('开始调用占卜API');
    
    try {
      // 添加随机延迟来模拟真实的网络请求
      await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 1200));
      
      // 调用后端API进行占卜
      const response = await fetch('http://localhost:8000/api/divination', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          question: question.trim()
        }),
      });
      
      console.log('API响应状态:', response.status);
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || '占卜请求失败');
      }

      const data = await response.json();
      console.log('API响应数据:', data);
      
      // 计算互卦
      const mutualHexagram = calculateMutualHexagram(data.originalHexagram);
      
      // 转换后端数据格式为前端需要的格式
      const processedResult: DivinationResult = {
        question: data.question,
        originalHexagram: data.originalHexagram,
        changedHexagram: data.changedHexagram,
        mutualHexagram,
        lines: data.lines,
        timestamp: new Date(data.timestamp).toISOString(),
        interpretation: data.interpretation,
        divinerName: divinerName || '匿名',
        notes: '',
        changeInfo: {
          hasChanges: data.changedHexagram ? true : false,
          changingLines: data.lines.filter((line: Line) => line.changing).map((line: Line) => line.position),
          changedHexagram: data.changedHexagram
        }
      };
      
      console.log('处理后的结果:', processedResult);
      setResult(processedResult);
    } catch (error) {
      console.error('占卜错误:', error);
      alert(error instanceof Error ? error.message : '占卜过程中发生错误，请重试');
      console.log('使用模拟数据作为后备...');
      
      // 使用模拟数据作为后备方案
      const mockResult = generateMockResult();
      setResult(mockResult);
    } finally {
      setIsLoading(false);
    }
  };

  // 计算互卦
  const calculateMutualHexagram = (hexagram: Hexagram): Hexagram => {
    if (!hexagram.lines || hexagram.lines.length !== 6) {
      return hexagram;
    }
    
    // 取2、3、4爻组成下卦，3、4、5爻组成上卦
    const lowerMutual = [hexagram.lines[1], hexagram.lines[2], hexagram.lines[3]]
      .map(line => line.type === 'yang' ? '1' : '0').join('');
    const upperMutual = [hexagram.lines[2], hexagram.lines[3], hexagram.lines[4]]
      .map(line => line.type === 'yang' ? '1' : '0').join('');
    
    // 这里简化处理，实际应该通过卦象查找对应的卦
    return {
      ...hexagram,
      number: 99, // 临时编号
      name: '互卦',
      chineseName: '互卦',
      upperTrigram: upperMutual,
      lowerTrigram: lowerMutual,
    };
  };

  // 生成模拟结果（作为后备）
  const generateMockResult = (): DivinationResult => {
    const lines: Line[] = Array.from({ length: 6 }, (_, i) => ({
      position: i + 1,
      type: Math.random() > 0.5 ? 'yang' : 'yin',
      changing: Math.random() > 0.8,
      text: `第${i + 1}爻爻辞`,
      explanation: `第${i + 1}爻的详细解释...`,
    }));

    const originalHexagram: Hexagram = {
      number: 1,
      name: '乾卦',
      chineseName: '乾為天',
      symbol: '☰',
      upperTrigram: '111',
      lowerTrigram: '111',
      kingWen: {
        text: '乾。元亨利貞。',
        explanation: '乾卦：大吉大利，吉利的貞卜。'
      },
      image: {
        text: '天行健，君子以自強不息。',
        explanation: '天道剛健，運行不已。君子觀此卦象，從而以天為法，自強不息。'
      },
      interpretations: {
        traditional: {
          description: '乾卦是純陽之卦，象徵天道剛健...'
        }
      },
      lines
    };

    const mutualHexagram = calculateMutualHexagram(originalHexagram);

    return {
      question: question,
      originalHexagram,
      mutualHexagram,
      lines,
      timestamp: new Date().toISOString(),
      interpretation: '这是一个模拟的占卜结果。请检查后端连接是否正常。',
      divinerName: divinerName || '匿名',
      notes: '',
      changeInfo: {
        hasChanges: false,
        changingLines: [],
      }
    };
  };

  // 下载结果
  const downloadResult = () => {
    if (!result) return;
    
    const content = generateReportContent(result);
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `易经占卜结果_${new Date().toISOString().slice(0, 10)}.txt`;
    link.click();
  };

  // 生成报告内容
  const generateReportContent = (result: DivinationResult): string => {
    const timestamp = new Date(result.timestamp).toLocaleString();
    return `易经占卜结果报告

问题：${result.question}
占卜师：${result.divinerName || '匿名'}
时间：${timestamp}

本卦：${result.originalHexagram.chineseName} (${result.originalHexagram.name})
${result.changedHexagram ? `变卦：${result.changedHexagram.chineseName} (${result.changedHexagram.name})` : ''}

解释：
${result.interpretation}

${result.notes ? `备注：${result.notes}` : ''}

---
此报告由易经占卜工作台生成
`;
  };
  // 保存到历史记录
  const saveToHistory = () => {
    if (!result) return;
    
    try {
      const record: DivinationRecord = {
        id: Date.now().toString(),
        question: result.question,
        originalHexagram: {
          number: result.originalHexagram.number,
          name: result.originalHexagram.name,
          chineseName: result.originalHexagram.chineseName,
          symbol: result.originalHexagram.symbol,
        },
        divinerName: result.divinerName,
        timestamp: result.timestamp,
        notes: result.notes,
        changingLinesCount: result.lines?.filter(line => line.changing).length || 0,
      };

      if (result.changedHexagram) {
        record.changedHexagram = {
          number: result.changedHexagram.number,
          name: result.changedHexagram.name,
          chineseName: result.changedHexagram.chineseName,
          symbol: result.changedHexagram.symbol,
        };
      }

      // 保存到localStorage
      const existingRecords = JSON.parse(localStorage.getItem('divinationHistory') || '[]');
      existingRecords.unshift(record);
      
      // 只保留最近100条记录
      if (existingRecords.length > 100) {
        existingRecords.splice(100);
      }
      
      localStorage.setItem('divinationHistory', JSON.stringify(existingRecords));
      showSuccess('保存成功', '占卜结果已保存到历史记录');
    } catch (error) {
      showError('保存失败', '无法保存到历史记录');
      console.error('保存历史记录失败:', error);
    }
  };

  // 重置占卜
  const resetDivination = () => {
    setQuestion('');
    setResult(null);
    setNotes('');
    setSelectedView('original');
    setDivinationInput(null);
    setDivinerName('');
    if (onClearViewingRecord) {
      onClearViewingRecord();
    }
  };
  // 渲染卦象 - 增强版本
  const renderHexagram = (hexagram: Hexagram) => {
    if (!hexagram.lines || hexagram.lines.length === 0) {
      // 如果没有爻的详细信息，使用简化显示
      return (
        <div className="text-center animate-fade-in-up">
          <div className="text-6xl mb-4 animate-float">{hexagram.symbol}</div>
          <div className="text-xl font-bold text-gradient">{hexagram.chineseName}</div>
          <div className="text-lg text-white/70">{hexagram.name}</div>
        </div>
      );
    }    // 转换为 AnimatedHexagram 需要的格式（数字数组）
    const animatedLines = hexagram.lines.map(line => {
      // 根据易经规则转换为数字
      if (line.type === 'yang') {
        return line.changing ? 9 : 7; // 老阳（变）：9，少阳（不变）：7
      } else {
        return line.changing ? 6 : 8; // 老阴（变）：6，少阴（不变）：8
      }
    });

    return (
      <div className="text-center animate-fade-in-up">
        <AnimatedHexagram
          lines={animatedLines}
          size="lg"
          animated={animatedResult}
          className="mb-4"
        />
        <div className="text-4xl mb-2 animate-float">{hexagram.symbol}</div>
        <div className="text-xl font-bold text-gradient">{hexagram.chineseName}</div>
        <div className="text-lg text-white/70">{hexagram.name}</div>
      </div>
    );
  };

  // 渲染卦象详细信息
  const renderHexagramDetails = (hexagram: Hexagram) => {
    return (
      <div className="space-y-6">
        {hexagram.kingWen && (
          <Card className="bg-[#1e293b] border-[#374151]">
            <CardHeader>
              <CardTitle className="text-white/90 flex items-center gap-2">
                <FileText className="h-5 w-5" />
                卦辞
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="font-semibold text-white">{hexagram.kingWen.text}</div>
                <div className="text-white/70">{hexagram.kingWen.explanation}</div>
              </div>
            </CardContent>
          </Card>
        )}

        {hexagram.image && (
          <Card className="bg-[#1e293b] border-[#374151]">
            <CardHeader>
              <CardTitle className="text-white/90 flex items-center gap-2">
                <Eye className="h-5 w-5" />
                象辞
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="font-semibold text-white">{hexagram.image.text}</div>
                <div className="text-white/70">{hexagram.image.explanation}</div>
              </div>
            </CardContent>
          </Card>
        )}

        {hexagram.lines && hexagram.lines.some(line => line.text) && (
          <Card className="bg-[#1e293b] border-[#374151]">
            <CardHeader>
              <CardTitle className="text-white/90 flex items-center gap-2">
                <Lightbulb className="h-5 w-5" />
                爻辞
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {hexagram.lines.map((line) => (
                  line.text && (
                    <div key={line.position} className="border-l-4 border-[#3b82f6] pl-4">
                      <div className="flex items-center gap-2 mb-2">
                        <div className="text-sm font-mono bg-[#334155] px-2 py-1 rounded text-white/80">
                          第{line.position}爻
                        </div>
                        {line.changing && (
                          <Badge variant="destructive" className="text-xs">
                            变爻
                          </Badge>
                        )}
                      </div>
                      <div className="font-semibold mb-1 text-white">{line.text}</div>
                      {line.explanation && (
                        <div className="text-white/70 text-sm">{line.explanation}</div>
                      )}
                    </div>
                  )
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    );
  };  return (
    <TooltipProvider>
      <div className="h-screen flex flex-col bg-[#0f172a] overflow-hidden dark-mode-enhanced">
        {/* Enhanced Loading Overlay */}
        {isLoading && (
          <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
            <EnhancedLoadingSpinner 
              size="lg" 
              variant="pulse" 
              text="占卜中..."
              className="text-white"
            />
          </div>
        )}
        
        {/* Toast Container */}
        <ToastContainer />
        
        {/* 头部导航 - 类似ChatGPT风格 */}
        <div className="bg-[#111827] border-b border-[#374151] glass-effect">
          <div className="flex items-center justify-between h-14 px-4">
            <div className="flex items-center gap-3">
              {viewingRecord && onClearViewingRecord ? (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onClearViewingRecord}
                  className="text-white/80 hover:bg-white/10 hover:text-white button-hover"
                >
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  返回
                </Button>
              ) : (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onNavigateToLanding}
                  className="text-white/80 hover:bg-white/10 hover:text-white button-hover"
                >
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  回到首页
                </Button>
              )}
              <h1 className="text-lg font-medium text-gradient">易经占卜工作台</h1>
            </div>
            
            <div className="flex items-center gap-2">
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={onNavigateToHistory}
                    className="text-white/80 hover:bg-white/10 hover:text-white button-hover"
                  >
                    <History className="h-4 w-4 mr-2" />
                    历史记录
                  </Button>
                </TooltipTrigger>
                <TooltipContent side="bottom" className="bg-[#1e293b] border-[#374151] text-white">
                  查看占卜历史记录
                </TooltipContent>
              </Tooltip>
              
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={onNavigateToSettings}
                    className="text-white/80 hover:bg-white/10 hover:text-white button-hover"
                  >
                    <Settings className="h-4 w-4" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent side="bottom" className="bg-[#1e293b] border-[#374151] text-white">
                  设置
                </TooltipContent>
              </Tooltip>
            </div>
          </div>
        </div>      {/* 主体内容区域 - 采用三栏布局充分利用空间 */}
      <div className="flex flex-1 h-[calc(100vh-3.5rem)] overflow-hidden">
          {/* 左侧工具栏 - 保持原有功能 */}
          <div className="w-[280px] lg:w-[320px] xl:w-[360px] bg-[#111827] border-r border-[#374151] flex flex-col overflow-y-auto glass-effect shrink-0">
            {/* 问题输入 */}
            <div className="p-4 border-b border-[#374151]">
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-sm font-medium text-white/90 flex items-center gap-2">
                  <FileText className="h-4 w-4" />
                  提出问题
                </h2>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-6 w-6 p-0 text-white/50 hover:text-white/80"
                    >
                      <Command className="h-3 w-3" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent side="right" className="bg-[#1e293b] border-[#374151] text-white text-xs">
                    <div className="space-y-1">
                      <div>Ctrl+K: 聚焦输入框</div>
                      <div>Ctrl+Enter: 开始占卜</div>
                      <div>Ctrl+R: 重置</div>
                    </div>
                  </TooltipContent>
                </Tooltip>
              </div>
              <Textarea
                ref={questionTextareaRef}
                id="question"
                placeholder="请输入您想要占卜的问题..."
                value={question}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setQuestion(e.target.value)}
                className="bg-[#1e293b] border-[#374151] text-white placeholder-white/50 text-sm resize-none input-focus transition-all duration-200 focus:ring-2 focus:ring-[#4f46e5] focus:border-transparent"
                rows={4}
              />
              
              <div className="mt-3">
                <Label htmlFor="diviner" className="text-sm text-white/80 mb-1 block">占卜师姓名（可选）</Label>
                <Input
                  id="diviner"
                  type="text"
                  placeholder="请输入占卜师姓名"
                  value={divinerName}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setDivinerName(e.target.value)}
                  className="bg-[#1e293b] border-[#374151] text-white placeholder-white/50 text-sm input-focus transition-all duration-200 focus:ring-2 focus:ring-[#4f46e5] focus:border-transparent"
                />
              </div>
            </div>

            {/* 起卦方式 */}
            <div className="p-4 border-b border-[#374151]">
              <h2 className="text-sm font-medium text-white/90 mb-3 flex items-center gap-2">
                <Coins className="h-4 w-4" />
                起卦方式
              </h2>              <DivinationMethodSelector
                selectedMethod={selectedMethod}
                onMethodChange={setSelectedMethod}
                onGenerate={handleDivinationInput}
                isLoading={isLoading}
              />
            </div>            {/* 执行按钮 */}
            <div className="p-4 flex-1 flex flex-col justify-end">
              <Button
                onClick={performDivination}
                disabled={!question.trim() || isLoading}
                className={`w-full bg-gradient-to-r from-[#4f46e5] to-[#7c3aed] hover:from-[#4338ca] hover:to-[#6d28d9] button-hover transition-all duration-300 transform ${
                  isLoading ? 'scale-95' : 'hover:scale-105'
                } shadow-lg hover:shadow-xl animate-pulse-glow`}
                size="lg"
              >
                <div className="flex items-center gap-2">
                  <Zap className="h-4 w-4" />
                  <span>开始占卜</span>
                  <kbd className="ml-2 px-1.5 py-0.5 text-xs bg-white/20 rounded">⌘↵</kbd>
                </div>
              </Button>
              
              {question.trim() && !isLoading && (
                <div className="mt-2 text-xs text-white/60 text-center animate-fade-in-up">
                  按 Ctrl+Enter 快速开始占卜
                </div>
              )}

              {/* 快速提示 */}
              {!result && (
                <div className="mt-4 text-xs text-white/50 space-y-2">
                  <div className="flex items-center gap-2">
                    <kbd className="px-1.5 py-0.5 bg-white/10 rounded text-xs">Ctrl+K</kbd>
                    <span>聚焦问题输入</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <kbd className="px-1.5 py-0.5 bg-white/10 rounded text-xs">Ctrl+R</kbd>
                    <span>重置表单</span>
                  </div>
                </div>
              )}
            </div>
          </div>        {/* 中间主内容区域 - 占卜结果显示 */}
        <div className="flex-1 min-w-0 flex flex-col overflow-hidden">
          {result ? (
            <div className="flex-1 overflow-y-auto p-4">
              {/* 问题和结果概要 - 紧凑布局 */}
              <div className="bg-[#1e293b] rounded-lg p-4 border border-[#374151] mb-4">
                <h2 className="text-lg font-medium text-white mb-2">问题</h2>
                <p className="text-white/90 mb-3 text-base">{result.question}</p>
                
                <div className="flex flex-wrap gap-3">
                  <div className="flex items-center gap-2">
                    <span className="text-white/70 text-sm">本卦:</span>
                    <Badge className="bg-[#4f46e5]">{result.originalHexagram.chineseName}</Badge>
                  </div>
                  {result.changedHexagram && (
                    <div className="flex items-center gap-2">
                      <span className="text-white/70 text-sm">变卦:</span>
                      <Badge className="bg-[#7c3aed]">{result.changedHexagram.chineseName}</Badge>
                    </div>
                  )}
                  <div className="flex items-center gap-2">
                    <span className="text-white/70 text-sm">时间:</span>
                    <span className="text-white/90 text-sm">{new Date(result.timestamp).toLocaleString()}</span>
                  </div>
                </div>
              </div>

              {/* 卦象选择和显示 - 中心位置 */}
              <Card className="bg-[#1e293b] border-[#374151] mb-4">
                <CardHeader className="pb-2">
                  <div className="flex justify-between items-center">
                    <CardTitle className="text-white/90">卦象</CardTitle>
                    <div className="flex gap-1">
                      <Button
                        variant={selectedView === 'original' ? 'default' : 'outline'}
                        size="sm"
                        onClick={() => setSelectedView('original')}
                        className={selectedView === 'original' 
                          ? 'bg-[#4f46e5] hover:bg-[#4338ca]' 
                          : 'bg-[#1e293b] border-[#374151] text-white/80 hover:bg-[#374151]/30 hover:text-white'
                        }
                      >
                        本卦
                      </Button>
                      {result.changedHexagram && (
                        <Button
                          variant={selectedView === 'changed' ? 'default' : 'outline'}
                          size="sm"
                          onClick={() => setSelectedView('changed')}
                          className={selectedView === 'changed' 
                            ? 'bg-[#4f46e5] hover:bg-[#4338ca]' 
                            : 'bg-[#1e293b] border-[#374151] text-white/80 hover:bg-[#374151]/30 hover:text-white'
                          }
                        >
                          变卦
                        </Button>
                      )}
                      {result.mutualHexagram && (
                        <Button
                          variant={selectedView === 'mutual' ? 'default' : 'outline'}
                          size="sm"
                          onClick={() => setSelectedView('mutual')}
                          className={selectedView === 'mutual' 
                            ? 'bg-[#4f46e5] hover:bg-[#4338ca]' 
                            : 'bg-[#1e293b] border-[#374151] text-white/80 hover:bg-[#374151]/30 hover:text-white'
                          }
                        >
                          互卦
                        </Button>
                      )}
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="text-white">
                  {selectedView === 'original' && renderHexagram(result.originalHexagram)}
                  {selectedView === 'changed' && result.changedHexagram && renderHexagram(result.changedHexagram)}
                  {selectedView === 'mutual' && result.mutualHexagram && renderHexagram(result.mutualHexagram)}
                </CardContent>
              </Card>              {/* 卦辞和象辞 - 移到中间栏 */}
              {selectedView === 'original' && renderHexagramDetails(result.originalHexagram)}
              {selectedView === 'changed' && result.changedHexagram && renderHexagramDetails(result.changedHexagram)}
              {selectedView === 'mutual' && result.mutualHexagram && renderHexagramDetails(result.mutualHexagram)}

              {/* 解释 - 中心展示 */}
              <Card className="bg-[#1e293b] border-[#374151] mt-4">
                <CardHeader>
                  <CardTitle className="text-white/90 flex items-center gap-2">
                    <Lightbulb className="h-5 w-5" />
                    解读
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-white whitespace-pre-wrap">{result.interpretation}</div>
                </CardContent>
              </Card>
            </div>
          ) : (
            <div className="flex items-center justify-center h-full">
              <div className="text-center text-white/70 max-w-lg">
                <Sparkles className="h-16 w-16 mx-auto mb-6 opacity-50" />
                <h2 className="text-2xl font-semibold mb-4">开始占卜</h2>
                <p className="mb-6">在左侧输入您的问题，选择起卦方式，然后点击"开始占卜"按钮。</p>
                <div className="text-sm opacity-75">
                  系统将根据古老的易经原理为您提供生活智慧和指导。
                </div>
              </div>
            </div>
          )}
        </div>        {/* 右侧AI解卦对话栏 - 新功能区域 */}
        <div className="w-[280px] lg:w-[320px] xl:w-[360px] bg-[#111827] border-l border-[#374151] flex flex-col overflow-y-auto glass-effect shrink-0">
          {result ? (
            <div className="flex flex-col h-full">
              {/* AI解卦对话区域 */}
              <div className="p-4 border-b border-[#374151] flex-1">
                <h3 className="text-sm font-medium text-white/90 mb-3 flex items-center gap-2">
                  <Sparkles className="h-4 w-4" />
                  AI解卦助手
                </h3>
                <div className="space-y-3 text-sm">
                  {/* AI对话消息区域 */}
                  <div className="bg-[#1e293b] p-3 rounded border border-[#374151] min-h-[300px] max-h-[400px] overflow-y-auto">
                    <div className="text-white/70 text-center py-8">
                      <Sparkles className="h-8 w-8 mx-auto mb-3 opacity-50" />
                      <p>AI解卦功能即将推出</p>
                      <p className="text-xs mt-2">将为您提供个性化的卦象解读</p>
                    </div>
                  </div>
                  
                  {/* AI对话输入框 */}
                  <div className="flex gap-2">
                    <Input
                      placeholder="询问AI关于这个卦象..."
                      className="bg-[#1e293b] border-[#374151] text-white placeholder-white/50 text-sm flex-1"
                      disabled
                    />
                    <Button
                      size="sm"
                      className="bg-[#4f46e5] hover:bg-[#4338ca] px-3"
                      disabled
                    >
                      <Zap className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </div>

              {/* 备注和保存 */}
              <div className="p-4 border-b border-[#374151]">
                <h3 className="text-sm font-medium text-white/90 mb-3">备注</h3>
                <Textarea
                  placeholder="添加您的备注..."
                  value={notes}
                  onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setNotes(e.target.value)}
                  className="bg-[#1e293b] border-[#374151] text-white placeholder-white/50 resize-none text-sm"
                  rows={3}
                />
                <Button
                  onClick={saveToHistory}
                  className="mt-3 w-full bg-[#10b981] hover:bg-[#059669] text-sm"
                  size="sm"
                >
                  <Calendar className="h-4 w-4 mr-2" />
                  保存到历史
                </Button>
              </div>

              {/* 快速操作 */}
              <div className="p-4">
                <h3 className="text-sm font-medium text-white/90 mb-3">快速操作</h3>
                <div className="space-y-2">
                  <Button
                    onClick={downloadResult}
                    className="w-full bg-[#1e293b] border border-[#374151] text-white/80 hover:bg-[#374151]/30 hover:text-white button-hover justify-start text-sm"
                    variant="outline"
                    size="sm"
                  >
                    <Download className="h-4 w-4 mr-2" />
                    下载结果
                  </Button>

                  <Button
                    onClick={() => copyToClipboard(generateReportContent(result), '占卜结果已复制')}
                    className="w-full bg-[#1e293b] border border-[#374151] text-white/80 hover:bg-[#374151]/30 hover:text-white button-hover justify-start text-sm"
                    variant="outline"
                    size="sm"
                  >
                    <Copy className="h-4 w-4 mr-2" />
                    复制结果
                  </Button>

                  <Button
                    onClick={resetDivination}
                    className="w-full bg-[#1e293b] border border-[#374151] text-white/80 hover:bg-[#374151]/30 hover:text-white button-hover justify-start text-sm"
                    variant="outline"
                    size="sm"
                  >
                    <RefreshCw className="h-4 w-4 mr-2" />
                    重新开始
                  </Button>

                  <Button
                    onClick={() => showInfo('分享功能', '分享功能即将推出')}
                    className="w-full bg-[#1e293b] border border-[#374151] text-white/80 hover:bg-[#374151]/30 hover:text-white button-hover justify-start text-sm"
                    variant="outline"
                    size="sm"
                  >
                    <Share2 className="h-4 w-4 mr-2" />
                    分享结果
                  </Button>
                </div>
              </div>
            </div>
          ) : (
            <div className="p-4">
              <h3 className="text-sm font-medium text-white/90 mb-3 flex items-center gap-2">
                <Sparkles className="h-4 w-4" />
                AI解卦助手
              </h3>
              <div className="space-y-3 text-white/70 text-sm">
                <div className="bg-[#1e293b] p-3 rounded border border-[#374151] text-center py-8">
                  <Sparkles className="h-8 w-8 mx-auto mb-3 opacity-50" />
                  <p>完成占卜后</p>
                  <p>AI将为您提供智能解读</p>
                </div>
                
                <div className="bg-[#1e293b] p-3 rounded border border-[#374151]">
                  <h4 className="text-white/90 font-medium mb-2">AI功能预告</h4>
                  <ul className="space-y-1 text-xs">
                    <li>• 个性化卦象解读</li>
                    <li>• 互动式问答</li>
                    <li>• 深度分析建议</li>
                    <li>• 历史对比参考</li>
                  </ul>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>      {/* 调试信息 */}
      {process.env.NODE_ENV === 'development' && (
        <div className="absolute bottom-2 left-2 text-white/50 text-xs bg-black/30 p-1 rounded">
          调试: 问题={question ? '已填写' : '未填写'}, 
          起卦={divinationInput ? '已完成' : '未完成（后端自动起卦）'}, 
          加载中={isLoading ? '是' : '否'}
        </div>
      )}
    </div>
    </TooltipProvider>
  );
};

export default DivinationWorkbench;
