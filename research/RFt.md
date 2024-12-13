### RFT是什么
- 粗白地看，RFT就是针对给定的 prompt,产生一些包含cot的response,再通过一个verifier来判断reponse是否正确,作为信号来指导模型进行参数更新。
- RFT和 RLHF可能唯一的区别就是，他的**return(reward信号)**,是通过verifier算出来的，而不是一个reward model计算出来的。verifier本书可以看成一个rule,比如math任务的答案是否正确，code任务的代码是否能够执行。因此 RFT = PPO + rule_based reward model
- **结论**: RFT或许并不是新的技术范式，而是PPO技术范式下的新应用范式，RFT相比传统PPO的创新点就是rule-based reward_model。


### RFT的价值
- 能够创建专门针对特定复杂，特定领域任务的专家模型。
- **只要能定制好一个任务的verifier,那么RFT便可以在这个新的领域场景，以十分之一的数据，轻松超过SFT的结果。**


### 字节的ReFt
1. 步骤
    - SFT 得到一个较好的模型
    - 给定 prompt，do_sample 多次，生成一些带 cot 的 response；
    - 答案正确，1 分；答案错误，0.1 分；提取不到答案（说明没有 follow 输出格式），0分；
    - 根据 returns 更新模型。
2. ReFT 这篇论文，好就好在它是在 o1 之前发表的。因为 o1 的出现，“cot 的推理过程，MCTS 采样，PRM，ORM，rule-based reward_model” 等概念，已经在 LLM 圈深入人心了。