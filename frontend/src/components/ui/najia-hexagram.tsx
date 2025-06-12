import React from 'react';
import { Badge } from './badge';
import type { NajiaLineInfo } from '../../types/najia';

interface NajiaHexagramProps {
  lines: NajiaLineInfo[];
  hexagramName: string;
  palace?: string;
  wuxing?: string;
  title?: string;
}

const NajiaHexagram: React.FC<NajiaHexagramProps> = ({ 
  lines, 
  hexagramName, 
  palace, 
  wuxing, 
  title 
}) => {
  // 六亲颜色映射
  const getLiuqinColor = (liuqin: string) => {
    switch (liuqin) {
      case '父母': return 'bg-blue-500/20 text-blue-300 border-blue-500/30';
      case '兄弟': return 'bg-green-500/20 text-green-300 border-green-500/30';
      case '子孙': return 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30';
      case '妻财': return 'bg-red-500/20 text-red-300 border-red-500/30';
      case '官鬼': return 'bg-purple-500/20 text-purple-300 border-purple-500/30';
      default: return 'bg-gray-500/20 text-gray-300 border-gray-500/30';
    }
  };

  // 六神颜色映射
  const getLiushenColor = (liushen: string) => {
    switch (liushen) {
      case '青龙': return 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30';
      case '朱雀': return 'bg-red-500/20 text-red-300 border-red-500/30';
      case '勾陈': return 'bg-amber-500/20 text-amber-300 border-amber-500/30';
      case '螣蛇': return 'bg-purple-500/20 text-purple-300 border-purple-500/30';
      case '白虎': return 'bg-gray-500/20 text-gray-300 border-gray-500/30';
      case '玄武': return 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30';
      default: return 'bg-slate-500/20 text-slate-300 border-slate-500/30';
    }
  };
  // 世应爻标记
  const getShiYingMark = (line: NajiaLineInfo) => {
    if (line.shi_yao) return '世';
    if (line.ying_yao) return '应';
    return '';
  };

  // 渲染爻线
  const renderYaoLine = (line: NajiaLineInfo, index: number) => {
    const lineNumber = 6 - index; // 从上到下：六爻、五爻、四爻、三爻、二爻、初爻
    const isYang = line.yao_type === 'yang';
    const isChanging = line.changing;
    const shiYingMark = getShiYingMark(line);

    return (
      <div key={index} className="flex items-center gap-4 mb-6">
        {/* 左侧：六神 */}
        <div className="w-16 text-right">
          <Badge className={`${getLiushenColor(line.liushen)} text-xs`}>
            {line.liushen}
          </Badge>
        </div>

        {/* 中左：六亲 */}
        <div className="w-16 text-right">
          <Badge className={`${getLiuqinColor(line.liuqin)} text-xs`}>
            {line.liuqin}
          </Badge>
        </div>

        {/* 中间：爻象 */}
        <div className="flex items-center gap-2">
          {/* 爻位标记 */}
          <div className="w-8 text-center text-white/60 text-sm">
            {lineNumber === 1 && '初'}
            {lineNumber === 2 && '二'}
            {lineNumber === 3 && '三'}
            {lineNumber === 4 && '四'}
            {lineNumber === 5 && '五'}
            {lineNumber === 6 && '六'}
          </div>

          {/* 爻线 */}
          <div className="relative">
            <div className="flex items-center">
              {isYang ? (
                // 阳爻：实线
                <div className={`w-20 h-1 ${isChanging ? 'bg-amber-400' : 'bg-white'} rounded`} />
              ) : (
                // 阴爻：虚线
                <div className="flex gap-2">
                  <div className={`w-8 h-1 ${isChanging ? 'bg-amber-400' : 'bg-white'} rounded`} />
                  <div className={`w-8 h-1 ${isChanging ? 'bg-amber-400' : 'bg-white'} rounded`} />
                </div>
              )}
            </div>
            
            {/* 变爻标记 */}
            {isChanging && (
              <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                <div className="w-2 h-2 bg-amber-400 rounded-full animate-pulse" />
              </div>
            )}
          </div>

          {/* 世应标记 */}
          {shiYingMark && (
            <div className="w-8 text-center">
              <Badge className="bg-amber-500/20 text-amber-300 border-amber-500/30 text-xs font-bold">
                {shiYingMark}
              </Badge>
            </div>
          )}
        </div>

        {/* 中右：纳甲地支 */}
        <div className="w-16">
          <Badge variant="outline" className="text-xs">
            {line.najia}
          </Badge>
        </div>

        {/* 右侧：五行 */}
        <div className="w-16">
          <Badge variant="outline" className="text-xs">
            {line.wuxing}
          </Badge>
        </div>

        {/* 最右：特殊标记（伏神、旬空） */}
        <div className="w-20 flex gap-1">
          {line.fushen && (
            <Badge className="bg-purple-500/20 text-purple-300 border-purple-500/30 text-xs">
              伏
            </Badge>
          )}
          {line.xunkong && (
            <Badge className="bg-gray-500/20 text-gray-300 border-gray-500/30 text-xs">
              空
            </Badge>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="bg-[#111827]/50 border border-[#374151]/30 rounded-lg p-6">
      {/* 标题 */}
      <div className="text-center mb-6">
        <h3 className="text-xl font-bold text-white/90 mb-2">
          {title || hexagramName}
        </h3>
        <div className="flex justify-center gap-2">
          {palace && (
            <Badge className="bg-green-500/20 text-green-300 border-green-500/30">
              {palace}宫
            </Badge>
          )}
          {wuxing && (
            <Badge className="bg-cyan-500/20 text-cyan-300 border-cyan-500/30">
              {wuxing}
            </Badge>
          )}
        </div>
      </div>

      {/* 表头 */}
      <div className="flex items-center gap-4 mb-4 text-xs text-white/60 font-medium">
        <div className="w-16 text-right">六神</div>
        <div className="w-16 text-right">六亲</div>
        <div className="w-32 text-center">爻象</div>
        <div className="w-16 text-center">纳甲</div>
        <div className="w-16 text-center">五行</div>
        <div className="w-20 text-center">标记</div>
      </div>

      {/* 分隔线 */}
      <div className="border-t border-white/10 mb-4" />

      {/* 爻线（从上到下：六爻到初爻） */}
      <div>
        {lines.map((line, index) => renderYaoLine(line, index))}
      </div>

      {/* 底部说明 */}
      <div className="mt-6 pt-4 border-t border-white/10">
        <div className="flex flex-wrap gap-4 text-xs text-white/60">
          <div className="flex items-center gap-1">
            <div className="w-2 h-2 bg-amber-400 rounded-full" />
            <span>变爻</span>
          </div>
          <div className="flex items-center gap-1">
            <Badge className="bg-amber-500/20 text-amber-300 border-amber-500/30 text-xs">世</Badge>
            <span>世爻</span>
          </div>
          <div className="flex items-center gap-1">
            <Badge className="bg-amber-500/20 text-amber-300 border-amber-500/30 text-xs">应</Badge>
            <span>应爻</span>
          </div>
          <div className="flex items-center gap-1">
            <Badge className="bg-purple-500/20 text-purple-300 border-purple-500/30 text-xs">伏</Badge>
            <span>伏神</span>
          </div>
          <div className="flex items-center gap-1">
            <Badge className="bg-gray-500/20 text-gray-300 border-gray-500/30 text-xs">空</Badge>
            <span>旬空</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NajiaHexagram;
