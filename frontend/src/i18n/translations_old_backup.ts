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
    trigrams: string;
    upperTrigram: string;
    lowerTrigram: string;
    linePosition: string;
    changingLine: string;
    changingLines: string;
    // AI related
    aiChat: string;
    aiChatPlaceholder: string;
    aiChatWelcome: string;
    aiChatDescription: string;
    aiHelperTitle: string;
    aiTips: string;
    aiInterpretationTitle: string;
    aiThinking: string;
    aiReplyReceived: string;
    aiChatFailed: string;
    cannotGetAiReply: string;
    // UI actions
    viewOriginal: string;
    viewChanged: string;
    viewMutual: string;
    downloadResult: string;
    restartDivination: string;
    shareFeature: string;
    shareFeatureComingSoon: string;
    // Form and method
    divinationMethod: string;
    focusQuestionInput: string;
    resetFormAction: string;
    questionTitle: string;fortuneAspects: {
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
    export: string;
    aiChat: string;
    aiChatPlaceholder: string;
    aiSend: string;
    viewOriginal: string;
    viewChanged: string;
    viewMutual: string;
    changingLines: string;
    noChangingLines: string;
    saveRecord: string;
    clearAll: string;
    copyResult: string;
    shareResult: string;
    mutualHexagram: string;
    traditionalInterpretation: string;
    modernInterpretation: string;
    sixLines: string;
    firstLine: string;
    secondLine: string;
    thirdLine: string;
    fourthLine: string;
    fifthLine: string;
    sixthLine: string;
    aiChatWelcome: string;
    aiChatDescription: string;
    aiHelperTitle: string;
    aiTips: string;
    aiUsageGuide: string;
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
    changingLine: "变爻",
    changingLines: "变爻",
    // AI related
    aiChat: "AI解卦",
    aiChatPlaceholder: "向AI询问关于这个卦象的问题...",
    aiChatWelcome: "与AI讨论您的卦象",
    aiChatDescription: "AI将基于当前卦象为您答疑解惑",
    aiHelperTitle: "AI解卦助手",
    aiTips: "AI助手功能",
    aiInterpretationTitle: "AI将为您提供智能解读",
    aiThinking: "AI正在思考...",
    aiReplyReceived: "已收到AI的解读回复",
    aiChatFailed: "AI聊天失败",
    cannotGetAiReply: "无法获取AI回复，请稍后重试",
    // UI actions
    viewOriginal: "本卦",
    viewChanged: "变卦",
    viewMutual: "互卦",
    downloadResult: "下载结果",
    restartDivination: "重新开始",
    shareFeature: "分享功能",
    shareFeatureComingSoon: "分享功能即将推出",
    // Form and method
    divinationMethod: "起卦方式",
    focusQuestionInput: "聚焦问题输入",
    resetFormAction: "重置表单",
    questionTitle: "问题",
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
    trigrams: "八卦",    notes: "备注",
    notesPlaceholder: "添加您的备注...",
    export: "导出结果",
    aiSend: "发送",
    noChangingLines: "无变爻",
    saveRecord: "保存记录",
    clearAll: "清空所有",
    copyResult: "复制结果",
    shareResult: "分享结果",
    mutualHexagram: "互卦",
    traditionalInterpretation: "传统解释",
    modernInterpretation: "现代解释",
    sixLines: "六爻",
    firstLine: "初爻",
    secondLine: "二爻",
    thirdLine: "三爻",
    fourthLine: "四爻",
    fifthLine: "五爻",
    sixthLine: "上爻",
    aiUsageGuide: "使用提示",
    aiChat: "AI解卦",
    aiChatPlaceholder: "向AI询问关于这个卦象的问题...",
    aiSend: "发送",
    viewOriginal: "本卦",
    viewChanged: "变卦",
    viewMutual: "互卦",
    changingLines: "变爻",
    noChangingLines: "无变爻",
    saveRecord: "保存记录",
    clearAll: "清空所有",
    copyResult: "复制结果",
    shareResult: "分享结果",
    mutualHexagram: "互卦",
    traditionalInterpretation: "传统解释",
    modernInterpretation: "现代解释",
    sixLines: "六爻",
    firstLine: "初爻",
    secondLine: "二爻",
    thirdLine: "三爻",
    fourthLine: "四爻",
    fifthLine: "五爻",
    sixthLine: "上爻",
    aiChatWelcome: "与AI讨论您的卦象",
    aiChatDescription: "AI将基于当前卦象为您答疑解惑",
    aiHelperTitle: "AI解卦助手",    aiTips: "AI助手功能",
    aiUsageGuide: "使用提示",
    // 新增翻译项
    downloadResult: "下载结果",
    restartDivination: "重新开始",
    shareFeature: "分享功能",
    shareFeatureComingSoon: "分享功能即将推出",
    divinationResultCopied: "占卜结果已复制",
    questionTitle: "问题",
    timeTitle: "时间",
    hexagramTitle: "卦象",
    interpretationTitle: "解读",
    originalHexagramPrefix: "本卦:",
    changedHexagramPrefix: "变卦:",
    timePrefix: "时间:",
    aiThinking: "AI正在思考...",
    aiReplyReceived: "已收到AI的解读回复",
    aiChatFailed: "AI聊天失败",
    cannotGetAiReply: "无法获取AI回复，请稍后重试",
    divinationMethod: "起卦方式",
    focusQuestionInput: "聚焦问题输入",
    resetFormAction: "重置表单",
    aiInterpretationTitle: "AI将为您提供智能解读",
    aiFeaturesList: "AI助手功能",
    usageTips: "使用提示",
    aiFeatureDeepAnalysis: "深度卦象解析",
    aiFeaturePersonalizedQA: "个性化问题答疑",
    aiFeatureRealTimeChat: "实时智能对话",
    aiFeatureTraditionalModern: "传统与现代结合",
    aiUsageDescription: "占卜完成后，您可以向AI询问卦象的深层含义、如何应用到具体问题中，或者请求更详细的解释。",
    debugQuestionFilled: "已填写",
    debugQuestionEmpty: "未填写",
    debugDivinationCompleted: "已完成",
    debugDivinationPending: "未完成（后端自动起卦）",
    debugLoadingYes: "是",    debugLoadingNo: "否",
    linePosition: "第{position}爻",
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
    changingLine: "Changing Line",
    changingLines: "Changing Lines",
    // AI related
    aiChat: "AI Interpretation",
    aiChatPlaceholder: "Ask AI about this hexagram...",
    aiChatWelcome: "Discuss your hexagram with AI",
    aiChatDescription: "AI will answer your questions based on the current hexagram",
    aiHelperTitle: "AI Interpretation Assistant",
    aiTips: "AI Assistant Features",
    aiInterpretationTitle: "AI will provide intelligent interpretation",
    aiThinking: "AI is thinking...",
    aiReplyReceived: "AI interpretation received",
    aiChatFailed: "AI chat failed",
    cannotGetAiReply: "Cannot get AI reply, please try again later",
    // UI actions
    viewOriginal: "Original",
    viewChanged: "Changed",
    viewMutual: "Mutual",
    downloadResult: "Download Result",
    restartDivination: "Restart",
    shareFeature: "Share Feature",
    shareFeatureComingSoon: "Share feature coming soon",
    // Form and method
    divinationMethod: "Divination Method",
    focusQuestionInput: "Focus question input",
    resetFormAction: "Reset form",
    questionTitle: "Question",
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
    trigrams: "Trigrams",
    upperTrigram: "Upper Trigram",
    lowerTrigram: "Lower Trigram",
    linePosition: "Line Position",
    changingLine: "Changing Line",    fortuneAspects: {
      overall: "Overall Fortune",
      career: "Career Fortune",
      business: "Business Fortune",
      fame: "Fame Fortune",
      love: "Love Fortune",
      health: "Health Fortune",
      advice: "Decision Advice",
    },
    divinerName: "Diviner Name",
    divinerNamePlaceholder: "Enter your name (optional)",
    method: "Divination Method",
    methodCoins: "Coin Method",
    methodSticks: "Yarrow Stalks",
    methodTime: "Time Divination",
    quickStart: "Quick Start",
    quickStartDesc: "Quick divination with default settings",
    resetForm: "Reset Form",
    focusInput: "Focus Input",
    hotkeysTitle: "Hotkeys",
    hotkeyFocus: "Focus question input",
    hotkeyStart: "Start divination",
    hotkeyReset: "Reset form",
    notes: "Notes",
    notesPlaceholder: "Add your notes...",
    export: "Export Result",
    aiChat: "AI Interpretation",
    aiChatPlaceholder: "Ask AI about this hexagram...",
    aiSend: "Send",
    viewOriginal: "Original",
    viewChanged: "Changed",
    viewMutual: "Mutual",
    changingLines: "Changing L    notes: "Notes",
    notesPlaceholder: "Add your notes...",
    export: "Export Result",
    aiSend: "Send",
    noChangingLines: "No Changing Lines",
    saveRecord: "Save Record",
    clearAll: "Clear All",
    copyResult: "Copy Result",
    shareResult: "Share Result",
    mutualHexagram: "Mutual Hexagram",
    traditionalInterpretation: "Traditional Interpretation",
    modernInterpretation: "Modern Interpretation",
    sixLines: "Six Lines",
    firstLine: "First Line",
    secondLine: "Second Line",
    thirdLine: "Third Line",
    fourthLine: "Fourth Line",
    fifthLine: "Fifth Line",
    sixthLine: "Sixth Line",
    aiUsageGuide: "Usage Tips",pretation",
    originalHexagramPrefix: "Original:",
    changedHexagramPrefix: "Changed:",
    timePrefix: "Time:",
    aiThinking: "AI is thinking...",
    aiReplyReceived: "AI interpretation received",
    aiChatFailed: "AI chat failed",
    cannotGetAiReply: "Cannot get AI reply, please try again later",
    divinationMethod: "Divination Method",
    focusQuestionInput: "Focus question input",
    resetFormAction: "Reset form",
    aiInterpretationTitle: "AI will provide intelligent interpretation",
    aiFeaturesList: "AI Assistant Features",
    usageTips: "Usage Tips",
    aiFeatureDeepAnalysis: "Deep hexagram analysis",
    aiFeaturePersonalizedQA: "Personalized Q&A",
    aiFeatureRealTimeChat: "Real-time intelligent chat",
    aiFeatureTraditionalModern: "Traditional & modern combined",
    aiUsageDescription: "After divination, you can ask AI about deeper meanings of the hexagram, how to apply it to specific questions, or request more detailed explanations.",
    debugQuestionFilled: "Filled",
    debugQuestionEmpty: "Empty",
    debugDivinationCompleted: "Completed",
    debugDivinationPending: "Pending (auto by backend)",
    debugLoadingYes: "Yes",    debugLoadingNo: "No",
    linePosition: "Line {position}",
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