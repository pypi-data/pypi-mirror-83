from django.db.models import Q
import operator
from functools import reduce


def parse_or(queries):
    or_queries = []
    for k,v in queries.items():
        if '~' in k:
            or_queries.append(~Q(**{k[1:]: v}))
        else:
            or_queries.append(Q(**{k: v}))
    return reduce(operator.or_, or_queries)


def parse_and(queries):
    and_queries = []
    for k, v in queries.items():
        if "~" in k:
            and_queries.append(~Q(**{k[1:]: v}))
        else:
            and_queries.append(Q(**{k: v}))
    return Q(reduce(operator.and_, and_queries))


def Parse(d):
    queries=[]
    for k,v in d.items():
        if k == "and":
            queries.append(parse_and(v))
        elif k == "or":
           queries.append(parse_or(v))
        elif "~" in k:
            queries.append(~Q(**{k[1:]:v}))
        else:
            queries.append(Q(**{k:v}))
    return Q(*queries)






