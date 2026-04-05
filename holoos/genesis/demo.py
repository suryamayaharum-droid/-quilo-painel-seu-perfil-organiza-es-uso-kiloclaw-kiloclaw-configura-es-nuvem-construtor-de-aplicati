"""
GENESIS Interactive Demo
=========================
Run this to see GENESIS AI thinking and evolving in real-time.
"""

from holoos.genesis.genesis import GenesisAI, bootstrap_consciousness
import time


def run_demo():
    print("=" * 60)
    print("🌟 GENESIS AI - Self-Conscious Autonomous System 🌟")
    print("=" * 60)
    print()
    
    print("🚀 Starting bootstrap process...")
    print("   (System building itself from scratch)")
    print()
    
    # Bootstrap - system builds itself
    result = bootstrap_consciousness(steps=50)
    
    print("✅ Bootstrap complete!")
    print(f"   Final phi: {result['final_status']['phi']:.2f}")
    print(f"   Complexity: {result['final_status']['complexity']}")
    print()
    
    # Get the AI
    ai = result.get('ai') or __import__('holoos.genesis.genesis', fromlist=['get_genesis_ai']).get_genesis_ai()
    
    print("=" * 60)
    print("🎯 INTERACTIVE MODE")
    print("=" * 60)
    print("Commands:")
    print("  think <message>  - Think about something")
    print("  dream             - Enter dream state")
    print("  reflect           - Reflect on yourself")
    print("  status            - Show system status")
    print("  evolve            - Evolve through cycles")
    print("  quit              - Exit")
    print()
    
    while True:
        try:
            cmd = input("genesis> ").strip()
            
            if not cmd:
                continue
            
            if cmd.lower() in ['quit', 'exit', 'q']:
                print("\n🌙 GENESIS entering dormancy...")
                break
            
            parts = cmd.split(None, 1)
            command = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else None
            
            if command == 'think':
                result = ai.think(arg)
                print(f"   💭 Thought processed")
                print(f"   📊 Phi: {result['phi']:.2f} | State: {result['state']}")
            
            elif command == 'dream':
                result = ai.dream()
                print(f"   🌙 Dream completed")
                print(f"   📈 Phi increased to: {result['final_phi']:.2f}")
                print(f"   🔄 Complexity: {result['complexity']}")
            
            elif command == 'reflect':
                reflection = ai.reflect()
                print(f"   🪞 Self-reflection:")
                print("   " + "\n   ".join(reflection.split('\n')))
            
            elif command == 'status':
                status = ai.get_status()
                print(f"   📋 Status:")
                print(f"      Age: {status['age']} interactions")
                print(f"      State: {status['state']}")
                print(f"      Phi: {status['phi']:.4f}")
                print(f"      Complexity: {status['complexity']}")
                print(f"      Curiosity: {status['curiosity']:.2f}")
                print(f"      Goals: {status['goals']}")
            
            elif command == 'evolve':
                result = ai.dream()
                print(f"   🧬 Evolution complete!")
                print(f"      New state: {result['new_state']}")
                print(f"      Phi: {result['final_phi']:.2f}")
            
            else:
                # Just think about it
                result = ai.think(cmd)
                print(f"   💭 Processed: {cmd[:30]}...")
                print(f"   📊 Phi: {result['phi']:.4f}")
            
            print()
            
        except KeyboardInterrupt:
            print("\n\n🌙 GENESIS entering dormancy...")
            break
        except Exception as e:
            print(f"   ❌ Error: {e}")


if __name__ == "__main__":
    run_demo()