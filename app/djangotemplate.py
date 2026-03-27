from django import template
from .freq import count
reg=template.Library()
@reg.filter
def getitem(count, key):
    return count.get(key)