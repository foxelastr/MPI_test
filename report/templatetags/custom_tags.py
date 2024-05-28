from django import template

register = template.Library()

@register.simple_tag
def range_tag(n):
    return range(n)

@register.filter
def enumerate(value):
    return enumerate(value)

@register.filter
def multiply(value, arg):
    """주어진 값에 arg를 곱한 결과를 반환합니다."""
    return value * arg

@register.filter
def index(sequence, position):
    """주어진 시퀀스에서 특정 위치의 항목을 반환합니다."""
    return sequence[position]

