# II. Related Work

The increasing complexity of modern cyber threats has motivated extensive research in artificial intelligence-driven intrusion detection, IoT security analytics, blockchain-enabled security architectures, explainable artificial intelligence, and trust-aware autonomous systems. This section reviews the most relevant studies in these domains and identifies the research gaps addressed by the proposed framework.

## A. AI-Based Intrusion Detection Systems

Intrusion detection systems (IDSs) constitute one of the most extensively studied areas in cybersecurity research. Traditional signature-based approaches are effective against known threats but often fail to identify previously unseen attacks and zero-day exploits. To overcome these limitations, machine learning and data mining techniques have been widely adopted for anomaly detection and attack classification tasks [13], [14].

Garcia-Teodoro et al. [15] provided one of the earliest comprehensive reviews of anomaly-based intrusion detection systems and highlighted their potential for identifying unknown threats. Subsequently, Sommer and Paxson [16] discussed the practical challenges associated with deploying machine learning models in operational network environments, emphasizing issues related to dataset quality, model generalization, and real-world applicability. Recent advances in deep learning have further improved detection capabilities through the use of neural networks, recurrent architectures, and ensemble learning methods [17].

The availability of benchmark datasets has significantly accelerated IDS research. UNSW-NB15 [7], CICIDS2017 [8], TON_IoT [9], Edge-IIoTset [10], and Bot-IoT [11] have become widely adopted evaluation platforms for cybersecurity research. These datasets provide realistic attack scenarios and support the development of AI-driven security analytics. However, the majority of existing IDS studies focus primarily on attack detection and classification, while providing limited support for incident response, explainability, trust evaluation, and forensic evidence preservation.

## B. Multi-Agent Systems for Cybersecurity

Multi-agent systems have emerged as a promising paradigm for solving complex and distributed decision-making problems. Unlike monolithic architectures, multi-agent frameworks distribute tasks among specialized agents that collaborate to achieve shared objectives [1], [2]. Early work by Smith [3] introduced the Contract Net Protocol, which established foundational concepts for cooperative agent-based systems.

Recent advances in large language models have renewed interest in multi-agent artificial intelligence architectures. Frameworks such as CAMEL [4] and AutoGen [5] demonstrate how multiple AI agents can coordinate tasks through structured communication and collaborative reasoning. Contemporary surveys further indicate that multi-agent architectures offer improved scalability, modularity, and task specialization compared with single-agent systems [6].

Despite their growing popularity, relatively few studies have explored the integration of multi-agent architectures into cybersecurity workflows. Existing approaches typically focus on isolated tasks such as threat detection or automated analysis, while comprehensive frameworks capable of combining detection, explanation, response generation, trust evaluation, and forensic logging remain limited.

## C. Explainable Artificial Intelligence for Cybersecurity

The increasing adoption of artificial intelligence in security-critical applications has raised significant concerns regarding transparency and accountability. Security analysts often require explanations for AI-generated decisions before taking defensive actions. Consequently, explainable artificial intelligence (XAI) has become an important research area within cybersecurity [22].

Ribeiro et al. [20] introduced the Local Interpretable Model-Agnostic Explanations (LIME) framework, which enables local interpretation of machine learning predictions. Lundberg and Lee [21] later proposed SHAP, a unified framework based on cooperative game theory that provides consistent feature attribution explanations. Subsequent surveys by Samek et al. [23] and Adadi and Berrada [24] highlighted the importance of explainability for improving user trust, model transparency, and decision accountability.

Although XAI techniques have been widely applied in intrusion detection research, many cybersecurity frameworks still operate as black-box systems that provide limited insight into the reasoning behind attack classifications. This lack of transparency can hinder analyst confidence and reduce the practical adoption of autonomous security solutions.

## D. Blockchain-Based Cybersecurity Frameworks

Blockchain technology has attracted considerable attention as a mechanism for establishing trust, integrity, and auditability in distributed systems. Nakamoto’s introduction of Bitcoin [25] demonstrated how cryptographic hash chains could create immutable transaction ledgers without centralized control. Subsequent developments such as Ethereum expanded blockchain capabilities through programmable smart contracts [26].

Researchers have increasingly investigated blockchain applications in IoT and cybersecurity environments. Christidis and Devetsikiotis [27] explored the potential of blockchain and smart contracts for securing IoT ecosystems. Dorri et al. [28] proposed a blockchain-enabled smart home architecture that improved device authentication and privacy. Novo [29] introduced a blockchain-based access management framework for IoT networks, while Bao et al. [30] proposed IoTChain, a multi-layer security architecture designed to improve trust and accountability.

Recent surveys have further highlighted the potential of blockchain for securing distributed IoT infrastructures and preserving tamper-resistant security records [31]. Nevertheless, most blockchain-based security solutions focus on access control, authentication, or data integrity. The integration of blockchain with AI-driven cyber defense workflows, particularly for preserving incident evidence generated by autonomous security agents, remains relatively underexplored.

## E. Trust Management in Autonomous Security Systems

Trust management represents a critical requirement for autonomous decision-making systems operating in uncertain and adversarial environments. Jøsang et al. [34] presented a foundational survey of trust and reputation systems, while Cho et al. [35] investigated trust management mechanisms in distributed communication networks. More recent studies have explored trust-aware frameworks for collaborative autonomous agents and intelligent transportation systems [36].

The emergence of large language model-based agent ecosystems has further increased interest in trust-aware AI architectures. Recent studies propose attention-based trust mechanisms and Trust, Risk, and Security Management (TRiSM) frameworks for evaluating the reliability of agent-generated decisions [37], [38]. In parallel, international organizations have emphasized trustworthy AI principles through governance frameworks such as the European Commission’s Ethics Guidelines for Trustworthy AI [39] and the NIST AI Risk Management Framework [40].

Despite these developments, trust evaluation remains largely absent from current AI-based cybersecurity systems. Most intrusion detection frameworks generate predictions without explicitly assessing the reliability of those predictions before initiating defensive actions.

## F. Research Gap

The literature review reveals that significant progress has been achieved in AI-based intrusion detection, explainable artificial intelligence, blockchain-enabled security, and multi-agent systems. However, existing approaches generally address these capabilities in isolation. Current intrusion detection systems primarily focus on attack identification, blockchain-based frameworks emphasize secure data storage, and explainable AI solutions concentrate on model interpretability. Very few studies integrate all of these capabilities within a unified cybersecurity architecture.

Furthermore, existing cybersecurity frameworks rarely incorporate explicit trust evaluation mechanisms that determine whether autonomous security decisions should be executed automatically or reviewed by human analysts. Similarly, the use of blockchain technology for preserving AI-generated incident evidence, trust assessments, explanations, and response recommendations remains insufficiently investigated.

To address these limitations, this work proposes a unified Multi-Agent AI Cyber Defense Framework that combines attack detection, threat classification, explainable threat intelligence, trust-aware decision management, automated response generation, and blockchain-based immutable incident logging within a single end-to-end architecture.
