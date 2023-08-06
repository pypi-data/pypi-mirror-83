# -*- coding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et tw=79
"""
Mock data for template development and debugging
"""

def mock_project(project_id=None, **kwargs):
    """
    Return a dict which represents a project

    >>> def mp(*args, **kwargs):
    ...     return sorted(mock_project(*args, **kwargs).items())
    >>> mp()
    [('project_id', None)]
    >>> mp(42)  # doctest: +NORMALIZE_WHITESPACE
    [('acronym', 'PRJ42'), ('announcement', None), ('project_id', 42),
     ('rc_member_id', 'member42'), ('subtitle', 'subtitle of project 42'),
     ('termtime', None), ('title', 'title of project 42')]
    """
    dic = {
        'project_id': project_id,
        }
    if project_id is None:
        return dic
    dic['rc_member_id'] = kwargs.get('rc_member_id',
                                     'member%d' % (project_id,))
    for key, mask in [
        ('title', 'title of project %(project_id)d'),
        ('acronym', 'PRJ%(project_id)d'),
        ('subtitle', 'subtitle of project %(project_id)d'),
        ('announcement', None),
        ('termtime', None),
        ]:
        if key in kwargs:
            dic[key] = kwargs.pop(key)
        elif mask is None:
            dic[key] = None
        else:
            dic[key] = mask % locals()
    return dic


def mock_p1result(*args, **kwargs):
    return None


if __name__ == '__main__':
    from doctest import testmod
    testmod()
