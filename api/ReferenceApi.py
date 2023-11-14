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
                (Reference.name.contains(term))
            )
            combined_query = term_query if combined_query is None else combined_query | term_query
        queryset = queryset.where(combined_query)
    return queryset.distinct()

def reference_list(search: str = None) -> tuple[bool, dict | None]:
    queryset = Reference.select()
    queryset = _filter(search, queryset)
    return True, [Reference._to_dict(reference_object) for reference_object in queryset.order_by(Reference.SN)]

def get_reference(SN: int) -> tuple[bool, dict | None]:
    try:
        reference = Reference.select().where(Reference.SN == SN).get()
        return True, Reference._to_dict(reference)
    except Reference.DoesNotExist:
        return False, None

def create_reference(data: dict) -> tuple[bool, dict | None]:
    try:
        _data = data.copy()
        reference_object = Reference.create(**_data)
        return True, Reference._to_dict(reference_object)
    except Exception:
        return False, None
    
def update_reference(data: dict) -> tuple[bool, dict | None]:
    try :
        _data = data.copy()
        SN = _data.pop('SN')
        reference_object = Reference.get_by_id(SN)

        for key, value in _data.items():
            if hasattr(reference_object, key):
                setattr(reference_object, key, value)
        reference_object.save()
        return True, Reference._to_dict(reference_object)
    except Exception:
        return False, None
    
def delete_reference(SN) -> bool:
    try :
        Reference.delete_by_id(SN)
        return True
    except Exception:
        return False