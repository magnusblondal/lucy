from rich import print

class View:
    COLUMN_HEADER_COL: str = '[grey54]' 

    def dim(self, s: str, val: str = None) -> str:
        v = f" {val}" if val is not None else ""            
        return f"[dim italic]{s}[/dim italic]{v}"
    
    def indent(self, s: str, length: int = 1) -> str:
        t = " " * 3 * length
        return f"{t}{s}"
    
    def emp(self, s: str) -> str:
        return f"[bold blue]{s}[/bold blue]"
    
    def desc(self, s: str) -> None:
        print( f"[green]{s}[/green]")
    
    def process_title(self, title: str) -> None:
        print( f"[bold green]{title}[/bold green]")

    def confirmation(self, msg: str) -> None:
        print(f"[bold green]{msg}[/bold green]")

    def warning(self, msg: str) -> None:
        print(f"[bold orange]{msg}[/bold orange]")

    def open(self, msg: str) -> None:
        return f"[bold purple]{msg}[/bold purple]"
  
    def closed(self, msg: str) -> None:
        return f"[bold yellow]{msg}[/bold yellow]"

    def open_or_closed(self, is_open: bool) -> str:
        return self.open('OPEN') if is_open else self.closed('CLOSED')
    
    def left_pad(self, s: str, length: int = 1) -> str:
        ss = "{:>" + str(length) + "}"
        return ss.format(s)
    
    def right_pad(self, s: str, length: int = 1) -> str:
        ss = "{:<" + str(length) + "}"
        return ss.format(s)