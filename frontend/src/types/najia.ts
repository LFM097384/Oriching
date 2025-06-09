// 纳甲占卜相关类型定义

export interface NajiaLineInfo {
  position: number;
  yao_type: 'yang' | 'yin';
  changing: boolean;
  najia: string;
  wuxing: string;
  liuqin: string;
  liushen: string;
  shi_yao: boolean;
  ying_yao: boolean;
  fushen?: string;
  xunkong: boolean;
}

export interface NajiaHexagramInfo {
  number: number;
  name: string;
  palace: string;
  wuxing: string;
  lines: NajiaLineInfo[];
  shi_yao_pos: number;
  ying_yao_pos: number;
}

export interface GanZhiTime {
  year_gz: string;
  month_gz: string;
  day_gz: string;
  hour_gz: string;
  xunkong: string[];
}

export interface NajiaDivinationResult {
  question: string;
  divination_time: string;
  ganzhi_time: GanZhiTime;
  original_hexagram: NajiaHexagramInfo;
  changed_hexagram?: NajiaHexagramInfo;
  traditional_interpretation: string;
  detailed_analysis: Record<string, any>;
}

// 扩展原有的占卜结果类型以包含纳甲信息
export interface EnhancedDivinationResult {
  question: string;
  originalHexagram: any;
  changedHexagram?: any;
  mutualHexagram?: any;
  lines: any[];
  timestamp: string;
  interpretation: string;
  divinerName?: string;
  notes?: string;
  changeInfo?: any;
  najia?: NajiaDivinationResult; // 纳甲分析结果
}
