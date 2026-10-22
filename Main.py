"""CRONO · Ecos del tiempo. Run this file or use Jugar.bat."""
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
vendor = ROOT / '.vendor'
if vendor.is_dir():
    sys.path.insert(0, str(vendor))
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

if __name__ == '__main__':
    try:
        from crono.game import main
        main()
    except Exception:
        import traceback
        details=traceback.format_exc()
        log_root=Path(sys.executable).parent if getattr(sys,'frozen',False) else ROOT
        try:
            (log_root/'crono-error.log').write_text(details,encoding='utf-8')
        except OSError:
            pass
        if sys.stderr:
            print(details,file=sys.stderr)
        sys.exit(1)
