from models import (
    Tool,
    Reference
)

from peewee import JOIN
import settings

# returns filtering query with search key
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

# returns tool list with search key
def tool_list(search: str = None) -> tuple[bool, dict | None]:
    queryset = Tool.select()
    queryset = _filter(search, queryset)
    return True, [Tool._to_dict(tool_object) for tool_object in queryset.order_by(Tool.SN.desc())]

# returns tool with SN
def get_tool(SN: int) -> tuple[bool, dict | None]:
    try:
        tool = Tool.select().where(Tool.SN == SN).get()
        return True, Tool._to_dict(tool)
    except Tool.DoesNotExist:
        return False, None
    
# reference if tool exists with name and SN
def check_duplicate(name: str, SN: int = None) -> bool:
    try:
        if SN is None:
            Tool.select().where(Tool.name == name).get()
        else:
            Tool.select().where(Tool.name == name).where(Tool.SN != SN).get()
        return True
    except Tool.DoesNotExist:
        return False

# creates a tool
def create_tool(data: dict) -> tuple[bool, dict | None]:
    try:
        _data = data.copy()
        tool_object = Tool.create(**_data)
        return True, Tool._to_dict(tool_object)
    except Exception as e:
        print(e)
        return False, None

# updates a reference
def update_tool(data: dict) -> tuple[bool, dict | None]:
    try :
        _data = data.copy()
        SN = _data.pop('SN')
        tool_object = Tool.get_by_id(SN)
        last_name = tool_object.name
        Reference.update(name = data['name']).where(Reference.name == last_name).execute()
        for key, value in _data.items():
            if hasattr(tool_object, key):
                setattr(tool_object, key, value)
        tool_object.save()
        return True, Tool._to_dict(tool_object)
    except Exception as e:
        print(e)
        return False, None

# delete a tool
def delete_tool(SN: int) -> bool:
    try:
        Tool.delete_by_id(SN)
        return True
    except Exception:
        return False