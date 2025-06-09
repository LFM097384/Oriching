// 扩展的国际化配置和翻译
export interface ExtendedTranslations {
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
    trigrams: string;
    upperTrigram: string;
    lowerTrigram: string;
    linePosition: string;
    changingLine: string;
    fortuneAspects: {
      overall: string;
      career: string;
      business: string;
      fame: string;
      love: string;
      health: string;
      advice: string;
    };
    divinerName: string;
    divinerNamePlaceholder: string;
    method: string;
    methodCoins: string;
    methodSticks: string;
    methodTime: string;
    quickStart: string;
    quickStartDesc: string;
    resetForm: string;
    focusInput: string;
    hotkeysTitle: string;
    hotkeyFocus: string;
    hotkeyStart: string;
    hotkeyReset: string;
    notes: string;
    notesPlaceholder: string;
    saveToHistory: string;
    downloadResult: string;
    copyResult: string;
    shareResult: string;
    restart: string;
    aiAssistant: string;
    aiPlaceholder: string;
    aiThinking: string;
    aiFeatures: string;
    aiUsageTips: string;
    aiTipTitle: string;
    aiTipContent: string;
    quickActions: string;
    originalHex: string;
    changedHex: string;
    mutualHex: string;
    hexagramDisplay: string;
    startDivinationTitle: string;
    startDivinationDesc1: string;
    startDivinationDesc2: string;
    discussWithAi: string;
    aiWillHelp: string;
    returnToHome: string;
    switchLanguage: string;
    debugInfo: string;
    questionFilled: string;
    questionNotFilled: string;
    hexagramCompleted: string;
    hexagramNotCompleted: string;
    autoGenerate: string;
    loadingYes: string;
    loadingNo: string;
    lineNumber: string;
    reportTitle: string;
    reportGenerated: string;
    anonymous: string;
    messages: {
      divinationComplete: string;
      divinationCompleteDesc: string;
      copySuccess: string;
      copyFailed: string;
      clipboardError: string;
      saveSuccess: string;
      saveSuccessDesc: string;
      saveFailed: string;
      saveFailedDesc: string;
      divinationError: string;
      requestFailed: string;
      aiChatFailed: string;
      aiChatFailedDesc: string;
      aiReply: string;
      aiReplyDesc: string;
      shareFeature: string;
      shareFeatureDesc: string;
      historyView: string;
      historyViewDesc: string;
    };
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
      quickActions: string;
    };
    
    fortune: {
      overall: string;
      career: string;
      love: string;
      auspicious: string;
      inauspicious: string;
      suggestions: string;
    };
    
    hexagram: {
      yang: string;
      yin: string;
      changing: string;
      position: string;
      number: string;
    };
  };
  
  // 设置
  settings: {
    language: string;
    darkMode: string;
    notifications: string;
    account: string;
    help: string;
    about: string;
  };
  
  // 历史记录
  history: {
    title: string;
    empty: string;
    viewDetailed: string;
    divination: string;
    today: string;
    total: string;
  };
  
  // 用户
  user: {
    level: string;
    vip: string;
    divinationCount: string;
    historyRecords: string;
    memberLevel: string;
  };
  
  // 操作
  actions: {
    viewHistory: string;
    learnYijing: string;
    advancedMode: string;
    tutorial: string;
  };
}

