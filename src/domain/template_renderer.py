import os
import sys
from typing import List, Dict, Union, Any
from jinja2 import Environment, FileSystemLoader
from src.domain.models import TestCase
import openpyxl
from io import BytesIO

class TemplateRenderer:
    """
    Renders test cases into code using Jinja2 templates.
    """
    
    def __init__(self, template_dir: str = None):
        if template_dir is None:
            if getattr(sys, 'frozen', False):
                # PyInstaller unpacked content
                base_dir = sys._MEIPASS
                template_dir = os.path.join(base_dir, "src", "templates")
            else:
                # Default to 'src/templates' relative to this file
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                template_dir = os.path.join(base_dir, "templates")
            
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def render(self, cases: List[TestCase], language: str) -> Union[str, bytes]:
        """
        Renders the list of test cases into a string (or bytes for Excel).
        
        Args:
            cases: List of TestCase objects
            language: Target language ('csharp', 'python', 'json', 'excel')
            
        Returns:
            Rendered code string or binary bytes (for excel)
        """
        if language == "excel":
            return self._render_excel(cases)
            
        template_name = self._get_template_name(language)
        template = self.env.get_template(template_name)
        
        return template.render(cases=cases)

    def _render_excel(self, cases: List[TestCase]) -> bytes:
        """
        Generates an Excel file (in bytes) from test cases.
        """
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Test Cases"
        
        # Headers
        headers = ["테스트명", "설명", "입력 데미지", "입력 HP", 
                   "기대 HP", "치명타?", "회피?", "사망?"]
        ws.append(headers)
        
        # Data
        for case in cases:
            row = [
                case.name,
                case.description,
                case.input_damage,
                case.input_hp,
                case.expected_hp,
                "예" if case.is_critical else "아니오",
                "예" if case.is_dodge else "아니오",
                "예" if case.is_death else "아니오"
            ]
            ws.append(row)
            
        # Adjust column widths (approximate)
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter # Get the column name
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column].width = adjusted_width

        # Save to bytes
        stream = BytesIO()
        wb.save(stream)
        stream.seek(0)
        return stream.getvalue()
    
    def _get_template_name(self, language: str) -> str:
        if language == "csharp":
            return "combat_test_csharp.j2"
        elif language == "python":
            return "combat_test_python.j2"
        elif language == "json":
            return "combat_test_json.j2"
        else:
            raise ValueError(f"Unsupported language: {language}")
