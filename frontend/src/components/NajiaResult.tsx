import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { 
  Clock, 
  Star, 
  Zap, 
  Target, 
  Eye, 
  Shield,
  Calendar,
  Compass
} from 'lucide-react';
import type { NajiaDivinationResult, NajiaLineInfo, GanZhiTime } from '../types/najia';

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
      </div>
      {ganzhi.xunkong.length > 0 && (
        <div className="col-span-2 md:col-span-4 text-center mt-2">
          <div className="text-xs text-white/60 mb-1">旬空</div>
          <div className="flex justify-center gap-1">
            {ganzhi.xunkong.map((xk, idx) => (
              <Badge key={idx} className="bg-gray-500/20 text-gray-300 border-gray-500/30 text-xs">
                {xk}
              </Badge>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  const renderNajiaLine = (line: NajiaLineInfo, index: number) => (
    <div key={index} className={`p-3 rounded-lg border ${
      line.shi_yao ? 'bg-amber-500/10 border-amber-500/30' : 
      line.ying_yao ? 'bg-blue-500/10 border-blue-500/30' : 
      'bg-[#1f2937]/30 border-[#374151]/30'
    }`}>
      <div className="flex justify-between items-start mb-2">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-white/90">
            {['初', '二', '三', '四', '五', '上'][index]}爻
          </span>
          <div className={`w-6 h-2 rounded ${
            line.yao_type === 'yang' ? 'bg-red-400' : 'bg-blue-400'
          }`} />
          {line.changing && (
            <Badge className="bg-orange-500/20 text-orange-300 border-orange-500/30 text-xs">
              变
            </Badge>
          )}
        </div>
        <div className="flex gap-1">
          {line.shi_yao && (
            <Badge className="bg-amber-500/20 text-amber-300 border-amber-500/30 text-xs">
              <Star className="w-3 h-3 mr-1" />
              世
            </Badge>
          )}
          {line.ying_yao && (
            <Badge className="bg-blue-500/20 text-blue-300 border-blue-500/30 text-xs">
              <Target className="w-3 h-3 mr-1" />
              应
            </Badge>
          )}
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
        <div>
          <span className="text-white/60">纳甲:</span>
          <Badge variant="outline" className="ml-1 text-xs">
            {line.najia}
          </Badge>
        </div>
        <div>
          <span className="text-white/60">五行:</span>
          <Badge variant="outline" className="ml-1 text-xs">
            {line.wuxing}
          </Badge>
        </div>
        <div>
          <span className="text-white/60">六亲:</span>
          <Badge variant="outline" className="ml-1 text-xs">
            {line.liuqin}
          </Badge>
        </div>
        <div>
          <span className="text-white/60">六神:</span>
          <Badge variant="outline" className="ml-1 text-xs">
            {line.liushen}
          </Badge>
        </div>
      </div>

      {(line.fushen || line.xunkong) && (
        <div className="mt-2 pt-2 border-t border-white/10">
          <div className="flex gap-3 text-xs">
            {line.fushen && (
              <div>
                <span className="text-white/60">伏神:</span>
                <Badge className="bg-purple-500/20 text-purple-300 border-purple-500/30 ml-1 text-xs">
                  {line.fushen}
                </Badge>
              </div>
            )}
            {line.xunkong && (
              <Badge className="bg-gray-500/20 text-gray-300 border-gray-500/30 text-xs">
                <Shield className="w-3 h-3 mr-1" />
                旬空
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
        </CardHeader>
        <CardContent>
          <div className="text-sm text-white/70 mb-3">
            {new Date(najiaResult.divination_time).toLocaleString('zh-CN')}
          </div>
          {renderGanZhiTime(najiaResult.ganzhi_time)}
        </CardContent>
      </Card>

      {/* 本卦纳甲信息 */}
      <Card className="bg-[#111827]/50 border-[#374151]/30">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg text-white/90 flex items-center gap-2">
            <Compass className="h-5 w-5 text-blue-400" />
            本卦 - {najiaResult.original_hexagram.name}
          </CardTitle>
          <div className="flex gap-2 mt-2">
            <Badge className="bg-green-500/20 text-green-300 border-green-500/30">
              {najiaResult.original_hexagram.palace}宫
            </Badge>
            <Badge className="bg-cyan-500/20 text-cyan-300 border-cyan-500/30">
              {najiaResult.original_hexagram.wuxing}
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {najiaResult.original_hexagram.lines.map((line, index) => 
              renderNajiaLine(line, index)
            )}
          </div>
        </CardContent>
      </Card>

      {/* 变卦纳甲信息 */}
      {najiaResult.changed_hexagram && (
        <Card className="bg-[#111827]/50 border-[#374151]/30">
          <CardHeader className="pb-3">
            <CardTitle className="text-lg text-white/90 flex items-center gap-2">
              <Zap className="h-5 w-5 text-orange-400" />
              变卦 - {najiaResult.changed_hexagram.name}
            </CardTitle>
            <div className="flex gap-2 mt-2">
              <Badge className="bg-green-500/20 text-green-300 border-green-500/30">
                {najiaResult.changed_hexagram.palace}宫
              </Badge>
              <Badge className="bg-cyan-500/20 text-cyan-300 border-cyan-500/30">
                {najiaResult.changed_hexagram.wuxing}
              </Badge>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {najiaResult.changed_hexagram.lines.map((line, index) => 
                renderNajiaLine(line, index)
              )}
            </div>
          </CardContent>
        </Card>
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
      </Card>

      {/* 详细分析 */}
      {Object.keys(najiaResult.detailed_analysis).length > 0 && (
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
