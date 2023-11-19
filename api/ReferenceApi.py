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
                (Reference.name.contains(term))
            )
            combined_query = term_query if combined_query is None else combined_query | term_query
        queryset = queryset.where(combined_query)
    return queryset.distinct()

# returns reference list with search key
def reference_list(search: str = None) -> tuple[bool, dict | None]:
    queryset = Reference.select()
    queryset = _filter(search, queryset)
    return True, [Reference._to_dict(reference_object) for reference_object in queryset.order_by(Reference.SN.desc())]

# returns refrence with SN
def get_reference(SN: int) -> tuple[bool, dict | None]:
    try:
        reference = Reference.select().where(Reference.SN == SN).get()
        return True, Reference._to_dict(reference)
    except Reference.DoesNotExist:
        return False, None

# returns if reference exists with name and SN
def check_duplicate(name: str, SN: int = None) -> bool:
    try:
        if SN is None:
            Reference.select().where(Reference.name == name).get()
        else:
            Reference.select().where(Reference.name == name).where(Reference.SN != SN).get()
        return True
    except Reference.DoesNotExist:
        return False

# creates a reference
def create_reference(data: dict) -> tuple[bool, dict | None]:
    try:
        _data = data.copy()
        reference_object = Reference.create(**_data)
        return True, Reference._to_dict(reference_object)
    except Exception:
        return False, None
    
# updates a reference
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

# deletes a reference
def delete_reference(SN) -> bool:
    try :
        Reference.delete_by_id(SN)
        return True
    except Exception:
        return False