"""
PCBO Engine — нейро-символический пайплайн синтеза и верификации PC-сборок.

7 детерминированных Python-навыков для использования Hermes-агентом.
Онтология: 0_lab/PCBOv2 (в репозитории tech_and_play_blog).
База компонентов: kaizin-lab/pc_hardware_knowledge_base.

Приоритет внедрения (от критических к вспомогательным):
1. verify_structural_clearance  — геометрия (GPU/кулер/корпус)
2. evaluate_pcie_topology       — линии PCIe, бифуркация, DRAM-less SSD
3. simulate_thermal_profiles    — взаимный нагрев, ambient
4. evaluate_marginal_value      — MV = ΔPerf% / ΔPrice%, правило AR-03
5. calculate_power_states       — TDP, ATX 3.0, transient spikes
6. assess_acoustic_class        — класс шума, DPC latency
7. validate_l5_rules            — агрегатор, rollback trigger
