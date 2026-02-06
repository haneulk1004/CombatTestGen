from pydantic import ValidationError

def format_validation_error(e: ValidationError) -> str:
    """
    Translates Pydantic ValidationError into a user-friendly string message.
    """
    messages = []
    for error in e.errors():
        loc = error.get("loc", ("unknown",))
        field = loc[0] if loc else "unknown"
        msg = error.get("msg", "")
        ctx = error.get("ctx", {})

        if field == "player_damage":
            if "greater_than_equal" in error["type"]:
                messages.append(f"플레이어 데미지는 0 이상이어야 합니다. (입력값: {ctx.get('ge') or ctx.get('gt')})")
            elif "less_than_equal" in error["type"]:
                 messages.append(f"플레이어 데미지는 9999 이하여야 합니다.")
            else:
                 messages.append(f"플레이어 데미지 형식이 올바르지 않습니다.")
        
        elif field == "enemy_hp":
            if "greater_than_equal" in error["type"]:
                messages.append(f"적 HP는 1 이상이어야 합니다.")
            elif "less_than_equal" in error["type"]:
                 messages.append(f"적 HP는 999999 이하여야 합니다.")
            else:
                 messages.append(f"적 HP 형식이 올바르지 않습니다.")
                 
        elif field == "language":
             messages.append(f"지원하지 않는 언어입니다. (csharp, python, json, excel 중 선택)")
             
        else:
            messages.append(f"{field}: {msg}")
            
    return "\n".join(messages)
