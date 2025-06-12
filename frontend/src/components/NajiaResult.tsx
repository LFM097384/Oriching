import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import NajiaHexagram from './ui/najia-hexagram';
import { 
  Clock, 
  Eye, 
  Shield,
  Calendar
} from 'lucide-react';
import type { NajiaDivinationResult, GanZhiTime } from '../types/najia';

interface NajiaResultProps {
  najiaResult: NajiaDivinationResult;
}

const NajiaResult: React.FC<NajiaResultProps> = ({ najiaResult }) => {
  const renderGanZhiTime = (ganzhi: GanZhiTime) => (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      <div className="text-center">
        <div className="text-xs text-white/60 mb-1">年</div>
        <Badge className="bg-red-500/20 text-red-300 border-red-500/30">
          {ganzhi.year_gz}
        </Badge>
      </div>
      <div className="text-center">
        <div className="text-xs text-white/60 mb-1">月</div>
        <Badge className="bg-green-500/20 text-green-300 border-green-500/30">
          {ganzhi.month_gz}
        </Badge>
      </div>
      <div className="text-center">
        <div className="text-xs text-white/60 mb-1">日</div>
        <Badge className="bg-blue-500/20 text-blue-300 border-blue-500/30">
          {ganzhi.day_gz}
        </Badge>
      </div>
      <div className="text-center">
        <div className="text-xs text-white/60 mb-1">时</div>
        <Badge className="bg-purple-500/20 text-purple-300 border-purple-500/30">
          {ganzhi.hour_gz}
        </Badge>
      </div>      {ganzhi.xunkong && (
        <div className="col-span-2 md:col-span-4 text-center mt-2">
          <div className="text-xs text-white/60 mb-1">旬空</div>
          <div className="flex justify-center gap-1">
            {Array.isArray(ganzhi.xunkong) ? (
              ganzhi.xunkong.map((xk, idx) => (
                <Badge key={idx} className="bg-gray-500/20 text-gray-300 border-gray-500/30 text-xs">
                  <Shield className="w-3 h-3 mr-1" />
                  {xk}
                </Badge>
              ))
            ) : (
              <Badge className="bg-gray-500/20 text-gray-300 border-gray-500/30 text-xs">
                <Shield className="w-3 h-3 mr-1" />
                {ganzhi.xunkong}
              </Badge>
            )}
          </div>
        </div>
      )}
    </div>
  );

  return (
    <div className="space-y-4">
      {/* 干支时间 */}
      <Card className="bg-[#111827]/50 border-[#374151]/30">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg text-white/90 flex items-center gap-2">
            <Calendar className="h-5 w-5 text-amber-400" />
            起卦时间
          </CardTitle>
        </CardHeader>        <CardContent>
          <div className="text-sm text-white/70 mb-3">
            {new Date(najiaResult.divination_time).toLocaleString('zh-CN')}
          </div>
          {najiaResult.ganzhi_time && renderGanZhiTime(najiaResult.ganzhi_time)}
        </CardContent>
      </Card>      {/* 本卦纳甲信息 */}
      {najiaResult.original_hexagram && najiaResult.original_hexagram.lines && (
        <NajiaHexagram 
          lines={najiaResult.original_hexagram.lines}
          hexagramName={najiaResult.original_hexagram.name}
          palace={najiaResult.original_hexagram.palace}
          wuxing={najiaResult.original_hexagram.wuxing}
          title={`本卦 - ${najiaResult.original_hexagram.name}`}
        />
      )}      {/* 变卦纳甲信息 */}
      {najiaResult.changed_hexagram && najiaResult.changed_hexagram.lines && (
        <NajiaHexagram 
          lines={najiaResult.changed_hexagram.lines}
          hexagramName={najiaResult.changed_hexagram.name}
          palace={najiaResult.changed_hexagram.palace}
          wuxing={najiaResult.changed_hexagram.wuxing}
          title={`变卦 - ${najiaResult.changed_hexagram.name}`}
        />
      )}

      {/* 纳甲解卦 */}
      <Card className="bg-[#111827]/50 border-[#374151]/30">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg text-white/90 flex items-center gap-2">
            <Eye className="h-5 w-5 text-purple-400" />
            纳甲解卦
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="prose prose-invert max-w-none">
            <div className="text-white/80 leading-relaxed whitespace-pre-wrap">
              {najiaResult.traditional_interpretation}
            </div>
          </div>
        </CardContent>
      </Card>      {/* 详细分析 */}
      {najiaResult.detailed_analysis && Object.keys(najiaResult.detailed_analysis).length > 0 && (
        <Card className="bg-[#111827]/50 border-[#374151]/30">
          <CardHeader className="pb-3">
            <CardTitle className="text-lg text-white/90 flex items-center gap-2">
              <Clock className="h-5 w-5 text-indigo-400" />
              详细分析
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {Object.entries(najiaResult.detailed_analysis).map(([key, value]) => (
                <div key={key} className="p-3 bg-[#1f2937]/30 rounded-lg">
                  <div className="text-sm font-medium text-white/90 mb-1">
                    {key}
                  </div>
                  <div className="text-white/70 text-sm">
                    {typeof value === 'string' ? value : JSON.stringify(value)}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default NajiaResult;
