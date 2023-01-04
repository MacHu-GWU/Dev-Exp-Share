from rich.prompt import Prompt
name = Prompt.ask("Enter your name", choices=["Paul", "Jessica", "Duncan"], default="Paul")