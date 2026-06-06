"""
agent.py — Terminal orqali coding agent ishga tushirish
"""
import sys
from agent_core import run_agent


def main():
    if len(sys.argv) < 2:
        print('Ishlatish: python agent.py "vazifa tavsifi"')
        print('Misol:     python agent.py "fibonacci funksiya yoz va test qil"')
        sys.exit(1)

    task = " ".join(sys.argv[1:])
    result = run_agent(task)
    print(result)


if __name__ == "__main__":
    main()
