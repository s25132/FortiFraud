from fastapi import HTTPException

def validate_non_empty_strings(data):
    for field_name, value in data:
        if isinstance(value, str) and value.strip() == "":
            raise HTTPException(
                status_code=400,
                detail=f"Pole '{field_name}' nie może być puste."
            )