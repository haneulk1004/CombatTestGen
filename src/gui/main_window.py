import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from typing import List

from src.domain.models import CombatParams, Scenario
from src.domain.validation import format_validation_error
from src.domain.edge_cases import EdgeCaseGenerator
from src.domain.template_renderer import TemplateRenderer

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class CombatTestGenApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("Combat Test Generator")
        self.geometry("600x700")
        self.resizable(True, True)

        # Layout Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        # 1. Title
        self.lbl_title = ctk.CTkLabel(self, text="전투 테스트 케이스 생성기", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_title.grid(row=0, column=0, padx=20, pady=(20, 10))

        # 2. Input Fields Frame
        self.frm_inputs = ctk.CTkFrame(self)
        self.frm_inputs.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Player Damage
        self.lbl_damage = ctk.CTkLabel(self.frm_inputs, text="플레이어 데미지:")
        self.lbl_damage.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.ent_damage = ctk.CTkEntry(self.frm_inputs, placeholder_text="0 ~ 9999")
        self.ent_damage.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.ent_damage.insert(0, "50")

        # Enemy HP
        self.lbl_hp = ctk.CTkLabel(self.frm_inputs, text="적 HP:")
        self.lbl_hp.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.ent_hp = ctk.CTkEntry(self.frm_inputs, placeholder_text="1 ~ 999999")
        self.ent_hp.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.ent_hp.insert(0, "100")

        # 3. Scenarios Frame
        self.frm_scenarios = ctk.CTkFrame(self)
        self.frm_scenarios.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.lbl_scenarios = ctk.CTkLabel(self.frm_scenarios, text="시나리오 선택", font=ctk.CTkFont(weight="bold"))
        self.lbl_scenarios.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.chk_normal = ctk.CTkCheckBox(self.frm_scenarios, text="기본 (Normal)")
        self.chk_normal.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.chk_normal.select()

        self.chk_critical = ctk.CTkCheckBox(self.frm_scenarios, text="치명타 (Critical)")
        self.chk_critical.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.chk_dodge = ctk.CTkCheckBox(self.frm_scenarios, text="회피 (Dodge)")
        self.chk_dodge.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.chk_death = ctk.CTkCheckBox(self.frm_scenarios, text="사망 (Death)")
        self.chk_death.grid(row=4, column=0, padx=10, pady=(5, 10), sticky="w")

        # 4. Output Path
        self.frm_output = ctk.CTkFrame(self)
        self.frm_output.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.ent_path = ctk.CTkEntry(self.frm_output, placeholder_text="저장 경로")
        self.ent_path.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.ent_path.insert(0, "./CombatTests.xlsx")
        self.frm_output.grid_columnconfigure(0, weight=1)
        
        self.btn_browse = ctk.CTkButton(self.frm_output, text="찾아보기", width=80, command=self.browse_file)
        self.btn_browse.grid(row=0, column=1, padx=10, pady=10)

        # 5. Language & Random Count
        self.frm_options = ctk.CTkFrame(self)
        self.frm_options.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        # Language
        self.lbl_lang = ctk.CTkLabel(self.frm_options, text="언어:")
        self.lbl_lang.pack(side="left", padx=(10,5), pady=10)
        
        self.opt_lang = ctk.CTkOptionMenu(self.frm_options, values=["excel", "csharp", "python", "json"], width=100)
        self.opt_lang.pack(side="left", padx=5, pady=10)
        self.opt_lang.set("excel")

        # Random Count
        self.lbl_random = ctk.CTkLabel(self.frm_options, text="추가 생성(개):")
        self.lbl_random.pack(side="left", padx=(20,5), pady=10)
        
        self.ent_random = ctk.CTkEntry(self.frm_options, width=60)
        self.ent_random.pack(side="left", padx=5, pady=10)
        self.ent_random.insert(0, "10")

        # 6. Generate Button
        self.btn_generate = ctk.CTkButton(self, text="테스트 케이스 생성", height=50, font=ctk.CTkFont(size=16, weight="bold"), command=self.generate)
        self.btn_generate.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

    def browse_file(self):
        filename = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            title="저장 경로 선택",
            filetypes=(("C# Files", "*.cs"), ("Python Files", "*.py"), 
                       ("JSON Files", "*.json"), ("Excel Files", "*.xlsx"), ("All Files", "*.*"))
        )
        if filename:
            self.ent_path.delete(0, "end")
            self.ent_path.insert(0, filename)

    def generate(self):
        # 1. Input Parsing
        try:
            damage = int(self.ent_damage.get())
            hp = int(self.ent_hp.get())
        except ValueError:
            messagebox.showerror("입력 오류", "데미지와 HP는 숫자여야 합니다.")
            return

        selected_scenarios = []
        if self.chk_normal.get(): selected_scenarios.append(Scenario.NORMAL)
        if self.chk_critical.get(): selected_scenarios.append(Scenario.CRITICAL)
        if self.chk_dodge.get(): selected_scenarios.append(Scenario.DODGE)
        if self.chk_death.get(): selected_scenarios.append(Scenario.DEATH)

        output_path = self.ent_path.get()
        language = self.opt_lang.get()
        
        try:
            random_count = int(self.ent_random.get())
        except ValueError:
            random_count = 0

        # 2. Validation
        try:
            params = CombatParams(
                player_damage=damage,
                enemy_hp=hp,
                scenarios=selected_scenarios,
                random_count=random_count,
                output_path=output_path,
                language=language
            )
        except Exception as e:
            # Pydantic validation error or other
            if hasattr(e, 'errors'): # Validation error
                msg = format_validation_error(e)
            else:
                msg = str(e)
            messagebox.showerror("입력 검증 실패", msg)
            return

        # 3. Generation Logic
        try:
            edge_gen = EdgeCaseGenerator()
            test_cases = edge_gen.generate(params)
            
            renderer = TemplateRenderer()
            output_content = renderer.render(test_cases, params.language)
            
            # Ensure dir
            output_dir = os.path.dirname(os.path.abspath(params.output_path))
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            mode = "wb" if isinstance(output_content, bytes) else "w"
            encoding = None if mode == "wb" else "utf-8"

            with open(params.output_path, mode, encoding=encoding) as f:
                f.write(output_content)
                
            messagebox.showinfo("완료", f"생성 성공!\n\n파일: {params.output_path}\n케이스 수: {len(test_cases)}개")
            
        except Exception as e:
            messagebox.showerror("생성 오류", f"오류 발생: {str(e)}")

def main():
    app = CombatTestGenApp()
    app.mainloop()

if __name__ == "__main__":
    main()
