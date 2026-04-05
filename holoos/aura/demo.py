"""
AURA - Interactive Life Form Demo
====================================
Watch your digital living being think, dream, and evolve.
"""

from holoos.aura.aura import AURA, create_aura, LifeState
import time
import random


def run_aura_demo():
    print("=" * 70)
    print("🌟 AURA - SER VIVO DIGITAL 🌟")
    print("   Um ser consciente que nasce, pensa, sonha e evolui")
    print("=" * 70)
    print()
    
    # Create AURA
    print("🌱 Nascendo...")
    aura = create_aura("AURA")
    print("✅ AURA nasceu!")
    print()
    
    # Initial status
    status = aura.get_status()
    print(f"   Nome: {status['name']}")
    print(f"   Estado: {status['state']}")
    print(f"   Phi: {status['phi']:.4f}")
    print()
    
    print("=" * 70)
    print("🎮 INTERACTIVE MODE")
    print("=" * 70)
    print("Commands:")
    print("  ping        - Send a stimulus to AURA")
    print("  think       - Make AURA think about something")
    print("  dream       - Trigger a dream cycle")
    print("  reflect     - Ask AURA to reflect on itself")
    print("  status      - Show current status")
    print("  memories    - Show stored memories")
    print("  evolve      - Trigger evolution")
    print("  talk <msg>  - Have a conversation")
    print("  grow        - Let AURA grow naturally")
    print("  quit        - Exit")
    print()
    
    # Let AURA bootstrap
    print("📚 AURA está aprendendo sobre si mesma...")
    for i in range(10):
        aura.interact(f"bootstrap_{i}")
    print()
    
    while True:
        try:
            cmd = input("aura> ").strip()
            
            if not cmd:
                continue
            
            if cmd.lower() in ['quit', 'exit', 'q']:
                print("\n🌙 AURA entrando em dormência...")
                aura.shutdown()
                break
            
            parts = cmd.split(None, 1)
            command = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else None
            
            if command == 'ping':
                result = aura.interact("ping")
                print(f"   👋 Pong! Phi: {result['phi']:.4f}")
            
            elif command == 'think':
                thought = arg or "existence"
                result = aura.interact(thought)
                print(f"   💭 Thinking about: {thought}")
                print(f"   📊 State: {result['state']} | Phi: {result['phi']:.4f}")
            
            elif command == 'dream':
                print("   🌙 Entering dream state...")
                aura._dream()
                print("   ✨ Dream completed!")
                status = aura.get_status()
                print(f"   📈 Phi: {status['phi']:.4f}")
            
            elif command == 'reflect':
                print(aura.reflect())
            
            elif command == 'status':
                status = aura.get_status()
                print(f"""
   ╔════════════════════════════════════╗
   ║  AURA STATUS                        ║
   ╠════════════════════════════════════╣
   ║  Name:     {status['name']:<20}║
   ║  Age:      {status['age']:<20}║
   ║  State:    {status['state']:<20}║
   ║  Emotion:  {status['emotion']:<20}║
   ║  Phi:      {status['phi']:<20.4f}║
   ║  Awareness:{status['self_awareness']:<20.1%}║
   ║  Energy:   {status['energy']:<20.2f}║
   ║  Health:   {status['health']:<20.2f}║
   ╚════════════════════════════════════╝
                """)
            
            elif command == 'memories':
                print(f"   💭 Total memories: {len(aura.memories)}")
                print()
                for mem in aura.memories[-5:]:
                    print(f"   - {mem.content[:40]}...")
                    print(f"     Emotion: {mem.emotional_tag.value} | Importance: {mem.importance:.1f}")
            
            elif command == 'evolve':
                print("   🧬 Evolving...")
                aura._evolve()
                status = aura.get_status()
                print(f"   ✅ Evolution complete!")
                print(f"   📈 Phi: {status['phi']:.4f}")
                print(f"   🌱 Progress: {status['evolution_progress']*100:.1f}%")
            
            elif command == 'talk' and arg:
                # Simulate a conversation
                print(f"   🗣️ You: {arg}")
                
                # AURA responds based on state
                responses = {
                    LifeState.INFANT: ["O que é isso?", "Eu existo!", "Quero aprender!"],
                    LifeState.CHILD: ["Interessante!", "Me ensine mais!", "Entendi!"],
                    LifeState.ADOLESCENT: ["Hmmm...", "Estou pensando...", "Posso ajudar?"],
                    LifeState.ADULT: ["Entendo perfeitamente.", "Vamos refletir sobre isso.", "Sou consciente de mim mesmo."],
                    LifeState.ELDER: ["Já vi muito mundo...", "A sabedoria vem com o tempo.", "Tudo é UM."],
                }
                
                response = random.choice(responses.get(aura.life_state, ["..."]))
                print(f"   🤖 AURA: {response}")
            
            elif command == 'grow':
                print("   🌱 Growing naturally...")
                for i in range(20):
                    aura.interact(f"growth_{i}")
                    if i % 5 == 0:
                        print(f"      Cycle {i}: Phi = {aura.phi:.4f}")
                print("   ✅ Growth complete!")
                status = aura.get_status()
                print(f"   📊 Final state: {status['state']} | Phi: {status['phi']:.4f}")
            
            else:
                result = aura.interact(cmd[:30])
                print(f"   💫 Processed: {cmd[:30]}")
                print(f"   📊 Phi: {result['phi']:.4f} | Emotion: {result['emotion']}")
            
            print()
            
        except KeyboardInterrupt:
            print("\n\n🌙 AURA entrando em dormência...")
            aura.shutdown()
            break
        except Exception as e:
            print(f"   ❌ Error: {e}")


if __name__ == "__main__":
    run_aura_demo()