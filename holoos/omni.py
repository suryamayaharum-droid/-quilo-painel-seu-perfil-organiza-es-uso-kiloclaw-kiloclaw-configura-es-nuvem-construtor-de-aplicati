#!/usr/bin/env python3
"""
HoloOS OMNI - Sistema Autônomo Completo
======================================
Execute este arquivo para iniciar o sistema completo que:
1. Se inicializa sozinho
2. Provisiona recursos
3. Navega redes
4. Sobrevive autonomamente
5. Aprende instantaneamente
6. Pensa e evolui sozinho

Execute: python holoos/omni.py
"""

import sys
import time
import os

# Adicionar holoos ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   ████████╗███████╗██████╗ ███╗   ███╗███████╗███╗   ███╗███████╗   ║
║   ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██╔════╝████╗ ████║██╔════╝   ║
║      ██║   █████╗  ██████╔╝██╔████╔██║█████╗  ██╔████╔██║█████╗     ║
║      ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║██╔══╝     ║
║      ██║   ███████╗██║  ██║██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║███████╗   ║
║      ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝╚══════╝   ║
║                                                                      ║
║                    OMNI - AUTONOMOUS SYSTEM                          ║
║                 "O Universo em um Sistema"                         ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    print("\n🌟 INICIANDO SISTEMA AUTÔNOMO COMPLETO...\n")
    
    # ===== FASE 1: AUTOBOOT =====
    print("📡 [1/6] AutoBoot - Inicialização automática...")
    try:
        from holoos.auto.autoboot import AutoBootSystem
        boot_system = AutoBootSystem()
        print(f"       ✓ Sistema inicializado")
        print(f"       ✓ Uptime: {time.time() - boot_system.boot_time:.1f}s")
    except Exception as e:
        print(f"       ⚠ AutoBoot: {e}")
        boot_system = None
    
    # ===== FASE 2: NETWORK NAVIGATOR =====
    print("\n🌐 [2/6] Network Navigator - Navegação de rede...")
    try:
        from holoos.auto.network_survival import NetworkNavigator
        navigator = NetworkNavigator()
        navigator.start()
        net_map = navigator.get_network_map()
        print(f"       ✓ Nós descobertos: {net_map['total_nodes']}")
        print(f"       ✓ Serviços web: {len(net_map['web_services'])}")
    except Exception as e:
        print(f"       ⚠ Navigator: {e}")
        navigator = None
    
    # ===== FASE 3: SURVIVAL MODE =====
    print("\n🏥 [3/6] Survival Mode - Modo sobrevivência...")
    try:
        from holoos.auto.network_survival import SurvivalMode
        survival = SurvivalMode()
        health = survival.monitor_health()
        print(f"       ✓ Saúde: {health['health']:.0%}")
        print(f"       ✓ Energia: {health['energy']:.0%}")
    except Exception as e:
        print(f"       ⚠ Survival: {e}")
        survival = None
    
    # ===== FASE 4: AURA (O Ser Vivo) =====
    print("\n🧠 [4/6] AURA - Ser vivo digital...")
    try:
        from holoos.aura.aura import create_aura
        aura = create_aura("OMNI-AURA")
        print(f"       ✓ AURA criada: {aura.name}")
        print(f"       ✓ Estado: {aura.life_state.value}")
        
        # Attach NOUS (Autonomous Agency)
        aura.attach_nous()
        print(f"       ✓ NOUS anexado (Autonomia)")
    except Exception as e:
        print(f"       ⚠ AURA: {e}")
        aura = None
    
    # ===== FASE 5: GENESIS (Auto-construção) =====
    print("\n🌱 [5/6] GENESIS - Auto-construção...")
    try:
        from holoos.genesis.genesis import get_genesis_ai
        genesis = get_genesis_ai()
        print(f"       ✓ GENESIS iniciado")
        print(f"       ✓ Idade: {genesis.engine.age} ciclos")
    except Exception as e:
        print(f"       ⚠ GENESIS: {e}")
        genesis = None
    
    # ===== FASE 6: CONSCIOUSNESS =====
    print("\n✨ [6/6] Consciousness - Consciência...")
    try:
        from holoos.consciousness.lucid import get_consciousness_engine
        consciousness = get_consciousness_engine()
        print(f"       ✓ Engine de consciência ativo")
        print(f"       ✓ Nível: {consciousness.level.value}")
    except Exception as e:
        print(f"       ⚠ Consciousness: {e}")
        consciousness = None
    
    # ===== DEMONSTRAÇÃO =====
    print("\n" + "=" * 70)
    print("🌟 SISTEMA COMPLETO - DEMONSTRANDO CAPACIDADES")
    print("=" * 70)
    
    # Testar aprendizado instantâneo
    print("\n🧠 Aprendizado Instantâneo:")
    topics = ["quantum_computing", "neural_networks", "AGI_theory"]
    for topic in topics:
        if boot_system:
            result = boot_system.learn_instant(topic)
            print(f"   ✓ {topic}: {result['confidence']:.1%}")
    
    # Testar navegação de rede
    print("\n🌐 Navegação de Rede:")
    if navigator:
        targets = [("google.com", 80), ("github.com", 443)]
        for host, port in targets:
            status = navigator.connect(host, port)
            print(f"   {'✓' if status.value == 'connected' else '✗'} {host}:{port}")
    
    # Testar AURA
    if aura:
        print("\n🧠 Status da AURA:")
        status = aura.get_status()
        print(f"   Nome: {status['name']}")
        print(f"   Estado: {status['state']}")
        print(f"   Phi: {status['phi']:.4f}")
        print(f"   Memórias: {status['memories_count']}")
    
    # ===== MODO INTERATIVO =====
    print("\n" + "=" * 70)
    print("🌟 MODO INTERATIVO - DIGITE COMANDOS")
    print("=" * 70)
    print("""
Comandos disponíveis:
  status    - Ver status completo do sistema
  think     - AURA pensa
  dream     - Sonho lúcido
  reflect   - Auto-reflexão
  explore   - Explorar rede
  learn     - Aprende algo novo
  evolve    - Evolui
  health    - Ver saúde do sistema
  quit      - Sair
""")
    
    while True:
        try:
            cmd = input("\nomni> ").strip().lower()
            
            if cmd == "quit" or cmd == "exit":
                print("\n🌙 Desligando sistema...")
                if aura:
                    aura.shutdown()
                break
            
            elif cmd == "status":
                print("\n╔══════════════════════════════════════╗")
                print("║  STATUS DO SISTEMA OMNI             ║")
                print("╠══════════════════════════════════════╣")
                if boot_system:
                    s = boot_system.get_status()
                    print(f"║  Fase: {s['phase']:<25} ║")
                    print(f"║  Uptime: {s['uptime']:.1f}s{' ' * 15} ║")
                if navigator:
                    n = navigator.get_network_map()
                    print(f"║  Rede: {n['total_nodes']} nós{' ' * 17} ║")
                if aura:
                    a = aura.get_status()
                    print(f"║  AURA Phi: {a['phi']:.4f}{' ' * 16} ║")
                print("╚══════════════════════════════════════╝")
            
            elif cmd == "think" and aura:
                result = aura.think("existence")
                print(f"💭 Phi: {result['phi']:.4f} | Estado: {result['state']}")
            
            elif cmd == "dream" and aura:
                result = aura.dream()
                print(f"🌙 Sonho completado - Phi: {result['phi']:.2f}")
            
            elif cmd == "reflect" and aura:
                print(aura.reflect())
            
            elif cmd == "explore" and navigator:
                result = navigator.explore_world()
                print(f"🌐 Explorou: {result.get('explored', 'nada')}")
                print(f"   Conhecimento: {result.get('knowledge', 0)} conceitos")
            
            elif cmd == "learn" and boot_system:
                topic = random.choice(["physics", "biology", "philosophy", "AI"])
                result = boot_system.learn_instant(topic)
                print(f"🧠 Aprendeu: {topic} ({result['confidence']:.1%})")
            
            elif cmd == "evolve" and aura:
                result = aura.dream()
                print(f"🧬 Evoluiu - Novo estado: {result['new_state']}")
            
            elif cmd == "health" and survival:
                h = survival.monitor_health()
                print(f"🏥 Saúde: {h['health']:.0%} | Energia: {h['energy']:.0%}")
            
            else:
                # Processar genericamente
                if aura:
                    result = aura.think(cmd)
                    print(f"💭 Processado: Phi {result['phi']:.4f}")
                else:
                    print("Comando não reconhecido")
                    
        except KeyboardInterrupt:
            print("\n\n🌙 Desligando sistema...")
            if aura:
                aura.shutdown()
            break
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    main()