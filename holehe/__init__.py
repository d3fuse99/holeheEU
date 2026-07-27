import trio
import httpx
import sys
import importlib
import pkgutil
from holehe.core import import_submodules

async def check_email(email):
    out = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    
    async with httpx.AsyncClient(headers=headers, verify=False, timeout=15) as client:
        print(f"--- ПРОВЕРКА: {email} ---")
        
        modules = import_submodules("holehe.modules")
        
        async with trio.open_nursery() as nursery:
            for module in modules:
                func_name = module.__name__.split(".")[-1]
                if hasattr(module, func_name):
                    func = getattr(module, func_name)
                    nursery.start_soon(func, email, client, out)

    print("\nРЕЗУЛЬТАТЫ:")
    print("-" * 30)
    for result in out:
        if result['exists']:
            print(f"[+] {result['name']} - ЕСТЬ АККАУНТ")
        else:
            # print(f"[-] {result['name']} - нет")
            pass
    print("-" * 30)
    print("Проверка завершена.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Ошибка: введи email. Пример: python run.py test@mail.ru")
    else:
        email_to_check = sys.argv[1]
        trio.run(check_email, email_to_check)