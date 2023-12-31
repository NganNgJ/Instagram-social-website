from enum import Enum
import inspect

class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not(m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices
    
class Status(ChoiceEnum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'


class ReactionType(ChoiceEnum):
    NONE = 'NOT_REACT'
    REACTION = 'LOVE'
    

