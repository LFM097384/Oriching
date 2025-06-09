import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { 
  Coins, 
  Hash, 
  Calendar, 
  Clock,
  Dice1,
  Dice2,
  Dice3,
  Dice4,
  Dice5,
  Dice6,
  Play
} from 'lucide-react';

// 占卜方法类型
export type DivinationMethod = 'coins' | 'numbers' | 'yarrow' | 'time' | 'random';

// 占卜输入结果
export interface DivinationInputResult {
  method: DivinationMethod;
  data?: any;
  timestamp?: Date;
}

interface DivinationMethodSelectorProps {
  selectedMethod: DivinationMethod;
  onMethodChange: (method: DivinationMethod) => void;
  onGenerate: (result: DivinationInputResult) => void;
  isLoading?: boolean;
}

const DivinationMethodSelector: React.FC<DivinationMethodSelectorProps> = ({
  selectedMethod,
  onMethodChange,
  onGenerate,
  isLoading = false
}) => {
  const [coinResults, setCoinResults] = useState<number[]>([]);
  const [numberInput, setNumberInput] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const methods = [
    {
      id: 'coins' as DivinationMethod,
      name: '铜钱法',
      description: '传统三枚铜钱起卦',
      icon: Coins,
      color: 'bg-amber-500/20 text-amber-400'
    },
    {
      id: 'numbers' as DivinationMethod,
      name: '数字法',
      description: '输入数字进行起卦',
      icon: Hash,
      color: 'bg-blue-500/20 text-blue-400'
    },
    {
      id: 'time' as DivinationMethod,
      name: '时间法',
      description: '根据当前时间起卦',
      icon: Clock,
      color: 'bg-green-500/20 text-green-400'
    },
    {
      id: 'random' as DivinationMethod,
      name: '随机法',
      description: '系统随机生成卦象',
      icon: Calendar,
      color: 'bg-purple-500/20 text-purple-400'
    }
  ];

  // 掷铜钱动画
  const throwCoins = async () => {
    setIsGenerating(true);
    const results: number[] = [];
    
    for (let i = 0; i < 6; i++) {
      // 模拟掷铜钱延迟
      await new Promise(resolve => setTimeout(resolve, 300));
      
      // 生成三枚铜钱的结果 (正面=3, 反面=2)
      const coinThrow = Array.from({length: 3}, () => Math.random() < 0.5 ? 2 : 3);
      const sum = coinThrow.reduce((a, b) => a + b, 0);
      results.push(sum);
      setCoinResults([...results]);
    }
    
    setIsGenerating(false);
    onGenerate({
      method: 'coins',
      data: results,
      timestamp: new Date()
    });
  };

  // 数字法生成
  const generateFromNumbers = () => {
    if (!numberInput.trim()) return;
    
    const numbers = numberInput.split('').map(n => parseInt(n)).filter(n => !isNaN(n));
    if (numbers.length < 2) return;
    
    onGenerate({
      method: 'numbers',
      data: numbers,
      timestamp: new Date()
    });
  };

  // 时间法生成
  const generateFromTime = () => {
    const now = new Date();
    const timeData = {
      year: now.getFullYear(),
      month: now.getMonth() + 1,
      day: now.getDate(),
      hour: now.getHours(),
      minute: now.getMinutes()
    };
    
    onGenerate({
      method: 'time',
      data: timeData,
      timestamp: now
    });
  };

  // 随机法生成
  const generateRandom = () => {
    const randomData = Array.from({length: 6}, () => Math.floor(Math.random() * 4) + 6);
    
    onGenerate({
      method: 'random',
      data: randomData,
      timestamp: new Date()
    });
  };

  const handleGenerate = () => {
    switch (selectedMethod) {
      case 'coins':
        throwCoins();
        break;
      case 'numbers':
        generateFromNumbers();
        break;
      case 'time':
        generateFromTime();
        break;
      case 'random':
        generateRandom();
        break;
    }
  };

  const getDiceIcon = (value: number) => {
    const icons = [Dice1, Dice2, Dice3, Dice4, Dice5, Dice6];
    const Icon = icons[Math.min(value - 1, 5)] || Dice1;
    return Icon;
  };

  return (
    <div className="space-y-4">
      {/* 方法选择 */}
      <div className="grid grid-cols-2 gap-2">
        {methods.map((method) => {
          const Icon = method.icon;
          return (
            <button
              key={method.id}
              onClick={() => onMethodChange(method.id)}
              className={`p-3 rounded-lg border transition-all ${
                selectedMethod === method.id
                  ? 'border-blue-500 bg-blue-500/10 text-blue-400'
                  : 'border-gray-600 bg-gray-800/50 text-gray-400 hover:border-gray-500'
              }`}
            >
              <div className="flex items-center gap-2">
                <Icon className="h-4 w-4" />
                <div className="text-left">
                  <div className="text-sm font-medium">{method.name}</div>
                  <div className="text-xs opacity-70">{method.description}</div>
                </div>
              </div>
            </button>
          );
        })}
      </div>

      {/* 方法特定输入 */}
      <Card className="bg-gray-900/50 border-gray-700">
        <CardContent className="p-4">
          {selectedMethod === 'coins' && (
            <div className="space-y-3">
              <div className="text-sm text-gray-400">
                点击按钮投掷铜钱，每次生成一爻
              </div>
              {coinResults.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {coinResults.map((result, index) => {
                    const Icon = getDiceIcon(result);
                    return (
                      <Badge key={index} variant="outline" className="flex items-center gap-1">
                        <Icon className="h-3 w-3" />
                        {result}
                      </Badge>
                    );
                  })}
                </div>
              )}
            </div>
          )}

          {selectedMethod === 'numbers' && (
            <div className="space-y-3">
              <div className="text-sm text-gray-400">
                输入一串数字，系统将根据数字规律生成卦象
              </div>
              <input
                type="text"
                value={numberInput}
                onChange={(e) => setNumberInput(e.target.value)}
                placeholder="例如：123456789"
                className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md text-white"
                disabled={isLoading}
              />
            </div>
          )}

          {selectedMethod === 'time' && (
            <div className="space-y-3">
              <div className="text-sm text-gray-400">
                根据当前时间的年、月、日、时、分生成卦象
              </div>
              <div className="text-xs text-gray-500">
                当前时间：{new Date().toLocaleString()}
              </div>
            </div>
          )}

          {selectedMethod === 'random' && (
            <div className="space-y-3">
              <div className="text-sm text-gray-400">
                系统随机生成卦象，适合快速占卜
              </div>
            </div>
          )}

          <Button
            onClick={handleGenerate}
            disabled={isLoading || isGenerating || (selectedMethod === 'numbers' && !numberInput.trim())}
            className="w-full mt-4"
          >
            <Play className="h-4 w-4 mr-2" />
            {isGenerating ? '生成中...' : '生成卦象'}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default DivinationMethodSelector;
