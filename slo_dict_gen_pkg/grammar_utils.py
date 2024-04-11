from common.imports import *

# Grammar Feature categories
gfcat: Dict[str, List[str]] = {
    'aspect': ['perfective', 'progressive', 'biaspectual'],
    'number': ['singular', 'dual', 'plural'],
    'negative': ['yes', 'no'],
    'case': ['nominative', 'genitive', 'dative', 'accusative', 'locative',
             'instrumental'],
    'animate': ['yes', 'no'],
    'definiteness': ['yes', 'no'],
    'word_type': [
        'special', 'personal', 'relative', 'general', 'auxiliary', 'cardinal',
        'proper', 'ordinal', 'reflexive', 'pronominal', 'possessive',
        'coordinating', 'negative', 'interrogative', 'subordinating', 'main',
        'demonstrative', 'indefinite', 'common'],
    'person': ['first', 'second', 'third'],
    'degree': ['positive', 'comparative', 'superlative'],
    'vform': [
        'present', 'imperative', 'participle', 'conditional', 'future',
        'infinitive', 'supine'
    ],
    'gender': ['masculine', 'feminine', 'neuter'],
    'form': ['letter', 'roman', 'digit'],
    'clitic': ['yes', 'bound']
}

#           table_name : (top/columns, left/rows)
table_types: Dict[str, Dict[str, List[List[str]]]] = dict(
    noun=dict(
        declension=[gfcat['number'], gfcat['case']]
    ),
    verb={
        'present': [gfcat['number'], gfcat['person'], ],
        'imperative': [gfcat['number'], ['first', 'second']],
        'participle': [gfcat['number'], gfcat['gender']],
        'Non-Finite': [['form', ], ['infinitive', 'supine']],
        'conditional': [['form', ], ['form', ], ],
        'future': [gfcat['number'], gfcat['person'], ],
    },
    adjective={
        'masculine': [gfcat['number'], gfcat['case']],
        'feminine': [gfcat['number'], gfcat['case']],
        'neuter': [gfcat['number'], gfcat['case']],
    },
    adverb=dict(
        form=[['form', ], ['form', ], ]
    ),
    particle=dict(
        form=[['form', ], ['form', ], ]
    ),
    interjection=dict(
        form=[['form', ], ['form', ], ]
    ),
    conjunction=dict(
        form=[['form', ], ['form', ], ]
    ),
    preposition=dict(
        form=[['form', ], ['form', ], ]
    ),
    abbreviation=dict(
        form=[['form', ], ['form', ], ]
    ),
    pronoun={
        'agender': [gfcat['number'], gfcat['case']],
        'masculine': [gfcat['number'], gfcat['case']],
        'feminine': [gfcat['number'], gfcat['case']],
        'neuter': [gfcat['number'], gfcat['case']],
    },
)

'''
    
    numeral={
        '': [gfcat[''], gfcat['']],
    },'''


#   'owner_number':  ['dual', 'singular', 'plural']
#   'owner_gender':  ['masculine', 'neuter', 'feminine']


def ordered_grammar_name(
        *,
        v_form: str = None,
        case: str = None,
        person: str = None,
        number: str = None,
        gender: str = None,
        degree: str = None,
        return_type: str = "tuple"
):
    """
    Ensures that grammatical data is ordered correctly before concatenating
    them into a grammar name. Intended for use for individual word forms.
    kwargs mandatory.

    :param v_form: Verb form.
    :param case: Grammatical case.
    :param person: Grammatical person (1st, 2nd, 3rd).
    :param number: Singular/Dual/Plural.
    :param gender: Grammatical gender.
    :return: String of found items concatenated with an underscore in the
        correct order.
    """
    if return_type == "string":
        return concatenate_variables(
            v_form, case, person, number, gender, degree
        )
    else:
        types = [v_form, case, person, number, gender, degree]
        non_none_types = [item for item in types if item is not None]
        if return_type == "list":
            return non_none_types
        elif return_type == "tuple":
            return tuple(non_none_types)



def concatenate_variables(*items):
    """
    Concatenates variables into a string, separated by underscores, and
    ignoring empty strings.

    :param items: Arguments to concatenate.
    :return: Concatenated string.
    """
    out = "_".join(str(item) for item in items if item not in {None, "", " "})
    return out


def return_gram_feat_type(sample: str) -> Union[str, None]:
    """
    Takes a string and returns its grammar feature name.

    e.g.
        "first"      -> "person"

        "nominative" -> "case"

    :param sample: (str) sample word to check for feature type
    :return: string of feature type
    """
    gram_feat_dict = {
        'aspect': gfcat['aspect'],
        'number': gfcat['number'],
        'negative': gfcat['negative'],
        'case': gfcat['case'],
        'animate': gfcat['animate'],
        'definiteness': gfcat['definiteness'],
        'type': gfcat['word_type'],  # 'participle' removed!
        'person': gfcat['person'],
        'degree': gfcat['degree'],
        'vform': gfcat['vform'],
        'gender': gfcat['gender'],
        'form': gfcat['form'],
        'clitic': gfcat['clitic']
    }

    for key, values in gram_feat_dict.items():
        if sample == "no":
            lg.warning("'no' appears in two grammar features")
            return_value = "animate/negative"
            return ic([sample, return_value])[1]
        if sample == "yes":
            lg.warning("'yes' appears in three grammar features")
            return_value = "animate/clitic/negative"
            return ic([sample, return_value])[1]
        if sample in values:
            if sample in {"participle"}:
                lg.warning('"participle" removed from "type" feature '
                           'for functionality')
            return key
    if sample not in {'form'}:
        lg.warning(f'"{sample}" not a known grammar feature.')
    return None


if __name__ == "__main__":
    return_gram_feat_type('yes')
