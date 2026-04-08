from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from juniorfetch.core.palace import MemoryPalace

class JuniorFetchCrawler:
    def __init__(self):
        self.palace = MemoryPalace()
        # Expanded production-grade file support
        self.supported = {
            '.txt', '.md', '.py', '.json', '.csv', '.log', '.pdf', 
            '.html', '.yml', '.yaml', '.ini', '.toml', '.js', '.ts', 
            '.cpp', '.h', '.c', '.rs', '.go', '.sh'
        }

    def index(self, root: str, max_files=100000):
        root_path = Path(root).expanduser().resolve()
        print(f"[SYNC] JuniorFetch indexing {root_path} (full disk support)")
        
        # Generator for memory efficiency on massive disks
        file_gen = (p for p in root_path.rglob("*") if p.is_file() and p.suffix.lower() in self.supported)
        files = []
        for _ in range(max_files):
            try:
                files.append(next(file_gen))
            except StopIteration:
                break

        def process(f: Path):
            try:
                if f.suffix.lower() == '.pdf':
                    text = f.read_text(errors="ignore")[:50000]
                else:
                    text = f.read_text(encoding="utf-8", errors="ignore")[:50000]
                
                if not text.strip(): return # Skip empty files
                
                hall_name = str(f.parent.relative_to(root_path)).replace("/", "_") or "root"
                self.palace.store(
                    wing="files",
                    hall=hall_name,
                    room=f.name,
                    content=text,
                    metadata={
                        "path": str(f), 
                        "extension": f.suffix.lower(), 
                        "mtime": f.stat().st_mtime,
                        "size_bytes": f.stat().st_size
                    }
                )
            except Exception:
                pass

        with ThreadPoolExecutor(max_workers=8) as ex:
            ex.map(process, files)
        print(f"[OK] Indexed {len(files)} files into local topological mesh.")