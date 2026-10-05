"""Vigenere cipher encrypt/decrypt (terminal toy).

Classical polyalphabetic cipher. NOT secure by modern standards --
a toy for learning, not for protecting secrets.

Examples:
    python -m vigenere -k LEMON enc "ATTACKATDAWN"   -> LXFOPVEFRNHR
    python -m vigenere -k LEMON dec "LXFOPVEFRNHR"   -> ATTACKATDAWN
    echo hello | python -m vigenere -k key enc
"""
import argparse
import sys


def _check_key(key: str) -> str:
    if not key or not key.isalpha():
        raise ValueError("密钥必须是非空的纯字母字符串")
    return key.upper()


def _shift(ch: str, k: str, decrypt: bool = False) -> str:
    base = ord("A") if ch.isupper() else ord("a")
    s = ord(k) - ord("A")
    if decrypt:
        s = -s
    return chr((ord(ch) - base + s) % 26 + base)


def enc(text: str, key: str) -> str:
    """Encrypt text with the key (case and non-letters preserved)."""
    key = _check_key(key)
    out, i = [], 0
    for ch in text:
        if ch.isalpha():
            out.append(_shift(ch, key[i % len(key)]))
            i += 1
        else:
            out.append(ch)
    return "".join(out)


def dec(text: str, key: str) -> str:
    """Decrypt text with the key."""
    key = _check_key(key)
    out, i = [], 0
    for ch in text:
        if ch.isalpha():
            out.append(_shift(ch, key[i % len(key)], decrypt=True))
            i += 1
        else:
            out.append(ch)
    return "".join(out)


def crack(text: str, key_len: int) -> str:
    """Demo-grade frequency-analysis crack.

    Assumes a fixed key length and English plaintext: for each key
    position, try every shift and pick the one whose decrypted column
    best matches English letter frequencies (chi-squared). Works on
    long English texts; may fail on short ones.
    """
    if key_len < 1:
        raise ValueError("密钥长度必须 >= 1")
    # English letter frequencies (a-z)
    freq = [0.0817, 0.0150, 0.0278, 0.0425, 0.1270, 0.0223, 0.0202,
            0.0609, 0.0697, 0.0015, 0.0077, 0.0403, 0.0241, 0.0675,
            0.0751, 0.0193, 0.0010, 0.0599, 0.0633, 0.0906, 0.0276,
            0.0098, 0.0236, 0.0015, 0.0197, 0.0007]
    letters = [c.lower() for c in text if c.isalpha()]
    key = []
    for pos in range(key_len):
        col = letters[pos::key_len]
        if not col:
            key.append("A")
            continue
        best, best_chi = "A", float("inf")
        n = len(col)
        for s in range(26):
            counts = [0] * 26
            for c in col:
                counts[(ord(c) - ord("a") - s) % 26] += 1
            chi = sum((counts[i] - n * freq[i]) ** 2 / (n * freq[i])
                      for i in range(26))
            if chi < best_chi:
                best_chi, best = chi, chr(ord("A") + s)
        key.append(best)
    return "".join(key)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="vigenere",
        description="维吉尼亚密码: 加密/解密(教学玩具, 非现代安全算法)。")
    p.add_argument("-k", "--key", default="",
                   help="密钥(纯字母); 也可用 --key-file 从文件读取")
    p.add_argument("--key-file", default="",
                   help="从文件读取密钥(取第一个字母串)")
    sub = p.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("enc", help="加密")
    e.add_argument("text", nargs="?", default="", help="明文(缺省读 stdin)")
    d = sub.add_parser("dec", help="解密")
    d.add_argument("text", nargs="?", default="", help="密文(缺省读 stdin)")
    c = sub.add_parser("crack", help="频率分析破解(演示级, 需英文长文本)")
    c.add_argument("text", nargs="?", default="", help="密文(缺省读 stdin)")
    c.add_argument("-l", "--key-length", type=int, default=5,
                   help="假设的密钥长度(默认 5)")
    a = p.parse_args(argv)

    if a.key_file:
        try:
            raw = open(a.key_file, encoding="utf-8").read()
        except OSError as exc:
            print(f"error: 读密钥文件失败: {exc}", file=sys.stderr)
            return 2
        alpha = "".join(ch for ch in raw if ch.isalpha())
        a.key = alpha
    key = a.key
    text = a.text or (sys.stdin.read() if not sys.stdin.isatty() else "")
    if a.cmd in ("enc", "dec") and not key:
        print("error: 需要密钥, 用 -k/--key 或 --key-file 指定", file=sys.stderr)
        return 2
    try:
        if a.cmd == "enc":
            print(enc(text, key))
        elif a.cmd == "dec":
            print(dec(text, key))
        else:
            print(crack(text, a.key_length))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
