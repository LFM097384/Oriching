// 国际化配置和翻译
export interface Translations {
  // 通用
  common: {
    loading: string;
    error: string;
    success: string;
    confirm: string;
    cancel: string;
    save: string;
    delete: string;
    edit: string;
    share: string;
    export: string;
    clear: string;
    back: string;
    next: string;
    close: string;
  };
  
  // 占卜相关
  divination: {
    title: string;
    subtitle: string;
    questionPlaceholder: string;
    startDivination: string;
    divining: string;
    result: string;
    question: string;
    time: string;
    interpretation: string;
    originalHexagram: string;
    changedHexagram: string;
    detailedInfo: string;
    hexagramLines: string;
    lineExplanation: string;
    judgment: string;
    image: string;
    description: string;
  };
  
  // 界面
  ui: {
    sidebar: {
      left: string;
      right: string;
      history: string;
      settings: string;
      todayFortune: string;
      recommendations: string;
      userInfo: string;
      questionInput: string;
    };
    
    settings: {
      darkMode: string;
      language: string;
      help: string;
      about: string;
    };
    
    welcome: {
      title: string;
      description: string;
      instruction: string;
    };
    
    interpretFuture: string;
    noHistoryRecords: string;
    
    fortune: {
      overall: string;
      career: string;
      love: string;
      auspicious: string;
      inauspicious: string;
      suggestions: string;
    };
    
    recommendations: {
      suitable: string;
      avoid: string;
      suitableActions: string;
      avoidActions: string;
    };
    
    user: {
      level: string;
      vip: string;
      divinationCount: string;
      historyRecords: string;
      memberLevel: string;
      today: string;
      total: string;
    };
    
    actions: {
      viewHistory: string;
      learnYijing: string;
      advancedMode: string;
      tutorial: string;
    };
  };
  
  // 卦象相关
  hexagram: {
    number: string;
    judgment: string;
    description: string;
    lineDetails: string;
    yang: string;
    yin: string;
    changing: string;
    position: string;
  };
}

// 中文翻译
export const zhTranslations: Translations = {
  common: {
    loading: "加载中...",
    error: "错误",
    success: "成功",
    confirm: "确认",
    cancel: "取消",
    save: "保存",
    delete: "删除",
    edit: "编辑",
    share: "分享",
    export: "导出",
    clear: "清空",
    back: "返回",
    next: "下一步",
    close: "关闭",
  },
  
  divination: {
    title: "占卜工作台",
    subtitle: "探索未知，解读命运",
    questionPlaceholder: "请详细描述您想要占卜的问题...",
    startDivination: "开始占卜",
    divining: "占卜中...",
    result: "占卜结果",
    question: "占卜问题",
    time: "占卜时间",
    interpretation: "卦象解释",
    originalHexagram: "本卦",
    changedHexagram: "变卦",
    detailedInfo: "详细信息",
    hexagramLines: "爻象",
    lineExplanation: "爻辞详解",
    judgment: "卦辞",
    image: "象辞",
    description: "说明",
  },
  
  ui: {
    sidebar: {
      left: "左侧边栏",
      right: "右侧边栏",
      history: "历史记录",
      settings: "设置",
      todayFortune: "今日运势",
      recommendations: "今日建议",
      userInfo: "用户信息",
      quickActions: "快速操作",
    },
    
    fortune: {
      overall: "整体运势",
      career: "事业财运",
      love: "感情运势",
      auspicious: "宜",
      inauspicious: "忌",
      suggestions: "建议",
    },
    
    hexagram: {
      yang: "阳爻",
      yin: "阴爻",
      changing: "变爻",
      position: "位置",
      number: "第 {number} 卦",
    },
  },
  
  settings: {
    language: "语言",
    darkMode: "深色模式",
    notifications: "通知",
    account: "账户",
    help: "帮助",
    about: "关于",
  },
  
  history: {
    title: "历史记录",
    empty: "暂无历史记录",
    viewDetailed: "查看详细历史",
    divination: "次占卜",
    today: "今日占卜次数",
    total: "历史记录",
  },
  
  user: {
    level: "等级",
    vip: "VIP",
    divinationCount: "占卜次数",
    historyRecords: "条记录",
    memberLevel: "会员等级",
  },
  
  actions: {
    viewHistory: "查看详细历史",
    learnYijing: "学习易经知识",
    advancedMode: "高级占卜模式",
    tutorial: "使用教程",
  },
};

// 英文翻译
export const enTranslations: Translations = {
  common: {
    loading: "Loading...",
    error: "Error",
    success: "Success",
    confirm: "Confirm",
    cancel: "Cancel",
    save: "Save",
    delete: "Delete",
    edit: "Edit",
    share: "Share",
    export: "Export",
    clear: "Clear",
    back: "Back",
    next: "Next",
    close: "Close",
  },
  
  divination: {
    title: "Divination Workbench",
    subtitle: "Explore the unknown, interpret destiny",
    questionPlaceholder: "Please describe your question in detail...",
    startDivination: "Start Divination",
    divining: "Divining...",
    result: "Divination Result",
    question: "Question",
    time: "Time",
    interpretation: "Interpretation",
    originalHexagram: "Original Hexagram",
    changedHexagram: "Changed Hexagram",
    detailedInfo: "Detailed Information",
    hexagramLines: "Hexagram Lines",
    lineExplanation: "Line Explanations",
    judgment: "Judgment",
    image: "Image",
    description: "Description",
  },
  
  ui: {
    sidebar: {
      left: "Left Sidebar",
      right: "Right Sidebar",
      history: "History",
      settings: "Settings",
      todayFortune: "Today's Fortune",
      recommendations: "Recommendations",
      userInfo: "User Info",
      quickActions: "Quick Actions",
    },
    
    fortune: {
      overall: "Overall Fortune",
      career: "Career & Finance",
      love: "Love & Relationships",
      auspicious: "Auspicious",
      inauspicious: "Inauspicious",
      suggestions: "Suggestions",
    },
    
    hexagram: {
      yang: "Yang Line",
      yin: "Yin Line",
      changing: "Changing Line",
      position: "Position",
      number: "Hexagram {number}",
    },
  },
  
  settings: {
    language: "Language",
    darkMode: "Dark Mode",
    notifications: "Notifications",
    account: "Account",
    help: "Help",
    about: "About",
  },
  
  history: {
    title: "History",
    empty: "No history records",
    viewDetailed: "View Detailed History",
    divination: "divinations",
    today: "Today's Divinations",
    total: "History Records",
  },
  
  user: {
    level: "Level",
    vip: "VIP",
    divinationCount: "Divination Count",
    historyRecords: "records",
    memberLevel: "Member Level",
  },
  
  actions: {
    viewHistory: "View Detailed History",
    learnYijing: "Learn I Ching",
    advancedMode: "Advanced Mode",
    tutorial: "Tutorial",
  },
};

// 支持的语言
export type Language = 'zh' | 'en';

// 语言配置
export const languages = {
  zh: {
    name: '中文',
    flag: '🇨🇳',
    translations: zhTranslations,
  },
  en: {
    name: 'English',
    flag: '🇺🇸',
    translations: enTranslations,
  },
};

// 默认语言
export const defaultLanguage: Language = 'zh';
