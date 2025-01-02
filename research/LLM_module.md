### Tokenizer

- 分词器把句子切分为一个一个的token，作为模型的输入。
- 通常情况下，Tokenizer有三种粒度：word/char/subword。llm使用的 Tokenizer 一般为subword。常见的方法有：

- **Byte-Pair Encoding (BPE)**：字节对编码

1. 本质是一种数据压缩方法。2015年Sennrich 通过论文Neural Machine Translation of Rare Words with Subword Units[2] 将这个算法使用在生成Tokenizer的词表上，做法是先**将每个文本词（Word）拆分成 Char粒度的字母序列**，然后**通过迭代地合并最频繁出现的字符**或字符序列来实现生成Tokenizer最终词表的过程• 最早OpenAI GPT-2 与Facebook RoBERTa均采用此方法进阶版BBPE构建 Subword 向量，也是目前最常用的Tokenizer方法之一。
- **Byte-level BPE（BBPE）**

1. 2019年12月，论文：Neural Machine Translation with Byte-Level Subwords[3] 在基于BPE基础上提出以Byte-level为粒度的分词算法Byte-level BPE，即BBPE。
2. 解决中文、日文等语言时的词表OOV问题，BBPE考虑将一段文本的UTF-8编码(UTF-8保证任何语言都可以通用)中的一个字节256位不同的编码作为词表的初始化基础Subword。
3. 但对中文、日文不友好。中文字符 UTF8 为三字节，编码效率低。Llama 使用。 
- **WordPiece**：对BPE的改变是使用语言本身的分布概率代替词频进行编码

- **SentencePiece** 
1. 固定词汇表，空格还原；内部支持BPE、wordpiece编码；快速且轻量级
2. 参考：https://zhuanlan.zhihu.com/p/630696264• Yi 使用