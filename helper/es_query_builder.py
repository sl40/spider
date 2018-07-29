class EsQueryBuilder:
    """
    elasticsearch query builder
    """

    def __init__(self):
        self.__filters = []
        self.__should = []
        self.__must = []
        self.__must_not = []
        self.__paths = {}
        self.__sort = []
        self.__source = []
        self.__aggs = {}
        self.__minimum_should_match = None

    def search(self, es_model, page=1, page_size=20):
        """
        :param es_model:
        :param page:
        :param page_size:
        :return:
        """
        return EsSearchResultParse(es_model.search(self.get_query(page, page_size)))

    def get_query(self, page=1, page_size=20):
        """
        get query
        :param page:
        :param page_size:
        :return:
        """
        bool_dict = {}
        if self.get_filters():
            bool_dict.setdefault('filter', self.get_filters())
        if self.__should:
            bool_dict.setdefault('should', self.__should)
            if self.__minimum_should_match:
                bool_dict.setdefault('minimum_should_match', self.__minimum_should_match)
        if self.__must:
            bool_dict.setdefault('must', self.__must)
        if self.__must_not:
            bool_dict.setdefault('must_not', self.__must_not)

        return {
            'sort': self.__sort,
            '_source': self.__source,
            'query': {
                'bool': bool_dict
            },
            'aggs': self.__aggs,
            'from': (page - 1) * page_size,
            'size': page_size
        }

    def get_filters(self):
        """
        get filters
        :return:
        """
        return self.__filters + self.__get_nested_filters()

    def term(self, field, value):
        """
        term
        :param field:
        :param value:
        :return:
        """
        if value is not None:
            self.__append(field, {
                'term': {
                    field: value
                }
            })
        return self

    def terms(self, field, values: list):
        """
        terms
        :param field:
        :param values:
        :return:
        """
        if values is not None and len(values) > 0:
            self.__append(field, {
                'terms': {
                    field: values
                }
            })
        return self

    def range(self, field, start, end):
        """
        range gt lt
        :param field:
        :param start:
        :param end:
        :return:
        """
        if start is not None or end is not None:
            self.__append(field, {
                'range': {
                    field: {
                        'gt': start,
                        'lt': end
                    }
                }
            })
        return self

    def range_e(self, field, start, end):
        """
        range gte lte
        :param field:
        :param start:
        :param end:
        :return:
        """
        if start is not None or end is not None:
            self.__append(field, {
                'range': {
                    field: {
                        'gte': start,
                        'lte': end
                    }
                }
            })
        return self

    def range_gte(self, field, start, end):
        """
        range gte lt
        :param field:
        :param start:
        :param end:
        :return:
        """

        if start is not None or end is not None:
            self.__append(field, {
                'range': {
                    field: {
                        'gte': start,
                        'lt': end
                    }
                }
            })
        return self

    def range_lte(self, field, start, end):
        """
        range gt lte
        :param field:
        :param start:
        :param end:
        :return:
        """
        if start is not None or end is not None:
            self.__append(field, {
                'range': {
                    field: {
                        'gt': start,
                        'lte': end
                    }
                }
            })
        return self

    def exists(self, field):
        """
        exists
        :param field:
        :return:
        """
        self.__append(field, {
            'exists': {
                'field': field
            }
        })
        return self

    def should(self, query_builder):
        """
        should
        :param query_builder:
        :return:
        """
        self.__should.append({
            'bool': {
                'filter': query_builder.get_filters()
            }
        })
        return self

    def should_constant_score(self, query_builder, boost=1):
        """
        should
        :param query_builder:
        :param boost:
        :return:
        """
        self.__should.append({
            'constant_score': {
                'filter': query_builder.get_filters().pop(),
                'boost': boost
            }
        })
        return self

    def must(self, query_builder):
        """
        must
        :param query_builder:
        :return:
        """
        self.__must.append({
            'bool': {
                'filter': query_builder.get_filters()
            }
        })
        return self

    def must_not(self, query_builder):
        """
        must not
        :param query_builder:
        :return:
        """
        self.__must_not.append({
            'bool': {
                'filter': query_builder.get_filters()
            }
        })
        return self

    def minimum_should_match(self, minimum_should_match):
        """
        set minimum_should_match
        :param minimum_should_match:
        :return:
        """
        self.__minimum_should_match = minimum_should_match
        return self

    def add_sort(self, field, sort_type='desc'):
        """
        add sort
        :param field:
        :param sort_type:
        :return:
        """
        self.__sort.append({
            field: sort_type
        })
        return self

    def source(self, fields: list):
        """
        es result source
        :param fields:
        :return:
        """
        self.__source = fields
        return self

    def aggs(self, aggs):
        """
        aggs
        :param aggs:
        :return:
        """
        self.__aggs = aggs.get_aggs() if isinstance(aggs, EsAggsBuilder) else aggs
        return self

    def __get_nested_filters(self):
        """
        nested filters
        :return:
        """
        result = []
        for path, filters in self.__paths.items():
            result.append({
                'nested': {
                    'path': path,
                    'query': {
                        'bool': {
                            'filter': filters
                        }
                    }
                }
            })
        return result

    def __append(self, field, f):
        """
        append filter
        :param field:
        :param f:
        :return:
        """
        if '.' in field.replace('.keyword', ''):
            path = field.split('.')[0]
            self.__paths.setdefault(path, [])
            self.__paths[path].append(f)
        else:
            self.__filters.append(f)


