# vigenere

终端维吉尼亚密码(多表替换古典密码)工具: 加密/解密, 附演示级频率分析破解。

> **诚实说明: 这是教学玩具, 不是现代安全算法。**
> 维吉尼亚密码 19 世纪就被 Kasiski / Friedman 方法攻破。
> 不要用它保护任何真实秘密。

## 用法

```bash
# 经典例子
python -m vigenere -k LEMON enc "ATTACKATDAWN"   # LXFOPVEFRNHR
python -m vigenere -k LEMON dec "LXFOPVEFRNHR"   # ATTACKATDAWN

# 大小写和非字母(标点/空格/数字)原样保留
python -m vigenere -k key enc "Hello, World!"    # Rijvs, Uyvjn!

# 管道
echo hello | python -m vigenere -k secret enc

# 从文件读密钥(取其中的字母串)
python -m vigenere --key-file key.txt enc "secret message"

# 频率分析破解(演示级: 假设密钥长度, 英文长文本)
python -m vigenere crack -l 5 "$(cat cipher.txt)"
```

## 设计取舍

- 密钥只推进字母位置: 非字母不消耗密钥字符(经典做法)。
- `--crack` 对每个密钥位置用卡方统计找最贴合英语字母频率的位移;
  短文本/非英文文本会失败, 属预期行为, 非 bug。
- 只支持加法型维吉尼亚, 不做 autokey 等变体。

## 已知局限

- 无密钥派生、无认证: 密文可被篡改而不被发现。
- `--crack` 需要已知密钥长度(`-l`), 不做 Kasiski 自动估计。
- 只处理 A–Z 字母密钥; 中文等非字母字符透传。
