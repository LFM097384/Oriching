"""
纳甲六爻占卜核心模块
基于传统六爻理论的完整实现

包含功能：
- 六爻纳甲配置
- 世应爻计算
- 卦宫归属
- 六亲关系
- 六神配置
- 伏神计算
- 变卦分析
- 干支纪年
- 旬空计算
"""

import math
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from pathlib import Path
import pickle

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

# ==================== 常量定义 ====================

# 六神
SHEN6 = ('青龙', '朱雀', '勾陈', '螣蛇', '白虎', '玄武')

# 六亲
QING6 = ('兄弟', '父母', '官鬼', '妻财', '子孙')

# 五行
XING5 = ('木', '火', '土', '金', '水')

# 纳甲配置 (八宫纳甲)
NAJIA = (
    ('甲子寅辰', '壬午申戌'),  # 乾金甲子外壬午 子寅辰午申戌
    ('丁巳卯丑', '丁亥酉未'),  # 兑金丁巳外丁亥 巳卯丑亥酉未
    ('己卯丑亥', '己酉未巳'),  # 离火己卯外己酉 卯丑亥酉未巳
    ('庚子寅辰', '庚午申戌'),  # 震木庚子外庚午 子寅辰午申戌
    ('辛丑亥酉', '辛未巳卯'),  # 巽木辛丑外辛未 丑亥酉未巳卯
    ('戊寅辰午', '戊申戌子'),  # 坎水戊寅外戊申 寅辰午申戌子
    ('丙辰午申', '丙戌子寅'),  # 艮土丙辰外丙戌 辰午申戌子寅
    ('乙未巳卯', '癸丑亥酉'),  # 坤土乙未外癸丑 未巳卯丑亥酉
)

# 八卦名称
GUAS = ('乾', '兑', '离', '震', '巽', '坎', '艮', '坤')

# 卦五行
GUA5 = (3, 3, 1, 0, 0, 4, 2, 2)  # 对应 金金火木木水土土

# 爻位 (卦宫索引用)
YAOS = ('111', '110', '101', '100', '011', '010', '001', '000')

# 天干
GANS = ('甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸')

# 地支
ZHIS = ('子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥')

# 地支五行索引
ZHI5 = (4, 2, 0, 0, 2, 1, 1, 2, 3, 3, 2, 4)  # 对应水土木木土火火土金金土水

# 64卦名称映射
GUA64 = {
    '111111': '乾为天', '011111': '天风姤', '001111': '天山遁', '000111': '天地否', 
    '000011': '风地观', '000001': '山地剥', '000101': '火地晋', '111101': '火天大有', 
    '110110': '兑为泽', '010110': '泽水困', '000110': '泽地萃', '001110': '泽山咸',
    '001010': '水山蹇', '001000': '地山谦', '001100': '雷山小过', '110100': '雷泽归妹', 
    '101101': '离为火', '001101': '火山旅', '011101': '火风鼎', '010101': '火水未济', 
    '010001': '山水蒙', '010011': '风水涣', '010111': '天水讼', '101111': '天火同人',
    '100100': '震为雷', '000100': '雷地豫', '010100': '雷水解', '011100': '雷风恒', 
    '011000': '地风升', '011010': '水风井', '011110': '泽风大过', '100110': '泽雷随', 
    '011011': '巽为风', '111011': '风天小畜', '101011': '风火家人', '100011': '风雷益',
    '100111': '天雷无妄', '100101': '火雷噬嗑', '100001': '山雷颐', '011001': '山风蛊', 
    '010010': '坎为水', '110010': '水泽节', '100010': '水雷屯', '101010': '水火既济', 
    '101110': '泽火革', '101100': '雷火丰', '101000': '地火明夷', '010000': '地水师',
    '001001': '艮为山', '101001': '山火贲', '111001': '山天大畜', '110001': '山泽损', 
    '110101': '火泽睽', '110111': '天泽履', '110011': '风泽中孚', '001011': '风山渐', 
    '000000': '坤为地', '100000': '地雷复', '110000': '地泽临', '111000': '地天泰',
    '111100': '雷天大壮', '111110': '泽天夬', '111010': '水天需', '000010': '水地比'
}

