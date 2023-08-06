from py_stringsimjoin.filter.filter_utils import get_prefix_length
from py_stringsimjoin.index.index import Index
from py_stringsimjoin.utils.token_ordering import order_using_token_ordering


class PrefixIndex(Index):
    """Builds an inverted index on the prefixes of the strings in the input 
    column in the input table.                                                                  
                                                                                
    Prefix index is used by prefix filter and edit distance join.      
    """                

    def __init__(self, table, index_attr, tokenizer, 
                 sim_measure_type, threshold, token_ordering):
        self.table = table
        self.index_attr = index_attr
        self.tokenizer = tokenizer
        self.sim_measure_type = sim_measure_type
        self.threshold = threshold
        self.token_ordering = token_ordering
        self.index = None
        super(self.__class__, self).__init__()

    def build(self, cache_empty_records=True):
        """Build prefix index."""                                             
        self.index = {}
        empty_records = []
        row_id = 0
        for row in self.table:
            # tokenize string and order the tokens using the token ordering
            index_string = row[self.index_attr]
            index_attr_tokens = order_using_token_ordering(
                self.tokenizer.tokenize(index_string), self.token_ordering)

            # compute prefix length
            num_tokens = len(index_attr_tokens)
            prefix_length = get_prefix_length(
                                num_tokens,
                                self.sim_measure_type, self.threshold,
                                self.tokenizer)
 
            # update index
            for token in index_attr_tokens[0:prefix_length]:
                if self.index.get(token) is None:
                    self.index[token] = []
                self.index.get(token).append(row_id)

            if cache_empty_records and num_tokens == 0:
                empty_records.append(row_id)

            row_id += 1

        return {'empty_records': empty_records}

    def probe(self, token):
        """Probe prefix index using the input token."""
        return self.index.get(token, [])