// 中文翻译
export const zhExtendedTranslations: ExtendedTranslations = {
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
    questionPlaceholder: "请输入您想要占卜的问题...",
    startDivination: "开始占卜",
    divining: "占卜中...",
    result: "占卜结果",
    question: "问题",
    time: "占卜时间",
    interpretation: "解读",
    originalHexagram: "本卦",
    changedHexagram: "变卦",
    detailedInfo: "详细信息",
    hexagramLines: "爻象",
    lineExplanation: "爻辞详解",
    judgment: "卦辞",
    image: "象辞",
    description: "说明",
    trigrams: "八卦",
    upperTrigram: "上卦",
    lowerTrigram: "下卦",
    linePosition: "爻位",
    changingLine: "变爻",
    fortuneAspects: {
      overall: "总体运势",
      career: "事业运势",
      business: "经商运势",
      fame: "求名运势",
      love: "感情运势",
      health: "健康运势",
      advice: "决策建议",
    },
    divinerName: "占卜师姓名（可选）",
    divinerNamePlaceholder: "请输入占卜师姓名",
    method: "起卦方式",
    methodCoins: "金钱卦",
    methodSticks: "蓍草卦",
    methodTime: "时间卦",
    quickStart: "按 Ctrl+Enter 快速开始占卜",
    quickStartDesc: "在左侧输入您的问题，选择起卦方式，然后点击"开始占卜"按钮。",
    resetForm: "重置表单",
    focusInput: "聚焦问题输入",
    hotkeysTitle: "快捷键帮助",
    hotkeyFocus: "Ctrl+K: 聚焦输入框",
    hotkeyStart: "Ctrl+Enter: 开始占卜",
    hotkeyReset: "Ctrl+R: 重置",
    notes: "备注",
    notesPlaceholder: "添加您的备注...",
    saveToHistory: "保存到历史",
    downloadResult: "下载结果",
    copyResult: "复制结果",
    shareResult: "分享结果",
    restart: "重新开始",
    aiAssistant: "AI解卦助手",
    aiPlaceholder: "询问AI关于这个卦象...",
    aiThinking: "AI正在思考...",
    aiFeatures: "AI助手功能",
    aiUsageTips: "使用提示",
    aiTipTitle: "AI助手功能",
    aiTipContent: "占卜完成后，您可以向AI询问卦象的深层含义、如何应用到具体问题中，或者请求更详细的解释。",
    quickActions: "快速操作",
    originalHex: "本卦",
    changedHex: "变卦",
    mutualHex: "互卦",
    hexagramDisplay: "卦象",
    startDivinationTitle: "开始占卜",
    startDivinationDesc1: "在左侧输入您的问题，选择起卦方式，然后点击"开始占卜"按钮。",
    startDivinationDesc2: "系统将根据古老的易经原理为您提供生活智慧和指导。",
    discussWithAi: "与AI讨论您的卦象",
    aiWillHelp: "AI将基于当前卦象为您答疑解惑",
    returnToHome: "返回",
    switchLanguage: "切换到中文",
    debugInfo: "调试",
    questionFilled: "已填写",
    questionNotFilled: "未填写",
    hexagramCompleted: "已完成",
    hexagramNotCompleted: "未完成（后端自动起卦）",
    autoGenerate: "后端自动起卦",
    loadingYes: "是",
    loadingNo: "否",
    lineNumber: "第{number}爻",
    reportTitle: "易经占卜结果报告",
    reportGenerated: "此报告由易经占卜工作台生成",
    anonymous: "匿名",
    messages: {
      divinationComplete: "占卜完成",
      divinationCompleteDesc: "您的卦象已生成，请查看结果",
      copySuccess: "复制成功",
      copyFailed: "复制失败",
      clipboardError: "无法复制到剪贴板",
      saveSuccess: "保存成功",
      saveSuccessDesc: "占卜结果已保存到历史记录",
      saveFailed: "保存失败",
      saveFailedDesc: "无法保存到历史记录",
      divinationError: "占卜过程中发生错误，请重试",
      requestFailed: "占卜请求失败",
      aiChatFailed: "AI聊天失败",
      aiChatFailedDesc: "无法获取AI回复，请稍后重试",
      aiReply: "AI回复",
      aiReplyDesc: "已收到AI的解读回复",
      shareFeature: "分享功能",
      shareFeatureDesc: "分享功能即将推出",
      historyView: "这是历史记录查看",
      historyViewDesc: "详细解释请查看原始占卜结果。",
    },
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
export const enExtendedTranslations: ExtendedTranslations = {
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
    questionPlaceholder: "Please enter your divination question...",
    startDivination: "Start Divination",
    divining: "Divining...",
    result: "Divination Result",
    question: "Question",
    time: "Divination Time",
    interpretation: "Interpretation",
    originalHexagram: "Original Hexagram",
    changedHexagram: "Changed Hexagram",
    detailedInfo: "Detailed Information",
    hexagramLines: "Hexagram Lines",
    lineExplanation: "Line Explanations",
    judgment: "Judgment",
    image: "Image",
    description: "Description",
    trigrams: "Trigrams",
    upperTrigram: "Upper Trigram",
    lowerTrigram: "Lower Trigram",
    linePosition: "Line Position",
    changingLine: "Changing Line",
    fortuneAspects: {
      overall: "Overall Fortune",
      career: "Career Fortune",
      business: "Business Fortune",
      fame: "Fame Fortune",
      love: "Love Fortune",
      health: "Health Fortune",
      advice: "Decision Advice",
    },
    divinerName: "Diviner Name (Optional)",
    divinerNamePlaceholder: "Please enter diviner name",
    method: "Divination Method",
    methodCoins: "Coin Method",
    methodSticks: "Yarrow Stalk Method",
    methodTime: "Time-based Method",
    quickStart: "Press Ctrl+Enter to start quickly",
    quickStartDesc: "Enter your question on the left, select a divination method, then click 'Start Divination'.",
    resetForm: "Reset Form",
    focusInput: "Focus Input",
    hotkeysTitle: "Keyboard Shortcuts",
    hotkeyFocus: "Ctrl+K: Focus input box",
    hotkeyStart: "Ctrl+Enter: Start divination",
    hotkeyReset: "Ctrl+R: Reset",
    notes: "Notes",
    notesPlaceholder: "Add your notes...",
    saveToHistory: "Save to History",
    downloadResult: "Download Result",
    copyResult: "Copy Result",
    shareResult: "Share Result",
    restart: "Restart",
    aiAssistant: "AI Interpretation Assistant",
    aiPlaceholder: "Ask AI about this hexagram...",
    aiThinking: "AI is thinking...",
    aiFeatures: "AI Assistant Features",
    aiUsageTips: "Usage Tips",
    aiTipTitle: "AI Assistant Features",
    aiTipContent: "After divination, you can ask AI about the deeper meaning of the hexagram, how to apply it to specific situations, or request more detailed explanations.",
    quickActions: "Quick Actions",
    originalHex: "Original",
    changedHex: "Changed",
    mutualHex: "Mutual",
    hexagramDisplay: "Hexagram",
    startDivinationTitle: "Start Divination",
    startDivinationDesc1: "Enter your question on the left, select a divination method, then click 'Start Divination'.",
    startDivinationDesc2: "The system will provide life wisdom and guidance based on ancient I Ching principles.",
    discussWithAi: "Discuss your hexagram with AI",
    aiWillHelp: "AI will help answer questions based on the current hexagram",
    returnToHome: "Back",
    switchLanguage: "Switch to English",
    debugInfo: "Debug",
    questionFilled: "Filled",
    questionNotFilled: "Not filled",
    hexagramCompleted: "Completed",
    hexagramNotCompleted: "Not completed (backend auto-generation)",
    autoGenerate: "Backend auto-generation",
    loadingYes: "Yes",
    loadingNo: "No",
    lineNumber: "Line {number}",
    reportTitle: "I Ching Divination Result Report",
    reportGenerated: "This report was generated by the I Ching Divination Workbench",
    anonymous: "Anonymous",
    messages: {
      divinationComplete: "Divination Complete",
      divinationCompleteDesc: "Your hexagram has been generated, please check the result",
      copySuccess: "Copy Successful",
      copyFailed: "Copy Failed",
      clipboardError: "Unable to copy to clipboard",
      saveSuccess: "Save Successful",
      saveSuccessDesc: "Divination result has been saved to history",
      saveFailed: "Save Failed",
      saveFailedDesc: "Unable to save to history",
      divinationError: "An error occurred during divination, please try again",
      requestFailed: "Divination request failed",
      aiChatFailed: "AI Chat Failed",
      aiChatFailedDesc: "Unable to get AI response, please try again later",
      aiReply: "AI Reply",
      aiReplyDesc: "Received AI interpretation response",
      shareFeature: "Share Feature",
      shareFeatureDesc: "Share feature coming soon",
      historyView: "This is a history record view",
      historyViewDesc: "For detailed explanations, please check the original divination result.",
    },
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

// 扩展语言配置
export const extendedLanguages = {
  zh: {
    name: '中文',
    flag: '🇨🇳',
    translations: zhExtendedTranslations,
  },
  en: {
    name: 'English',
    flag: '🇺🇸',
    translations: enExtendedTranslations,
  },
};

// 默认语言
export const defaultLanguage: Language = 'zh';
