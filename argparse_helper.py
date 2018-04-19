import argparse


def get_function_name(function):
    return function.func_name, function.func_code.co_varnames, function.func_defaults


def test_optional(opt_1='opt_1', opt_2='opt_2', opt_3='opt_3', help='this is the help for test_optional'):
    print ('opt_1=', opt_1)
    print ('opt_2=', opt_2)
    print ('opt_3=', opt_3)
    print ('help=', help)

def test_empty(help='this is the help for test_empty'):
    print ('help=', help)

def test_required(first_required, second_required, third_required, help='this is the help for test_required'):
    print ('first_required=', first_required)
    print ('second_required=', second_required)
    print ('third_required=', third_required)
    print ('help=', help)

def test_mixed(first_required, second_required, third_required, opt_1='opt_1', opt_2='opt_2', opt_3='opt_3', help='this is the help for test_mixed'):
    print ('first_required=', first_required)
    print ('second_required=', second_required)
    print ('third_required=', third_required)
    print ('opt_1=', opt_1)
    print ('opt_2=', opt_2)
    print ('opt_3=', opt_3)
    print ('help=', help)


if __name__ == '__main__':
    case = {
        'netapi': netapi_client,
        'runner': runner_client,
        'test1': test_required,
        'test2': test_empty,
        'test3': test_optional,
        'test4': test_mixed,
    }
    parser = argparse.ArgumentParser()
    test_name = sys.argv[1]
    if case[test_name]:
        func_name, func_vars, func_defaults = get_function_name(case[test_name])
        iter_vars = iter(func_vars)
        kwargs = {}
        for default in func_defaults:
            fv = iter_vars.next()
            if fv != 'help':
                parser.add_argument('--' + fv,
                                    type=str,
                                    default=default)
                kwargs.update({fv: default})
            else:
                parser.add_argument('test_name')
                # parser.add_argument('test_name', help=default)
    parse = parser.parse_args()
    kwargs = vars(parse)
    del kwargs['test_name']
    f_name = get_function_name(case[test_name])
    case[test_name](**kwargs)