class EsAggsBuilder:
    """
    elasticsearch aggs builder
    """
    def __init__(self):
        self.__names = {}
        self.__last_name = None

    def get_aggs(self):
        """
        get aggs
        :return:
        """
        return self.__names

    def terms(self, name, field, size=1000):
        """
        terms agg
        :param name:
        :param field:
        :param size:
        :return:
        """
        self.__names[name] = {
            'terms': {
                'field': field,
                'size': size
            }
        }
        self.__last_name = name
        return self

    def cardinality(self, name, field):
        """
        cardinality agg
        :param name:
        :param field:
        :return:
        """
        self.__names[name] = {
            'cardinality': {
                'field': field
            }
        }
        return self

    def percentiles(self, name, field):
        """
        percentiles agg
        :param name:
        :param field:
        :return:
        """
        self.__names[name] = {
            'percentiles': {
                'field': field
            }
        }
        return self

    def sum(self, name, field):
        """
        sum agg
        :param name:
        :param field:
        :return:
        """
        self.__names[name] = {
            'sum': {
                'field': field
            }
        }
        return self

    def min(self, name, field):
        """
        min agg
        :param name:
        :param field:
        :return:
        """
        self.__names[name] = {
            'min': {
                'field': field
            }
        }
        return self

    def max(self, name, field):
        """
        max agg
        :param name:
        :param field:
        :return:
        """
        self.__names[name] = {
            'max': {
                'field': field
            }
        }
        return self

    def avg(self, name, field):
        """
        avg agg
        :param name:
        :param field:
        :return:
        """
        self.__names[name] = {
            'avg': {
                'field': field
            }
        }
        return self

    def top_hits(self, name, size=1, sort_field=None, sort_type='desc'):
        """
        top hits
        :param name:
        :param size:
        :param sort_field:
        :param sort_type:
        :return:
        """
        self.__names[name] = {
            'top_hits': {
                'size': size,
            }
        }
        if sort_field:
            self.__names[name]['top_hits']['sort'] = {
                sort_field: sort_type
            }
        return self

    def date_histogram(self, name, field, interval, time_zone=None, order=None):
        """
        date histogram
        :param name:
        :param field:
        :param interval:
        :param time_zone:
        :param order:
        :return:
        """
        self.__names[name] = {
            'date_histogram': {k: v for k, v in {
                'field': field,
                'interval': interval,
                'time_zone': time_zone,
                'order': order
            }.items() if v is not None}
        }
        self.__last_name = name
        return self

    def nested(self, name, field):
        """
        nested path
        :param name:
        :param field:
        :return:
        """
        self.__names[name] = {
            'nested': {
                'path': field
            }
        }
        self.__last_name = name
        return self

    def reverse_nested(self, name):
        self.__names[name] = {
            'reverse_nested': {}
        }
        self.__last_name = name
        return self

    def aggs(self, aggs):
        """
        nested aggs
        :param aggs:
        :return:
        """
        if aggs and isinstance(aggs, EsAggsBuilder) and self.__last_name in self.__names:
            self.__names[self.__last_name]['aggs'] = aggs.get_aggs()
        return self

    def filter_term(self, name, field, value):
        """
        filter term
        :param name:
        :param field:
        :param value:
        :return:
        """
        self.__names[name] = {
            'filter': {
                'term': {
                    field: value
                }
            }
        }
        self.__last_name = name
        return self

    def filter_terms(self, name, field, values: list):
        """
        filter terms
        :param name:
        :param field:
        :param values:
        :return:
        """
        self.__names[name] = {
            'filter': {
                'terms': {
                    field: values
                }
            }
        }
        self.__last_name = name
        return self

    def filter_range(self, name, field, start, end):
        """
        filter range gt lt
        :param name:
        :param field:
        :param start:
        :param end:
        :return:
        """
        self.__names[name] = {
            'filter': {
                'range': {
                    field: {
                        'gt': start,
                        'lt': end
                    }
                }
            }
        }
        self.__last_name = name
        return self

    def filter_range_e(self, name, field, start, end):
        """
        filter range gte lte
        :param name:
        :param field:
        :param start:
        :param end:
        :return:
        """
        self.__names[name] = {
            'filter': {
                'range': {
                    field: {
                        'gte': start,
                        'lte': end
                    }
                }
            }
        }
        self.__last_name = name
        return self

    def filter_range_gte(self, name, field, start, end):
        """
        filter range gte lt
        :param name: str
        :param field:
        :param start:
        :param end:
        :return:
        """
        self.__names[name] = {
            'filter': {
                'range': {
                    field: {
                        'gte': start,
                        'lt': end
                    }
                }
            }
        }
        self.__last_name = name
        return self

    def filter_range_lte(self, name, field, start, end):
        """
        filter range gt lte
        :param name:
        :param field:
        :param start:
        :param end:
        :return:
        """
        self.__names[name] = {
            'filter': {
                'range': {
                    field: {
                        'gt': start,
                        'lte': end
                    }
                }
            }
        }
        self.__last_name = name
        return self

    def stats(self, name, field):
        """
        stats agg
        :param name:
        :param field:
        :return:
        """
        self.__names[name] = {
            'stats': {
                'field': field
            }
        }
        return self


class EsSearchResultParse:
    """
    elasticsearch search result parse
    """

    def __init__(self, result):
        self.result = result

    def get_reslut(self):
        return self.result

    def get_list(self, get_id=True):
        """
        get list
        :return:
        """
        return_data = []
        for _ in self.result['hits']['hits']:
            if get_id:
                _['_source']['_id'] = _['_id']
            return_data.append(_['_source'])
        return return_data

    def get_one(self):
        """
        get one
        :return:
        """
        result = self.get_list()
        return self.get_list()[0] if result else {}

    def get_count(self):
        """
        get count
        :return:
        """
        return self.result['hits']['total']

    def get_aggregations(self):
        """
        get aggregations
        :return:
        """
        return self.result['aggregations']

    def get_scroll_id(self):
        """
        get scroll id
        :return:
        """
        return self.result['_scroll_id']