# 旬空
KONG = ('子丑', '寅卯', '辰巳', '午未', '申酉', '戌亥')

# ==================== 工具函数 ====================

def GZ5X(gz: str = '') -> str:
    """
    干支五行配置
    
    Args:
        gz: 干支组合，如 '甲子'
        
    Returns:
        干支+五行，如 '甲子水'
    """
    if len(gz) < 2:
        return gz
    
    _, z = gz[0], gz[1]
    zm = ZHIS.index(z) if z in ZHIS else 0
    
    return gz + XING5[ZHI5[zm]]


def xkong(gz: str = '甲子') -> str:
    """
    计算旬空
    
    Args:
        gz: 干支组合
        
    Returns:
        旬空地支
    """
    if len(gz) < 2:
        return ''
    
    gm, zm = gz[0], gz[1]
    
    if gm in GANS and zm in ZHIS:
        gm_idx = GANS.index(gm)
        zm_idx = ZHIS.index(zm)
        
        if gm_idx == zm_idx or zm_idx < gm_idx:
            zm_idx += 12
        
        xk = (gm_idx - zm_idx + 12) % 12
        kong_pair = KONG[xk // 2]
        
        return kong_pair
    
    return ''


def get_god6(gz: str = None) -> List[str]:
    """
    计算六神
    根据日干五行配对六神五行
    
    Args:
        gz: 日干支
        
    Returns:
        六神列表，从上到下（六爻到初爻）
    """
    if not gz or len(gz) < 1:
        return list(SHEN6)
    
    gm = gz[0]
    
    if gm in GANS:
        gm_idx = GANS.index(gm)
    else:
        return list(SHEN6)
    
    # 六神配置计算
    num = math.ceil((gm_idx + 1) / 2) - 7
    
    if gm_idx == 4:  # 戊
        num = -4
    elif gm_idx == 5:  # 己
        num = -3
    elif gm_idx > 5:
        num += 1
    
    # 重新排列六神顺序
    return list(SHEN6[num:] + SHEN6[:num])


def set_shi_yao(symbol: str = None) -> Tuple[int, int]:
    """
    获取世应爻位置
    
    寻世诀：
    天同二世天变五，地同四世地变初。
    本宫六世三世异，人同游魂人变归。
    
    Args:
        symbol: 卦的二进制码（六位）
        
    Returns:
        (世爻位置, 应爻位置) - 1到6，从下往上数
    """
    if not symbol or len(symbol) < 6:
        return (6, 3)  # 默认值
    
    wai = symbol[3:]  # 外卦（上卦）
    nei = symbol[:3]  # 内卦（下卦）
    
    def shiy(shi: int) -> Tuple[int, int]:
        """计算世应爻"""
        ying = shi - 3 if shi > 3 else shi + 3
        return shi, ying
    
    # 天同二世天变五
    if wai[2] == nei[2]:  # 天爻相同
        if wai[1] != nei[1] and wai[0] != nei[0]:  # 人地不同
            return shiy(2)
    else:  # 天爻不同
        if wai[1] == nei[1] and wai[0] == nei[0]:  # 人地相同
            return shiy(5)
    
    # 人同游魂人变归
    if wai[1] == nei[1]:  # 人爻相同
        if wai[0] != nei[0] and wai[2] != nei[2]:  # 天地不同
            return shiy(4)  # 游魂
    else:  # 人爻不同
        if wai[0] == nei[0] and wai[2] == nei[2]:  # 天地相同
            return shiy(3)  # 归魂
    
    # 地同四世地变初
    if wai[0] == nei[0]:  # 地爻相同
        if wai[1] != nei[1] and wai[2] != nei[2]:  # 人天不同
            return shiy(4)
    else:  # 地爻不同
        if wai[1] == nei[1] and wai[2] == nei[2]:  # 人天相同
            return shiy(1)
    
    # 本宫六世
    if wai == nei:
        return shiy(6)
    
    # 三世异
    return shiy(3)


def get_type(symbol: str = None) -> str:
    """
    获取卦的类型（游魂、归魂、六冲等）
    
    Args:
        symbol: 卦的二进制码
        
    Returns:
        卦的类型描述
    """
    if not symbol or len(symbol) < 6:
        return ''
    
    wai = symbol[3:]  # 外卦
    nei = symbol[:3]  # 内卦
    
    # 判断游魂归魂
    if wai[1] == nei[1]:  # 人爻相同
        if wai[0] != nei[0] and wai[2] != nei[2]:  # 天地不同
            return '游魂'
    else:  # 人爻不同
        if wai[0] == nei[0] and wai[2] == nei[2]:  # 天地相同
            return '归魂'
    
    # 判断六冲（内外卦相同）
    if wai == nei:
        return '六冲'
    
    return ''


def palace(symbol: str = None, index: int = None) -> int:
    """
    确定卦宫归属
    
    认宫诀：
    一二三六外卦宫，四五游魂内变更。
    若问归魂何所取，归魂内卦是本宫。
    
    Args:
        symbol: 卦的二进制码
        index: 世爻位置
        
    Returns:
        卦宫索引（0-7）
    """
    if not symbol or len(symbol) < 6:
        return 0
    
    wai = symbol[3:]  # 外卦
    nei = symbol[:3]  # 内卦
    hun = ''
    
    # 判断游魂归魂
    if wai[1] == nei[1]:
        if wai[0] != nei[0] and wai[2] != nei[2]:
            hun = '游魂'
    else:
        if wai[0] == nei[0] and wai[2] == nei[2]:
            hun = '归魂'
    
    # 归魂内卦是本宫
    if hun == '归魂':
        if nei in YAOS:
            return YAOS.index(nei)
    
    # 一二三六外卦宫
    if index and index in (1, 2, 3, 6):
        if wai in YAOS:
            return YAOS.index(wai)
    
    # 四五游魂内变更
    if (index and index in (4, 5)) or hun == '游魂':
        # 内卦变换
        changed_nei = ''.join([str(int(c) ^ 1) for c in nei])
        if changed_nei in YAOS:
            return YAOS.index(changed_nei)
    
    # 默认按外卦归宫
    if wai in YAOS:
        return YAOS.index(wai)
    
    return 0


def get_najia(symbol: str = None) -> List[str]:
    """
    纳甲配干支
    
    Args:
        symbol: 卦的二进制码
        
    Returns:
        六爻的干支列表，从下往上（初爻到上爻）
    """
    if not symbol or len(symbol) < 6:
        return ['甲子'] * 6
    
    wai = symbol[3:]  # 外卦
    nei = symbol[:3]  # 内卦
    
    wai_idx = YAOS.index(wai) if wai in YAOS else 0
    nei_idx = YAOS.index(nei) if nei in YAOS else 0
    
    # 内卦配干支（初、二、三爻）
    gan = NAJIA[nei_idx][0][0]
    ngz = [f'{gan}{zhi}' for zhi in NAJIA[nei_idx][0][1:]]
    
    # 外卦配干支（四、五、六爻）
    gan = NAJIA[wai_idx][1][0]
    wgz = [f'{gan}{zhi}' for zhi in NAJIA[wai_idx][1][1:]]
    
    return ngz + wgz


def get_qin6(w1: str, w2: str) -> str:
    """
    两个五行判断六亲关系
    
    Args:
        w1: 卦宫五行
        w2: 爻的五行
        
    Returns:
        六亲关系
    """
    w1_idx = XING5.index(w1) if w1 in XING5 else 0
    w2_idx = XING5.index(w2) if w2 in XING5 else 0
    
    ws = w1_idx - w2_idx
    ws = ws + 5 if ws < 0 else ws
    
    return QING6[ws]


# ==================== 纳甲主类 ====================

class NajiaOracle:
    """纳甲六爻占卜核心类"""
    
    def __init__(self, verbose: int = 0):
        """
        初始化纳甲占卜器
        
        Args:
            verbose: 显示模式 0-2
        """
        self.verbose = min(verbose, 2)
        self.data = None
    
    def _daily(self, date: datetime = None) -> Dict[str, Any]:
        """
        计算日期干支和旬空
        
        Args:
            date: 指定日期，默认当前时间
            
        Returns:
            包含干支和旬空信息的字典
        """
        try:
            from lunar_python import Solar
            
            if date is None:
                date = datetime.now()
            
            solar = Solar.fromYmdHms(date.year, date.month, date.day, 
                                   date.hour, date.minute or 0, date.second or 0)
            lunar = solar.getLunar()
            ganzi = lunar.getBaZi()
            
            return {
                'xkong': lunar.getDayXunKong(),
                'gz': {
                    'year': ganzi[0],
                    'month': ganzi[1],
                    'day': ganzi[2],
                    'hour': ganzi[3],
                }
            }
        except ImportError:
            # 如果没有lunar_python，使用简化计算
            if date is None:
                date = datetime.now()
            return {
                'xkong': '戌亥',
                'gz': {
                    'year': '甲子',
                    'month': '甲子',
                    'day': '甲子',
                    'hour': '甲子',
                }
            }
    
    def _hidden(self, gong: int = None, qins: List[str] = None) -> Optional[Dict[str, Any]]:
        """
        计算伏神卦
        
        Args:
            gong: 卦宫索引
            qins: 当前卦的六亲列表
            
        Returns:
            伏神信息或None
        """
        if gong is None or qins is None:
            return None
        
        # 如果六亲不全（少于5种），需要找伏神
        if len(set(qins)) < 5:
            # 本宫卦（重复六位）
            mark = YAOS[gong] * 2
            
            # 计算本宫卦的六亲
            qin6 = []
            qinx = []
            najia_list = get_najia(mark)
            
            for gz in najia_list:
                if len(gz) >= 2:
                    zhi_idx = ZHIS.index(gz[1]) if gz[1] in ZHIS else 0
                    qin = get_qin6(XING5[GUA5[gong]], XING5[ZHI5[zhi_idx]])
                    qin6.append(qin)
                    qinx.append(GZ5X(gz))
            
            # 找出缺失的六亲对应的位置
            missing_qins = list(set(qin6).difference(set(qins)))
            seat = []
            for missing in missing_qins:
                if missing in qin6:
                    seat.append(qin6.index(missing))
            
            return {
                'name': GUA64.get(mark, '未知卦'),
                'mark': mark,
                'qin6': qin6,
                'qinx': qinx,
                'seat': seat,
            }
        
        return None
    
    def _transform(self, params: List[int] = None, gong: int = None) -> Optional[Dict[str, Any]]:
        """
        计算变卦
        
        Args:
            params: 摇卦参数列表
            gong: 原卦宫
            
        Returns:
            变卦信息或None
        """
        if not params or len(params) < 6:
            return None
        
        # 检查是否有动爻（3或4表示动爻）
        if 3 in params or 4 in params:
            # 生成变卦码：动爻变化，静爻不变
            mark = ''.join(['1' if v in [1, 4] else '0' for v in params])
            
            # 计算变卦的世应爻
            shiy = set_shi_yao(mark)
            
            # 计算变卦的卦宫
            bian_gong = palace(mark, shiy[0])
            
            # 计算变卦的六亲和干支五行
            najia_list = get_najia(mark)
            qin6 = []
            qinx = []
            
            for gz in najia_list:
                if len(gz) >= 2:
                    zhi_idx = ZHIS.index(gz[1]) if gz[1] in ZHIS else 0
                    qin = get_qin6(XING5[GUA5[gong]], XING5[ZHI5[zhi_idx]])
                    qin6.append(qin)
                    qinx.append(GZ5X(gz))
            
            return {
                'name': GUA64.get(mark, '未知卦'),
                'mark': mark,
                'qin6': qin6,
                'qinx': qinx,
                'gong': GUAS[bian_gong],
            }
        
        return None
    
    def compile(self, params: List[int] = None, gender: str = None, 
                date: datetime = None, title: str = None, 
                guaci: bool = False, **kwargs) -> 'NajiaOracle':
        """
        根据参数编译卦象
        
        Args:
            params: 摇卦参数 [1-4] * 6，1老阳，2少阴，3少阳，4老阴
            gender: 性别
            date: 起卦时间
            title: 所测事项
            guaci: 是否显示卦辞
            
        Returns:
            自身实例
        """
        title = title or ''
        if date is None:
            date = datetime.now()
        
        lunar = self._daily(date)
        gender = gender or ''
        
        # 生成卦码（二进制）
        mark = ''.join([str(int(p) % 2) for p in params])
        
        # 计算世应爻
        shiy = set_shi_yao(mark)
        
        # 计算卦宫
        gong = palace(mark, shiy[0])
        
        # 获取卦名
        name = GUA64.get(mark, '未知卦')
        
        # 计算六亲和干支五行
        najia_list = get_najia(mark)
        qin6 = []
        qinx = []
        
        for gz in najia_list:
            if len(gz) >= 2:
                zhi_idx = ZHIS.index(gz[1]) if gz[1] in ZHIS else 0
                qin = get_qin6(XING5[GUA5[gong]], XING5[ZHI5[zhi_idx]])
                qin6.append(qin)
                qinx.append(GZ5X(gz))
        
        # 计算六神
        god6 = get_god6(lunar['gz']['day'])
        
        # 动爻位置
        dong = [i for i, x in enumerate(params) if x > 2]
        
        # 计算伏神
        hide = self._hidden(gong, qin6)
        
        # 计算变卦
        bian = self._transform(params=params, gong=gong)
        
        self.data = {
            'params': params,
            'gender': gender,
            'title': title,
            'guaci': guaci,
            'date': date,
            'lunar': lunar,
            'god6': god6,
            'dong': dong,
            'name': name,
            'mark': mark,
            'gong': GUAS[gong],
            'shiy': shiy,
            'qin6': qin6,
            'qinx': qinx,
            'bian': bian,
            'hide': hide,
        }
        
        return self
    
    def get_najia_result(self) -> Dict[str, Any]:
        """
        获取纳甲占卜的完整结果
        
        Returns:
            包含所有纳甲信息的字典
        """
        if not self.data:
            return {}
        
        return {
            'original_hexagram': {
                'name': self.data['name'],
                'mark': self.data['mark'],
                'gong': self.data['gong'],
                'type': get_type(self.data['mark']),
                'shiy': self.data['shiy'],  # (世爻, 应爻)
            },
            'changed_hexagram': self.data['bian'],
            'lines': [
                {
                    'position': i + 1,
                    'najia': self.data['qinx'][i] if i < len(self.data['qinx']) else '',
                    'qin6': self.data['qin6'][i] if i < len(self.data['qin6']) else '',
                    'god6': self.data['god6'][5-i] if i < len(self.data['god6']) else '',  # 六神从上往下
                    'changing': i in self.data['dong'],
                }
                for i in range(6)
            ],
            'hidden': self.data['hide'],
            'lunar_info': self.data['lunar'],
            'title': self.data['title'],
            'gender': self.data['gender'],
            'date': self.data['date'].isoformat() if self.data['date'] else '',
        }
