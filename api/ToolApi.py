from models import (
    Tool,
    Reference
)

from peewee import JOIN
import settings

def _filter(search, queryset):
    if search not in (None, 'None'):
        search_terms = [term.strip() for term in search.split(settings.SEARCH_DELIMETER)]
        combined_query = None

        for term in search_terms:
            term_query = (
                (Tool.name.contains(term))
            )
            combined_query = term_query if combined_query is None else combined_query | term_query
        queryset = queryset.where(combined_query)
    return queryset.distinct()

def tool_list(search: str = None) -> tuple[bool, dict | None]:
    queryset = Tool.select()
    queryset = _filter(search, queryset)
    return True, [Tool._to_dict(tool_object) for tool_object in queryset.order_by(Tool.SN)]

def get_tool(SN: int) -> tuple[bool, dict | None]:
    try:
        tool = Tool.select().where(Tool.SN == SN).get()
        return True, Tool._to_dict(tool)
    except Tool.DoesNotExist:
        return False, None

def create_tool(data: dict) -> tuple[bool, dict | None]:
    try:
        _data = data.copy()
        tool_object = Tool.create(**_data)
        return True, Tool._to_dict(tool_object)
    except Exception:
        return False, None
    
def update_tool(data: dict) -> tuple[bool, dict | None]:
    try :
        _data = data.copy()
        SN = _data.pop('SN')
        tool_object = Tool.get_by_id(SN)

        for key, value in _data.items():
            if hasattr(tool_object, key):
                setattr(tool_object, key, value)
        tool_object.save()
        return True, Tool._to_dict(tool_object)
    except Exception:
        return False, None
    
def delete_tool(SN: int) -> bool:
    try:
        Tool.delete_by_id(SN)
        return True
    except Exception:
        return False