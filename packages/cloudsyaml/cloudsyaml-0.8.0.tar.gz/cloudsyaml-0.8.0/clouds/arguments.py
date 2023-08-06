

def arg_list(parser):
    parser.add_argument('--grep', type=str, action='append',
                        help='Regexp to grep the clouds by names, can be repeated')

    parser.add_argument('--eval', action='store_true', default=False,
                        help='Print command for shell to evaluation')

    return parser


def arg_show(parser):
    parser.add_argument('cloud', nargs='?', type=str, action='store', default=None,
                        help='Cloud name to show')

    parser.add_argument('--detail', action='store_true', default=False,
                        help='Print detailed cloud config')

    return parser
