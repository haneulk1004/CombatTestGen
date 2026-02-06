import typer
import sys
import os
from typing import List, Optional
from pydantic import ValidationError

from src.domain.models import CombatParams, Scenario
from src.domain.validation import format_validation_error
from src.domain.edge_cases import EdgeCaseGenerator
from src.domain.template_renderer import TemplateRenderer

app = typer.Typer(help="Combat Test Case Generator")

@app.command()
def create(
    damage: int = typer.Option(..., help="Player Damage (0-9999)"),
    hp: int = typer.Option(..., help="Enemy HP (1-999999)"),
    scenarios: Optional[List[str]] = typer.Option(
        None, 
        help="List of scenarios (normal, critical, dodge, death)"
    ),
    output: str = typer.Option("./CombatTests.cs", help="Output file path"),
    language: str = typer.Option("excel", help="Target language (csharp, python, json, excel)"),
    random_count: int = typer.Option(0, help="Number of random variations to generate")
):
    """
    Generate combat test cases based on parameters.
    """
    # 1. Parse Scenarios
    selected_scenarios = []
    if scenarios:
        # Handle comma-separated string if passed as single arg, or multiple args provided by shell
        # Typer handles list options by repeating flags usually, but let's be robust
        for s in scenarios:
            for part in s.split(','):
                clean_s = part.strip().lower()
                try:
                    selected_scenarios.append(Scenario(clean_s))
                except ValueError:
                    typer.secho(f"Warning: Unknown scenario '{clean_s}'. Ignored.", fg=typer.colors.YELLOW)
    else:
        selected_scenarios = [Scenario.NORMAL]

    # 2. Validate Input via Domain Model
    try:
        params = CombatParams(
            player_damage=damage,
            enemy_hp=hp,
            scenarios=selected_scenarios,
            random_count=random_count,
            output_path=output,
            language=language
        )
    except ValidationError as e:
        error_msg = format_validation_error(e)
        typer.secho(f"Input Error:\n{error_msg}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    # 3. Generate Test Cases
    typer.echo(f"Generating test cases for Damage={damage}, HP={hp}...")
    edge_gen = EdgeCaseGenerator()
    test_cases = edge_gen.generate(params)
    typer.echo(f"  - Generated {len(test_cases)} cases (including edge cases)")

    # 4. Render Template
    try:
        renderer = TemplateRenderer()
        output_content = renderer.render(test_cases, params.language)
    except Exception as e:
        typer.secho(f"Template Rendering Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    # 5. Write to File
    try:
        # Ensure directory exists
        output_dir = os.path.dirname(os.path.abspath(params.output_path))
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        mode = "wb" if isinstance(output_content, bytes) else "w"
        encoding = None if mode == "wb" else "utf-8"
        
        with open(params.output_path, mode, encoding=encoding) as f:
            f.write(output_content)
            
        typer.secho(f"Success! Saved to {params.output_path}", fg=typer.colors.GREEN)
        
    except OSError as e:
        typer.secho(f"File Write Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command()
def batch(
    config_dir: str = typer.Option(..., help="Directory containing config files (.json)"),
    output_dir: str = typer.Option(..., help="Directory to save generated tests")
):
    """
    Generate multiple test files from a directory of JSON config files.
    """
    import json
    
    if not os.path.exists(config_dir):
        typer.secho(f"Error: Config directory '{config_dir}' not found.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    files = [f for f in os.listdir(config_dir) if f.endswith(".json")]
    if not files:
         typer.secho(f"No .json files found in '{config_dir}'", fg=typer.colors.YELLOW)
         return

    success_count = 0
    for filename in files:
        config_path = os.path.join(config_dir, filename)
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Construct CombatParams from JSON data
            # Allow data to override output_path if needed, but default to output_dir
            base_name = os.path.splitext(filename)[0]
            target_file = os.path.join(output_dir, f"Test_{base_name}.{data.get('language', 'csharp') == 'python' and 'py' or 'cs'}")
            
            # Use 'create' logic internally (calling validation etc)
            # For simplicity, we manually map here since Typer options are different
            scenarios = []
            for s_str in data.get("scenarios", ["normal"]):
                try:
                    scenarios.append(Scenario(s_str.lower()))
                except ValueError:
                    pass # Ignore invalid

            params = CombatParams(
                player_damage=data["player_damage"],
                enemy_hp=data["enemy_hp"],
                scenarios=scenarios,
                output_path=target_file,
                language=data.get("language", "csharp")
            )
            
            edge_gen = EdgeCaseGenerator()
            test_cases = edge_gen.generate(params)
            
            renderer = TemplateRenderer()
            output_content = renderer.render(test_cases, params.language)
            
            mode = "wb" if isinstance(output_content, bytes) else "w"
            encoding = None if mode == "wb" else "utf-8"

            with open(target_file, mode, encoding=encoding) as f:
                 f.write(output_content)
                 
            success_count += 1
            typer.echo(f"  - Processed {filename} -> {target_file}")
            
        except (json.JSONDecodeError, ValidationError, KeyError) as e:
            typer.secho(f"  X Failed {filename}: {e}", fg=typer.colors.RED)
            
    typer.secho(f"Batch completed. {success_count}/{len(files)} successful.", fg=typer.colors.GREEN)

@app.command()
def gui():
    """
    Launch the GUI application.
    """
    try:
        from src.gui.main_window import main as gui_main
        gui_main()
    except ImportError as e:
        typer.secho(f"GUI Import Error: {e}\nEnsure customtkinter is installed.", fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"GUI Error: {e}", fg=typer.colors.RED)

if __name__ == "__main__":
    try:
        # Default to GUI if no arguments provided (for double-click usage)
        if len(sys.argv) == 1:
            sys.argv.append("gui")
            
        app()
    except Exception as e:
        import traceback
        import datetime
        
        err_msg = traceback.format_exc()
        print(err_msg)
        
        with open("crash.log", "w", encoding="utf-8") as f:
            f.write(f"Timestamp: {datetime.datetime.now()}\n")
            f.write(err_msg)
            
        print("\n[!] Error log saved to 'crash.log'. Please report this file.")
        input("Press Enter to exit...")
