def xpath_func_tokenize(context, string, split_token):
    if type(string) is list:
        string = string[0]
    return string.split(split_token)


def xpath_func_make_title(context, string):
    if type(string) is list:
        string = string[0]
    return string.title()


def xpath_func_remove_empy(context, str_list):
    final_list = []
    for elm in str_list:
        if elm.strip() != '':
            final_list.append(elm)
    return final_list


def xpath_func_merge(context, str_a, str_b):
    print str_a
    return str_a + str_b


def xpath_func_merge_lists(context, list_a, list_b, joint):
    list_fin = []
    for i in range(0, len(list_a)):
        list_fin.append(list_a[i] + joint + list_b[i])
    return list_fin


def xpath_func_join_list(context, lst, joint):
    return joint.join(lst)


def xpath_func_to_string(context, node):
    final_list = []
    for nod in node:
        final_list.append(nod.text_content())
    return final_list


def xpath_func_remove_string(context, str_a, to_remove):
    if str_a == "":
        return ""

    if type(str_a) is list:
        str_a = str_a[0]
    return str_a.replace(to_remove, "").strip()


def xpath_func_replace_regex(context, regex, replacement, elm):
    import re
    if type(elm) is list:
        elm = elm[0]
    return re.sub(regex, replacement, elm)


def xpath_func_split(context, by, take, elm):
    if type(elm) is list:
        elm = elm[0]
    return elm.split(by)[int(take)]


def xpath_func_to_html(context, nodes):
    from lxml import etree

    result = []
    for node in nodes:
        result.append(etree.tostring(node, pretty_print=False))
    return result


def xpath_func_contains_string(context, haystak, needle):
    haystak = " ".join(haystak)
    # if haystak.strip() != "":
    #     print haystak
    return needle in haystak